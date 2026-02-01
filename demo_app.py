"""Demo application for cjm-fasthtml-card-stack library.

This demo showcases the card stack component:

1. CardStackConfig & CardStackState:
   - Auto-generated prefix for HTML ID uniqueness
   - Configurable visible count, width, and scale bounds
   - Click-to-focus for context card navigation

2. Convenience Router:
   - init_card_stack_router wires up all navigation/viewport/preference routes
   - Returns (APIRouter, CardStackUrls) tuple

3. Viewport Rendering:
   - 3-section CSS Grid layout (before / focused / after)
   - Placeholder cards at list edges
   - Opacity reveal pattern preventing FOUC

4. Controls:
   - Width slider with localStorage persistence
   - Scale slider with localStorage persistence
   - Card count selector dropdown
   - Progress indicator

5. Keyboard Navigation:
   - Arrow Up/Down for item navigation
   - Ctrl+Arrow for page jump
   - Ctrl+Shift+Arrow for first/last
   - [ / ] for viewport width adjustment
   - Scroll wheel navigation

6. Click-to-Focus:
   - Transparent overlay on context cards
   - Click any visible card to navigate to it

Run with: python demo_app.py
"""


# Sample items for the demo
SAMPLE_QUOTES = [
    "The only way to do great work is to love what you do.",
    "Innovation distinguishes between a leader and a follower.",
    "Stay hungry, stay foolish.",
    "The people who are crazy enough to think they can change the world are the ones who do.",
    "Your time is limited, so don't waste it living someone else's life.",
    "Design is not just what it looks like and feels like. Design is how it works.",
    "The best way to predict the future is to invent it.",
    "Simplicity is the ultimate sophistication.",
    "Quality is not an act, it is a habit.",
    "The only limit to our realization of tomorrow is our doubts of today.",
    "In the middle of difficulty lies opportunity.",
    "It does not matter how slowly you go as long as you do not stop.",
    "The journey of a thousand miles begins with one step.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals.",
    "Believe you can and you're halfway there.",
    "Act as if what you do makes a difference. It does.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "The secret of getting ahead is getting started.",
    "It is during our darkest moments that we must focus to see the light.",
    "The only impossible journey is the one you never begin.",
    "Do what you can, with what you have, where you are.",
    "Everything you've ever wanted is on the other side of fear.",
    "You miss 100% of the shots you don't take.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Life is what happens when you're busy making other plans.",
]


