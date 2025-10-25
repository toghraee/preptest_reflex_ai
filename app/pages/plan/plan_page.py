import reflex as rx
from app.components.shared.navbar import navbar
from app.components.shared.footer import footer
from app.pages.auth.auth_backend import AuthState
from app.pages.plan.plan_backend import PlanState, Topic, StudyPlanItem


def _form_select(
    label: str,
    placeholder: str,
    items: rx.Var[list[str]],
    on_change: rx.event.EventHandler,
    value: rx.Var[str],
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.select(
            rx.el.option(placeholder, value="", disabled=True),
            rx.foreach(items, lambda item: rx.el.option(item, value=item)),
            on_change=on_change,
            value=value,
            class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
        ),
    )


def _subject_select(
    label: str,
    placeholder: str,
    items: rx.Var[list],
    on_change: rx.event.EventHandler,
    value: rx.Var,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.select(
            rx.el.option(placeholder, value="0", disabled=True),
            rx.foreach(
                items,
                lambda item: rx.el.option(
                    f"{item['subject']} ({item['examcode']})", value=item["id"].to(str)
                ),
            ),
            on_change=on_change,
            value=value.to(str),
            class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
        ),
    )


def _topic_checkbox(topic: Topic) -> rx.Component:
    return rx.el.label(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=PlanState.selected_topic_ids.contains(topic["id"]),
                on_change=lambda: PlanState.toggle_topic(topic["id"]),
                class_name="h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500",
            ),
            rx.el.div(
                rx.el.p(topic["topic"], class_name="font-medium text-gray-800"),
                rx.el.p(
                    f"{topic['size']} • {topic['hours']} hours",
                    class_name="text-sm text-gray-500",
                ),
                class_name="ml-3 text-sm",
            ),
        ),
        class_name="flex items-center p-3 hover:bg-gray-100 rounded-lg cursor-pointer",
    )


def _plan_table_row(item: StudyPlanItem, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["date"], class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600"
        ),
        rx.el.td(
            item["subject"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            item["hours"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600 text-center",
        ),
        rx.el.td(
            rx.el.select(
                rx.el.option("Not Started", value="Not Started"),
                rx.el.option("In Progress", value="In Progress"),
                rx.el.option("Completed", value="Completed"),
                value=item["status"],
                on_change=lambda val: PlanState.update_plan_item_status(
                    item["id"], val
                ),
                class_name="w-full p-1 border-gray-300 rounded-md text-sm",
                bg=rx.match(
                    item["status"],
                    ("Completed", "bg-emerald-100"),
                    ("In Progress", "bg-yellow-100"),
                    "bg-gray-100",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        class_name=rx.cond(index % 2 == 0, "bg-white", "bg-gray-50"),
    )


def _authenticated_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("My Study Plan", class_name="text-3xl font-bold text-gray-800 mb-2"),
        rx.el.p(
            "Create and manage your personalized exam study schedule.",
            class_name="text-gray-600",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "1. Select Your Exam",
                    class_name="text-xl font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    _form_select(
                        "Level",
                        "Select Level",
                        PlanState.available_levels,
                        PlanState.on_level_change,
                        PlanState.selected_level,
                    ),
                    _form_select(
                        "Board",
                        "Select Board",
                        PlanState.available_boards,
                        PlanState.on_board_change,
                        PlanState.selected_board,
                    ),
                    _subject_select(
                        "Subject",
                        "Select Subject",
                        PlanState.available_subjects,
                        PlanState.on_subject_change,
                        PlanState.selected_subject_id,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "2. Choose Your Topics",
                    class_name="text-xl font-semibold text-gray-800 mb-4",
                ),
                rx.cond(
                    PlanState.selected_subject_id > 0,
                    rx.el.div(
                        rx.foreach(PlanState.available_topics, _topic_checkbox),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 border rounded-lg p-2 max-h-72 overflow-y-auto",
                    ),
                    rx.el.p(
                        "Select a subject to see available topics.",
                        class_name="text-gray-500",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        f"Total study time: {PlanState.total_study_hours} hours",
                        class_name="font-semibold",
                    ),
                    rx.el.p(
                        f"Exam Date: {PlanState.selected_exam_date}",
                        class_name="text-sm text-gray-600",
                    ),
                ),
                rx.el.button(
                    "Generate Study Plan",
                    on_click=PlanState.generate_plan,
                    is_loading=PlanState.generation_in_progress,
                    disabled=(PlanState.selected_topic_ids.length() == 0)
                    | PlanState.generation_in_progress,
                    class_name="px-6 py-2 bg-emerald-500 text-white font-semibold rounded-lg shadow-md hover:bg-emerald-600 disabled:bg-gray-300 transition-all",
                ),
                class_name="flex justify-between items-center mt-6",
            ),
            class_name="space-y-8 bg-white p-8 rounded-2xl shadow-sm border border-gray-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "3. Your Generated Plan",
                    class_name="text-xl font-semibold text-gray-800",
                ),
                rx.cond(
                    PlanState.study_plan_items.length() > 0,
                    rx.el.button(
                        rx.icon("trash_2", class_name="mr-2 h-4 w-4"),
                        "Delete Plan",
                        on_click=lambda: PlanState.delete_plan(True),
                        class_name="flex items-center text-sm text-red-600 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-md transition-colors",
                    ),
                    None,
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.cond(
                PlanState.study_plan_items.length() > 0,
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Date",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Topic",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Hours",
                                    class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                            ),
                            class_name="bg-gray-50",
                        ),
                        rx.el.tbody(
                            rx.foreach(PlanState.study_plan_items, _plan_table_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="shadow-sm overflow-hidden border-b border-gray-200 sm:rounded-lg",
                ),
                rx.el.div(
                    rx.el.p(
                        "Your study plan is empty. Generate a new plan above to get started.",
                        class_name="text-gray-500",
                    ),
                    class_name="text-center py-12 bg-white rounded-lg border",
                ),
            ),
        ),
        class_name="container mx-auto px-6 py-12 space-y-12",
    )


def _unauthenticated_view() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Please log in to access your study plan.",
            class_name="text-xl text-gray-600 font-medium",
        ),
        rx.el.a(
            "Go to Login",
            href="/login",
            class_name="mt-4 px-6 py-2 bg-emerald-500 text-white font-semibold rounded-lg shadow-md hover:bg-emerald-600 transition-all",
        ),
        class_name="text-center flex flex-col items-center justify-center min-h-[calc(100vh-280px)]",
    )


def plan_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                AuthState.is_hydrated,
                rx.cond(
                    AuthState.is_authenticated,
                    _authenticated_view(),
                    _unauthenticated_view(),
                ),
                rx.el.div(
                    rx.spinner(class_name="text-emerald-500 w-12 h-12"),
                    class_name="min-h-[calc(100vh-280px)] flex items-center justify-center",
                ),
            ),
            class_name="font-['Montserrat'] min-h-[calc(100vh-280px)]",
        ),
        footer(),
        class_name="bg-gray-50",
        on_mount=[AuthState.hydrate_user, PlanState.on_page_load],
    )