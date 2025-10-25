import reflex as rx
from app.pages.auth.auth_backend import AuthState, User


def nav_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="text-gray-600 hover:text-emerald-500 font-medium transition-colors",
    )


def nav_button(text: str, href: str, primary: bool = False) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            primary,
            "px-4 py-2 bg-emerald-500 text-white rounded-lg shadow-sm hover:bg-emerald-600 transition-all",
            "px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all",
        ),
    )


def dropdown_menu(title: str, items: list[tuple[str, str]]) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            title,
            rx.icon("chevron_down", class_name="ml-1 w-5 h-5"),
            class_name="flex items-center text-gray-600 hover:text-emerald-500 font-medium transition-colors group",
        ),
        rx.el.div(
            rx.foreach(
                items,
                lambda item: rx.el.a(
                    item[0],
                    href=item[1],
                    class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
                ),
            ),
            class_name="absolute top-full mt-2 w-48 bg-white rounded-md shadow-lg border hidden group-hover:block",
        ),
        class_name="relative",
    )


def user_menu(user: User) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={user.username}",
                class_name="w-8 h-8 rounded-full",
            ),
            rx.icon("chevron_down", class_name="ml-2 w-4 h-4 text-gray-500"),
            class_name="flex items-center group",
        ),
        rx.el.div(
            rx.el.a(
                "My Account",
                href="/account",
                class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
            ),
            rx.el.a(
                "Upgrade",
                href="/upgrade",
                class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
            ),
            rx.el.button(
                "Logout",
                on_click=AuthState.handle_logout,
                class_name="w-full text-left block px-4 py-2 text-sm text-red-600 hover:bg-red-50 border-t",
            ),
            class_name="absolute top-full right-0 mt-2 w-48 bg-white rounded-md shadow-lg border hidden group-hover:block z-10",
        ),
        class_name="relative",
    )


def navbar() -> rx.Component:
    study_plan_items = [
        ("New Plan", "/plan"),
        ("My Plans", "#"),
        ("Topic Tracker", "#"),
        ("Your Week", "#"),
        ("Past Week", "#"),
    ]
    test_me_items = [("Test on Subjects", "#"), ("My Predictions", "#")]
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("book_check", class_name="h-7 w-7 text-emerald-500"),
                        rx.el.span(
                            "PrepMyExam",
                            class_name="text-2xl font-bold text-gray-800 tracking-tight",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    href=rx.cond(
                        AuthState.is_authenticated, "/authenticated_home", "/"
                    ),
                )
            ),
            rx.cond(
                AuthState.is_authenticated,
                rx.el.nav(
                    dropdown_menu("Study Plan", study_plan_items),
                    dropdown_menu("Test Me", test_me_items),
                    user_menu(AuthState.current_user),
                    class_name="hidden md:flex items-center gap-8",
                ),
                rx.el.nav(
                    nav_link("About", "#"),
                    nav_link("Pricing", "#"),
                    class_name="hidden md:flex items-center gap-8",
                ),
            ),
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(),
                rx.el.div(
                    nav_button("Login", "/login"),
                    nav_button("Sign Up", "/signup", primary=True),
                    class_name="hidden md:flex items-center gap-3",
                ),
            ),
            rx.el.button(
                rx.icon("menu", class_name="w-6 h-6"),
                class_name="md:hidden p-2 rounded-md hover:bg-gray-100",
            ),
            class_name="container mx-auto px-6 h-20 flex items-center justify-between",
        ),
        class_name="bg-white/80 backdrop-blur-md border-b sticky top-0 z-50 font-['Montserrat']",
        on_mount=AuthState.hydrate_user,
    )