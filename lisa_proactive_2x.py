#!/usr/bin/env python3
"""
LISA Strategic 2x Daily Bot — Georgian — Telegram

10:00 — დღის ფოკუსი (Action Mode)
21:00 — ანალიზი + გონებრივი ზრდა (Strategic Mode)

Required GitHub Secrets:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- ANTHROPIC_API_KEY or OPENAI_API_KEY
"""

from __future__ import annotations
import os
import requests
from datetime import datetime, timezone

MODE = os.getenv("MODE", "morning").strip().lower()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

PROFILE = """
User: Rezi
Businesses:
- ASTROMAN (astro shop, high margin telescopes)
- NERO Burger Bar
Goal: increase daily revenue, build systems, improve financial intelligence.
Style: direct, high ROI, no fluff, fully Georgian.
""".strip()


def build_prompt(mode: str) -> str:

    if mode == "morning":
        return f"""{PROFILE}

დრო: 10:00 — დღის ფოკუსი

შექმენი ერთი ძლიერი დილის მესიჯი ქართულად:

სტრუქტურა:

🚀 დღევანდელი 3 მთავარი ამოცანა (15–30 წუთიანი, მაღალი ROI)
💰 1 გაყიდვების შეტევა დღესვე
📢 1 კონტენტის იდეა რეალური კონვერტაციით
📊 1 ფინანსური მინი-კონტროლი
🧠 მოკლე ფოკუსის მესიჯი (არაბანალური)

კონკრეტული და მოქმედებაზე ორიენტირებული.
არა ზოგადი რჩევები.
"""

    if mode == "night":
        return f"""{PROFILE}

დრო: 21:00 — ანალიზი + ზრდა

შექმენი საღამოს სტრატეგიული მესიჯი ქართულად:

📊 სწრაფი დღიური შეფასება (3 კითხვა)
📚 ერთი ძლიერი ბიზნეს/ეკონომიკური კონცეფცია მარტივად
🎯 3 სტრატეგიული კითხვა რეზისთვის
🔥 ხვალის 1 მთავარი ფოკუსი

არა მოტივაციური ციტატები.
რეალური აზროვნება.
"""

    return "Write a short useful message."


def call_openai(prompt: str) -> str:
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4.1-mini",
        "input": prompt,
        "temperature": 0.7,
        "max_output_tokens": 800,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=45)
    data = r.json()

    out = ""
    for item in data.get("output", []):
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                out += c.get("text", "")

    return out.strip()


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
    data = r.json()

    text = ""
    for b in data.get("content", []):
        if b.get("type") == "text":
            text += b.get("text", "")

    return text.strip()


def ai_generate(prompt: str) -> str:
    if ANTHROPIC_API_KEY:
        return call_claude(prompt)
    if OPENAI_API_KEY:
        return call_openai(prompt)
    return "❌ API key missing."


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": True,
    }
    requests.post(url, json=payload, timeout=30)


def main():
    prompt = build_prompt(MODE)
    text = ai_generate(prompt)

    stamp = datetime.now().strftime("%Y-%m-%d")
    title = "🚀 დღის ფოკუსი" if MODE == "morning" else "🌙 ანალიზი + ზრდა"

    send_telegram(f"{title} — {stamp}\n\n{text}")


if __name__ == "__main__":
    main()
