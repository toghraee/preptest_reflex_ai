import reflex as rx
from app.components.shared.navbar import navbar
from app.components.shared.footer import footer
from app.pages.auth.auth_backend import AuthState


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Master Your Exams with a Personalized Study Plan",
                    class_name="text-4xl md:text-6xl font-bold text-gray-800 tracking-tighter mb-6",
                ),
                rx.el.p(
                    "PrepMyExam leverages AI to create optimized study schedules, helping you learn smarter, not harder. Stop guessing, start acing.",
                    class_name="max-w-2xl mx-auto text-lg text-gray-600 mb-8",
                ),
                rx.el.div(
                    rx.el.a(
                        "Get Started - It's Free",
                        href="/signup",
                        class_name="px-8 py-3 bg-emerald-500 text-white font-semibold rounded-lg shadow-md hover:bg-emerald-600 transition-all duration-300",
                    ),
                    rx.el.a(
                        "Watch Demo",
                        rx.icon("circle_play", class_name="mr-2"),
                        href="#",
                        class_name="flex items-center px-8 py-3 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-all duration-300",
                    ),
                    class_name="flex flex-col sm:flex-row items-center justify-center gap-4",
                ),
            ),
            class_name="container mx-auto px-6 text-center",
        ),
        class_name="py-20 md:py-32 bg-white",
    )


def video_placeholder_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("play", class_name="text-emerald-500 w-16 h-16"),
                    class_name="w-full h-full bg-gray-200 rounded-2xl flex items-center justify-center",
                ),
                class_name="aspect-video bg-gray-100 rounded-2xl shadow-lg p-2 border",
            ),
            class_name="container mx-auto px-6",
        ),
        class_name="py-16",
    )


def features_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "How It Works",
                class_name="text-3xl md:text-4xl font-bold text-gray-800 text-center mb-12",
            ),
            rx.el.div(
                _feature_card(
                    icon="edit_calendar",
                    title="1. Select Your Exam",
                    description="Choose your subject, exam board, and exam date from our extensive database.",
                ),
                _feature_card(
                    icon="checklist",
                    title="2. Pick Your Topics",
                    description="Select the specific topics and sub-topics you need to cover for your exam.",
                ),
                _feature_card(
                    icon="auto_awesome",
                    title="3. Generate Your Plan",
                    description="Our algorithm creates a balanced and effective study schedule tailored just for you.",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            class_name="container mx-auto px-6",
        ),
        class_name="py-16 bg-white",
    )


def _feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-10 h-10 mb-4 text-emerald-500"),
        rx.el.h3(title, class_name="text-xl font-semibold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-gray-600"),
        class_name="p-8 bg-gray-50 rounded-2xl border border-gray-100 text-center",
    )


def public_landing_page() -> rx.Component:
    return rx.el.main(
        hero_section(),
        video_placeholder_section(),
        features_section(),
        class_name="font-['Montserrat']",
    )


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