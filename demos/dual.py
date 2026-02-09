"""Dual card stack demo with side-by-side layout and zone switching.

Demonstrates multi-instance support with two independent card stacks:
- Left: Text segments (using SAMPLE_ITEMS)
- Right: Audio chunks (using SAMPLE_AUDIO_CHUNKS)

Each stack has its own state, router, and viewport height calculation.
Keyboard navigation switches between stacks with Left/Right arrow keys.
"""

from fasthtml.common import Div, H1, H2, P, Span, Script

from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w, w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import (
    flex_display, items, justify, gap, grow
)
from cjm_fasthtml_tailwind.utilities.borders import rounded
from cjm_fasthtml_tailwind.utilities.effects import opacity
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_keyboard_navigation.core.manager import ZoneManager
from cjm_fasthtml_keyboard_navigation.components.system import render_keyboard_system

from cjm_fasthtml_card_stack.core.config import CardStackConfig
from cjm_fasthtml_card_stack.core.models import CardStackState, CardRenderContext
from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
from cjm_fasthtml_card_stack.core.button_ids import CardStackButtonIds
from cjm_fasthtml_card_stack.routes.router import init_card_stack_router
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

from demos.data import SAMPLE_ITEMS, SAMPLE_AUDIO_CHUNKS
from demos.shared import generate_scale_spacing_js


# -----------------------------------------------------------------------------
# Card renderers
# -----------------------------------------------------------------------------

def render_text_card(item, context: CardRenderContext):
    """Render a text segment card with index badge."""
    is_focused = context.card_role == "focused"

    index_badge = Span(
        f"#{context.index + 1}",
        cls=combine_classes(
            badge,
            badge_colors.primary if is_focused else badge_colors.neutral,
        )
    )

    text = P(
        f'"{item}"',
        cls=combine_classes(
            font_weight.medium if is_focused else font_weight.normal,
            text_dui.base_content,
            font_size('[calc(1rem*var(--card-stack-scale,100)/100)]'),
        ),
    )

    return Div(
        Div(
            Div(
                index_badge,
                cls=combine_classes(flex_display, items.center, gap(2), m.b(2)),
            ),
            text,
            cls=card_body,
        ),
        cls=combine_classes(card, bg_dui.base_100, w.full),
    )


def render_audio_card(item, context: CardRenderContext):
    """Render an audio chunk card with time range and duration.

    item is a tuple: (start_seconds, end_seconds, label)
    """
    start, end, label = item
    duration = end - start
    is_focused = context.card_role == "focused"

    def format_time(seconds):
        """Format seconds as m:ss.s"""
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}:{secs:04.1f}"

    time_badge = Span(
        f"{format_time(start)} - {format_time(end)}",
        cls=combine_classes(
            badge,
            badge_colors.secondary if is_focused else badge_colors.neutral,
        )
    )

    duration_badge = Span(
        f"{duration:.1f}s",
        cls=combine_classes(badge, badge_colors.accent),
    )

    return Div(
        Div(
            Div(
                time_badge,
                duration_badge,
                cls=combine_classes(flex_display, items.center, gap(2), m.b(2)),
            ),
            P(
                label,
                cls=combine_classes(
                    font_weight.medium if is_focused else font_weight.normal,
                    text_dui.base_content,
                    font_size('[calc(1rem*var(--card-stack-scale,100)/100)]'),
                ),
            ),
            cls=card_body,
        ),
        cls=combine_classes(card, bg_dui.base_100, w.full),
    )


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

