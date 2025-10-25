import reflex as rx
from app.pages.auth.auth_backend import AuthState, User
from sqlalchemy import text
from typing import TypedDict, Optional
from datetime import datetime, timedelta
import random