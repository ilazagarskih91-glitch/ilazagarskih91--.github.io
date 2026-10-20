#!/usr/bin/env python3
"""Создаёт QR-код на опубликованный сайт и обновляет HTML-макеты.

Использование из папки сайта:
  python generate_qr.py https://ваш-адрес-сайта.example
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

try:
    import qrcode
except ImportError:
    print("Не установлен модуль qrcode. Установи его командой: python -m pip install qrcode[pil]")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
PLACEHOLDER = "qr-placeholder.svg"
QR_FILE = "qr.png"


def main() -> None:
    parser = argparse.ArgumentParser(description="Создать QR-код для публичного адреса сайта.")
    parser.add_argument("url", help="Публичный URL сайта, например https://example.github.io/ai-search-memo/")
    args = parser.parse_args()
    url = args.url.strip()
    if not url.startswith(("https://", "http://")):
        parser.error("Адрес должен начинаться с https:// или http://")

    image = qrcode.make(url, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    image.save(ROOT / QR_FILE)

    for filename in ("index.html", "pamyatka.html"):
        path = ROOT / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        content = content.replace(PLACEHOLDER, QR_FILE)
        content = content.replace(
            "QR на макете пока не сканируется. Инструкция по созданию рабочего кода находится в README.txt.",
            "QR-код ведёт на опубликованную версию сайта."
        )
        content = content.replace(
            "QR-код станет рабочим после публикации сайта в интернете.",
            "QR-код ведёт на опубликованную версию сайта."
        )
        path.write_text(content, encoding="utf-8")

    (ROOT / "SITE_URL.txt").write_text(url + "\n", encoding="utf-8")
    print(f"QR-код сохранён: {ROOT / QR_FILE}")
    print(f"HTML обновлены. Адрес: {url}")
    print("Загрузи обновлённые index.html, pamyatka.html, qr.png и SITE_URL.txt на тот же хостинг.")


if __name__ == "__main__":
    main()
