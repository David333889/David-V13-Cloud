# -*- coding: utf-8 -*-
"""David V13.100 - 100檔最近20交易日歷史回補

用法（在 C:\\David戰情室\\V13_Cloud）：
    python backfill_20days_v13.py

安全：優先讀環境變數 SUPABASE_URL / SUPABASE_KEY；若沒有，讀 .streamlit/secrets.toml。
不會列印 Secret Key。
"""
from __future__ import annotations

import os
import time
import tomllib
from pathlib import Path
import pandas as pd
from supabase import create_client

from daily_snapshot_v13 import (
    DEFAULT_STOCKS,
    fetch_page,
    analyze_stock,
    make_payload,
)

ROOT = Path(__file__).resolve().parent
MAX_STOCKS = 100
BACKFILL_DAYS = 20
MIN_ROWS_FOR_ANALYSIS = 60


def load_credentials():
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if url and key:
        return url, key

    p = ROOT / ".streamlit" / "secrets.toml"
    if not p.exists():
        raise SystemExit("找不到 Supabase 設定：請確認 .streamlit\\secrets.toml 存在。")
    with p.open("rb") as f:
        cfg = tomllib.load(f)
    supa = cfg.get("supabase", {})
    url = str(supa.get("url", "")).strip()
    key = str(supa.get("key", "")).strip()
    if not url or not key:
        raise SystemExit("secrets.toml 內缺少 [supabase] url/key。")
    return url, key


def load_stock_config(client):
    rows = []
    try:
        resp = client.table("stock_config").select("position,code,name,market").order("position").execute()
        for x in (resp.data or []):
            rows.append({
                "code": str(x["code"]),
                "name": str(x["name"]),
                "market": str(x["market"]).upper(),
            })
    except Exception as e:
        print("雲端 stock_config 讀取失敗，改用本機預設：", e)

    seen = {x["code"] for x in rows}
    for item in DEFAULT_STOCKS:
        if len(rows) >= MAX_STOCKS:
            break
        if item["code"] not in seen:
            rows.append(item.copy())
            seen.add(item["code"])

    # 8271 防呆：宇瞻為上市，固定 TW
    for x in rows:
        if x["code"] == "8271":
            x["market"] = "TW"
    return rows[:MAX_STOCKS]


def payload_for_date(item, sliced):
    if sliced is None or sliced.empty or len(sliced) < MIN_ROWS_FOR_ANALYSIS:
        return None
    symbol = f"{item['code']}.{item['market']}"
    result = analyze_stock(item["code"], item["name"], sliced, symbol)
    payload = make_payload(item, result, sliced)
    return payload


def upsert_chunks(client, payloads, chunk_size=200):
    total = 0
    for i in range(0, len(payloads), chunk_size):
        chunk = payloads[i:i+chunk_size]
        client.table("stock_history").upsert(
            chunk, on_conflict="trade_date,code"
        ).execute()
        total += len(chunk)
        print(f"  Supabase 已寫入 {total}/{len(payloads)} 筆")
    return total


def main():
    started = time.perf_counter()
    url, key = load_credentials()
    client = create_client(url, key)
    stocks = load_stock_config(client)
    print(f"開始回補：{len(stocks)} 檔 × 最近 {BACKFILL_DAYS} 交易日")

    all_payloads = []
    failed = []
    insufficient = []

    for page in range(10):
        rows = stocks[page*10:(page+1)*10]
        print(f"\nPage {page+1}：抓取 {len(rows)} 檔歷史行情...")
        data_map = fetch_page(rows)

        for item in rows:
            symbol = f"{item['code']}.{item['market']}"
            data = data_map.get(symbol, pd.DataFrame())
            if data is None or data.empty:
                failed.append(symbol)
                print(f"  [失敗] {symbol} 無行情")
                continue
            data = data.sort_index()
            if len(data) < MIN_ROWS_FOR_ANALYSIS + BACKFILL_DAYS - 1:
                insufficient.append((symbol, len(data)))
                # 仍盡可能回補可分析日期
            target_positions = list(range(max(MIN_ROWS_FOR_ANALYSIS-1, len(data)-BACKFILL_DAYS), len(data)))
            stock_count = 0
            for pos in target_positions:
                sliced = data.iloc[:pos+1].copy()
                try:
                    payload = payload_for_date(item, sliced)
                    if payload:
                        all_payloads.append(payload)
                        stock_count += 1
                except Exception as e:
                    print(f"  [分析錯誤] {symbol} {data.index[pos]}: {e}")
            print(f"  {symbol}：準備 {stock_count} 個交易日")

    # 去除重複，以 (trade_date, code) 最後一筆為準
    dedup = {}
    for p in all_payloads:
        dedup[(p["trade_date"], p["code"])] = p
    payloads = list(dedup.values())
    payloads.sort(key=lambda x: (x["trade_date"], x["code"]))

    print(f"\n準備寫入 Supabase：{len(payloads)} 筆")
    written = upsert_chunks(client, payloads)

    elapsed = time.perf_counter() - started
    print("\n==============================")
    print(f"完成：寫入/更新 {written} 筆")
    print(f"行情完全失敗：{len(failed)} 檔 {failed}")
    if insufficient:
        print(f"歷史列數較少：{len(insufficient)} 檔 {insufficient}")
    print(f"耗時：{elapsed:.1f} 秒")
    print("請重新整理 Streamlit；20日歷史應接近 20/20。")


if __name__ == "__main__":
    main()
