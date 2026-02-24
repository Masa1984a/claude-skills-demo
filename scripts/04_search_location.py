"""
ロケーション Wikipedia検索
使い方: python scripts/04_searchLocation.py --location 東京都
"""

import json
import argparse
import sys
from playwright.sync_api import sync_playwright

# Claude Code（WSL環境）での文字化け防止
sys.stdout.reconfigure(encoding="utf-8")


def search_wikipedia(location: str) -> dict:
    url = f"https://ja.wikipedia.org/wiki/{location}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)  # slow_mo: 操作を500ms遅延して見やすくする
        page = browser.new_page()

        # Wikipediaのメインページを表示
        page.goto("https://ja.wikipedia.org/wiki/メインページ")
        page.wait_for_load_state("domcontentloaded")

        # 検索ボックスのセレクタ（新旧UI両対応）
        search_selectors = [
            "input[name='search']",
            "input#searchInput",
            "input.cdx-text-input__input",
            "[placeholder*='検索']",
        ]
        search_box = None
        for selector in search_selectors:
            el = page.query_selector(selector)
            if el:
                search_box = selector
                break

        if not search_box:
            raise Exception("検索ボックスが見つかりませんでした")

        # 検索ボックスをクリックして入力
        page.click(search_box)
        page.wait_for_timeout(500)
        page.fill(search_box, location)
        page.wait_for_timeout(500)

        # 検索を実行（Enterキー）— ナビゲーション完了を待機
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.keyboard.press("Enter")
        page.wait_for_load_state("load")

        # ページタイトル
        title = page.title()

        # 概要文（最初の段落）を取得
        paragraphs = page.query_selector_all("#mw-content-text .mw-parser-output > p")
        summary = ""
        for p in paragraphs:
            text = p.inner_text().strip()
            if len(text) > 50:  # 短すぎる段落はスキップ
                summary = text
                break

        # 目次（セクション一覧）を取得（新旧UI両対応）
        sections = []
        toc_selectors = [
            ".vector-toc-text",         # 新UI
            "#toc .toctext",            # 旧UI
            ".mw-parser-output h2 .mw-headline",  # フォールバック
        ]
        for selector in toc_selectors:
            items = page.query_selector_all(selector)
            if items:
                for item in items[:8]:
                    text = item.inner_text().strip()
                    # 番号・タブ・改行を除去してセクション名だけ残す
                    import re
                    text = re.sub(r"^\d+(\.\d+)*\s*", "", text)  # 先頭の番号を除去
                    text = re.sub(r"\s+", " ", text).strip()      # 空白を正規化
                    if text and text != "ページ先頭":
                        sections.append(text)
                break

        browser.close()

    return {
        "title":    title,
        "url":      url,
        "summary":  summary,
        "sections": sections
    }


def main():
    parser = argparse.ArgumentParser(description="都道府県のWikipedia検索")
    parser.add_argument("--location", required=True, help="検索する都道府県（例: 東京都）")
    args = parser.parse_args()

    try:
        result = search_wikipedia(args.location)
        output = {
            "status":   "ok",
            "location": args.location,
            **result
        }

    except Exception as e:
        output = {
            "status":  "error",
            "message": str(e),
            "hint":    "pip install playwright && python -m playwright install chromium"
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()