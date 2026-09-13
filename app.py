import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import json
import time
import os
from datetime import date
from pathlib import Path


# ============================================================
# David 戰情室 V12 正式穩定版
# V10 六買六賣核心
# + 視覺強化
# + Pivot Swing Fibonacci
# + 禁止瀏覽器誤翻譯關鍵文字
# ============================================================

st.set_page_config(
    page_title="David 戰情室 V13 Cloud｜100檔智慧戰情版",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# 0. 全站設定 + 禁止翻譯提示
# ============================================================

st.markdown(
    """
    <meta name="google" content="notranslate">
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                180deg,
                #06101A 0%,
                #08131E 100%
            );
        color: #EAF2F8;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        max-width: 1900px;
    }

    h1, h2, h3 {
        color: #F7FBFF !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* =========================
       主標題
       ========================= */

    .main-title {
        font-size: 42px;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .sub-title {
        color: #9FB1C2;
        font-size: 14px;
        margin-bottom: 12px;
    }


    /* =========================
       戰情摘要
       ========================= */

    .summary-card {
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid;
        min-height: 120px;
        box-shadow:
            0 0 14px rgba(0,0,0,.28);
    }

    .summary-title {
        font-size: 17px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .summary-value {
        font-size: 34px;
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1.05;
    }

    .summary-pct {
        margin-top: 8px;
        color: #D3DEE8;
        font-size: 14px;
        font-weight: 700;
    }


    /* =========================
       股票名稱
       ========================= */

    .stock-title {
        font-size: 30px;
        font-weight: 900;
        color: #FFFFFF;
        margin-top: 8px;
        margin-bottom: 12px;
    }


    /* =========================
       Fib 卡片
       ========================= */

    .fib-card {
        background: #0D1822;
        border: 1px solid #31485A;
        border-radius: 12px;
        padding: 15px 17px;
        min-height: 105px;
        box-shadow:
            0 0 10px rgba(0,0,0,.22);
    }

    .fib-label {
        color: #AAB9C6;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .fib-value {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 900;
        line-height: 1.05;
    }


    /* =========================
       Selectbox
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #F4F6F8;
        color: #111111;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 1. 標題
# ============================================================

st.markdown(
    '<div class="main-title notranslate" translate="no">'
    '📊 David 戰情室｜V13 Cloud'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '100檔十頁｜首頁 TOP10｜本週熱門候補｜異常轉強｜20交易日歷史｜Supabase 雲端保存'
    '</div>',
    unsafe_allow_html=True
)

st.success(
    "系統狀態：正常"
)


# ============================================================
# 2. AI 精選族群 / 線上股票設定
# V12 測試版：主畫面維持原版，設定放在 Sidebar
# 每檔直接指定 TW / TWO，避免逐檔猜市場別
# ============================================================

APP_DIR = Path(__file__).resolve().parent
STOCK_CONFIG_PATH = APP_DIR / "stock_config_v13.json"
MAX_STOCKS = 100
STOCKS_PER_PAGE = 10
TOTAL_PAGES = 10

PAGE_NAMES = {1: 'AI伺服器／ASIC／核心運算', 2: 'PCB／CCL／ABF載板', 3: 'CPO／光通訊／高速網路', 4: '散熱／液冷／電源', 5: '記憶體／儲存', 6: '被動元件／矽晶圓／先進封測', 7: 'DAVID自選A／設備測試材料', 8: 'DAVID自選B／輪動與機器人', 9: '🔥 本週熱門候補', 10: '🚨 異常轉強股'}

DEFAULT_STOCKS = [{'code': '2330', 'name': '台積電', 'market': 'TW'},
    {'code': '2454', 'name': '聯發科', 'market': 'TW'},
    {'code': '2317', 'name': '鴻海', 'market': 'TW'},
    {'code': '2382', 'name': '廣達', 'market': 'TW'},
    {'code': '3231', 'name': '緯創', 'market': 'TW'},
    {'code': '6669', 'name': '緯穎', 'market': 'TW'},
    {'code': '3443', 'name': '創意', 'market': 'TW'},
    {'code': '3661', 'name': '世芯-KY', 'market': 'TW'},
    {'code': '2357', 'name': '華碩', 'market': 'TW'},
    {'code': '2376', 'name': '技嘉', 'market': 'TW'},
    {'code': '2383', 'name': '台光電', 'market': 'TW'},
    {'code': '2368', 'name': '金像電', 'market': 'TW'},
    {'code': '3037', 'name': '欣興', 'market': 'TW'},
    {'code': '8046', 'name': '南電', 'market': 'TW'},
    {'code': '3189', 'name': '景碩', 'market': 'TW'},
    {'code': '6274', 'name': '台燿', 'market': 'TWO'},
    {'code': '6213', 'name': '聯茂', 'market': 'TW'},
    {'code': '2313', 'name': '華通', 'market': 'TW'},
    {'code': '4958', 'name': '臻鼎-KY', 'market': 'TW'},
    {'code': '1815', 'name': '富喬', 'market': 'TWO'},
    {'code': '2345', 'name': '智邦', 'market': 'TW'},
    {'code': '6442', 'name': '光聖', 'market': 'TW'},
    {'code': '3081', 'name': '聯亞', 'market': 'TWO'},
    {'code': '4979', 'name': '華星光', 'market': 'TWO'},
    {'code': '3163', 'name': '波若威', 'market': 'TWO'},
    {'code': '3363', 'name': '上詮', 'market': 'TWO'},
    {'code': '3450', 'name': '聯鈞', 'market': 'TW'},
    {'code': '2455', 'name': '全新', 'market': 'TW'},
    {'code': '4971', 'name': 'IET-KY', 'market': 'TWO'},
    {'code': '4991', 'name': '環宇-KY', 'market': 'TWO'},
    {'code': '3017', 'name': '奇鋐', 'market': 'TW'},
    {'code': '3324', 'name': '雙鴻', 'market': 'TWO'},
    {'code': '3653', 'name': '健策', 'market': 'TW'},
    {'code': '2059', 'name': '川湖', 'market': 'TW'},
    {'code': '8996', 'name': '高力', 'market': 'TW'},
    {'code': '2308', 'name': '台達電', 'market': 'TW'},
    {'code': '2301', 'name': '光寶科', 'market': 'TW'},
    {'code': '2421', 'name': '建準', 'market': 'TW'},
    {'code': '6230', 'name': '尼得科超眾', 'market': 'TW'},
    {'code': '3483', 'name': '力致', 'market': 'TWO'},
    {'code': '2408', 'name': '南亞科', 'market': 'TW'},
    {'code': '2344', 'name': '華邦電', 'market': 'TW'},
    {'code': '2337', 'name': '旺宏', 'market': 'TW'},
    {'code': '8299', 'name': '群聯', 'market': 'TWO'},
    {'code': '5289', 'name': '宜鼎', 'market': 'TWO'},
    {'code': '3260', 'name': '威剛', 'market': 'TWO'},
    {'code': '2451', 'name': '創見', 'market': 'TW'},
    {'code': '3006', 'name': '晶豪科', 'market': 'TW'},
    {'code': '8271', 'name': '宇瞻', 'market': 'TW'},
    {'code': '6770', 'name': '力積電', 'market': 'TW'},
    {'code': '2327', 'name': '國巨', 'market': 'TW'},
    {'code': '2492', 'name': '華新科', 'market': 'TW'},
    {'code': '3026', 'name': '禾伸堂', 'market': 'TW'},
    {'code': '6173', 'name': '信昌電', 'market': 'TWO'},
    {'code': '5483', 'name': '中美晶', 'market': 'TWO'},
    {'code': '6488', 'name': '環球晶', 'market': 'TWO'},
    {'code': '2449', 'name': '京元電子', 'market': 'TW'},
    {'code': '3711', 'name': '日月光投控', 'market': 'TW'},
    {'code': '6223', 'name': '旺矽', 'market': 'TWO'},
    {'code': '6515', 'name': '穎崴', 'market': 'TW'},
    {'code': '7769', 'name': '鴻勁', 'market': 'TW'},
    {'code': '6640', 'name': '均華', 'market': 'TWO'},
    {'code': '2467', 'name': '志聖', 'market': 'TW'},
    {'code': '3131', 'name': '弘塑', 'market': 'TWO'},
    {'code': '6510', 'name': '精測', 'market': 'TWO'},
    {'code': '1560', 'name': '中砂', 'market': 'TW'},
    {'code': '5269', 'name': '祥碩', 'market': 'TW'},
    {'code': '6187', 'name': '萬潤', 'market': 'TWO'},
    {'code': '6271', 'name': '同欣電', 'market': 'TW'},
    {'code': '3034', 'name': '聯詠', 'market': 'TW'},
    {'code': '3008', 'name': '大立光', 'market': 'TW'},
    {'code': '3665', 'name': '貿聯-KY', 'market': 'TW'},
    {'code': '2303', 'name': '聯電', 'market': 'TW'},
    {'code': '5347', 'name': '世界', 'market': 'TWO'},
    {'code': '2207', 'name': '和泰車', 'market': 'TW'},
    {'code': '2049', 'name': '上銀', 'market': 'TW'},
    {'code': '1590', 'name': '亞德客-KY', 'market': 'TW'},
    {'code': '2359', 'name': '所羅門', 'market': 'TW'},
    {'code': '6215', 'name': '和椿', 'market': 'TW'},
    {'code': '4576', 'name': '大銀微系統', 'market': 'TW'},
    {'code': '2356', 'name': '英業達', 'market': 'TW'},
    {'code': '4938', 'name': '和碩', 'market': 'TW'},
    {'code': '2377', 'name': '微星', 'market': 'TW'},
    {'code': '3706', 'name': '神達', 'market': 'TW'},
    {'code': '8210', 'name': '勤誠', 'market': 'TW'},
    {'code': '3013', 'name': '晟銘電', 'market': 'TW'},
    {'code': '3533', 'name': '嘉澤', 'market': 'TW'},
    {'code': '2360', 'name': '致茂', 'market': 'TW'},
    {'code': '2395', 'name': '研華', 'market': 'TW'},
    {'code': '6414', 'name': '樺漢', 'market': 'TW'},
    {'code': '3583', 'name': '辛耘', 'market': 'TW'},
    {'code': '3413', 'name': '京鼎', 'market': 'TW'},
    {'code': '3680', 'name': '家登', 'market': 'TWO'},
    {'code': '6643', 'name': 'M31', 'market': 'TWO'},
    {'code': '6531', 'name': '愛普*', 'market': 'TW'},
    {'code': '6789', 'name': '采鈺', 'market': 'TW'},
    {'code': '6282', 'name': '康舒', 'market': 'TW'},
    {'code': '6781', 'name': 'AES-KY', 'market': 'TW'},
    {'code': '6805', 'name': '富世達', 'market': 'TW'},
    {'code': '3693', 'name': '營邦', 'market': 'TWO'}]


# ============================================================
# V13 Cloud：Supabase 雲端資料庫
# - 未設定 Secrets 時仍可在本機執行（歷史資料不會永久上雲）
# - Streamlit Community Cloud 請在 App Secrets 設定：
#   [supabase]
#   url = "https://xxxx.supabase.co"
#   key = "YOUR_SECRET_OR_SERVICE_ROLE_KEY"
# ============================================================

@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = ""
    key = ""

    try:
        if "supabase" in st.secrets:
            url = str(st.secrets["supabase"].get("url", "")).strip()
            key = str(st.secrets["supabase"].get("key", "")).strip()
    except Exception:
        pass

    url = url or os.getenv("SUPABASE_URL", "").strip()
    key = key or os.getenv("SUPABASE_KEY", "").strip()

    if not url or not key:
        return None

    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception as e:
        print(f"Supabase 初始化失敗：{e}")
        return None


def cloud_db_enabled():
    return get_supabase_client() is not None


def load_stock_config_from_cloud():
    client = get_supabase_client()
    if client is None:
        return []
    try:
        resp = (
            client.table("stock_config")
            .select("position,code,name,market")
            .order("position")
            .execute()
        )
        rows = resp.data or []
        if rows:
            return [
                {"code": str(x["code"]), "name": str(x["name"]), "market": str(x["market"]).upper()}
                for x in rows
            ]
    except Exception as e:
        print(f"雲端股票設定讀取失敗：{e}")
    return []


def save_stock_config_to_cloud(rows):
    client = get_supabase_client()
    if client is None:
        return False
    try:
        payload = [
            {
                "position": i + 1,
                "code": str(row["code"]),
                "name": str(row["name"]),
                "market": str(row["market"]).upper(),
            }
            for i, row in enumerate(rows)
        ]
        client.table("stock_config").upsert(payload, on_conflict="position").execute()
        return True
    except Exception as e:
        print(f"雲端股票設定儲存失敗：{e}")
        return False


def _to_number(value, suffix=""):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    try:
        text = str(value).strip()
        if suffix:
            text = text.replace(suffix, "")
        if text in ("", "--", "nan", "None"):
            return None
        return float(text)
    except Exception:
        return None


def history_payload_for_page(rows, results, batch_data):
    result_map = {
        str(r.get("AI 精選族群", "")).split(" ", 1)[0]: r
        for r in results
    }
    payload = []

    for item in rows:
        code = item["code"]
        symbol = f'{code}.{item["market"]}'
        r = result_map.get(code)
        data = batch_data.get(symbol, pd.DataFrame())
        if not r or data is None or data.empty or r.get("決策") in ("無資料", "資料錯誤"):
            continue

        idx = data.index[-1]
        try:
            trade_date = pd.Timestamp(idx).date().isoformat()
        except Exception:
            trade_date = date.today().isoformat()

        payload.append({
            "trade_date": trade_date,
            "code": code,
            "name": item["name"],
            "market": item["market"],
            "symbol": symbol,
            "prev_close": _to_number(r.get("昨收")),
            "open_price": _to_number(r.get("開盤")),
            "close_price": _to_number(r.get("現價")),
            "change_value": _to_number(r.get("漲跌")),
            "change_pct": _to_number(r.get("幅%"), "%"),
            "volume_ratio": _to_number(r.get("量比"), "x"),
            "bias_pct": _to_number(r.get("乖離"), "%"),
            "morning": str(r.get("早盤", "")),
            "momentum": str(r.get("動能", "")),
            "cost": str(r.get("成本", "")),
            "strength": str(r.get("力道", "")),
            "buy_score": int(r["六買"]) if str(r.get("六買", "")).isdigit() else None,
            "sell_score": int(r["六賣"]) if str(r.get("六賣", "")).isdigit() else None,
            "fib_position": str(r.get("Fib位置", "")),
            "decision": str(r.get("決策", "")),
        })

    return payload


def upsert_history(payload):
    client = get_supabase_client()
    if client is None or not payload:
        return False, 0, "尚未設定 Supabase"
    try:
        client.table("stock_history").upsert(
            payload,
            on_conflict="trade_date,code"
        ).execute()
        return True, len(payload), ""
    except Exception as e:
        return False, 0, str(e)


@st.cache_data(ttl=60, show_spinner=False)
def fetch_history_20(code):
    client = get_supabase_client()
    if client is None:
        return pd.DataFrame()
    try:
        resp = (
            client.table("stock_history")
            .select("trade_date,code,name,market,close_price,change_pct,volume_ratio,bias_pct,buy_score,sell_score,fib_position,decision")
            .eq("code", str(code))
            .order("trade_date", desc=True)
            .limit(20)
            .execute()
        )
        data = resp.data or []
        dfh = pd.DataFrame(data)
        if not dfh.empty:
            dfh["trade_date"] = pd.to_datetime(dfh["trade_date"])
            dfh = dfh.sort_values("trade_date")
        return dfh
    except Exception as e:
        print(f"20日歷史讀取失敗：{e}")
        return pd.DataFrame()


def normalize_stock_rows(rows):
    cleaned = []
    seen = set()

    for row in rows:
        code = str(row.get("code", "")).strip()
        if code.endswith(".0") and code[:-2].isdigit():
            code = code[:-2]

        name = str(row.get("name", "")).strip()
        market = str(row.get("market", "TW")).strip().upper()

        if not code or not name:
            continue

        if market not in ("TW", "TWO"):
            market = "TW"

        if code in seen:
            continue

        seen.add(code)
        cleaned.append({
            "code": code,
            "name": name,
            "market": market,
        })

    return cleaned


def load_stock_config():
    # 先讀雲端；若目前 Supabase 仍只有舊版60檔，會自動以新版預設補足到100檔。
    cloud_rows = normalize_stock_rows(load_stock_config_from_cloud())
    if cloud_rows:
        used = {x["code"] for x in cloud_rows}
        rows = cloud_rows[:MAX_STOCKS]
        for item in DEFAULT_STOCKS:
            if len(rows) >= MAX_STOCKS:
                break
            if item["code"] not in used:
                rows.append(item.copy())
                used.add(item["code"])
        return rows[:MAX_STOCKS]

    try:
        if STOCK_CONFIG_PATH.exists():
            rows = json.loads(STOCK_CONFIG_PATH.read_text(encoding="utf-8"))
            rows = normalize_stock_rows(rows)
            used = {x["code"] for x in rows}
            for item in DEFAULT_STOCKS:
                if len(rows) >= MAX_STOCKS:
                    break
                if item["code"] not in used:
                    rows.append(item.copy())
                    used.add(item["code"])
            if rows:
                return rows[:MAX_STOCKS]
    except Exception as e:
        print(f"股票設定讀取失敗：{e}")

    return DEFAULT_STOCKS.copy()


def save_stock_config(rows):
    STOCK_CONFIG_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    save_stock_config_to_cloud(rows)


stock_rows = load_stock_config()

with st.sidebar:
    st.markdown("### 📑 戰情頁面")
    if cloud_db_enabled():
        st.success("☁️ 雲端資料庫：已連線")
    else:
        st.warning("☁️ 雲端資料庫：尚未設定；目前可本機測試，但20日歷史不會永久保存。")

    view_options = ["HOME"] + list(range(1, TOTAL_PAGES + 1))
    def _view_label(v):
        if v == "HOME":
            return "🏆 首頁｜DAVID 今日 TOP 10"
        if v == 9:
            return "🔥 Page 9｜本週熱門候補（100檔自動選）"
        if v == 10:
            return "🚨 Page 10｜異常轉強股（100檔自動選）"
        return f"Page {v}｜{PAGE_NAMES.get(v, '')}"

    active_view = st.radio(
        "選擇頁面",
        options=view_options,
        format_func=_view_label,
        horizontal=False,
        key="active_view_v13_100",
    )
    active_page = 0 if active_view == "HOME" else int(active_view)

    st.markdown("### ⚙️ 100檔股票設定")
    st.caption("設定池共100檔／10組，每組10檔。首頁、Page 9、Page 10 會從100檔自動重新排名。")
    config_page = st.selectbox(
        "選擇要編輯的設定組",
        options=list(range(1, TOTAL_PAGES + 1)),
        format_func=lambda p: f"設定 {p}｜{PAGE_NAMES.get(p, '')}",
        key="config_page_v13_100",
    )
    config_start = (config_page - 1) * STOCKS_PER_PAGE
    config_end = config_start + STOCKS_PER_PAGE
    editor_df = pd.DataFrame(stock_rows[config_start:config_end])

    edited_df = st.data_editor(
        editor_df, hide_index=True, use_container_width=True, num_rows="fixed",
        column_config={
            "code": st.column_config.TextColumn("股票代碼", help="例如 2330、3324"),
            "name": st.column_config.TextColumn("公司名稱", help="請輸入繁體中文公司名稱"),
            "market": st.column_config.SelectboxColumn("市場", options=["TW", "TWO"], help="TW=上市；TWO=上櫃", required=True),
        },
        key=f"stock_editor_v13_100_page_{config_page}",
    )

    c1, c2 = st.columns(2)
    with c1:
        save_clicked = st.button("💾 儲存本組", use_container_width=True)
    with c2:
        reset_clicked = st.button("↩️ 還原100檔", use_container_width=True)

    if save_clicked:
        edited_rows = normalize_stock_rows(edited_df.to_dict("records"))
        if len(edited_rows) != STOCKS_PER_PAGE:
            st.error("本組必須保留10檔有效股票，且代碼不可重複。")
        else:
            merged = stock_rows.copy()
            merged[config_start:config_end] = edited_rows
            if len({x["code"] for x in merged}) != len(merged):
                st.error("100檔股票代碼不可重複，請檢查後再儲存。")
            else:
                save_stock_config(merged)
                st.cache_data.clear()
                st.success(f"設定組 {config_page} 已儲存。")
                st.rerun()

    if reset_clicked:
        save_stock_config(DEFAULT_STOCKS)
        st.cache_data.clear()
        st.success("已還原新版預設100檔。")
        st.rerun()

stock_rows = load_stock_config()
stock_list = {x["code"]: x["name"] for x in stock_rows}
symbol_map = {
    x["code"]: f'{x["code"]}.{x["market"]}'
    for x in stock_rows
}


# ============================================================
# 3. Yahoo Finance 高速批次 + 缺檔自動補抓
# 第一層：一次批次下載全部股票
# 第二層：只針對批次缺漏股票，依指定 TW/TWO 個別補抓
# ============================================================

MIN_HISTORY_ROWS = 60
CACHE_TTL_SECONDS = 300


def _clean_history_frame(data):
    """統一整理 Yahoo 回傳的 OHLCV DataFrame。"""
    if data is None or data.empty:
        return pd.DataFrame()

    try:
        data = data.copy()

        if isinstance(data.columns, pd.MultiIndex):
            # 單檔 download 有時也會保留 MultiIndex
            if len(data.columns.levels) >= 2:
                last_level = data.columns.get_level_values(-1)
                first_level = data.columns.get_level_values(0)
                ohlcv = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
                if any(str(x) in ohlcv for x in first_level):
                    data.columns = [str(c[0]) for c in data.columns]
                elif any(str(x) in ohlcv for x in last_level):
                    data.columns = [str(c[-1]) for c in data.columns]

        # 去除全空列，並要求核心欄位存在
        data = data.dropna(how="all")
        required = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in data.columns for col in required):
            return pd.DataFrame()

        data = data.dropna(subset=["Close"])
        return data

    except Exception as e:
        print(f"Yahoo 資料整理錯誤：{e}")
        return pd.DataFrame()


def _extract_symbol_frame(raw, symbol, symbol_count):
    if raw is None or raw.empty:
        return pd.DataFrame()

    try:
        if isinstance(raw.columns, pd.MultiIndex):
            lv0 = raw.columns.get_level_values(0)
            lv1 = raw.columns.get_level_values(1)

            if symbol in lv0:
                data = raw[symbol].copy()
            elif symbol in lv1:
                data = raw.xs(symbol, axis=1, level=1).copy()
            else:
                return pd.DataFrame()
        else:
            if symbol_count != 1:
                return pd.DataFrame()
            data = raw.copy()

        return _clean_history_frame(data)

    except Exception as e:
        print(f"{symbol} 批次資料拆分錯誤：{e}")
        return pd.DataFrame()


def _fetch_one_symbol(symbol):
    """個別補抓。先用 yf.download，再用 Ticker.history 做第二次救援。"""
    # 方法 A：單檔 download
    try:
        raw = yf.download(
            tickers=symbol,
            period="1y",
            interval="1d",
            auto_adjust=False,
            threads=False,
            progress=False,
            timeout=10
        )
        data = _clean_history_frame(raw)
        if len(data) >= MIN_HISTORY_ROWS:
            return data
    except Exception as e:
        print(f"{symbol} 單檔 download 補抓失敗：{e}")

    # 方法 B：Ticker.history 再救援一次
    try:
        raw = yf.Ticker(symbol).history(
            period="1y",
            interval="1d",
            auto_adjust=False,
            timeout=10
        )
        data = _clean_history_frame(raw)
        if len(data) >= MIN_HISTORY_ROWS:
            return data
    except Exception as e:
        print(f"{symbol} Ticker.history 補抓失敗：{e}")

    return pd.DataFrame()


@st.cache_data(
    ttl=CACHE_TTL_SECONDS,
    show_spinner=False
)
def get_stock_batch(stock_key):
    # stock_key: ((code, name, market), ...)
    symbols = [
        f"{code}.{market}"
        for code, name, market in stock_key
    ]

    result = {symbol: pd.DataFrame() for symbol in symbols}
    stats = {
        "total": len(symbols),
        "batch_success": 0,
        "fallback_attempted": 0,
        "fallback_success": 0,
        "failed": 0,
        "failed_symbols": [],
    }

    if not symbols:
        return result, stats

    # ------------------------------
    # 第一層：高速批次抓取
    # ------------------------------
    raw = pd.DataFrame()
    try:
        raw = yf.download(
            tickers=" ".join(symbols),
            period="1y",
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            threads=True,
            progress=False,
            timeout=12
        )
    except Exception as e:
        print(f"Yahoo 批次抓取錯誤：{e}")

    missing = []

    for symbol in symbols:
        data = _extract_symbol_frame(raw, symbol, len(symbols))
        if len(data) >= MIN_HISTORY_ROWS:
            result[symbol] = data.copy()
            stats["batch_success"] += 1
        else:
            missing.append(symbol)

    # ------------------------------
    # 第二層：只補抓批次遺漏股票
    # ------------------------------
    stats["fallback_attempted"] = len(missing)

    for symbol in missing:
        data = _fetch_one_symbol(symbol)
        if len(data) >= MIN_HISTORY_ROWS:
            result[symbol] = data.copy()
            stats["fallback_success"] += 1
        else:
            stats["failed_symbols"].append(symbol)

    stats["failed"] = len(stats["failed_symbols"])
    return result, stats


# ============================================================
# 4. MACD Histogram
# ============================================================

def calculate_macd(close):

    ema12 = close.ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False
    ).mean()

    macd_line = (
        ema12 - ema26
    )

    signal_line = macd_line.ewm(
        span=9,
        adjust=False
    ).mean()

    histogram = (
        macd_line
        - signal_line
    )

    return histogram


# ============================================================
# 5. Pivot Swing + Fibonacci
# ============================================================

def calculate_pivot_fib(
    data,
    lookback=120,
    left=3,
    right=3
):

    empty_result = {

        "方向": "資料不足",

        "波段高": np.nan,

        "波段低": np.nan,

        "0.236": np.nan,

        "0.382": np.nan,

        "0.500": np.nan,

        "0.618": np.nan,

        "0.786": np.nan,

        "1.272": np.nan,

        "1.618": np.nan,

        "Fib位置": "資料不足"
    }


    if (
        data is None
        or data.empty
        or len(data) < left + right + 20
    ):

        return empty_result


    d = (
        data
        .tail(lookback)
        .copy()
        .reset_index(drop=True)
    )


    highs = (
        d["High"]
        .astype(float)
        .to_numpy()
    )

    lows = (
        d["Low"]
        .astype(float)
        .to_numpy()
    )

    close_now = float(
        d["Close"].iloc[-1]
    )


    pivot_highs = []
    pivot_lows = []


    for i in range(
        left,
        len(d) - right
    ):

        hi_window = highs[
            i-left:
            i+right+1
        ]

        lo_window = lows[
            i-left:
            i+right+1
        ]


        if (
            highs[i]
            == np.max(hi_window)
        ):

            pivot_highs.append(i)


        if (
            lows[i]
            == np.min(lo_window)
        ):

            pivot_lows.append(i)


    # --------------------------------------------------------
    # 找不到 Pivot 時
    # 使用區間最高 / 最低
    # --------------------------------------------------------

    if (
        not pivot_highs
        or not pivot_lows
    ):

        high_idx = int(
            d["High"].idxmax()
        )

        low_idx = int(
            d["Low"].idxmin()
        )


    else:

        high_idx = (
            pivot_highs[-1]
        )

        low_idx = (
            pivot_lows[-1]
        )


    swing_high = float(
        d.loc[
            high_idx,
            "High"
        ]
    )

    swing_low = float(
        d.loc[
            low_idx,
            "Low"
        ]
    )


    wave = (
        swing_high
        - swing_low
    )


    if wave <= 0:

        result = (
            empty_result.copy()
        )

        result.update({

            "方向":
                "無有效波段",

            "波段高":
                swing_high,

            "波段低":
                swing_low,

            "Fib位置":
                "無有效波段"
        })

        return result


    # ========================================================
    # 多頭波段
    # ========================================================

    if low_idx < high_idx:

        direction = (
            "多頭波段"
        )


        levels = {

            "0.236":
                swing_high
                - wave * 0.236,

            "0.382":
                swing_high
                - wave * 0.382,

            "0.500":
                swing_high
                - wave * 0.500,

            "0.618":
                swing_high
                - wave * 0.618,

            "0.786":
                swing_high
                - wave * 0.786,

            "1.272":
                swing_high
                + wave * 0.272,

            "1.618":
                swing_high
                + wave * 0.618,
        }


        if close_now > swing_high:

            fib_status = (
                "突破前高"
            )


        elif (
            close_now
            >= levels["0.236"]
        ):

            fib_status = (
                "近前高"
            )


        elif (
            close_now
            >= levels["0.382"]
        ):

            fib_status = (
                "0.382支撐"
            )


        elif (
            close_now
            >= levels["0.500"]
        ):

            fib_status = (
                "0.500支撐"
            )


        elif (
            close_now
            >= levels["0.618"]
        ):

            fib_status = (
                "0.618關鍵"
            )


        elif (
            close_now
            >= levels["0.786"]
        ):

            fib_status = (
                "0.786深回"
            )


        else:

            fib_status = (
                "跌破0.786"
            )


    # ========================================================
    # 空頭波段
    # ========================================================

    else:

        direction = (
            "空頭波段"
        )


        levels = {

            "0.236":
                swing_low
                + wave * 0.236,

            "0.382":
                swing_low
                + wave * 0.382,

            "0.500":
                swing_low
                + wave * 0.500,

            "0.618":
                swing_low
                + wave * 0.618,

            "0.786":
                swing_low
                + wave * 0.786,

            "1.272":
                swing_low
                - wave * 0.272,

            "1.618":
                swing_low
                - wave * 0.618,
        }


        if close_now < swing_low:

            fib_status = (
                "跌破前低"
            )


        elif (
            close_now
            <= levels["0.236"]
        ):

            fib_status = (
                "近前低"
            )


        elif (
            close_now
            <= levels["0.382"]
        ):

            fib_status = (
                "0.382壓力"
            )


        elif (
            close_now
            <= levels["0.500"]
        ):

            fib_status = (
                "0.500壓力"
            )


        elif (
            close_now
            <= levels["0.618"]
        ):

            fib_status = (
                "0.618壓力"
            )


        elif (
            close_now
            <= levels["0.786"]
        ):

            fib_status = (
                "0.786壓力"
            )


        else:

            fib_status = (
                "逼近前高"
            )


    return {

        "方向":
            direction,

        "波段高":
            swing_high,

        "波段低":
            swing_low,

        **levels,

        "Fib位置":
            fib_status
    }


# ============================================================
# 6. 單檔股票分析
# ============================================================

def analyze_stock(
    code,
    name,
    data,
    symbol
):

    if (
        data.empty
        or len(data) < 60
    ):

        return {

            "AI 精選族群":
                f"{code} {name}",

            "昨收":
                np.nan,

            "開盤":
                np.nan,

            "現價":
                np.nan,

            "漲跌":
                np.nan,

            "幅%":
                "--",

            "量比":
                "--",

            "乖離":
                "--",

            "早盤":
                "--",

            "動能":
                "--",

            "成本":
                "--",

            "力道":
                "--",

            "六買":
                "--",

            "六賣":
                "--",

            "Fib位置":
                "資料不足",

            "決策":
                "無資料",

            "_fib":
                None
        }


    close = (
        data["Close"]
        .astype(float)
    )

    volume_series = (
        data["Volume"]
        .astype(float)
    )


    latest = (
        data.iloc[-1]
    )

    previous = (
        data.iloc[-2]
    )


    p = float(
        latest["Close"]
    )

    op = float(
        latest["Open"]
    )

    hi = float(
        latest["High"]
    )

    lo = float(
        latest["Low"]
    )

    vo = float(
        latest["Volume"]
    )

    pc = float(
        previous["Close"]
    )


    # ========================================================
    # MA20 / VM20 / MA5
    # ========================================================

    ma20_series = (
        close
        .rolling(20)
        .mean()
    )

    vm20_series = (
        volume_series
        .rolling(20)
        .mean()
    )

    ma5_series = (
        close
        .rolling(5)
        .mean()
    )


    ma20 = float(
        ma20_series.iloc[-1]
    )

    vm20 = float(
        vm20_series.iloc[-1]
    )

    ma5_now = float(
        ma5_series.iloc[-1]
    )

    ma5_prev = float(
        ma5_series.iloc[-2]
    )


    ma5_up = (

        not np.isnan(
            ma5_now
        )

        and

        not np.isnan(
            ma5_prev
        )

        and

        ma5_now
        > ma5_prev
    )


    # ========================================================
    # MACD
    # ========================================================

    macd_hist = (
        calculate_macd(
            close
        )
    )

    mh = float(
        macd_hist.iloc[-1]
    )

    if np.isnan(mh):

        mh = 0.0


    # ========================================================
    # 基礎計算
    # ========================================================

    diff = (
        p - pc
    )


    ch = (

        ((p - pc) / pc)
        * 100

        if pc > 0

        else 0.0
    )


    vr = (

        vo / vm20

        if vm20 > 0

        else 1.0
    )


    bias = (

        ((p - ma20) / ma20)
        * 100

        if ma20 > 0

        else 0.0
    )


    mid = (
        hi + lo
    ) / 2


    # ========================================================
    # 六買 V10
    # ========================================================

    b1 = p > op
    b2 = p > ma20
    b3 = vo > vm20
    b4 = p > mid
    b5 = ma5_up
    b6 = mh > 0


    b_score = sum([

        b1,
        b2,
        b3,
        b4,
        b5,
        b6
    ])


    # ========================================================
    # 六賣 V10
    # ========================================================

    s1 = p < op

    s2 = p < ma20

    s3 = (
        vo > vm20
        and
        p < pc
    )

    s4 = p < mid

    s5 = (
        not ma5_up
    )

    s6 = (
        mh <= 0
    )


    s_score = sum([

        s1,
        s2,
        s3,
        s4,
        s5,
        s6
    ])


    # ========================================================
    # 早盤
    # ========================================================

    is_strong = (
        ch >= 3.0
    )


    if is_strong:

        morning = (
            "強攻"
        )


    elif b1:

        morning = (
            "合格"
        )


    else:

        morning = (
            "待定"
        )


    # ========================================================
    # 動能 / 成本 / 力道
    # ========================================================

    momentum = (

        "放量"

        if vo > vm20

        else "量縮"
    )


    cost = (

        "站穩"

        if p > ma20

        else "破位"
    )


    strength = (

        "強勢"

        if p > mid

        else "弱勢"
    )


    # ========================================================
    # V10 最終決策
    # ========================================================

    if b_score == 6:

        decision = (
            "全導通"
        )


    elif s_score == 6:

        decision = (
            "全空破"
        )


    elif b_score >= 4:

        decision = (
            "看多"
        )


    elif s_score >= 4:

        decision = (
            "看空"
        )


    else:

        decision = (
            "觀望"
        )


    # ========================================================
    # Fib
    # ========================================================

    fib = (
        calculate_pivot_fib(
            data
        )
    )


    # ========================================================
    # 回傳
    # ========================================================

    return {

        "AI 精選族群":
            f"{code} {name}",

        "昨收":
            pc,

        "開盤":
            op,

        "現價":
            p,

        "漲跌":
            diff,

        "幅%":
            f"{ch:+.1f}%",

        "量比":
            f"{vr:.1f}x",

        "乖離":
            f"{bias:+.1f}%",

        "早盤":
            morning,

        "動能":
            momentum,

        "成本":
            cost,

        "力道":
            strength,

        "六買":
            int(
                b_score
            ),

        "六賣":
            int(
                s_score
            ),

        "Fib位置":
            fib["Fib位置"],

        "決策":
            decision,

        "_fib":
            fib
    }


# ============================================================
# V13.100 智慧排名：首頁 / 本週熱門候補 / 異常轉強
# ============================================================
def _safe_float(value, suffix=""):
    try:
        text = str(value).replace(suffix, "").strip()
        if text in ("", "--", "nan", "None"):
            return 0.0
        return float(text)
    except Exception:
        return 0.0


def _technical_metrics(data):
    m = {
        "ret1": 0.0, "ret5": 0.0, "ret20": 0.0, "vol_ratio": 1.0,
        "new20": False, "macd_flip": False, "ma_cross": False,
    }
    if data is None or data.empty or len(data) < 25:
        return m
    try:
        close = data["Close"].astype(float)
        vol = data["Volume"].astype(float)
        m["ret1"] = (close.iloc[-1] / close.iloc[-2] - 1) * 100 if close.iloc[-2] else 0.0
        m["ret5"] = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if close.iloc[-6] else 0.0
        m["ret20"] = (close.iloc[-1] / close.iloc[-21] - 1) * 100 if close.iloc[-21] else 0.0
        vm20 = float(vol.rolling(20).mean().iloc[-1])
        m["vol_ratio"] = float(vol.iloc[-1] / vm20) if vm20 > 0 else 1.0
        prior20_high = float(close.iloc[-21:-1].max())
        m["new20"] = float(close.iloc[-1]) >= prior20_high
        macd = calculate_macd(close)
        m["macd_flip"] = bool(macd.iloc[-1] > 0 and macd.iloc[-2] <= 0)
        ma5 = close.rolling(5).mean()
        ma20 = close.rolling(20).mean()
        m["ma_cross"] = bool(ma5.iloc[-1] > ma20.iloc[-1] and ma5.iloc[-2] <= ma20.iloc[-2])
    except Exception:
        pass
    return m


def _score_bundle(result, data):
    buy = _safe_float(result.get("六買"))
    sell = _safe_float(result.get("六賣"))
    vr = _safe_float(result.get("量比"), "x")
    bias = abs(_safe_float(result.get("乖離"), "%"))
    fib = str(result.get("Fib位置", ""))
    decision = str(result.get("決策", ""))
    tech = _technical_metrics(data)

    # 首頁綜合分數 0~100：六買30、六賣15、MACD/動能15、量能10、趨勢10、乖離5、Fib10、短中期持續5
    score = buy / 6 * 30 + max(0.0, 6 - sell) / 6 * 15
    score += 15 if (str(result.get("動能")) == "放量" or tech["ret5"] > 3) else 6
    score += min(max(vr, 0), 2.0) / 2.0 * 10
    score += 10 if str(result.get("成本")) == "站穩" else 0
    score += max(0.0, 5 - max(0.0, bias - 5) * 0.5)
    if any(k in fib for k in ["突破前高", "近前高", "0.382支撐"]):
        score += 10
    elif any(k in fib for k in ["0.500", "0.618"]):
        score += 6
    else:
        score += 2
    score += 5 if tech["ret5"] > 0 and tech["ret20"] > 0 else 0
    if decision in ("全導通", "看多"):
        score += 3
    if bias > 15:
        score -= min(8, (bias - 15) * 0.6)
    david = max(0.0, min(100.0, score))

    # Page 9：本週熱門候補，強調5日動能、量能、突破與買分
    weekly = 30 + min(max(tech["ret5"], -8), 12) * 1.8
    weekly += min(max(tech["vol_ratio"] - 0.8, 0), 2.2) * 9
    weekly += buy * 3.5
    weekly += 12 if tech["new20"] else 0
    weekly += min(max(tech["ret20"], -10), 20) * 0.5
    if bias > 18:
        weekly -= 10
    weekly = max(0.0, min(100.0, weekly))

    # Page 10：異常轉強，強調單日爆量、價格急升、MACD/均線翻多
    abnormal = 10
    abnormal += min(max(tech["vol_ratio"] - 1.0, 0), 3.0) * 18
    abnormal += min(max(tech["ret1"], 0), 10) * 2.0
    abnormal += 18 if tech["macd_flip"] else 0
    abnormal += 14 if tech["ma_cross"] else 0
    abnormal += buy * 2.5
    abnormal = max(0.0, min(100.0, abnormal))
    return david, weekly, abnormal, tech


def _select_ranked(stock_rows_all, result_all, data_all, mode="home", top_n=10):
    result_map = {str(r.get("AI 精選族群", "")).split(" ", 1)[0]: r for r in result_all}
    ranked = []
    for idx, item in enumerate(stock_rows_all):
        code = item["code"]
        result = result_map.get(code)
        if not result or result.get("決策") in ("無資料", "資料錯誤"):
            continue
        symbol = f"{code}.{item['market']}"
        david, weekly, abnormal, tech = _score_bundle(result, data_all.get(symbol, pd.DataFrame()))
        score = david if mode == "home" else weekly if mode == "weekly" else abnormal
        group_no = idx // 10 + 1
        ranked.append((score, david, weekly, abnormal, group_no, item, result, tech))
    ranked.sort(key=lambda x: x[0], reverse=True)

    chosen = []
    group_count = {}
    for rec in ranked:
        # 首頁單一設定群最多3檔，避免Top10被單一族群完全佔滿；Page9/10不限制。
        if mode == "home":
            g = rec[4]
            if group_count.get(g, 0) >= 3:
                continue
            group_count[g] = group_count.get(g, 0) + 1
        chosen.append(rec)
        if len(chosen) >= top_n:
            break

    rows, results = [], []
    for rank_no, rec in enumerate(chosen, start=1):
        score, david, weekly, abnormal, group_no, item, result, tech = rec
        rr = result.copy()
        rr["DAVID分數"] = round(david, 1)
        if mode == "weekly":
            rr["本週熱度"] = round(weekly, 1)
        elif mode == "abnormal":
            rr["異常轉強"] = round(abnormal, 1)
        rr["自動排名"] = rank_no
        rr["所屬族群"] = PAGE_NAMES.get(group_no, f"設定{group_no}")
        rows.append(item)
        results.append(rr)
    return rows, results


# ============================================================
# 7. 執行頁面資料：固定頁只抓10檔；首頁/Page9/Page10抓100檔後自動排名
# ============================================================
load_started = time.perf_counter()
is_dynamic_view = active_view in ("HOME", 9, 10)
all_results = []

if is_dynamic_view:
    batch_data = {}
    total_stats = {"total": 0, "batch_success": 0, "fallback_attempted": 0, "fallback_success": 0, "failed": 0, "failed_symbols": []}
    with st.spinner("正在掃描100檔並計算智慧排名；已載入資料會直接使用300秒快取..."):
        for p in range(1, TOTAL_PAGES + 1):
            a = (p - 1) * STOCKS_PER_PAGE
            b = a + STOCKS_PER_PAGE
            rows = stock_rows[a:b]
            key = tuple((x["code"], x["name"], x["market"]) for x in rows)
            page_data, page_stats = get_stock_batch(key)
            batch_data.update(page_data)
            for k in total_stats:
                if k == "failed_symbols":
                    total_stats[k].extend(page_stats.get(k, []))
                else:
                    total_stats[k] += page_stats.get(k, 0)
            for item in rows:
                code = item["code"]
                symbol = f"{code}.{item['market']}"
                try:
                    all_results.append(analyze_stock(code, item["name"], page_data.get(symbol, pd.DataFrame()), symbol))
                except Exception as e:
                    print(f"{code} 分析錯誤：{e}")
    fetch_stats = total_stats
    if active_view == "HOME":
        current_rows, results = _select_ranked(stock_rows, all_results, batch_data, mode="home")
        active_view_title = "🏆 DAVID 今日 TOP 10｜100檔智慧精選"
    elif active_view == 9:
        current_rows, results = _select_ranked(stock_rows, all_results, batch_data, mode="weekly")
        active_view_title = "🔥 Page 9｜本週熱門候補 TOP 10"
    else:
        current_rows, results = _select_ranked(stock_rows, all_results, batch_data, mode="abnormal")
        active_view_title = "🚨 Page 10｜異常轉強股 TOP 10"
    page_start, page_end = 0, 10
else:
    page_start = (active_page - 1) * STOCKS_PER_PAGE
    page_end = page_start + STOCKS_PER_PAGE
    current_rows = stock_rows[page_start:page_end]
    page_key = tuple((x["code"], x["name"], x["market"]) for x in current_rows)
    with st.spinner(f"正在載入 Page {active_page} 的10檔資料；缺漏股票將自動個別補抓..."):
        batch_data, fetch_stats = get_stock_batch(page_key)
        results = []
        for item in current_rows:
            code = item["code"]
            symbol = f"{code}.{item['market']}"
            try:
                results.append(analyze_stock(code, item["name"], batch_data.get(symbol, pd.DataFrame()), symbol))
            except Exception as e:
                print(f"{code} 分析錯誤：{e}")
                results.append({
                    "AI 精選族群": f"{code} {item['name']}", "昨收": np.nan, "開盤": np.nan,
                    "現價": np.nan, "漲跌": np.nan, "幅%": "--", "量比": "--", "乖離": "--",
                    "早盤": "--", "動能": "--", "成本": "--", "力道": "--", "六買": "--", "六賣": "--",
                    "Fib位置": "資料錯誤", "決策": "資料錯誤", "_fib": None
                })
    active_view_title = f"📄 Page {active_page}｜{PAGE_NAMES.get(active_page, '')}"

current_symbol_map = {x["code"]: f"{x['code']}.{x['market']}" for x in current_rows}
load_seconds = time.perf_counter() - load_started
success_total = fetch_stats["total"] - fetch_stats["failed"]

# V13：目前顯示10檔自動保存到雲端。同一交易日+同一股票採 upsert，不會重複累加。
current_history_payload = history_payload_for_page(current_rows, results, batch_data)
history_saved_ok = False
history_saved_count = 0
history_saved_error = ""
if cloud_db_enabled() and current_history_payload:
    history_saved_ok, history_saved_count, history_saved_error = upsert_history(current_history_payload)
    if history_saved_ok:
        fetch_history_20.clear()

with st.sidebar:
    st.divider()
    st.markdown("### 🚀 本頁資料狀態")

    m1, m2 = st.columns(2)
    with m1:
        st.metric("完整取得", f"{success_total}/{fetch_stats['total']}")
    with m2:
        st.metric("本頁耗時", f"{load_seconds:.2f} 秒")

    st.caption(
        f"批次成功：{fetch_stats['batch_success']}｜"
        f"補抓嘗試：{fetch_stats['fallback_attempted']}｜"
        f"補抓成功：{fetch_stats['fallback_success']}｜"
        f"最終失敗：{fetch_stats['failed']}"
    )

    if fetch_stats["failed_symbols"]:
        st.warning("仍無法取得：" + ", ".join(fetch_stats["failed_symbols"]))
    else:
        st.success(f"資料完整取得：{success_total}/{fetch_stats['total']}。")

    st.caption(
        "智慧載入：固定頁只抓10檔；首頁／Page 9／Page 10掃描100檔後自動排名。300秒內使用快取。"
    )

    st.markdown("### 🗄️ 20日歷史")
    if history_saved_ok:
        st.success(f"本頁已保存／更新 {history_saved_count} 檔當日戰情。")
    elif cloud_db_enabled() and history_saved_error:
        st.warning("本頁歷史保存失敗：" + history_saved_error)
    else:
        st.caption("設定 Supabase 後，本頁每次載入都會自動 upsert，不會同日重複新增。")

    snapshot_all_clicked = st.button("📚 保存全部100檔今日戰情", use_container_width=True, disabled=not cloud_db_enabled())

    st.markdown("### ⚡ 選用：預載其他頁")
    preload_clicked = st.button("預載其餘設定組", use_container_width=True)

if snapshot_all_clicked:
    snap_started = time.perf_counter()
    snap_saved = 0
    snap_failed = []
    with st.spinner("正在抓取10組共100檔並保存今日戰情到 Supabase..."):
        for p in range(1, TOTAL_PAGES + 1):
            a = (p - 1) * STOCKS_PER_PAGE
            b = a + STOCKS_PER_PAGE
            rows = stock_rows[a:b]
            key = tuple((x["code"], x["name"], x["market"]) for x in rows)
            page_data, page_stats = get_stock_batch(key)
            page_results = []
            for item in rows:
                code = item["code"]
                symbol = f'{code}.{item["market"]}'
                try:
                    page_results.append(analyze_stock(code, item["name"], page_data.get(symbol, pd.DataFrame()), symbol))
                except Exception as e:
                    snap_failed.append(f"{code} 分析失敗")
            payload = history_payload_for_page(rows, page_results, page_data)
            ok, count, err = upsert_history(payload)
            if ok:
                snap_saved += count
            elif err:
                snap_failed.append(f"第{p}頁：{err}")
            snap_failed.extend(page_stats.get("failed_symbols", []))

    fetch_history_20.clear()
    elapsed = time.perf_counter() - snap_started
    if snap_failed:
        st.warning(f"100檔保存完成 {snap_saved}/100，耗時 {elapsed:.1f} 秒；異常：" + ", ".join(snap_failed[:10]))
    else:
        st.success(f"✅ 100檔今日戰情已保存／更新完成：{snap_saved}/100，耗時 {elapsed:.1f} 秒。")


if preload_clicked:
    preload_started = time.perf_counter()
    preload_ok = 0
    preload_fail = []
    with st.spinner("正在預載其餘頁面到快取；完成後切頁會更快..."):
        for p in range(1, TOTAL_PAGES + 1):
            if p == active_page:
                continue
            a = (p - 1) * STOCKS_PER_PAGE
            b = a + STOCKS_PER_PAGE
            rows = stock_rows[a:b]
            key = tuple((x["code"], x["name"], x["market"]) for x in rows)
            _, stat = get_stock_batch(key)
            preload_ok += stat["total"] - stat["failed"]
            if stat["failed_symbols"]:
                preload_fail.extend(stat["failed_symbols"])

    preload_seconds = time.perf_counter() - preload_started
    if preload_fail:
        st.warning(
            f"其餘設定組已預載 {preload_ok} 檔，耗時 {preload_seconds:.2f} 秒；"
            f"仍無法取得：{', '.join(preload_fail)}"
        )
    else:
        st.success(f"其餘設定組已完成預載，耗時 {preload_seconds:.2f} 秒。")

st.markdown(f"### {active_view_title}")

# Fib 下拉只顯示目前頁10檔
stock_list = {x["code"]: x["name"] for x in current_rows}

# ============================================================
# 8. 表格資料
# ============================================================

display_results = [

    {
        k: v

        for k, v
        in x.items()

        if k != "_fib"
    }

    for x in results
]


df = pd.DataFrame(
    display_results
)


# ============================================================
# 9. 表格條件配色
# ============================================================

def row_styles(row):

    styles = [
        ""
    ] * len(
        row.index
    )


    def set_style(
        column,
        style
    ):

        pos = (
            df.columns
            .get_loc(
                column
            )
        )

        styles[pos] = (
            style
        )


    # --------------------------------------------------------
    # 基礎
    # --------------------------------------------------------

    for col in df.columns:

        set_style(
            col,
            "background-color:#05090D;"
            "color:#DCE6EF;"
            "font-weight:600;"
        )


    set_style(
        "AI 精選族群",
        "background-color:#061019;"
        "color:#FFFFFF;"
        "font-weight:900;"
    )


    for col in [
        "昨收",
        "開盤"
    ]:

        set_style(
            col,
            "background-color:#081018;"
            "color:#AEBCC9;"
            "font-weight:600;"
        )


    # --------------------------------------------------------
    # 紅漲 / 綠跌
    # --------------------------------------------------------

    change = (
        row["漲跌"]
    )


    if pd.notna(
        change
    ):

        if change > 0:

            price_style = (
                "background-color:#2A080A;"
                "color:#FF4650;"
                "font-weight:900;"
            )


        elif change < 0:

            price_style = (
                "background-color:#042019;"
                "color:#00E08A;"
                "font-weight:900;"
            )


        else:

            price_style = (
                "background-color:#10161D;"
                "color:#FFFFFF;"
                "font-weight:800;"
            )


        for col in [
            "現價",
            "漲跌",
            "幅%"
        ]:

            set_style(
                col,
                price_style
            )


    # --------------------------------------------------------
    # 乖離
    # --------------------------------------------------------

    try:

        bias_value = float(

            str(
                row["乖離"]
            )

            .replace(
                "%",
                ""
            )
        )


        if bias_value > 0:

            set_style(
                "乖離",
                "background-color:#2A080A;"
                "color:#FF4650;"
                "font-weight:900;"
            )


        elif bias_value < 0:

            set_style(
                "乖離",
                "background-color:#042019;"
                "color:#00E08A;"
                "font-weight:900;"
            )


    except Exception:

        pass


    # --------------------------------------------------------
    # 量比
    # --------------------------------------------------------

    try:

        vr = float(

            str(
                row["量比"]
            )

            .replace(
                "x",
                ""
            )
        )


        if vr > 1.5:

            set_style(
                "量比",
                "background-color:#F7941D;"
                "color:#111111;"
                "font-weight:900;"
            )


        elif vr >= 1.0:

            set_style(
                "量比",
                "background-color:#4A2D05;"
                "color:#FFD180;"
                "font-weight:800;"
            )


    except Exception:

        pass


    # --------------------------------------------------------
    # 早盤
    # --------------------------------------------------------

    if (
        row["早盤"]
        == "強攻"
    ):

        set_style(
            "早盤",
            "background-color:#D91E2B;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        row["早盤"]
        == "合格"
    ):

        set_style(
            "早盤",
            "background-color:#2E9E4D;"
            "color:white;"
            "font-weight:900;"
        )


    else:

        set_style(
            "早盤",
            "background-color:#262B31;"
            "color:#CCD3DA;"
            "font-weight:700;"
        )


    # --------------------------------------------------------
    # 動能
    # --------------------------------------------------------

    if (
        row["動能"]
        == "放量"
    ):

        set_style(
            "動能",
            "background-color:#F57C00;"
            "color:white;"
            "font-weight:900;"
        )


    else:

        set_style(
            "動能",
            "background-color:#252A30;"
            "color:#AAB2BA;"
            "font-weight:700;"
        )


    # --------------------------------------------------------
    # 成本
    # --------------------------------------------------------

    if (
        row["成本"]
        == "站穩"
    ):

        set_style(
            "成本",
            "background-color:#1769E0;"
            "color:white;"
            "font-weight:900;"
        )


    else:

        set_style(
            "成本",
            "background-color:#252A30;"
            "color:#C4CBD2;"
            "font-weight:700;"
        )


    # --------------------------------------------------------
    # 力道
    # --------------------------------------------------------

    if (
        row["力道"]
        == "強勢"
    ):

        set_style(
            "力道",
            "background-color:#260A0A;"
            "color:#FF4650;"
            "font-weight:900;"
        )


    else:

        set_style(
            "力道",
            "background-color:#042019;"
            "color:#00E08A;"
            "font-weight:900;"
        )


    # --------------------------------------------------------
    # 六買
    # --------------------------------------------------------

    try:

        buy = int(
            row["六買"]
        )


        if buy == 6:

            set_style(
                "六買",
                "background-color:#FF1493;"
                "color:white;"
                "font-weight:900;"
            )


        elif buy >= 4:

            set_style(
                "六買",
                "background-color:#EF3340;"
                "color:white;"
                "font-weight:900;"
            )


        else:

            set_style(
                "六買",
                "background-color:#10151B;"
                "color:#F5F7F9;"
                "font-weight:800;"
            )


    except Exception:

        pass


    # --------------------------------------------------------
    # 六賣
    # --------------------------------------------------------

    try:

        sell = int(
            row["六賣"]
        )


        if sell == 6:

            set_style(
                "六賣",
                "background-color:#7B1FA2;"
                "color:white;"
                "font-weight:900;"
            )


        elif sell >= 4:

            set_style(
                "六賣",
                "background-color:#00796B;"
                "color:white;"
                "font-weight:900;"
            )


        else:

            set_style(
                "六賣",
                "background-color:#10151B;"
                "color:#F5F7F9;"
                "font-weight:800;"
            )


    except Exception:

        pass


    # --------------------------------------------------------
    # Fib位置
    # --------------------------------------------------------

    fib_status = str(
        row["Fib位置"]
    )


    if (
        "突破前高"
        in fib_status
    ):

        set_style(
            "Fib位置",
            "background-color:#FF1493;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        "0.382"
        in fib_status

        or

        "0.500"
        in fib_status
    ):

        set_style(
            "Fib位置",
            "background-color:#1B5E20;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        "0.618"
        in fib_status
    ):

        set_style(
            "Fib位置",
            "background-color:#F9A825;"
            "color:#111111;"
            "font-weight:900;"
        )


    elif (
        "0.786"
        in fib_status
    ):

        set_style(
            "Fib位置",
            "background-color:#EF6C00;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        "前高"
        in fib_status

        or

        "跌破"
        in fib_status
    ):

        set_style(
            "Fib位置",
            "background-color:#7F1D1D;"
            "color:white;"
            "font-weight:900;"
        )


    else:

        set_style(
            "Fib位置",
            "background-color:#2A3038;"
            "color:#E7EDF2;"
            "font-weight:800;"
        )


    # --------------------------------------------------------
    # 決策
    # --------------------------------------------------------

    decision = (
        row["決策"]
    )


    if (
        decision
        == "全導通"
    ):

        set_style(
            "決策",
            "background-color:#FF1493;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        decision
        == "全空破"
    ):

        set_style(
            "決策",
            "background-color:#7B1FA2;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        decision
        == "看多"
    ):

        set_style(
            "決策",
            "background-color:#EF3340;"
            "color:white;"
            "font-weight:900;"
        )


    elif (
        decision
        == "看空"
    ):

        set_style(
            "決策",
            "background-color:#00796B;"
            "color:white;"
            "font-weight:900;"
        )


    else:

        set_style(
            "決策",
            "background-color:#303640;"
            "color:white;"
            "font-weight:800;"
        )


    return styles


# ============================================================
# 10. DataFrame 樣式
# ============================================================

styled_df = (

    df.style

    .format(
        {

            "昨收":
                "{:.1f}",

            "開盤":
                "{:.1f}",

            "現價":
                "{:.1f}",

            "漲跌":
                "{:+.1f}",
        },

        na_rep="--"
    )

    .set_properties(
        **{

            "border-color":
                "#34414D",

            "font-size":
                "15px",

            "text-align":
                "center"
        }
    )

    .apply(
        row_styles,
        axis=1
    )

    .set_table_styles([

        {

            "selector":
                "th",

            "props": [

                (
                    "background-color",
                    "#182430"
                ),

                (
                    "color",
                    "#FFFFFF"
                ),

                (
                    "font-weight",
                    "900"
                ),

                (
                    "text-align",
                    "center"
                ),

                (
                    "font-size",
                    "15px"
                ),

                (
                    "border",
                    "1px solid #3B4B59"
                )
            ]
        },


        {

            "selector":
                "td",

            "props": [

                (
                    "border",
                    "1px solid #2E3943"
                )
            ]
        }

    ])
)


# ============================================================
# 11. 主戰情表
# ============================================================

st.subheader(
    "📋 DAVID 戰情總表"
)


table_height = (
    38
    * (
        len(df)
        + 1
    )
    + 8
)


st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True,
    height=table_height
)


# ============================================================
# 12. 戰情摘要
# 單行 HTML 防止 Markdown 顯示程式碼
# ============================================================

st.divider()

st.subheader(
    "🎯 戰情摘要"
)


full_long = sum(
    1
    for x in results
    if x["決策"]
    == "全導通"
)


long_count = sum(
    1
    for x in results
    if x["決策"]
    == "看多"
)


wait_count = sum(
    1
    for x in results
    if x["決策"]
    == "觀望"
)


short_count = sum(
    1
    for x in results
    if x["決策"]
    == "看空"
)


full_short = sum(
    1
    for x in results
    if x["決策"]
    == "全空破"
)


total = max(
    len(results),
    1
)


summary = [

    (
        "💗 全導通",
        full_long,
        "#8A1248",
        "#FF4FA3"
    ),

    (
        "🔴 看多",
        long_count,
        "#5B1015",
        "#FF3B47"
    ),

    (
        "⚪ 觀望",
        wait_count,
        "#202A34",
        "#A8B5C2"
    ),

    (
        "🟢 看空",
        short_count,
        "#063C2D",
        "#00D084"
    ),

    (
        "🟣 全空破",
        full_short,
        "#32104C",
        "#9B51E0"
    ),
]


cols = (
    st.columns(5)
)


for (
    col,
    (
        title,
        value,
        bg,
        accent
    )
) in zip(
    cols,
    summary
):


    pct = (
        value
        / total
        * 100
    )


    card_html = (

        f'<div class="summary-card" '
        f'style="background:{bg};'
        f'border-color:{accent};">'

        f'<div class="summary-title" '
        f'style="color:{accent};">'
        f'{title}'
        f'</div>'

        f'<div class="summary-value">'
        f'{value} 檔'
        f'</div>'

        f'<div class="summary-pct">'
        f'{pct:.0f}%'
        f'</div>'

        f'</div>'
    )


    with col:

        st.markdown(
            card_html,
            unsafe_allow_html=True
        )


# ============================================================
# 13. Fib 詳細區
# 下拉只顯示代碼，避免被翻譯
# ============================================================

st.divider()

st.subheader(
    "📐 個股 Fib 波段位置"
)


selected_code = st.selectbox(
    "選擇股票代碼",
    list(
        stock_list.keys()
    )
)


selected_name = (
    stock_list[
        selected_code
    ]
)


# ============================================================
# 股票名稱
# translate=no + notranslate
# ============================================================

stock_name_html = (

    f'<div '
    f'class="stock-title notranslate" '
    f'translate="no">'

    f'{selected_code} '
    f'{selected_name}'

    f'</div>'
)


st.markdown(
    stock_name_html,
    unsafe_allow_html=True
)


selected_result = next(

    (

        x

        for x
        in results

        if (
            x[
                "AI 精選族群"
            ]
            .startswith(
                selected_code
            )
        )
    ),

    None
)


# ============================================================
# 14. Fib 卡片
# translate=no 避免瀏覽器將 Fib 翻譯成其他文字
# ============================================================

def fib_card(
    column,
    label,
    value
):

    html = (

        f'<div '
        f'class="fib-card notranslate" '
        f'translate="no">'

        f'<div '
        f'class="fib-label">'
        f'{label}'
        f'</div>'

        f'<div '
        f'class="fib-value">'
        f'{value}'
        f'</div>'

        f'</div>'
    )


    with column:

        st.markdown(
            html,
            unsafe_allow_html=True
        )


# ============================================================
# 15. Fib 詳細內容
# ============================================================

if (
    selected_result
    and
    selected_result.get(
        "_fib"
    )
):

    fib = (
        selected_result[
            "_fib"
        ]
    )


    fib_status_html = (

        f'<div '
        f'class="notranslate" '
        f'translate="no" '
        f'style="'
        f'font-size:18px;'
        f'font-weight:800;'
        f'color:#FFFFFF;'
        f'margin-bottom:14px;'
        f'">'

        f'波段方向：'
        f'{fib["方向"]}'

        f'　｜　'

        f'Fib位置：'
        f'{fib["Fib位置"]}'

        f'</div>'
    )


    st.markdown(
        fib_status_html,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 第一列
    # --------------------------------------------------------

    row1 = (
        st.columns(4)
    )


    fib_card(
        row1[0],
        "Swing High",
        f"{fib['波段高']:.1f}"
    )


    fib_card(
        row1[1],
        "Swing Low",
        f"{fib['波段低']:.1f}"
    )


    fib_card(
        row1[2],
        "Fib 0.382",
        f"{fib['0.382']:.1f}"
    )


    fib_card(
        row1[3],
        "Fib 0.618",
        f"{fib['0.618']:.1f}"
    )


    # --------------------------------------------------------
    # 第二列
    # --------------------------------------------------------

    row2 = (
        st.columns(4)
    )


    fib_card(
        row2[0],
        "Fib 0.500",
        f"{fib['0.500']:.1f}"
    )


    fib_card(
        row2[1],
        "Fib 0.786",
        f"{fib['0.786']:.1f}"
    )


    fib_card(
        row2[2],
        "Extension 1.272",
        f"{fib['1.272']:.1f}"
    )


    fib_card(
        row2[3],
        "Extension 1.618",
        f"{fib['1.618']:.1f}"
    )



# ============================================================
# 16. V13：個股 20 交易日歷史戰情
# ============================================================

st.divider()
st.subheader("📈 個股 20 交易日戰情趨勢")

history_code = st.selectbox(
    "選擇要查看歷史的股票",
    [x["code"] for x in stock_rows],
    format_func=lambda c: f"{c} {next((x['name'] for x in stock_rows if x['code'] == c), '')}",
    key="history_stock_code_v13",
)

if cloud_db_enabled():
    hist_df = fetch_history_20(history_code)
    if hist_df.empty:
        st.info("目前尚無此股票的歷史紀錄。可先載入其所在頁，或按左側「保存全部100檔今日戰情」。")
    else:
        h1, h2, h3, h4 = st.columns(4)
        latest_h = hist_df.iloc[-1]
        h1.metric("已保存交易日", f"{len(hist_df)} / 20")
        h2.metric("最新收盤", "--" if pd.isna(latest_h.get("close_price")) else f"{float(latest_h['close_price']):.1f}")
        h3.metric("六買 / 六賣", f"{latest_h.get('buy_score', '--')} / {latest_h.get('sell_score', '--')}")
        h4.metric("最新決策", str(latest_h.get("decision", "--")))

        chart_df = hist_df.set_index("trade_date")[["buy_score", "sell_score"]].copy()
        st.caption("六買／六賣近20交易日變化")
        st.line_chart(chart_df)

        price_df = hist_df.set_index("trade_date")[["close_price"]].copy()
        st.caption("收盤價近20交易日變化")
        st.line_chart(price_df)

        show_cols = [
            "trade_date", "close_price", "change_pct", "volume_ratio", "bias_pct",
            "buy_score", "sell_score", "fib_position", "decision"
        ]
        hist_show = hist_df[show_cols].sort_values("trade_date", ascending=False).copy()
        hist_show.columns = ["日期", "收盤", "漲跌%", "量比", "乖離%", "六買", "六賣", "Fib位置", "決策"]
        st.dataframe(hist_show, use_container_width=True, hide_index=True)
else:
    st.warning(
        "20日歷史功能已完成，但目前尚未連接 Supabase。完成雲端資料庫設定後，"
        "手機與電腦都會共用同一份歷史資料。"
    )


# ============================================================
# 17. 頁尾
# ============================================================

st.caption(

    "V13 Cloud｜100檔智慧戰情版｜"

    "V10 六買六賣各 6 項｜"

    "MA5 趨勢｜"

    "MACD Histogram｜"

    "Pivot Swing Fibonacci｜"

    "Yahoo Finance｜"

    "快取 300 秒｜"

    "僅供戰情分析使用"
)