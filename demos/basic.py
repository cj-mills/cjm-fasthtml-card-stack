"""Basic centered card stack demo."""

from fasthtml.common import Div, P, Span

from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import m
from cjm_fasthtml_tailwind.utilities.sizing import w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import flex_display, items, gap
from cjm_fasthtml_tailwind.utilities.effects import opacity
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_card_stack.core.config import CardStackConfig
from cjm_fasthtml_card_stack.core.models import CardStackState, CardRenderContext
from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
from cjm_fasthtml_card_stack.core.button_ids import CardStackButtonIds
from cjm_fasthtml_card_stack.routes.router import init_card_stack_router

from demos.data import SAMPLE_ITEMS


def render_card(item, context: CardRenderContext):
    """Render a card with index badge and text content."""
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
        ),
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
            text,
            cls=card_body,
        ),
        cls=combine_classes(
            card,
            bg_dui.base_100 if is_focused else bg_dui.base_200,
            w.full,
        ),
    )


def setup(route_prefix="/basic"):
    """Set up the basic centered card stack demo.

    Returns dict with config, ids, btn_ids, router, urls, state management,
    and page rendering dependencies.
    """
    config = CardStackConfig(prefix="basic", click_to_focus=True)
    ids = CardStackHtmlIds(prefix=config.prefix)
    btn_ids = CardStackButtonIds(prefix=config.prefix)

    state = CardStackState(visible_count=5, card_width=60)

    def get_state():
        return state

    def set_state(s):
        nonlocal state
        state.focused_index = s.focused_index
        state.visible_count = s.visible_count
        state.card_width = s.card_width
        state.card_scale = s.card_scale
        state.active_mode = s.active_mode
        state.focus_position = s.focus_position

    def get_items():
        return SAMPLE_ITEMS

    router, urls = init_card_stack_router(
        config=config,
        state_getter=get_state,
        state_setter=set_state,
        get_items=get_items,
        render_card=render_card,
        route_prefix=route_prefix,
    )

    return dict(
        config=config,
        ids=ids,
        btn_ids=btn_ids,
        router=router,
        urls=urls,
        get_state=get_state,
        get_items=get_items,
        render_card=render_card,
        container_id="basic-demo-container",
        title="Basic Card Stack",
        description="Centered focus. Navigate with arrow keys, scroll wheel, or click any card.",
        progress_label="Item",
    )
