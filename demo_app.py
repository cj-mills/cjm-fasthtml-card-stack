"""Demo application for cjm-fasthtml-card-stack library.

Showcases the card stack component with multiple demo configurations.
Each demo is a self-contained module in the demos/ package.

Run with: python demo_app.py
"""


def main():
    """Initialize card stack demos and start the server."""
    from fasthtml.common import fast_app, Div, H1, H2, P, Span, A, APIRouter

    from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
    from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
    from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
    from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
    from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui

    from cjm_fasthtml_tailwind.utilities.spacing import p, m
    from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
    from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
    from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import grid_display, grid_cols, gap
    from cjm_fasthtml_tailwind.core.base import combine_classes

    from cjm_fasthtml_app_core.components.navbar import create_navbar
    from cjm_fasthtml_app_core.core.routing import register_routes
    from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
    from cjm_fasthtml_app_core.core.layout import wrap_with_layout

    from cjm_fasthtml_card_stack.core.config import _reset_prefix_counter

    from demos.shared import render_demo_page
    import demos.basic as basic_demo
    import demos.bottom as bottom_demo
    import demos.custom_position as custom_demo
    import demos.dual as dual_demo

    print("\n" + "=" * 70)
    print("Initializing cjm-fasthtml-card-stack Demo")
    print("=" * 70)

    _reset_prefix_counter()

    app, rt = fast_app(
        pico=False,
        hdrs=[*get_daisyui_headers(), create_theme_persistence_script()],
        title="Card Stack Demo",
        htmlkw={'data-theme': 'light'},
        secret_key="demo-secret-key"
    )

    router = APIRouter(prefix="")

    # -------------------------------------------------------------------------
    # Set up demos
    # -------------------------------------------------------------------------
    basic = basic_demo.setup()
    bottom = bottom_demo.setup()
    custom = custom_demo.setup()
    dual = dual_demo.setup()

    print(f"  Basic demo: centered, click-to-focus, {len(basic['get_items']()):,} items")
    print(f"  Bottom demo: bottom-anchored, click-to-focus, {len(bottom['get_items']()):,} items")
    print(f"  Custom demo: focus_position=1, click-to-focus, {len(custom['get_items']()):,} items")
    print(f"  Dual demo: two stacks side-by-side, {len(dual['get_text_items']()):,} text + {len(dual['get_audio_items']()):,} audio")

    # Build page content factories using shared renderer
    _page_keys = (
        'title', 'description', 'config', 'ids', 'btn_ids', 'urls',
        'container_id', 'progress_label', 'render_card', 'extra_scripts',
    )

    basic_page = render_demo_page(**{
        k: basic[k] for k in _page_keys if k in basic
    }, state_getter=basic['get_state'], items_getter=basic['get_items'])

    bottom_page = render_demo_page(**{
        k: bottom[k] for k in _page_keys if k in bottom
    }, state_getter=bottom['get_state'], items_getter=bottom['get_items'])

    custom_page = render_demo_page(**{
        k: custom[k] for k in _page_keys if k in custom
    }, state_getter=custom['get_state'], items_getter=custom['get_items'])

    # -------------------------------------------------------------------------
    # Page routes
    # -------------------------------------------------------------------------
    @router
    def index(request):
        """Homepage with demo overview."""

        def home_content():
            return Div(
                H1("Card Stack Demo",
                   cls=combine_classes(font_size._4xl, font_weight.bold, m.b(4))),

                P("A fixed-viewport card stack component for FastHTML with keyboard "
                  "navigation, scroll-to-nav, configurable focus position, and "
                  "HTMX-driven OOB updates.",
                  cls=combine_classes(font_size.lg, text_dui.base_content, m.b(8))),

                # Demo cards
                Div(
                    _demo_card(
                        "Basic Card Stack",
                        "Centered focus with keyboard navigation, scroll wheel, "
                        "width/scale sliders, and click-to-focus.",
                        badges=[("Centered", badge_colors.primary),
                                ("Click-to-focus", badge_colors.secondary),
                                (f"{len(basic['get_items']()):,} items", badge_colors.accent)],
                        href=demo_basic.to(),
                        btn_cls="btn btn-primary",
                    ),
                    _demo_card(
                        "Bottom-Anchored Stack",
                        "Chat-style layout with the focused card at the bottom. "
                        "Context cards appear above.",
                        badges=[("Bottom focus", badge_colors.primary),
                                ("Click-to-focus", badge_colors.secondary),
                                (f"{len(bottom['get_items']()):,} items", badge_colors.accent)],
                        href=demo_bottom.to(),
                        btn_cls="btn btn-secondary",
                    ),
                    _demo_card(
                        "Custom Focus Position",
                        "Focus at slot 1 (second from top). Tests non-standard "
                        "focus_position values with card count changes.",
                        badges=[("Slot 1 focus", badge_colors.primary),
                                ("Click-to-focus", badge_colors.secondary),
                                (f"{len(custom['get_items']()):,} items", badge_colors.accent)],
                        href=demo_custom.to(),
                        btn_cls="btn btn-accent",
                    ),
                    _demo_card(
                        "Dual Card Stack",
                        "Two independent card stacks side by side with Left/Right "
                        "zone switching. Tests multi-instance viewport calculation.",
                        badges=[("Two stacks", badge_colors.primary),
                                ("Zone switching", badge_colors.secondary),
                                (f"{len(dual['get_text_items']()):,} + {len(dual['get_audio_items']()):,}", badge_colors.accent)],
                        href=demo_dual.to(),
                        btn_cls="btn btn-info",
                    ),
                    cls=combine_classes(
                        grid_display, grid_cols(1), grid_cols(2).md, gap(6), m.b(8)
                    )
                ),

                # Features section
                Div(
                    H2("Keyboard Shortcuts",
                       cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                    Div(
                        P("Arrow Up/Down — Navigate between items", cls=m.b(1)),
                        P("Ctrl+Arrow Up/Down — Page jump", cls=m.b(1)),
                        P("Ctrl+Shift+Arrow Up/Down — First/last item", cls=m.b(1)),
                        P("[ / ] — Adjust viewport width", cls=m.b(1)),
                        P("- / = — Adjust content scale", cls=m.b(1)),
                        P("Mouse wheel — Scroll navigation", cls=m.b(1)),
                        P("Click context cards — Navigate to card", cls=m.b(1)),
                        cls=combine_classes(text_align.left, max_w.md, m.x.auto, font_size.sm)
                    ),
                    cls=m.b(8)
                ),

                cls=combine_classes(
                    container, max_w._5xl, m.x.auto, p(8), text_align.center
                )
            )

        return handle_htmx_request(
            request, home_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    def _demo_card(title, description, badges, href, btn_cls):
        """Render a demo card for the homepage."""
        return Div(
            Div(
                H2(title, cls=combine_classes(font_size.xl, font_weight.semibold, m.b(2))),
                P(description, cls=combine_classes(text_dui.base_content, m.b(4))),
                Div(
                    *[Span(label, cls=combine_classes(badge, color, m.r(2)))
                      for label, color in badges],
                    cls=m.b(4)
                ),
                A("Open Demo", href=href, cls=btn_cls),
                cls=card_body
            ),
            cls=combine_classes(card, bg_dui.base_200)
        )

    @router
    def demo_basic(request):
        """Basic centered card stack demo."""
        return handle_htmx_request(
            request, basic_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    @router
    def demo_bottom(request):
        """Bottom-anchored card stack demo."""
        return handle_htmx_request(
            request, bottom_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    @router
    def demo_custom(request):
        """Custom focus position card stack demo."""
        return handle_htmx_request(
            request, custom_page,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    @router
    def demo_dual(request):
        """Dual card stack demo with zone switching."""
        return handle_htmx_request(
            request, dual['page_content'],
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    # -------------------------------------------------------------------------
    # Navbar & route registration
    # -------------------------------------------------------------------------
    navbar = create_navbar(
        title="Card Stack Demo",
        nav_items=[
            ("Home", index),
            ("Basic", demo_basic),
            ("Bottom-Anchored", demo_bottom),
            ("Custom Position", demo_custom),
            ("Dual", demo_dual),
        ],
        home_route=index,
        theme_selector=True
    )

    register_routes(
        app, router,
        basic['router'], bottom['router'], custom['router'],
        dual['text_router'], dual['audio_router']
    )

    # Debug output
    print("\n" + "=" * 70)
    print("Registered Routes:")
    print("=" * 70)
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.path}")
    print("=" * 70)
    print("Demo App Ready!")
    print("=" * 70 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    app = main()

    port = 5033
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"Server: http://{display_host}:{port}")
    print(f"\n  http://{display_host}:{port}/              — Homepage")
    print(f"  http://{display_host}:{port}/demo_basic    — Basic centered")
    print(f"  http://{display_host}:{port}/demo_bottom   — Bottom-anchored")
    print(f"  http://{display_host}:{port}/demo_custom   — Custom position (slot 1)")
    print(f"  http://{display_host}:{port}/demo_dual     — Dual stacks with zone switching")
    print()

    timer = threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    uvicorn.run(app, host=host, port=port)
