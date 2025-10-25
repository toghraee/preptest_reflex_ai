import reflex as rx
from app.pages.auth.auth_backend import AuthState
from app.components.shared.navbar import navbar
from app.components.shared.footer import footer


def signup_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Create an Account",
                            class_name="text-3xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Start your journey with PrepMyExam.",
                            class_name="text-gray-600 mt-2",
                        ),
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Username",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="username",
                                placeholder="Enter your username",
                                class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email", class_name="text-sm font-medium text-gray-700"
                            ),
                            rx.el.input(
                                name="email",
                                placeholder="Enter your email",
                                type="email",
                                class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="password",
                                placeholder="Create a password",
                                type="password",
                                class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirm Password",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="confirm_password",
                                placeholder="Confirm your password",
                                type="password",
                                class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500",
                            ),
                            class_name="mb-6",
                        ),
                        rx.cond(
                            AuthState.error_message != "",
                            rx.el.div(
                                rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                                rx.el.p(AuthState.error_message),
                                class_name="flex items-center p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-md",
                            ),
                            None,
                        ),
                        rx.el.button(
                            "Sign Up",
                            type="submit",
                            class_name="w-full py-2 px-4 bg-emerald-500 text-white font-semibold rounded-lg shadow-md hover:bg-emerald-600 transition-all duration-300",
                        ),
                        on_submit=AuthState.handle_registration,
                        reset_on_submit=True,
                    ),
                    rx.el.p(
                        "Already have an account? ",
                        rx.el.a(
                            "Log in",
                            href="/login",
                            class_name="font-medium text-emerald-600 hover:text-emerald-500",
                        ),
                        class_name="mt-6 text-center text-sm text-gray-600",
                    ),
                    class_name="max-w-md w-full mx-auto bg-white p-8 rounded-2xl shadow-sm border border-gray-100",
                ),
                class_name="min-h-[calc(100vh-280px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8",
            ),
            class_name="font-['Montserrat']",
        ),
        footer(),
        class_name="bg-gray-50",
    )