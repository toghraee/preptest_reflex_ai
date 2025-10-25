import reflex as rx
from app.components.shared.navbar import navbar
from app.components.shared.footer import footer
from app.pages.auth.auth_backend import AuthState


def _action_card(icon: str, title: str, description: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-8 h-8 mb-4 text-emerald-500"),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-600"),
        href=href,
        class_name="p-6 bg-white rounded-xl border border-gray-200 hover:shadow-lg hover:-translate-y-1 transition-all",
    )


def authenticated_dashboard() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Welcome back, {AuthState.current_user.username}!",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Ready to ace your exams? Here is your dashboard.",
                    class_name="text-gray-600 mt-2",
                ),
            ),
            rx.el.div(
                _action_card(
                    "calendar_plus",
                    "Create a New Study Plan",
                    "Select your exam and topics to generate a personalized schedule.",
                    "/plan",
                ),
                _action_card(
                    "book_marked",
                    "View My Plans",
                    "Review and manage your existing study plans.",
                    "#",
                ),
                _action_card(
                    "line_chart",
                    "Track Progress",
                    "Monitor your study performance and topic coverage.",
                    "#",
                ),
                _action_card(
                    "file_question",
                    "Test Yourself",
                    "Take practice tests based on your selected subjects.",
                    "#",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8",
            ),
            class_name="container mx-auto px-6 py-12",
        ),
        class_name="font-['Montserrat'] min-h-[calc(100vh-280px)]",
    )


def authenticated_home_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.cond(AuthState.is_authenticated, authenticated_dashboard(), rx.el.div()),
        footer(),
        class_name="bg-gray-50",
        on_mount=AuthState.hydrate_user,
    )