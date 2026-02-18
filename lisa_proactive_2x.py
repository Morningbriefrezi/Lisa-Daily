#!/usr/bin/env python3
"""
ASTROMAN — DATA DRIVEN CEO MODE

Uses real 2025 performance:
Revenue: 184,023 GEL
Gross Margin: 59.4%
Core Driver: Telescopes

2x Daily:
10:00 Strategic Allocation
21:00 Structural Audit
"""

from __future__ import annotations
import os
import requests
from datetime import datetime

MODE = os.getenv("MODE", "morning").strip().lower()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

PROFILE = """
ბიზნესი: ASTROMAN

რეალური 2025 შედეგები:
- წლიური შემოსავალი: 184,023 GEL
- საშუალო თვიური: ~15,300 GEL
- მთლიანი მარჟა: 59.4%
- მთავარი შემოსავალი: ტელესკოპები
- დაბალი მარჟის შეცდომა: ზოგი პრემიუმ ტელესკოპი 2%-იანი მარჟით
- ბევრი ნელი მარაგი

სტრატეგიული მიზანი:
- ტელესკოპების გარშემო ბრენდის გამაგრება
- საშუალო ჩეკის ზრდა
- მაღალი მარჟის ფოკუსი
- ნელი მარაგის ლიკვიდაცია
- ონლაინ გაყიდვების წილის ზრდა

იმსჯელე როგორც კაპიტალის ალოკატორი CEO.
არ იყოს ზოგადი რჩევები.
"""


def build_prompt(mode: str):

    if mode == "morning":
        return f"""{PROFILE}

დრო: 10:00 — კაპიტალის განაწილების ბრიფინგი

I. სად არის ფული ჩაკეტილი მარაგში?
II. რომელი კატეგორია უნდა დავაწვეთ დღეს?
III. როგორ გავზარდოთ დღიური 15,300 → 20,000 თვიური საშუალო?
IV. რა ნაბიჯი გაზრდის საშუალო ჩეკს 20%-ით?
V. რომელი დაბალი მარჟის პროდუქტი უნდა გადაიხედოს?

მოიფიქრე კონკრეტული ქმედებები.
არ იყოს ზოგადი ტექსტი.
"""

    if mode == "night":
        return f"""{PROFILE}

დრო: 21:00 — სტრუქტურული აუდიტი

I. ტელესკოპებზე დამოკიდებულება — რისკია თუ ძალა?
II. მარაგის ბრუნვადობის პრობლემა სად არის?
III. რომელი პროდუქტი უნდა ამოვიღოთ?
IV. ერთი ღრმა კონცეფცია:
Inventory Turnover / Pricing Power / Unit Economics

აუხსენი ASTROMAN კონტექსტში.
ხვალ რა უნდა გაკეთდეს კონკრეტულად?

იმსჯელე როგორც გრძელვადიანი ბრენდის მშენებელი.
"""

    return "CEO MODE"


def call_openai(prompt: str):
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "input": prompt,
        "temperature": 0.6,
        "max_output_tokens": 1400
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    data = r.json()

    output = ""
    for item in data.get("output", []):
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                output += c.get("text", "")

    return output.strip()


def generate(prompt: str):
    return call_openai(prompt)


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }

    requests.post(url, json=payload, timeout=40)


def main():
    prompt = build_prompt(MODE)
    text = generate(prompt)

    today = datetime.now().strftime("%Y-%m-%d")
    title = "🚀 ASTROMAN CEO დილის ბრიფინგი" if MODE == "morning" else "🌙 ASTROMAN CEO ღამის აუდიტი"

    send_telegram(f"{title} — {today}\n\n{text}")


if __name__ == "__main__":
    main()
