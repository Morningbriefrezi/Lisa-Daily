#!/usr/bin/env python3
"""
ASTROMAN Proactive Scheduler Bot (7 pushes/day) — Claude/OpenAI -> Telegram

Times (Tbilisi):
- 09:00 Tasks (5 daily tasks)
- 12:00 3 ready-to-paste FB posts (Georgian)
- 13:00 Business tricks (from economics / business books)
- 15:00 2 totally new ideas for ASTROMAN
- 17:00 5 new product ideas + Alibaba *search* links
- 19:00 3 motivational quotes
- 21:00 Good night + day recap + sleep & lucid dreaming tips (safe)

GitHub Secrets (required):
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Choose ONE AI provider (Secrets):
- ANTHROPIC_API_KEY   (Claude)
or
- OPENAI_API_KEY

Optional GitHub Variables:
- ASTROMAN_ADDRESS
- ASTROMAN_PHONE
- ASTROMAN_CITY (default: Tbilisi)
"""

from __future__ import annotations

import os
import requests
from datetime import datetime, timezone

MODE = os.getenv("MODE", "tasks").strip().lower()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

ASTROMAN_ADDRESS = os.getenv("ASTROMAN_ADDRESS", "[ADDRESS]")
ASTROMAN_PHONE = os.getenv("ASTROMAN_PHONE", "[PHONE]")
ASTROMAN_CITY = os.getenv("ASTROMAN_CITY", "Tbilisi")

PROFILE = f"""User: Rezi. Business: ASTROMAN (cosmic-themed shop) in {ASTROMAN_CITY}.
Core products: telescopes, binoculars, star projectors, moon lamps, educational optics, cosmic gifts.
Priorities: increase daily sales (especially low season); boost conversions via fast replies, bundles, demos, B2B (schools/hotels/tour companies).
Style: practical, high-ROI, specific steps; Georgian preferred for customer-facing content.
Contacts: address={ASTROMAN_ADDRESS}, phone={ASTROMAN_PHONE}, website=astroman.ge.
""".strip()


def alibaba_search_link(query: str) -> str:
    from urllib.parse import quote_plus
    return f"https://www.alibaba.com/trade/search?SearchText={quote_plus(query)}"


def build_prompt(mode: str) -> str:
    base_rules = """Rules:
- Prefer Georgian for customer-facing content.
- Be specific and actionable.
- Avoid made-up facts (prices/discounts) unless clearly marked as 'optional'.
- Keep output compact (Telegram-friendly).
""".strip()

    if mode == "tasks":
        return f"""{PROFILE}

Task (09:00):
Create 5 daily tasks for Rezi TODAY that match ASTROMAN reality.
- Each task must be 10–30 minutes
- Include 1 sales task, 1 content task, 1 ops task, 1 B2B task, 1 learning task
Return:
✅ 5 Tasks (checkbox style)
\n\n{base_rules}"""

    if mode == "fb_posts":
        return f"""{PROFILE}

Task (12:00):
Write 3 totally different, ready-to-paste Facebook posts for ASTROMAN in Georgian.
Each post:
- strong hook line
- 3–5 short lines (benefits)
- CTA (DM / visit / website)
- include contacts:
  📍 {ASTROMAN_ADDRESS}
  📞 {ASTROMAN_PHONE}
  🌐 astroman.ge
- Keep emojis minimal (max 5 per post)

Topics must be different:
1) Telescopes / stargazing experience
2) Star projector / cozy home vibe
3) Gift idea (kids/couples)

Return exactly:
📌 Post 1
(text)
📌 Post 2
(text)
📌 Post 3
(text)
\n\n{base_rules}"""

    if mode == "biz_tricks":
        return f"""{PROFILE}

Task (13:00):
Teach 3 useful business/economics tricks inspired by classic business/econ books.
Make them practical for ASTROMAN today.
For each trick:
- 1-sentence idea
- 1 example for ASTROMAN
- 1 micro-action Rezi can do today

Return exactly:
🧠 Trick 1
🧠 Trick 2
🧠 Trick 3
\n\n{base_rules}"""

    if mode == "new_ideas":
        return f"""{PROFILE}

Task (15:00):
Generate 2 totally new growth ideas for ASTROMAN that are realistic in Tbilisi.
Each idea must include:
- What it is (1 sentence)
- Why it works (1 sentence)
- How to test in 48 hours (3 steps)

Return exactly:
💡 Idea 1
💡 Idea 2
\n\n{base_rules}"""

    if mode == "new_products":
        return f"""{PROFILE}

Task (17:00):
Propose 5 new product ideas to add for ASTROMAN (high demand, good margin, giftable).
For each product:
- Product name
- 1 key selling angle
- Target audience
- 3 search keywords (English) for Alibaba
Return exactly 5 items, numbered 1–5.
\n\n{base_rules}"""

    if mode == "motivation":
        return f"""{PROFILE}

Task (19:00):
Give 3 strong motivational quotes (English) + 1 Georgian line under each that feels personal for a business owner.
No clichés. Keep it punchy.

Return exactly:
🔥 Quote 1
🔥 Quote 2
🔥 Quote 3
\n\n{base_rules}"""

    if mode == "good_night":
        return f"""{PROFILE}

Task (21:00):
Write a warm good night message in Georgian.
Include:
- Quick checklist to review today's 5 tasks (ask Rezi to mark done/undone)
- 3 tips for better sleep tonight (safe, science-aligned)
- 3 lucid dreaming tactics (safe): dream journal, reality checks, MILD, etc.
Keep it calm, supportive, not too long.

Return exactly:
🌙 Good night
✅ Task check
😴 Sleep tips
🌌 Lucid dreaming
\n\n{base_rules}"""

    return f"""{PROFILE}

Write a short helpful message for Rezi about ASTROMAN.

{base_rules}"""


