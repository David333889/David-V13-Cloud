"""David 戰情室 V13 Cloud - 每日100檔歷史快照
由 GitHub Actions 於台灣收盤後執行。
"""
import os
import time
import pandas as pd
import numpy as np
import yfinance as yf
from supabase import create_client

MIN_HISTORY_ROWS = 60
STOCKS_PER_PAGE = 10
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

def _clean_history_frame(data):
    """統一整理 Yahoo 回傳的 OHLCV DataFrame。"""
    if data is None or data.empty:
        return pd.DataFrame()
    try:
        data = data.copy()
        if isinstance(data.columns, pd.MultiIndex):
            if len(data.columns.levels) >= 2:
                last_level = data.columns.get_level_values(-1)
                first_level = data.columns.get_level_values(0)
                ohlcv = {'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'}
                if any((str(x) in ohlcv for x in first_level)):
                    data.columns = [str(c[0]) for c in data.columns]
                elif any((str(x) in ohlcv for x in last_level)):
                    data.columns = [str(c[-1]) for c in data.columns]
        data = data.dropna(how='all')
        required = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all((col in data.columns for col in required)):
            return pd.DataFrame()
        data = data.dropna(subset=['Close'])
        return data
    except Exception as e:
        print(f'Yahoo 資料整理錯誤：{e}')
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
        print(f'{symbol} 批次資料拆分錯誤：{e}')
        return pd.DataFrame()

def _fetch_one_symbol(symbol):
    """個別補抓。先用 yf.download，再用 Ticker.history 做第二次救援。"""
    try:
        raw = yf.download(tickers=symbol, period='1y', interval='1d', auto_adjust=False, threads=False, progress=False, timeout=10)
        data = _clean_history_frame(raw)
        if len(data) >= MIN_HISTORY_ROWS:
            return data
    except Exception as e:
        print(f'{symbol} 單檔 download 補抓失敗：{e}')
    try:
        raw = yf.Ticker(symbol).history(period='1y', interval='1d', auto_adjust=False, timeout=10)
        data = _clean_history_frame(raw)
        if len(data) >= MIN_HISTORY_ROWS:
            return data
    except Exception as e:
        print(f'{symbol} Ticker.history 補抓失敗：{e}')
    return pd.DataFrame()

def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    return histogram

def calculate_pivot_fib(data, lookback=120, left=3, right=3):
    empty_result = {'方向': '資料不足', '波段高': np.nan, '波段低': np.nan, '0.236': np.nan, '0.382': np.nan, '0.500': np.nan, '0.618': np.nan, '0.786': np.nan, '1.272': np.nan, '1.618': np.nan, 'Fib位置': '資料不足'}
    if data is None or data.empty or len(data) < left + right + 20:
        return empty_result
    d = data.tail(lookback).copy().reset_index(drop=True)
    highs = d['High'].astype(float).to_numpy()
    lows = d['Low'].astype(float).to_numpy()
    close_now = float(d['Close'].iloc[-1])
    pivot_highs = []
    pivot_lows = []
    for i in range(left, len(d) - right):
        hi_window = highs[i - left:i + right + 1]
        lo_window = lows[i - left:i + right + 1]
        if highs[i] == np.max(hi_window):
            pivot_highs.append(i)
        if lows[i] == np.min(lo_window):
            pivot_lows.append(i)
    if not pivot_highs or not pivot_lows:
        high_idx = int(d['High'].idxmax())
        low_idx = int(d['Low'].idxmin())
    else:
        high_idx = pivot_highs[-1]
        low_idx = pivot_lows[-1]
    swing_high = float(d.loc[high_idx, 'High'])
    swing_low = float(d.loc[low_idx, 'Low'])
    wave = swing_high - swing_low
    if wave <= 0:
        result = empty_result.copy()
        result.update({'方向': '無有效波段', '波段高': swing_high, '波段低': swing_low, 'Fib位置': '無有效波段'})
        return result
    if low_idx < high_idx:
        direction = '多頭波段'
        levels = {'0.236': swing_high - wave * 0.236, '0.382': swing_high - wave * 0.382, '0.500': swing_high - wave * 0.5, '0.618': swing_high - wave * 0.618, '0.786': swing_high - wave * 0.786, '1.272': swing_high + wave * 0.272, '1.618': swing_high + wave * 0.618}
        if close_now > swing_high:
            fib_status = '突破前高'
        elif close_now >= levels['0.236']:
            fib_status = '近前高'
        elif close_now >= levels['0.382']:
            fib_status = '0.382支撐'
        elif close_now >= levels['0.500']:
            fib_status = '0.500支撐'
        elif close_now >= levels['0.618']:
            fib_status = '0.618關鍵'
        elif close_now >= levels['0.786']:
            fib_status = '0.786深回'
        else:
            fib_status = '跌破0.786'
    else:
        direction = '空頭波段'
        levels = {'0.236': swing_low + wave * 0.236, '0.382': swing_low + wave * 0.382, '0.500': swing_low + wave * 0.5, '0.618': swing_low + wave * 0.618, '0.786': swing_low + wave * 0.786, '1.272': swing_low - wave * 0.272, '1.618': swing_low - wave * 0.618}
        if close_now < swing_low:
            fib_status = '跌破前低'
        elif close_now <= levels['0.236']:
            fib_status = '近前低'
        elif close_now <= levels['0.382']:
            fib_status = '0.382壓力'
        elif close_now <= levels['0.500']:
            fib_status = '0.500壓力'
        elif close_now <= levels['0.618']:
            fib_status = '0.618壓力'
        elif close_now <= levels['0.786']:
            fib_status = '0.786壓力'
        else:
            fib_status = '逼近前高'
    return {'方向': direction, '波段高': swing_high, '波段低': swing_low, **levels, 'Fib位置': fib_status}

