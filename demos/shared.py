"""Shared utilities for card stack demos."""

from fasthtml.common import Div, H1, P, Span

from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import (
    flex_display, flex_direction, flex_wrap, items, justify, gap, grow
)
from cjm_fasthtml_tailwind.utilities.borders import rounded
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_keyboard_navigation.core.manager import ZoneManager
from cjm_fasthtml_keyboard_navigation.components.system import render_keyboard_system

from cjm_fasthtml_card_stack.core.config import CardStackConfig
from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
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


def generate_scale_spacing_js(config, ids):
    """Generate JS that adjusts card spacing proportionally to scale changes.

    Patches ns.updateScale and ns.applyScale to also update section-gap
    and slot-padding CSS custom properties based on the current scale value.
    Uses the style config defaults as the base values at 100% scale.
    """
    prefix = config.prefix
    style = config.style
    # Parse base rem values from config defaults
    base_gap = style.section_gap      # e.g. "1rem"
    base_pad = style.slot_padding     # e.g. "0.25rem"
    return f"""
        (function() {{
            const _baseGap = parseFloat('{base_gap}');
            const _basePad = parseFloat('{base_pad}');

            function _adjustSpacingForScale(scaleValue) {{
                const cs = document.getElementById('{ids.card_stack}');
                if (!cs) return;
                const s = parseInt(scaleValue) / 100;
                cs.style.setProperty('--{prefix}-section-gap', (_baseGap * s).toFixed(3) + 'rem');
                cs.style.setProperty('--{prefix}-slot-padding', (_basePad * s).toFixed(3) + 'rem');
            }}

            const _origUpdateScale = ns.updateScale;
            ns.updateScale = function(value) {{
                _origUpdateScale(value);
                _adjustSpacingForScale(value);
            }};

            const _origApplyScale = ns.applyScale;
            ns.applyScale = function() {{
                _origApplyScale();
                const slider = document.getElementById('{ids.scale_slider}');
                _adjustSpacingForScale(slider ? slider.value : 100);
            }};
        }})();
    """


def build_keyboard_system(config, btn_ids, ids, urls):
    """Build keyboard navigation system for a card stack."""
    zone = create_card_stack_focus_zone(ids)
    nav_actions = create_card_stack_nav_actions(zone.id, btn_ids, config)
    manager = ZoneManager(zones=(zone,), actions=nav_actions)

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


def render_demo_page(
    title,
    description,
    state_getter,
    items_getter,
    render_card,
    config,
    ids,
    btn_ids,
    urls,
    container_id,
    progress_label="Item",
    extra_scripts=(),
):
    """Render a standard card stack demo page.

    Returns a page_content() callable for use with handle_htmx_request.
    """

    def page_content():
        state = state_getter()
        card_items = items_getter()

        kb_system = build_keyboard_system(config, btn_ids, ids, urls)

        js_script = generate_card_stack_js(
            ids=ids,
            button_ids=btn_ids,
            config=config,
            urls=urls,
            container_id=container_id,
            focus_position=state.focus_position,
            extra_scripts=extra_scripts,
        )

        return Div(
            # Visual content container (used for viewport height calculation)
            Div(
                # Header
                Div(
                    H1(title, cls=combine_classes(font_size._2xl, font_weight.bold)),
                    P(description,
                      cls=combine_classes(text_dui.base_content, font_size.sm, m.b(4))),
                    cls=m.b(2)
                ),

                # Controls row
                Div(
                    Div(
                        render_card_count_select(config, ids, state.visible_count),
                        cls=combine_classes(flex_display, items.center, gap(2)),
                    ),
                    Div(
                        Span("Width:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                        render_width_slider(config, ids, state.card_width),
                        cls=combine_classes(flex_display, items.center, gap(2), grow()),
                    ),
                    Div(
                        Span("Scale:", cls=combine_classes(font_size.sm, text_dui.base_content)),
                        render_scale_slider(config, ids, state.card_scale),
                        cls=combine_classes(flex_display, items.center, gap(2), grow()),
                    ),
                    cls=combine_classes(
                        flex_display, flex_direction.col, flex_direction.row.sm,
                        flex_wrap.wrap, items.stretch, items.center.sm,
                        justify.between, gap.x(4), gap.y(2),
                        m.b(2), p(2),
                        bg_dui.base_200, rounded.lg,
                    )
                ),

                # Viewport
                render_viewport(
                    card_items=card_items,
                    state=state,
                    config=config,
                    render_card=render_card,
                    ids=ids,
                    urls=urls,
                ),

                # Footer
                Div(
                    render_progress_indicator(
                        state.focused_index, len(card_items), ids, label=progress_label
                    ),
                    cls=combine_classes(flex_display, justify.center, m.t(2))
                ),

                id=container_id,
            ),

            # Keyboard system
            kb_system.script,
            kb_system.hidden_inputs,
            kb_system.action_buttons,

            # Hidden buttons for JS-callback-triggered actions
            render_card_stack_action_buttons(btn_ids, urls, ids),

            # Card stack JS
            js_script,

            cls=combine_classes(container, max_w._6xl, m.x.auto, p(4))
        )

    return page_content
