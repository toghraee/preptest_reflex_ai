import reflex as rx
from app.pages.auth.auth_backend import AuthState, User
from sqlalchemy import text
from typing import TypedDict, Optional
from datetime import datetime, timedelta
import random


class Subject(TypedDict):
    id: int
    subject: str
    examcode: str
    examdate: str


class Topic(TypedDict):
    id: int
    topic: str
    size: str
    hours: int


class StudyPlanItem(TypedDict):
    id: int
    date: str
    subject: str
    hours: int
    status: str
    student_topic_id: int


class PlanState(rx.State):
    available_levels: list[str] = []
    available_boards: list[str] = []
    available_subjects: list[Subject] = []
    available_topics: list[Topic] = []
    selected_level: str = ""
    selected_board: str = ""
    selected_subject_id: int = 0
    selected_exam_date: str = ""
    selected_topic_ids: list[int] = []
    study_plan_items: list[StudyPlanItem] = []
    loading: bool = False
    generation_in_progress: bool = False

    @rx.var
    def total_study_hours(self) -> int:
        return sum(
            (
                topic["hours"]
                for topic in self.available_topics
                if topic["id"] in self.selected_topic_ids
            )
        )

    async def _get_current_user(self) -> Optional[User]:
        auth_state = await self.get_state(AuthState)
        return auth_state.current_user

    @rx.event(background=True)
    async def on_page_load(self):
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                yield rx.redirect("/login")
                return
        yield PlanState.load_levels()
        yield PlanState.load_plan()

    @rx.event(background=True)
    async def load_levels(self):
        async with self:
            self.loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT DISTINCT level FROM subjects ORDER BY level")
            )
            levels = [row[0] for row in result.fetchall()]
            async with self:
                self.available_levels = levels
                self.loading = False

    @rx.event(background=True)
    async def on_level_change(self, level: str):
        async with self:
            self.loading = True
            self.selected_level = level
            self.selected_board = ""
            self.selected_subject_id = 0
            self.available_boards = []
            self.available_subjects = []
            self.available_topics = []
            self.selected_topic_ids = []
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT DISTINCT board FROM subjects WHERE level = :level ORDER BY board"
                ),
                {"level": level},
            )
            boards = [row[0] for row in result.fetchall()]
            async with self:
                self.available_boards = boards
                self.loading = False

    @rx.event(background=True)
    async def on_board_change(self, board: str):
        async with self:
            self.loading = True
            self.selected_board = board
            self.selected_subject_id = 0
            self.available_subjects = []
            self.available_topics = []
            self.selected_topic_ids = []
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT id, subject, examcode, examdate FROM subjects WHERE level = :level AND board = :board ORDER BY subject"
                ),
                {"level": self.selected_level, "board": board},
            )
            subjects = [
                Subject(
                    id=r.id, subject=r.subject, examcode=r.examcode, examdate=r.examdate
                )
                for r in result.fetchall()
            ]
            async with self:
                self.available_subjects = subjects
                self.loading = False

    @rx.event(background=True)
    async def on_subject_change(self, subject_id_str: str):
        subject_id = int(subject_id_str)
        async with self:
            self.loading = True
            self.selected_subject_id = subject_id
            self.available_topics = []
            self.selected_topic_ids = []
            subject = next(
                (s for s in self.available_subjects if s["id"] == subject_id), None
            )
            if subject:
                self.selected_exam_date = subject["examdate"]
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT id, topic, size, hours FROM topics WHERE subjectid = :subject_id ORDER BY topic"
                ),
                {"subject_id": subject_id},
            )
            topics = [
                Topic(id=r.id, topic=r.topic, size=r.size, hours=r.hours)
                for r in result.fetchall()
            ]
            async with self:
                self.available_topics = topics
                self.loading = False

    @rx.event
    def toggle_topic(self, topic_id: int):
        if topic_id in self.selected_topic_ids:
            self.selected_topic_ids.remove(topic_id)
        else:
            self.selected_topic_ids.append(topic_id)

    @rx.event(background=True)
    async def generate_plan(self):
        user = await self._get_current_user()
        if not user or not self.selected_topic_ids or (not self.selected_subject_id):
            return
        async with self:
            self.generation_in_progress = True
        await self.delete_plan(clear_ui=False)
        selected_topics = [
            t for t in self.available_topics if t["id"] in self.selected_topic_ids
        ]
        subject_details = next(
            (s for s in self.available_subjects if s["id"] == self.selected_subject_id),
            None,
        )
        if not subject_details:
            async with self:
                self.generation_in_progress = False
            return
        plan = []
        for topic in selected_topics:
            plan.append(
                {
                    "student_id": user.id,
                    "level": self.selected_level,
                    "subject": topic["topic"],
                    "examboard": self.selected_board,
                    "examcode": subject_details["examcode"],
                    "examdate": self.selected_exam_date,
                }
            )
        async with rx.asession() as session:
            if plan:
                await session.execute(
                    text(
                        "INSERT INTO student_topics (student_id, level, subject, examboard, examcode, examdate) VALUES (:student_id, :level, :subject, :examboard, :examcode, :examdate)"
                    ),
                    plan,
                )
                await session.commit()
        async with self:
            self.generation_in_progress = False
        yield PlanState.load_plan()

    @rx.event(background=True)
    async def load_plan(self):
        user = await self._get_current_user()
        if not user:
            return
        async with self:
            self.loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT id, examdate, subject FROM student_topics
                       WHERE student_id = :user_id ORDER BY examdate, subject"""),
                {"user_id": user.id},
            )
            rows = result.fetchall()
        all_topics_result = await session.execute(
            text("SELECT topic, hours FROM topics")
        )
        topic_details_map = {r.topic: r.hours for r in all_topics_result.fetchall()}
        items = [
            StudyPlanItem(
                id=r.id,
                date=r.examdate,
                subject=r.subject,
                hours=topic_details_map.get(r.subject, 0),
                status="Not Started",
                student_topic_id=r.id,
            )
            for r in rows
        ]
        async with self:
            self.study_plan_items = items
            self.loading = False

    @rx.event
    def update_plan_item_status(self, item_id: int, new_status: str):
        for i, item in enumerate(self.study_plan_items):
            if item["id"] == item_id:
                self.study_plan_items[i]["status"] = new_status
                break

    @rx.event(background=True)
    async def delete_plan(self, clear_ui: bool = True):
        user = await self._get_current_user()
        if not user:
            return
        async with rx.asession() as session:
            await session.execute(
                text("DELETE FROM student_topics WHERE student_id = :user_id"),
                {"user_id": user.id},
            )
            await session.commit()
        if clear_ui:
            async with self:
                self.study_plan_items = []