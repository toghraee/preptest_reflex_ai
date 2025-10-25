import reflex as rx


def footer_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="text-gray-500 hover:text-emerald-500 transition-colors",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.el.div(
                            rx.icon(
                                "book_check", class_name="h-6 w-6 text-emerald-500"
                            ),
                            rx.el.span(
                                "PrepMyExam",
                                class_name="text-xl font-bold text-gray-800",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        href="/",
                    ),
                    rx.el.p(
                        "Your personal AI-powered study planner.",
                        class_name="mt-2 text-gray-500 max-w-xs",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Product", class_name="font-semibold text-gray-700 mb-4"
                        ),
                        footer_link("Features", "#"),
                        footer_link("Pricing", "#"),
                        footer_link("Updates", "#"),
                        class_name="flex flex-col gap-3",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Company", class_name="font-semibold text-gray-700 mb-4"
                        ),
                        footer_link("About Us", "#"),
                        footer_link("Contact", "#"),
                        footer_link("Careers", "#"),
                        class_name="flex flex-col gap-3",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Legal", class_name="font-semibold text-gray-700 mb-4"
                        ),
                        footer_link("Privacy Policy", "#"),
                        footer_link("Terms of Service", "#"),
                        class_name="flex flex-col gap-3",
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-8",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-12",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2024 PrepMyExam. All rights reserved.",
                    class_name="text-gray-500",
                ),
                rx.el.div(
                    rx.el.a(rx.icon("twitter", class_name="w-5 h-5"), href="#"),
                    rx.el.a(rx.icon("github", class_name="w-5 h-5"), href="#"),
                    rx.el.a(rx.icon("linkedin", class_name="w-5 h-5"), href="#"),
                    class_name="flex items-center gap-4 text-gray-500",
                ),
                class_name="mt-12 pt-8 border-t flex flex-col sm:flex-row items-center justify-between",
            ),
            class_name="container mx-auto px-6 py-12",
        ),
        class_name="bg-white border-t font-['Montserrat']",
    )