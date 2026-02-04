"""Custom focus position demo (focus at slot 1)."""

from fasthtml.common import Div, P, Span

from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors, badge_styles
from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import w
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_card_stack.core.config import CardStackConfig
from cjm_fasthtml_card_stack.core.models import CardStackState, CardRenderContext
from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
from cjm_fasthtml_card_stack.core.button_ids import CardStackButtonIds
from cjm_fasthtml_card_stack.routes.router import init_card_stack_router

from demos.data import SAMPLE_ITEMS


def render_card(item, context: CardRenderContext):
    """Render a card with position info for the custom focus demo."""
    is_focused = context.card_role == "focused"

    index_badge = Span(
        f"#{context.index + 1}",
        cls=combine_classes(
            badge,
            badge_colors.accent if is_focused else badge_colors.neutral,
        )
    )

    distance_label = Span(
        f"slot offset: {context.distance_from_focus:+d}",
        cls=combine_classes(
            badge, badge_styles.ghost,
        )
    ) if not is_focused else Span(
        "focused",
        cls=combine_classes(badge, badge_colors.accent),
    )

    return Div(
        Div(
            Div(index_badge, distance_label, cls=combine_classes(m.b(1))),
            P(
                item,
                cls=combine_classes(text_dui.base_content),
                style="font-size: calc(0.875rem * var(--card-stack-scale, 100) / 100)",
            ),
            cls=combine_classes(card_body, p(3)),
        ),
        cls=combine_classes(
            card,
            bg_dui.base_100,
            w.full,
        ),
    )


def setup(route_prefix="/custom"):
    """Set up the custom focus position demo.

    Returns dict with config, ids, btn_ids, router, urls, state management,
    and page rendering dependencies.
    """
    config = CardStackConfig(prefix="custom", click_to_focus=True)
    ids = CardStackHtmlIds(prefix=config.prefix)
    btn_ids = CardStackButtonIds(prefix=config.prefix)

    state = CardStackState(
        visible_count=5,
        card_width=60,
        focus_position=1,  # Second slot from top
    )

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
        container_id="custom-demo-container",
        title="Custom Focus Position",
        description="Focus at slot 1 (second from top). One context card above, rest below.",
        progress_label="Item",
    )