def main():
    """Main entry point - initializes card stack demo and starts the server."""
    from fasthtml.common import fast_app, Div, H1, H2, P, Span, A, Script, APIRouter

    # DaisyUI and Tailwind utilities
    from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
    from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
    from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
    from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
    from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui, border_dui

    from cjm_fasthtml_tailwind.utilities.spacing import p, m
    from cjm_fasthtml_tailwind.utilities.sizing import container, max_w, w, h, min_h
    from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
    from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import (
        flex_display, flex_direction, items, justify, gap, grid_display, grid_cols
    )
    from cjm_fasthtml_tailwind.utilities.borders import rounded, border, border_color
    from cjm_fasthtml_tailwind.utilities.layout import overflow
    from cjm_fasthtml_tailwind.utilities.effects import ring, ring_color, opacity
    from cjm_fasthtml_tailwind.core.base import combine_classes

    # App core utilities
    from cjm_fasthtml_app_core.components.navbar import create_navbar
    from cjm_fasthtml_app_core.core.routing import register_routes
    from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
    from cjm_fasthtml_app_core.core.layout import wrap_with_layout

    # Keyboard navigation
    from cjm_fasthtml_keyboard_navigation.core.manager import ZoneManager
    from cjm_fasthtml_keyboard_navigation.components.system import render_keyboard_system

    # Card stack library
    from cjm_fasthtml_card_stack.core.config import CardStackConfig, _reset_prefix_counter
    from cjm_fasthtml_card_stack.core.models import CardStackState, CardRenderContext, CardStackUrls
    from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
    from cjm_fasthtml_card_stack.core.button_ids import CardStackButtonIds
    from cjm_fasthtml_card_stack.components.viewport import render_viewport
    from cjm_fasthtml_card_stack.components.controls import (
        render_width_slider, render_scale_slider, render_card_count_select
    )
    from cjm_fasthtml_card_stack.components.progress import render_progress_indicator
    from cjm_fasthtml_card_stack.js.core import generate_card_stack_js
    from cjm_fasthtml_card_stack.keyboard.actions import (
        create_card_stack_focus_zone, create_card_stack_nav_actions,
        build_card_stack_url_map, render_card_stack_action_buttons
    )
    from cjm_fasthtml_card_stack.routes.router import init_card_stack_router

    print("\n" + "=" * 70)
    print("Initializing cjm-fasthtml-card-stack Demo")
    print("=" * 70)

    # Reset prefix counter for deterministic IDs
    _reset_prefix_counter()

    # Create the FastHTML app
    app, rt = fast_app(
        pico=False,
        hdrs=[
            *get_daisyui_headers(),
            create_theme_persistence_script(),
        ],
        title="Card Stack Demo",
        htmlkw={'data-theme': 'light'},
        secret_key="demo-secret-key"
    )

    router = APIRouter(prefix="")

    print("  FastHTML app created successfully")

    # -------------------------------------------------------------------------
    # Demo 1: Basic Card Stack (centered focus, keyboard nav)
    # -------------------------------------------------------------------------
    print("\n[1/2] Setting up basic card stack demo...")

    basic_config = CardStackConfig(
        prefix="basic",
        click_to_focus=True,
    )
    basic_ids = CardStackHtmlIds(prefix=basic_config.prefix)
    basic_btn_ids = CardStackButtonIds(prefix=basic_config.prefix)

    # State storage
    basic_state = CardStackState(visible_count=5, card_width=60)

    def basic_get_state():
        return basic_state

    def basic_set_state(s):
        nonlocal basic_state
        # Copy fields to preserve the object reference
        basic_state.focused_index = s.focused_index
        basic_state.visible_count = s.visible_count
        basic_state.card_width = s.card_width
        basic_state.card_scale = s.card_scale
        basic_state.active_mode = s.active_mode
        basic_state.focus_position = s.focus_position

    def basic_get_items():
        return SAMPLE_QUOTES

    def basic_render_card(item, context: CardRenderContext):
        """Render a quote card."""
        is_focused = context.card_role == "focused"

        # Card content
        index_badge = Span(
            f"#{context.index + 1}",
            cls=combine_classes(
                badge,
                badge_colors.primary if is_focused else badge_colors.neutral,
            )
        )

        quote_text = P(
            f'"{item}"',
            cls=combine_classes(
                font_weight.medium if is_focused else font_weight.normal,
                text_dui.base_content,
            ),
            # Use CSS custom property for immediate scale response
            style="font-size: calc(1rem * var(--card-stack-scale, 100) / 100)",
        )

        return Div(
            Div(
                Div(
                    index_badge,
                    Span(
                        f"Item {context.index + 1} of {context.total_items}",
                        cls=combine_classes(font_size.xs, text_dui.base_content, str(opacity(60))),
                    ),
                    cls=combine_classes(flex_display, items.center, gap(2), m.b(2)),
                ),
                quote_text,
                cls=card_body,
            ),
            cls=combine_classes(
                card,
                bg_dui.base_100 if is_focused else bg_dui.base_200,
                w.full,
            ),
        )

    # Create convenience router
    basic_router, basic_urls = init_card_stack_router(
        config=basic_config,
        state_getter=basic_get_state,
        state_setter=basic_set_state,
        get_items=basic_get_items,
        render_card=basic_render_card,
        route_prefix="/basic",
    )

    print("  Basic card stack configured (centered, click-to-focus, 25 quotes)")

    # -------------------------------------------------------------------------
    # Demo 2: Bottom-anchored Card Stack (chat-style)
    # -------------------------------------------------------------------------
    print("\n[2/2] Setting up bottom-anchored card stack demo...")

    bottom_config = CardStackConfig(
        prefix="bottom",
        click_to_focus=True,
    )
    bottom_ids = CardStackHtmlIds(prefix=bottom_config.prefix)
    bottom_btn_ids = CardStackButtonIds(prefix=bottom_config.prefix)

    bottom_state = CardStackState(
        visible_count=5,
        card_width=60,
        focus_position=-1,  # Bottom-anchored
    )

    def bottom_get_state():
        return bottom_state

    def bottom_set_state(s):
        nonlocal bottom_state
        bottom_state.focused_index = s.focused_index
        bottom_state.visible_count = s.visible_count
        bottom_state.card_width = s.card_width
        bottom_state.card_scale = s.card_scale
        bottom_state.active_mode = s.active_mode
        bottom_state.focus_position = s.focus_position

    def bottom_get_items():
        return SAMPLE_QUOTES

    def bottom_render_card(item, context: CardRenderContext):
        """Render a chat-style message card."""
        is_focused = context.card_role == "focused"

        index_badge = Span(
            f"#{context.index + 1}",
            cls=combine_classes(
                badge,
                badge_colors.secondary if is_focused else badge_colors.neutral,
            )
        )

        return Div(
            Div(
                Div(
                    index_badge,
                    cls=combine_classes(m.b(1)),
                ),
                P(
                    item,
                    cls=combine_classes(
                        text_dui.base_content,
                    ),
                    # Use CSS custom property for immediate scale response
                    style="font-size: calc(0.875rem * var(--card-stack-scale, 100) / 100)",
                ),
                cls=combine_classes(card_body, p(3)),
            ),
            cls=combine_classes(
                card,
                bg_dui.base_100 if is_focused else bg_dui.base_200,
                w.full,
            ),
        )

    bottom_router, bottom_urls = init_card_stack_router(
        config=bottom_config,
        state_getter=bottom_get_state,
        state_setter=bottom_set_state,
        get_items=bottom_get_items,
        render_card=bottom_render_card,
        route_prefix="/bottom",
    )

    print("  Bottom-anchored card stack configured (chat-style, 25 quotes)")

    # -------------------------------------------------------------------------
    # Keyboard Setup Helper
    # -------------------------------------------------------------------------
    def build_keyboard_system(config, btn_ids, ids, urls):
        """Build keyboard navigation system for a card stack."""
        zone = create_card_stack_focus_zone(ids)
        nav_actions = create_card_stack_nav_actions(zone.id, btn_ids, config)
        manager = ZoneManager(zones=(zone,), actions=nav_actions)

        # Build maps for all navigation buttons (nav up/down + page jump + first/last)
        url_map = build_card_stack_url_map(btn_ids, urls)
        target_map = {btn_id: f"#{ids.card_stack}" for btn_id in url_map}
        swap_map = {btn_id: "none" for btn_id in url_map}
        include_map = {btn_id: f"#{ids.focused_index_input}" for btn_id in url_map}

        return render_keyboard_system(
            manager,
            url_map=url_map,
            target_map=target_map,
            swap_map=swap_map,
            include_map=include_map,
            show_hints=False,
            include_state_inputs=True,
        )

    # -------------------------------------------------------------------------
    # Page Routes
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
                    # Basic demo card
                    Div(
                        Div(
                            H2("Basic Card Stack",
                               cls=combine_classes(font_size.xl, font_weight.semibold, m.b(2))),
                            P("Centered focus with keyboard navigation, scroll wheel, "
                              "width/scale sliders, and click-to-focus.",
                              cls=combine_classes(text_dui.base_content, m.b(4))),
                            Div(
                                Span("Centered", cls=combine_classes(badge, badge_colors.primary, m.r(2))),
                                Span("Click-to-focus", cls=combine_classes(badge, badge_colors.secondary, m.r(2))),
                                Span("25 items", cls=combine_classes(badge, badge_colors.accent)),
                                cls=m.b(4)
                            ),
                            A("Open Demo",
                              href=demo_basic.to(),
                              cls=combine_classes(
                                  "btn", "btn-primary",
                              )),
                            cls=card_body
                        ),
                        cls=combine_classes(card, bg_dui.base_200)
                    ),

                    # Bottom-anchored demo card
                    Div(
                        Div(
                            H2("Bottom-Anchored Stack",
                               cls=combine_classes(font_size.xl, font_weight.semibold, m.b(2))),
                            P("Chat-style layout with the focused card at the bottom. "
                              "Context cards appear above.",
                              cls=combine_classes(text_dui.base_content, m.b(4))),
                            Div(
                                Span("Bottom focus", cls=combine_classes(badge, badge_colors.primary, m.r(2))),
                                Span("Click-to-focus", cls=combine_classes(badge, badge_colors.secondary, m.r(2))),
                                Span("25 items", cls=combine_classes(badge, badge_colors.accent)),
                                cls=m.b(4)
                            ),
                            A("Open Demo",
                              href=demo_bottom.to(),
                              cls=combine_classes(
                                  "btn", "btn-secondary",
                              )),
                            cls=card_body
                        ),
                        cls=combine_classes(card, bg_dui.base_200)
                    ),

                    cls=combine_classes(
                        grid_display, grid_cols(1),
                        grid_cols(2).md,
                        gap(6), m.b(8)
                    )
                ),

                # Features section
                Div(
                    H2("Features", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                    Div(
                        P("Arrow Up/Down - Navigate between items", cls=m.b(1)),
                        P("Ctrl+Arrow Up/Down - Page jump", cls=m.b(1)),
                        P("Ctrl+Shift+Arrow Up/Down - First/last item", cls=m.b(1)),
                        P("[ / ] - Adjust viewport width", cls=m.b(1)),
                        P("Mouse wheel - Scroll navigation", cls=m.b(1)),
                        P("Click context cards - Navigate to card", cls=m.b(1)),
                        cls=combine_classes(text_align.left, max_w.md, m.x.auto, font_size.sm)
                    ),
                    cls=m.b(8)
                ),

                cls=combine_classes(
                    container,
                    max_w._5xl,
                    m.x.auto,
                    p(8),
                    text_align.center
                )
            )

        return handle_htmx_request(
            request,
            home_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    @router
    def demo_basic(request):
        """Basic centered card stack demo."""

        def page_content():
            state = basic_get_state()
            card_items = basic_get_items()

            # Build keyboard system
            kb_system = build_keyboard_system(
                basic_config, basic_btn_ids, basic_ids, basic_urls
            )

            # Container ID for viewport height calculation
            basic_container_id = "basic-demo-container"

            # Generate JS
            js_script = generate_card_stack_js(
                ids=basic_ids,
                button_ids=basic_btn_ids,
                config=basic_config,
                urls=basic_urls,
                container_id=basic_container_id,
            )

            return Div(
                # Visual content container (used for viewport height calculation)
                Div(
                    # Header
                    Div(
                        H1("Basic Card Stack",
                           cls=combine_classes(font_size._2xl, font_weight.bold)),
                        P("Centered focus. Navigate with arrow keys, scroll wheel, "
                          "or click any card.",
                          cls=combine_classes(text_dui.base_content, font_size.sm, m.b(4))),
                        cls=m.b(2)
                    ),

                    # Controls row
                    Div(
                        Div(
                            render_card_count_select(basic_config, basic_ids, state.visible_count),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        Div(
                            Span("Width:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                            render_width_slider(basic_config, basic_ids, state.card_width),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        Div(
                            Span("Scale:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                            render_scale_slider(basic_config, basic_ids, state.card_scale),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        cls=combine_classes(
                            flex_display, items.center, justify.between,
                            gap(4), m.b(2), p(2),
                            bg_dui.base_200, rounded.lg,
                        )
                    ),

                    # Viewport
                    render_viewport(
                        card_items=card_items,
                        state=state,
                        config=basic_config,
                        render_card=basic_render_card,
                        ids=basic_ids,
                        urls=basic_urls,
                    ),

                    # Footer
                    Div(
                        render_progress_indicator(
                            state.focused_index, len(card_items), basic_ids, label="Quote"
                        ),
                        cls=combine_classes(flex_display, justify.center, m.t(2))
                    ),

                    id=basic_container_id,
                    # cls=combine_classes(flex_display, flex_direction.col),
                ),

                # Keyboard system (renders hidden buttons + state inputs)
                kb_system.script,
                kb_system.hidden_inputs,
                kb_system.action_buttons,

                # Hidden buttons for JS-callback-triggered actions (page jump, first/last)
                render_card_stack_action_buttons(basic_btn_ids, basic_urls, basic_ids),

                # Card stack JS
                js_script,

                cls=combine_classes(container, max_w._6xl, m.x.auto, p(4))
            )

        return handle_htmx_request(
            request,
            page_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    @router
    def demo_bottom(request):
        """Bottom-anchored card stack demo."""

        def page_content():
            state = bottom_get_state()
            card_items = bottom_get_items()

            # Build keyboard system
            kb_system = build_keyboard_system(
                bottom_config, bottom_btn_ids, bottom_ids, bottom_urls
            )

            # Container ID for viewport height calculation
            bottom_container_id = "bottom-demo-container"

            # Generate JS
            js_script = generate_card_stack_js(
                ids=bottom_ids,
                button_ids=bottom_btn_ids,
                config=bottom_config,
                urls=bottom_urls,
                container_id=bottom_container_id,
            )

            return Div(
                # Visual content container (used for viewport height calculation)
                Div(
                    # Header
                    Div(
                        H1("Bottom-Anchored Card Stack",
                           cls=combine_classes(font_size._2xl, font_weight.bold)),
                        P("Chat-style layout with focused card at the bottom. "
                          "Context cards appear above.",
                          cls=combine_classes(text_dui.base_content, font_size.sm, m.b(4))),
                        cls=m.b(2)
                    ),

                    # Controls row
                    Div(
                        Div(
                            render_card_count_select(bottom_config, bottom_ids, state.visible_count),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        Div(
                            Span("Width:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                            render_width_slider(bottom_config, bottom_ids, state.card_width),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        Div(
                            Span("Scale:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                            render_scale_slider(bottom_config, bottom_ids, state.card_scale),
                            cls=combine_classes(flex_display, items.center, gap(2)),
                        ),
                        cls=combine_classes(
                            flex_display, items.center, justify.between,
                            gap(4), m.b(2), p(2),
                            bg_dui.base_200, rounded.lg,
                        )
                    ),

                    # Viewport
                    render_viewport(
                        card_items=card_items,
                        state=state,
                        config=bottom_config,
                        render_card=bottom_render_card,
                        ids=bottom_ids,
                        urls=bottom_urls,
                    ),

                    # Footer
                    Div(
                        render_progress_indicator(
                            state.focused_index, len(card_items), bottom_ids, label="Message"
                        ),
                        cls=combine_classes(flex_display, justify.center, m.t(2))
                    ),

                    id=bottom_container_id,
                    # cls=combine_classes(flex_display, flex_direction.col),
                ),

                # Keyboard system
                kb_system.script,
                kb_system.hidden_inputs,
                kb_system.action_buttons,

                # Hidden buttons for JS-callback-triggered actions (page jump, first/last)
                render_card_stack_action_buttons(bottom_btn_ids, bottom_urls, bottom_ids),

                # Card stack JS
                js_script,

                cls=combine_classes(container, max_w._6xl, m.x.auto, p(4))
            )

        return handle_htmx_request(
            request,
            page_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
        )

    # -------------------------------------------------------------------------
    # Navbar
    # -------------------------------------------------------------------------
    navbar = create_navbar(
        title="Card Stack Demo",
        nav_items=[
            ("Home", index),
            ("Basic", demo_basic),
            ("Bottom-Anchored", demo_bottom),
        ],
        home_route=index,
        theme_selector=True
    )

    # -------------------------------------------------------------------------
    # Register All Routes
    # -------------------------------------------------------------------------
    register_routes(
        app,
        router,
        basic_router,
        bottom_router,
    )

    # Debug: Print registered routes
    print("\n" + "=" * 70)
    print("Registered Routes:")
    print("=" * 70)
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.path}")

    print("\n" + "=" * 70)
    print("Demo App Ready!")
    print("=" * 70)
    print("\n Library Components:")
    print("  - CardStackConfig - Initialization settings with auto-prefix")
    print("  - CardStackState - Runtime viewport state")
    print("  - render_viewport - 3-section CSS Grid layout")
    print("  - init_card_stack_router - Convenience router factory")
    print("  - generate_card_stack_js - Namespaced JS callbacks")
    print("  - Keyboard navigation integration")
    print("=" * 70 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    app = main()

    def open_browser(url):
        print(f"Opening browser at {url}")
        webbrowser.open(url)

    port = 5033
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"Server: http://{display_host}:{port}")
    print("\nAvailable routes:")
    print(f"  http://{display_host}:{port}/              - Homepage with demo overview")
    print(f"  http://{display_host}:{port}/demo_basic    - Basic centered card stack")
    print(f"  http://{display_host}:{port}/demo_bottom   - Bottom-anchored card stack")
    print("\n" + "=" * 70 + "\n")

    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    uvicorn.run(app, host=host, port=port)