def analyze_stock(code, name, data, symbol):
    if data.empty or len(data) < 60:
        return {'AI 精選族群': f'{code} {name}', '昨收': np.nan, '開盤': np.nan, '現價': np.nan, '漲跌': np.nan, '幅%': '--', '量比': '--', '乖離': '--', '早盤': '--', '動能': '--', '成本': '--', '力道': '--', '六買': '--', '六賣': '--', 'Fib位置': '資料不足', '決策': '無資料', '_fib': None}
    close = data['Close'].astype(float)
    volume_series = data['Volume'].astype(float)
    latest = data.iloc[-1]
    previous = data.iloc[-2]
    p = float(latest['Close'])
    op = float(latest['Open'])
    hi = float(latest['High'])
    lo = float(latest['Low'])
    vo = float(latest['Volume'])
    pc = float(previous['Close'])
    ma20_series = close.rolling(20).mean()
    vm20_series = volume_series.rolling(20).mean()
    ma5_series = close.rolling(5).mean()
    ma20 = float(ma20_series.iloc[-1])
    vm20 = float(vm20_series.iloc[-1])
    ma5_now = float(ma5_series.iloc[-1])
    ma5_prev = float(ma5_series.iloc[-2])
    ma5_up = not np.isnan(ma5_now) and (not np.isnan(ma5_prev)) and (ma5_now > ma5_prev)
    macd_hist = calculate_macd(close)
    mh = float(macd_hist.iloc[-1])
    if np.isnan(mh):
        mh = 0.0
    diff = p - pc
    ch = (p - pc) / pc * 100 if pc > 0 else 0.0
    vr = vo / vm20 if vm20 > 0 else 1.0
    bias = (p - ma20) / ma20 * 100 if ma20 > 0 else 0.0
    mid = (hi + lo) / 2
    b1 = p > op
    b2 = p > ma20
    b3 = vo > vm20
    b4 = p > mid
    b5 = ma5_up
    b6 = mh > 0
    b_score = sum([b1, b2, b3, b4, b5, b6])
    s1 = p < op
    s2 = p < ma20
    s3 = vo > vm20 and p < pc
    s4 = p < mid
    s5 = not ma5_up
    s6 = mh <= 0
    s_score = sum([s1, s2, s3, s4, s5, s6])
    is_strong = ch >= 3.0
    if is_strong:
        morning = '強攻'
    elif b1:
        morning = '合格'
    else:
        morning = '待定'
    momentum = '放量' if vo > vm20 else '量縮'
    cost = '站穩' if p > ma20 else '破位'
    strength = '強勢' if p > mid else '弱勢'
    if b_score == 6:
        decision = '全導通'
    elif s_score == 6:
        decision = '全空破'
    elif b_score >= 4:
        decision = '看多'
    elif s_score >= 4:
        decision = '看空'
    else:
        decision = '觀望'
    fib = calculate_pivot_fib(data)
    return {'AI 精選族群': f'{code} {name}', '昨收': pc, '開盤': op, '現價': p, '漲跌': diff, '幅%': f'{ch:+.1f}%', '量比': f'{vr:.1f}x', '乖離': f'{bias:+.1f}%', '早盤': morning, '動能': momentum, '成本': cost, '力道': strength, '六買': int(b_score), '六賣': int(s_score), 'Fib位置': fib['Fib位置'], '決策': decision, '_fib': fib}


