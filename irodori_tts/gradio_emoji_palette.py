from __future__ import annotations

from html import escape

import gradio as gr

from .emoji_palette import EMOJI_PALETTE_ITEMS

EMOJI_PALETTE_CSS = """
.emoji-palette {
    max-width: 100%;
}

.emoji-palette-grid {
    display: flex;
    gap: 3px;
    flex-wrap: wrap;
    align-items: flex-start;
    max-height: 124px;
    overflow-y: auto;
}

.emoji-palette-button {
    flex: 0 0 28px !important;
    min-width: 28px !important;
    max-width: 28px !important;
}

.emoji-palette-button button {
    width: 28px !important;
    min-width: 28px !important;
    height: 28px !important;
    min-height: 28px !important;
    border-radius: 4px;
    font-size: 17px;
    line-height: 1;
    padding: 0 !important;
}

button.emoji-palette-button {
    width: 28px;
    min-width: 28px;
    height: 28px;
    min-height: 28px;
    border-radius: 4px;
    font-size: 17px;
    line-height: 1;
    padding: 0;
    cursor: pointer;
}
"""


_INSERT_EMOJI_ON_POINTER_DOWN = (
    "event.preventDefault();"
    "const root=this.closest('[data-irodori-emoji-palette]');"
    "const input=root?document.querySelector(root.dataset.target):null;"
    "if(!input)return;"
    "const emoji=this.dataset.emoji;"
    "const text=input.value||'';"
    "const focused=document.activeElement===input;"
    "const start=focused&&typeof input.selectionStart==='number'?input.selectionStart:text.length;"
    "const end=focused&&typeof input.selectionEnd==='number'?input.selectionEnd:text.length;"
    "const next=text.slice(0,start)+emoji+text.slice(end);"
    "const caret=start+emoji.length;"
    "input.value=next;"
    "input.focus({preventScroll:true});"
    "input.setSelectionRange(caret,caret);"
    "input.dispatchEvent(new Event('input',{bubbles:true}));"
    "input.dispatchEvent(new Event('change',{bubbles:true}));"
)


def _textbox_selector(textbox: gr.Textbox) -> str:
    elem_id = getattr(textbox, "elem_id", None)
    root_selector = f"#{elem_id}" if elem_id else f"#component-{textbox._id}"
    return f"{root_selector} textarea, {root_selector} input:not([type='hidden'])"


def _emoji_palette_html(textbox: gr.Textbox) -> str:
    target = escape(_textbox_selector(textbox), quote=True)
    handler = escape(_INSERT_EMOJI_ON_POINTER_DOWN, quote=True)
    buttons = []
    for item in EMOJI_PALETTE_ITEMS:
        emoji = escape(item.emoji, quote=True)
        title = escape(f"{item.label}: {item.description}", quote=True)
        buttons.append(
            '<button type="button" '
            'class="emoji-palette-button" '
            f'data-emoji="{emoji}" '
            f'title="{title}" '
            f'aria-label="{title}" '
            f'onpointerdown="{handler}">'
            f"{emoji}</button>"
        )
    return (
        '<div class="emoji-palette-grid" '
        'data-irodori-emoji-palette="true" '
        f'data-target="{target}">'
        f"{''.join(buttons)}</div>"
    )


def build_emoji_palette(textbox: gr.Textbox, *, open: bool = True) -> None:
    with gr.Accordion("Emoji Palette", open=open, elem_classes=["emoji-palette"]):
        gr.HTML(_emoji_palette_html(textbox))