def setup(route_prefix="/dual"):
    """Set up the dual card stack demo.

    Returns dict with configs, routers, and page rendering callable.
    """
    # --- Text stack (left) ---
    text_config = CardStackConfig(prefix="dual-text", click_to_focus=True)
    text_ids = CardStackHtmlIds(prefix=text_config.prefix)
    text_btn_ids = CardStackButtonIds(prefix=text_config.prefix)
    text_state = CardStackState(visible_count=5, card_width=60)

    def get_text_state():
        return text_state

    def set_text_state(s):
        text_state.focused_index = s.focused_index
        text_state.visible_count = s.visible_count
        text_state.card_width = s.card_width
        text_state.card_scale = s.card_scale
        text_state.active_mode = s.active_mode
        text_state.focus_position = s.focus_position

    def get_text_items():
        return SAMPLE_ITEMS

    text_router, text_urls = init_card_stack_router(
        config=text_config,
        state_getter=get_text_state,
        state_setter=set_text_state,
        get_items=get_text_items,
        render_card=render_text_card,
        route_prefix=f"{route_prefix}/text",
    )

    # --- Audio stack (right) ---
    audio_config = CardStackConfig(prefix="dual-audio", click_to_focus=True)
    audio_ids = CardStackHtmlIds(prefix=audio_config.prefix)
    audio_btn_ids = CardStackButtonIds(prefix=audio_config.prefix)
    audio_state = CardStackState(visible_count=5, card_width=50)

    def get_audio_state():
        return audio_state

    def set_audio_state(s):
        audio_state.focused_index = s.focused_index
        audio_state.visible_count = s.visible_count
        audio_state.card_width = s.card_width
        audio_state.card_scale = s.card_scale
        audio_state.active_mode = s.active_mode
        audio_state.focus_position = s.focus_position

    def get_audio_items():
        return SAMPLE_AUDIO_CHUNKS

    audio_router, audio_urls = init_card_stack_router(
        config=audio_config,
        state_getter=get_audio_state,
        state_setter=set_audio_state,
        get_items=get_audio_items,
        render_card=render_audio_card,
        route_prefix=f"{route_prefix}/audio",
    )

    # --- Column container IDs (for viewport height calculation) ---
    text_container_id = "dual-text-column"
    audio_container_id = "dual-audio-column"

    # --- Keyboard navigation with two zones ---
    def build_dual_keyboard_system():
        """Build keyboard system with two zones and zone switching."""
        text_zone = create_card_stack_focus_zone(text_ids)
        audio_zone = create_card_stack_focus_zone(audio_ids)

        text_nav_actions = create_card_stack_nav_actions(
            text_zone.id, text_btn_ids, text_config
        )
        audio_nav_actions = create_card_stack_nav_actions(
            audio_zone.id, audio_btn_ids, audio_config
        )

        # Zone switching is built into ZoneManager via prev_zone_key/next_zone_key
        # (defaults to ArrowLeft/ArrowRight)
        all_actions = text_nav_actions + audio_nav_actions

        manager = ZoneManager(
            zones=(text_zone, audio_zone),
            actions=all_actions,
            initial_zone_id=text_zone.id,
            on_zone_change="dualDemoOnZoneChange",  # global callback for visual updates
        )

        # Build URL/target/swap/include maps for both stacks
        text_url_map = build_card_stack_url_map(text_btn_ids, text_urls)
        audio_url_map = build_card_stack_url_map(audio_btn_ids, audio_urls)
        url_map = {**text_url_map, **audio_url_map}

        target_map = {
            **{btn_id: f"#{text_ids.card_stack}" for btn_id in text_url_map},
            **{btn_id: f"#{audio_ids.card_stack}" for btn_id in audio_url_map},
        }
        swap_map = {btn_id: "none" for btn_id in url_map}
        include_map = {
            **{btn_id: f"#{text_ids.focused_index_input}" for btn_id in text_url_map},
            **{btn_id: f"#{audio_ids.focused_index_input}" for btn_id in audio_url_map},
        }

        return render_keyboard_system(
            manager,
            url_map=url_map,
            target_map=target_map,
            swap_map=swap_map,
            include_map=include_map,
            show_hints=False,
            include_state_inputs=True,
        )

    # --- Page content factory ---
    def page_content():
        t_state = get_text_state()
        a_state = get_audio_state()
        text_items = get_text_items()
        audio_items = get_audio_items()

        kb_system = build_dual_keyboard_system()

        text_js = generate_card_stack_js(
            ids=text_ids,
            button_ids=text_btn_ids,
            config=text_config,
            urls=text_urls,
            container_id=text_container_id,
            focus_position=t_state.focus_position,
            extra_scripts=(generate_scale_spacing_js(text_config, text_ids),),
        )

        audio_js = generate_card_stack_js(
            ids=audio_ids,
            button_ids=audio_btn_ids,
            config=audio_config,
            urls=audio_urls,
            container_id=audio_container_id,
            focus_position=a_state.focus_position,
            extra_scripts=(generate_scale_spacing_js(audio_config, audio_ids),),
        )

        # Active zone visual styling via ZoneManager callback
        zone_style_js = Script(f"""
            (function() {{
                const textZoneId = '{text_ids.card_stack}';
                const textColId = '{text_container_id}';
                const audioColId = '{audio_container_id}';

                function updateZoneStyles(activeZoneId) {{
                    const textCol = document.getElementById(textColId);
                    const audioCol = document.getElementById(audioColId);
                    if (!textCol || !audioCol) return;

                    const isTextActive = activeZoneId === textZoneId;

                    // Ring classes
                    textCol.classList.toggle('ring-2', isTextActive);
                    textCol.classList.toggle('ring-primary', isTextActive);
                    audioCol.classList.toggle('ring-2', !isTextActive);
                    audioCol.classList.toggle('ring-primary', !isTextActive);

                    // Opacity
                    textCol.classList.toggle('opacity-70', !isTextActive);
                    audioCol.classList.toggle('opacity-70', isTextActive);
                }}

                // Global callback for ZoneManager
                window.dualDemoOnZoneChange = function(newZoneId, prevZoneId) {{
                    updateZoneStyles(newZoneId);
                }};

                // Initial update (text zone is active by default)
                updateZoneStyles(textZoneId);
            }})();
        """)

        return Div(
            # Header
            Div(
                H1("Dual Card Stack", cls=combine_classes(font_size._2xl, font_weight.bold)),
                P("Two independent card stacks with Left/Right zone switching. "
                  "Each stack has its own viewport, scroll navigation, and click-to-focus.",
                  cls=combine_classes(text_dui.base_content, font_size.sm, m.b(4))),
                cls=m.b(2)
            ),

            # Two-column layout
            Div(
                # Left column: Text segments
                Div(
                    # Column header
                    Div(
                        H2("Text Segments",
                           cls=combine_classes(font_size.lg, font_weight.semibold)),
                        Span(f"{len(text_items)} items",
                             cls=combine_classes(badge, badge_colors.primary)),
                        cls=combine_classes(
                            flex_display, items.center, justify.between, m.b(2)
                        )
                    ),

                    # Controls
                    Div(
                        render_card_count_select(text_config, text_ids, t_state.visible_count),
                        Div(
                            Span("W:", cls=combine_classes(font_size.xs, text_dui.base_content)),
                            render_width_slider(text_config, text_ids, t_state.card_width),
                            cls=combine_classes(flex_display, items.center, gap(1), grow()),
                        ),
                        Div(
                            Span("S:", cls=combine_classes(font_size.xs, text_dui.base_content)),
                            render_scale_slider(text_config, text_ids, t_state.card_scale),
                            cls=combine_classes(flex_display, items.center, gap(1), grow()),
                        ),
                        cls=combine_classes(
                            flex_display, items.center, gap(2), m.b(2), p(2),
                            bg_dui.base_200, rounded.lg, font_size.sm
                        )
                    ),

                    # Viewport
                    render_viewport(
                        card_items=text_items,
                        state=t_state,
                        config=text_config,
                        render_card=render_text_card,
                        ids=text_ids,
                        urls=text_urls,
                    ),

                    # Progress
                    Div(
                        render_progress_indicator(
                            t_state.focused_index, len(text_items), text_ids, label="Segment"
                        ),
                        cls=combine_classes(flex_display, justify.center, m.t(2))
                    ),

                    id=text_container_id,
                    cls=combine_classes(
                        w('[48%]'),
                        p(3), rounded.lg, bg_dui.base_100,
                    ),
                ),

                # Right column: Audio chunks
                Div(
                    # Column header
                    Div(
                        H2("Audio Chunks",
                           cls=combine_classes(font_size.lg, font_weight.semibold)),
                        Span(f"{len(audio_items)} chunks",
                             cls=combine_classes(badge, badge_colors.secondary)),
                        cls=combine_classes(
                            flex_display, items.center, justify.between, m.b(2)
                        )
                    ),

                    # Controls
                    Div(
                        render_card_count_select(audio_config, audio_ids, a_state.visible_count),
                        Div(
                            Span("W:", cls=combine_classes(font_size.xs, text_dui.base_content)),
                            render_width_slider(audio_config, audio_ids, a_state.card_width),
                            cls=combine_classes(flex_display, items.center, gap(1), grow()),
                        ),
                        Div(
                            Span("S:", cls=combine_classes(font_size.xs, text_dui.base_content)),
                            render_scale_slider(audio_config, audio_ids, a_state.card_scale),
                            cls=combine_classes(flex_display, items.center, gap(1), grow()),
                        ),
                        cls=combine_classes(
                            flex_display, items.center, gap(2), m.b(2), p(2),
                            bg_dui.base_200, rounded.lg, font_size.sm
                        )
                    ),

                    # Viewport
                    render_viewport(
                        card_items=audio_items,
                        state=a_state,
                        config=audio_config,
                        render_card=render_audio_card,
                        ids=audio_ids,
                        urls=audio_urls,
                    ),

                    # Progress
                    Div(
                        render_progress_indicator(
                            a_state.focused_index, len(audio_items), audio_ids, label="Chunk"
                        ),
                        cls=combine_classes(flex_display, justify.center, m.t(2))
                    ),

                    id=audio_container_id,
                    cls=combine_classes(
                        w('[48%]'),
                        p(3), rounded.lg, bg_dui.base_100,
                        opacity(70),  # Start inactive
                    ),
                ),

                cls=combine_classes(
                    flex_display, justify.between, gap(4),
                )
            ),

            # Keyboard system
            kb_system.script,
            kb_system.hidden_inputs,
            kb_system.action_buttons,

            # Hidden action buttons for both stacks
            render_card_stack_action_buttons(text_btn_ids, text_urls, text_ids),
            render_card_stack_action_buttons(audio_btn_ids, audio_urls, audio_ids),

            # Card stack JS for both stacks
            text_js,
            audio_js,

            # Zone style updater
            zone_style_js,

            cls=combine_classes(container, max_w._7xl, m.x.auto, p(4))
        )

    return dict(
        text_config=text_config,
        audio_config=audio_config,
        text_router=text_router,
        audio_router=audio_router,
        page_content=page_content,
        get_text_items=get_text_items,
        get_audio_items=get_audio_items,
    )
