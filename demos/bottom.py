"""Bottom-anchored card stack demo (chat-style)."""

from fasthtml.common import Div, P, Span

from cjm_fasthtml_daisyui.components.data_display.card import card, card_body
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui, text_dui
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import w
from cjm_fasthtml_tailwind.utilities.typography import font_size
from cjm_fasthtml_tailwind.core.base import combine_classes

from cjm_fasthtml_card_stack.core.config import CardStackConfig
from cjm_fasthtml_card_stack.core.models import CardStackState, CardRenderContext
from cjm_fasthtml_card_stack.core.html_ids import CardStackHtmlIds
from cjm_fasthtml_card_stack.core.button_ids import CardStackButtonIds
from cjm_fasthtml_card_stack.routes.router import init_card_stack_router

from demos.data import SAMPLE_ITEMS
from demos.shared import generate_scale_spacing_js


def render_card(item, context: CardRenderContext):
    """Render a compact chat-style message card."""
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
            Div(index_badge, cls=combine_classes(m.b(1))),
            P(
                item,
                cls=combine_classes(
                    text_dui.base_content,
                    font_size('[calc(0.875rem*var(--card-stack-scale,100)/100)]'),
                ),
            ),
            cls=combine_classes(card_body, p(3)),
        ),
        cls=combine_classes(
            card,
            bg_dui.base_100,
            w.full,
        ),
    )


def setup(route_prefix="/bottom"):
    """Set up the bottom-anchored card stack demo.

    Returns dict with config, ids, btn_ids, router, urls, state management,
    and page rendering dependencies.
    """
    config = CardStackConfig(prefix="bottom", click_to_focus=True)
    ids = CardStackHtmlIds(prefix=config.prefix)
    btn_ids = CardStackButtonIds(prefix=config.prefix)

    state = CardStackState(
        visible_count=5,
        card_width=60,
        focus_position=-1,  # Bottom-anchored
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
        container_id="bottom-demo-container",
        title="Bottom-Anchored Card Stack",
        description="Chat-style layout with focused card at the bottom. Context cards appear above.",
        progress_label="Message",
        extra_scripts=(generate_scale_spacing_js(config, ids),),
    )