def call_claude(prompt: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 900,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": prompt}],
    }
    r = requests.post(url, headers=headers, json=payload, timeout=45)
    if r.status_code != 200:
        return f"❌ Claude API error: {r.status_code}\n{r.text}"
    data = r.json()
    text = ""
    for b in data.get("content", []):
        if b.get("type") == "text":
            text += b.get("text", "")
    return text.strip() or "❌ Empty response from Claude."


def call_openai(prompt: str) -> str:
    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4.1-mini",
        "input": prompt,
        "temperature": 0.7,
        "max_output_tokens": 700,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=45)
    if r.status_code != 200:
        return f"❌ OpenAI API error: {r.status_code}\n{r.text}"
    data = r.json()
    out = ""
    for item in data.get("output", []):
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                out += c.get("text", "")
    return out.strip() or "❌ Empty response from OpenAI."


def ai_generate(prompt: str) -> str:
    if ANTHROPIC_API_KEY:
        return call_claude(prompt)
    if OPENAI_API_KEY:
        return call_openai(prompt)
    return "❌ Set ANTHROPIC_API_KEY (Claude) or OPENAI_API_KEY in GitHub Secrets."


def send_telegram(message: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        print(message)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "disable_web_page_preview": True}
    r = requests.post(url, json=payload, timeout=25)
    if r.status_code != 200:
        print("❌ Telegram error:", r.status_code, r.text)
    else:
        print("✅ Sent.")


def postprocess(mode: str, text: str) -> str:
    if mode != "new_products":
        return text

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out_lines = []
    current_item = None
    keywords = []

    def flush():
        nonlocal current_item, keywords
        if current_item is None:
            return
        if keywords:
            out_lines.append("🔎 Alibaba links:")
            for kw in keywords[:3]:
                out_lines.append(f"- {alibaba_search_link(kw)}")
        out_lines.append("")
        current_item = None
        keywords = []

    for ln in lines:
        if ln[0].isdigit() and (ln[1:2] in [")", "."]):
            flush()
            current_item = ln
            out_lines.append(ln)
            continue

        if "keyword" in ln.lower():
            part = ln.split(":", 1)[-1].strip() if ":" in ln else ln
            kws = [k.strip() for k in part.replace(";", ",").split(",") if k.strip()]
            keywords.extend(kws)
            out_lines.append(ln)
            continue

        # Add line, and also treat short lowercase lines as keyword candidates
        if current_item and len(keywords) < 3 and len(ln) <= 60 and any(ch.isalpha() for ch in ln):
            if "," in ln:
                kws = [k.strip() for k in ln.replace(";", ",").split(",") if k.strip()]
                keywords.extend(kws)

        out_lines.append(ln)

    flush()
    final = "\n".join(out_lines).strip()
    if "Alibaba links:" not in final:
        final += "\n\n🔎 Alibaba search:\n- " + alibaba_search_link("astronomy telescope accessories")
    return final


def mode_title(mode: str) -> str:
    titles = {
        "tasks": "09:00 — Daily Tasks",
        "fb_posts": "12:00 — Facebook Posts",
        "biz_tricks": "13:00 — Business Tricks",
        "new_ideas": "15:00 — New Ideas",
        "new_products": "17:00 — Product Ideas",
        "motivation": "19:00 — Motivation",
        "good_night": "21:00 — Good Night",
    }
    return titles.get(mode, mode)


def main():
    prompt = build_prompt(MODE)
    text = ai_generate(prompt)
    text = postprocess(MODE, text)

    stamp = datetime.now().strftime("%Y-%m-%d")
    header = f"📩 ASTROMAN — {mode_title(MODE)} — {stamp}\n\n"
    send_telegram(header + text)


if __name__ == "__main__":
    main()