def fetch_page(rows):
    symbols = [f"{x['code']}.{x['market']}" for x in rows]
    result = {s: pd.DataFrame() for s in symbols}
    raw = pd.DataFrame()
    try:
        raw = yf.download(
            tickers=" ".join(symbols), period="1y", interval="1d",
            group_by="ticker", auto_adjust=False, threads=True,
            progress=False, timeout=15,
        )
    except Exception as e:
        print("batch error:", e)

    missing = []
    for symbol in symbols:
        data = _extract_symbol_frame(raw, symbol, len(symbols))
        if len(data) >= MIN_HISTORY_ROWS:
            result[symbol] = data.copy()
        else:
            missing.append(symbol)

    for symbol in missing:
        data = _fetch_one_symbol(symbol)
        if len(data) >= MIN_HISTORY_ROWS:
            result[symbol] = data.copy()
        else:
            print("failed:", symbol)
    return result


def to_float(value, suffix=""):
    try:
        text = str(value).replace(suffix, "").strip()
        if text in ("", "--", "nan", "None"):
            return None
        return float(text)
    except Exception:
        return None


def make_payload(item, result, data):
    if data is None or data.empty or result.get("決策") in ("無資料", "資料錯誤"):
        return None
    trade_date = pd.Timestamp(data.index[-1]).date().isoformat()
    return {
        "trade_date": trade_date,
        "code": item["code"],
        "name": item["name"],
        "market": item["market"],
        "symbol": f"{item['code']}.{item['market']}",
        "prev_close": to_float(result.get("昨收")),
        "open_price": to_float(result.get("開盤")),
        "close_price": to_float(result.get("現價")),
        "change_value": to_float(result.get("漲跌")),
        "change_pct": to_float(result.get("幅%"), "%"),
        "volume_ratio": to_float(result.get("量比"), "x"),
        "bias_pct": to_float(result.get("乖離"), "%"),
        "morning": result.get("早盤"),
        "momentum": result.get("動能"),
        "cost": result.get("成本"),
        "strength": result.get("力道"),
        "buy_score": int(result["六買"]) if str(result.get("六買", "")).isdigit() else None,
        "sell_score": int(result["六賣"]) if str(result.get("六賣", "")).isdigit() else None,
        "fib_position": result.get("Fib位置"),
        "decision": result.get("決策"),
    }


def load_stock_config(client):
    """GitHub Actions 優先使用 Supabase 的100檔設定；不足時以新版預設補足。"""
    rows = []
    try:
        resp = client.table("stock_config").select("position,code,name,market").order("position").execute()
        rows = [
            {"code": str(x["code"]), "name": str(x["name"]), "market": str(x["market"]).upper()}
            for x in (resp.data or [])
        ]
    except Exception as e:
        print("cloud stock_config read failed:", e)
    seen = {x["code"] for x in rows}
    for item in DEFAULT_STOCKS:
        if len(rows) >= 100:
            break
        if item["code"] not in seen:
            rows.append(item.copy())
            seen.add(item["code"])
    return rows[:100]


def main():
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        raise SystemExit("Missing SUPABASE_URL / SUPABASE_KEY")

    client = create_client(url, key)
    stock_rows = load_stock_config(client)
    total_payload = []
    started = time.perf_counter()

    for page in range(10):
        rows = stock_rows[page*10:(page+1)*10]
        data_map = fetch_page(rows)
        page_payload = []
        for item in rows:
            symbol = f"{item['code']}.{item['market']}"
            data = data_map.get(symbol, pd.DataFrame())
            try:
                result = analyze_stock(item["code"], item["name"], data, symbol)
                payload = make_payload(item, result, data)
                if payload:
                    page_payload.append(payload)
            except Exception as e:
                print(item["code"], "analysis error:", e)

        if page_payload:
            client.table("stock_history").upsert(
                page_payload, on_conflict="trade_date,code"
            ).execute()
            total_payload.extend(page_payload)
        print(f"page {page+1}: saved {len(page_payload)}/10")

    print(f"DONE: saved {len(total_payload)}/100 in {time.perf_counter()-started:.1f}s")
    if len(total_payload) < 90:
        raise SystemExit("Too many missing stocks; workflow marked failed for review.")


if __name__ == "__main__":
    main()
