import reflex as rx
from typing import Optional
import bcrypt
import uuid
from datetime import datetime, timedelta
from sqlalchemy import text
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str


class AuthState(rx.State):
    """Manages authentication, user sessions, and registration."""

    error_message: str = ""
    current_user: Optional[User] = None
    is_hydrated: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def _verify_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    @rx.event(background=True)
    async def handle_registration(self, form_data: dict):
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        async with self:
            if password != confirm_password:
                self.error_message = "Passwords do not match."
                return
            if len(password) < 8:
                self.error_message = "Password must be at least 8 characters long."
                return
            self.error_message = ""
        hashed_password = self._hash_password(password)
        async with rx.asession() as session:
            async with session.begin():
                result_user = await session.execute(
                    text("SELECT id FROM localuser WHERE username = :username"),
                    {"username": username},
                )
                if result_user.first():
                    async with self:
                        self.error_message = "Username already exists."
                    return
                result_email = await session.execute(
                    text("SELECT user_id FROM userinfo WHERE email = :email"),
                    {"email": email},
                )
                if result_email.first():
                    async with self:
                        self.error_message = "Email already registered."
                    return
                await session.execute(
                    text(
                        "INSERT INTO localuser (username, password_hash, enabled) VALUES (:username, :password, :enabled)"
                    ),
                    {"username": username, "password": hashed_password, "enabled": 1},
                )
                result = await session.execute(text("SELECT LAST_INSERT_ID() as id"))
                new_user_id = result.scalar_one()
                await session.execute(
                    text(
                        "INSERT INTO userinfo (email, user_id, created_at, updated_at) VALUES (:email, :user_id, :created, :updated)"
                    ),
                    {
                        "email": email,
                        "user_id": new_user_id,
                        "created": datetime.utcnow().isoformat(),
                        "updated": datetime.utcnow().isoformat(),
                    },
                )
        return rx.redirect("/login")

    @rx.event(background=True)
    async def handle_login(self, form_data: dict):
        username = form_data.get("username")
        password = form_data.get("password")
        async with self:
            self.error_message = ""
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT id, password_hash FROM localuser WHERE username = :username"
                ),
                {"username": username},
            )
            user_row = result.first()
            if user_row and self._verify_password(password, user_row.password_hash):
                user_id = user_row.id
                session_id = str(uuid.uuid4())
                expiration = (datetime.utcnow() + timedelta(hours=24)).isoformat()
                await session.execute(
                    text(
                        "INSERT INTO localauthsession (user_id, session_id, expiration) VALUES (:user_id, :session_id, :expiration)"
                    ),
                    {
                        "user_id": user_id,
                        "session_id": session_id,
                        "expiration": expiration,
                    },
                )
                await session.commit()
                return rx.redirect("/authenticated_home")
            else:
                async with self:
                    self.error_message = "Invalid username or password."

    @rx.event(background=True)
    async def handle_logout(self):
        session_id = self.router.cookies.get("session_id")
        if session_id:
            async with rx.asession() as session:
                await session.execute(
                    text("DELETE FROM localauthsession WHERE session_id = :session_id"),
                    {"session_id": session_id},
                )
                await session.commit()
        yield rx.remove_cookie("session_id")
        async with self:
            self.current_user = None
        yield rx.redirect("/")
        return

    @rx.event(background=True)
    async def hydrate_user(self, _=None):
        """Check for a valid session and hydrate the current_user."""
        async with self:
            if self.is_hydrated:
                if self.router.page.path == "/plan" and (not self.is_authenticated):
                    yield rx.redirect("/login")
                    return
                elif (
                    self.router.page.path in ["/login", "/signup"]
                    and self.is_authenticated
                ):
                    yield rx.redirect("/plan")
                    return
                yield
                return
            session_id = self.router.cookies.get("session_id")
            if session_id:
                async with rx.asession() as session:
                    result = await session.execute(
                        text("""
                        SELECT u.id, u.username, i.email, s.expiration
                        FROM localuser u
                        JOIN localauthsession s ON u.id = s.user_id
                        JOIN userinfo i ON u.id = i.user_id
                        WHERE s.session_id = :session_id
                        """),
                        {"session_id": session_id},
                    )
                    user_row = result.first()
                if (
                    user_row
                    and user_row.expiration
                    and (
                        datetime.fromisoformat(user_row.expiration) > datetime.utcnow()
                    )
                ):
                    self.current_user = User(
                        id=user_row.id, username=user_row.username, email=user_row.email
                    )
                else:
                    yield rx.remove_cookie("session_id")
                    self.current_user = None
            async with self:
                self.is_hydrated = True
            if self.router.page.path == "/plan" and (not self.is_authenticated):
                yield rx.redirect("/login")
                return
            elif (
                self.router.page.path in ["/login", "/signup"] and self.is_authenticated
            ):
                yield rx.redirect("/plan")
                return
        yield