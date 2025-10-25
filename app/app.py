import reflex as rx
from app.pages.landing_page import landing_page
from app.pages.authenticated_home.authenticated_home_page import authenticated_home_page
from app.pages.auth.signup_page import signup_page
from app.pages.auth.login_page import login_page
from app.pages.plan.plan_page import plan_page

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="jade", radius="medium"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=["/styles.css"],
)
app.add_page(landing_page, route="/")
app.add_page(authenticated_home_page, route="/authenticated_home")
app.add_page(signup_page, route="/signup")
app.add_page(login_page, route="/login")
app.add_page(plan_page, route="/plan")