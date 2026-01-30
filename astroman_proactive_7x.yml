name: ASTROMAN Proactive Messages (7/day)

on:
  schedule:
    # Tbilisi is UTC+4
    - cron: "0 5 * * *"   # 09:00
    - cron: "0 8 * * *"   # 12:00
    - cron: "0 9 * * *"   # 13:00
    - cron: "0 11 * * *"  # 15:00
    - cron: "0 13 * * *"  # 17:00
    - cron: "0 15 * * *"  # 19:00
    - cron: "0 17 * * *"  # 21:00
  workflow_dispatch:

jobs:
  proactive:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Set MODE based on UTC hour
        run: |
          python3 - << 'PY'
          import os
          from datetime import datetime, timezone
          hour = datetime.now(timezone.utc).hour
          mapping = {
            5:  "tasks",
            8:  "fb_posts",
            9:  "biz_tricks",
            11: "new_ideas",
            13: "new_products",
            15: "motivation",
            17: "good_night",
          }
          mode = mapping.get(hour, "tasks")
          with open(os.environ["GITHUB_ENV"], "a") as f:
            f.write(f"MODE={mode}\n")
          print("MODE =", mode)
          PY

      - name: Run proactive bot
        run: python3 proactive_bot_7x.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          # Choose ONE AI provider:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          # Optional variables:
          ASTROMAN_ADDRESS: ${{ vars.ASTROMAN_ADDRESS }}
          ASTROMAN_PHONE: ${{ vars.ASTROMAN_PHONE }}
          ASTROMAN_CITY: ${{ vars.ASTROMAN_CITY }}
