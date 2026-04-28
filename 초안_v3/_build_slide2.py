"""Build slide 2 — 문제 정의. Appends to existing 초안v3.pptx."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from _design import (
    SLIDE_W, SLIDE_H, MARGIN_L, CONTENT_W,
    HEADLINE_Y, HEADLINE_H, DIVIDER_Y, CONTENT_Y,
    COL_HEAD, COL_SUB, COL_LABEL,
    SZ_HEADLINE, SZ_SCENARIO, SZ_BODY, SZ_QUOTE,
    new_slide, add_text, add_lines, add_divider, add_headline, add_footer,
)

OUT_PPTX = r"C:\home\labs\llm-wiki\초안_v3\초안v3.pptx"

prs = Presentation(OUT_PPTX)
slide = new_slide(prs)

# ── Headline ─────────────────────────────────────────────────────
add_headline(slide, "자료는 쌓이고 있다.  이해는 쌓이고 있는가?")
add_divider(slide)

# ── Scenario blocks ──────────────────────────────────────────────
BLOCKS = [
    {
        "label": "① 반복",
        "lines": [
            "오늘      →  ChatGPT에 배경부터 다시 설명  →  정리  →  ⨯ 휘발",
            "다음 달  →  또 처음부터                    →  정리  →  ⨯ 또 휘발",
            "                                     ← 지난달에 정리한 게 어딘가 있는데",
        ],
    },
    {
        "label": "② 진화 없음",
        "lines": [
            "1월  A라고 생각  →  메모 저장        4월  B로 바뀜  →  다른 메모에 저장",
            "7월  다시 꺼내보면  →  ⨯  A인지 B인지, 왜 바뀌었는지 모름",
            "                          생각의 흐름이 어디에도 없음",
        ],
    },
    {
        "label": "③ 관계 무지",
        "lines": [
            "책에서 읽은 아이디어  +  지난주 미팅에서 나온 얘기  +  어제 읽은 기사",
            "  →  ⨯  연결되는 줄 모름",
            '         나중에 "아, 그게 그거였네" 하고 지나침',
        ],
    },
]

LABEL_H   = Inches(0.4)
CONTENT_H = Inches(1.15)
BLOCK_H   = LABEL_H + CONTENT_H
GAP       = Inches(0.14)

for i, block in enumerate(BLOCKS):
    y = CONTENT_Y + i * (BLOCK_H + GAP)

    add_text(slide, MARGIN_L, y, CONTENT_W, LABEL_H,
             block["label"],
             size=SZ_SCENARIO, bold=True, color=COL_HEAD)

    add_lines(slide, MARGIN_L + Inches(0.4), y + LABEL_H,
              CONTENT_W - Inches(0.4), CONTENT_H,
              block["lines"],
              size=SZ_BODY, color=COL_SUB)

    if i < 2:
        add_divider(slide, y + BLOCK_H + GAP * 0.5)

# ── Footer ───────────────────────────────────────────────────────
add_footer(
    slide,
    pagenum=2,
    left_text="→ 단순 요약에서 멈춘다.",
    right_text='"이전에 했던 작업이 남지 않기 때문에, 매번 동일한 과정을 반복하게 된다." — Karpathy',
)

prs.save(OUT_PPTX)
print("saved:", OUT_PPTX)
print(f"total slides: {len(prs.slides)}")
