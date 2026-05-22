import requests
from bs4 import BeautifulSoup
import json
import re
import hashlib
from pathlib import Path
from datetime import date, datetime

BASE_URL = "https://jett.uz"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

STOCK_META = [
    # Bank sektori
    {"key": "agrobank", "name": "Agrobank", "ticker": "AGBN", "sector": "Bank", "basePrice": 4520, "vol": 0.018, "trend": 0.0004},
    {"key": "sqb", "name": "SQB", "ticker": "SQBB", "sector": "Bank", "basePrice": 8180, "vol": 0.015, "trend": -0.0002},
    {"key": "ipak", "name": "Ipak Yo'li", "ticker": "IPYK", "sector": "Bank", "basePrice": 5140, "vol": 0.017, "trend": 0.0003},
    {"key": "aloqa", "name": "Aloqa", "ticker": "ALQA", "sector": "Bank", "basePrice": 4080, "vol": 0.016, "trend": 0.0002},
    {"key": "nbk", "name": "NBK", "ticker": "NBKK", "sector": "Bank", "basePrice": 3250, "vol": 0.019, "trend": -0.0001},
    {"key": "hmb", "name": "Hamkorbank", "ticker": "HMKB", "sector": "Bank", "basePrice": 2890, "vol": 0.020, "trend": 0.0005},
    {"key": "asaka", "name": "Asaka", "ticker": "ASKU", "sector": "Bank", "basePrice": 5670, "vol": 0.016, "trend": 0.0003},
    {"key": "xalq", "name": "Xalq banki", "ticker": "XALQ", "sector": "Bank", "basePrice": 7340, "vol": 0.014, "trend": -0.0002},
    {"key": "mikro", "name": "Mikrokreditbank", "ticker": "MIKB", "sector": "Bank", "basePrice": 2150, "vol": 0.022, "trend": 0.0004},
    {"key": "trast", "name": "Trastbank", "ticker": "TRSB", "sector": "Bank", "basePrice": 1890, "vol": 0.025, "trend": -0.0003},
    {"key": "turon", "name": "Turon bank", "ticker": "TRNB", "sector": "Bank", "basePrice": 4120, "vol": 0.017, "trend": 0.0002},
    {"key": "kapital", "name": "Kapitalbank", "ticker": "KAPB", "sector": "Bank", "basePrice": 6300, "vol": 0.015, "trend": 0.0006},
    # Sug'urta
    {"key": "kafolat", "name": "Kafolat", "ticker": "KFOT", "sector": "Sug'urta", "basePrice": 3180, "vol": 0.014, "trend": 0.0006},
    {"key": "uzagrosug", "name": "Uzagrosug'urta", "ticker": "UZAG", "sector": "Sug'urta", "basePrice": 2450, "vol": 0.018, "trend": 0.0003},
    {"key": "aloqasug", "name": "Aloqasug'urta", "ticker": "ALQS", "sector": "Sug'urta", "basePrice": 1980, "vol": 0.020, "trend": -0.0001},
    {"key": "gross", "name": "Gross sug'urta", "ticker": "GRSS", "sector": "Sug'urta", "basePrice": 1520, "vol": 0.022, "trend": 0.0005},
    # Neft va gaz
    {"key": "ung", "name": "UNG", "ticker": "UNGD", "sector": "Neft va gaz", "basePrice": 12480, "vol": 0.022, "trend": 0.0008},
    {"key": "uzneft", "name": "O'zneftmahsulot", "ticker": "UZNM", "sector": "Neft va gaz", "basePrice": 9870, "vol": 0.020, "trend": 0.0003},
    {"key": "gazprom", "name": "O'ztransgaz", "ticker": "UZTG", "sector": "Neft va gaz", "basePrice": 11230, "vol": 0.018, "trend": -0.0002},
    # Qurilish
    {"key": "qizilqum", "name": "Qizilqum sement", "ticker": "QZSM", "sector": "Qurilish", "basePrice": 9520, "vol": 0.019, "trend": 0.0005},
    {"key": "kvars", "name": "Kvars", "ticker": "KVAR", "sector": "Qurilish", "basePrice": 4230, "vol": 0.021, "trend": 0.0002},
    {"key": "uzqur", "name": "O'zqurilish", "ticker": "UZQU", "sector": "Qurilish", "basePrice": 2870, "vol": 0.024, "trend": -0.0001},
    {"key": "beton", "name": "Betonchi", "ticker": "BTNC", "sector": "Qurilish", "basePrice": 1650, "vol": 0.026, "trend": 0.0004},
    # Telekommunikatsiya va IT
    {"key": "uztelecom", "name": "O'zbektelekom", "ticker": "UZTL", "sector": "Telekommunikatsiya", "basePrice": 5680, "vol": 0.017, "trend": 0.0003},
    {"key": "beeline", "name": "Beeline O'zbekiston", "ticker": "BEEL", "sector": "Telekommunikatsiya", "basePrice": 7450, "vol": 0.016, "trend": 0.0005},
    {"key": "ucell", "name": "Ucell", "ticker": "UCELL", "sector": "Telekommunikatsiya", "basePrice": 6890, "vol": 0.018, "trend": -0.0002},
    # Energetika
    {"key": "uzbekenergo", "name": "O'zbekenergo", "ticker": "UZEN", "sector": "Energetika", "basePrice": 8230, "vol": 0.019, "trend": 0.0004},
    {"key": "issiq", "name": "Issiqlik elektr stansiyalari", "ticker": "ISSI", "sector": "Energetika", "basePrice": 6140, "vol": 0.021, "trend": -0.0001},
    {"key": "gidro", "name": "Gidroenergo", "ticker": "GIDR", "sector": "Energetika", "basePrice": 7360, "vol": 0.018, "trend": 0.0006},
    # Kimyo
    {"key": "maxam", "name": "Maxam-Chirchiq", "ticker": "MXMC", "sector": "Kimyo", "basePrice": 8910, "vol": 0.020, "trend": 0.0003},
    {"key": "azot", "name": "O'zazot", "ticker": "AZOT", "sector": "Kimyo", "basePrice": 10500, "vol": 0.022, "trend": 0.0005},
    {"key": "fargona", "name": "Farg'onaazot", "ticker": "FRAZ", "sector": "Kimyo", "basePrice": 7140, "vol": 0.019, "trend": -0.0002},
    {"key": "navoiy", "name": "Navoiyazot", "ticker": "NAVZ", "sector": "Kimyo", "basePrice": 9480, "vol": 0.017, "trend": 0.0004},
    # Metallurgiya
    {"key": "uzmet", "name": "O'zmetkombinat", "ticker": "UZMK", "sector": "Metallurgiya", "basePrice": 15600, "vol": 0.024, "trend": 0.0006},
    {"key": "olgamet", "name": "Olmaliq KM", "ticker": "OLKM", "sector": "Metallurgiya", "basePrice": 18200, "vol": 0.022, "trend": 0.0008},
    # Birja
    {"key": "uzex", "name": "UzEx", "ticker": "UZEX", "sector": "Birja", "basePrice": 2760, "vol": 0.012, "trend": -0.0001},
    # Transport va logistika
    {"key": "uty", "name": "O'zbekiston temir yo'llari", "ticker": "UTY", "sector": "Transport", "basePrice": 11500, "vol": 0.018, "trend": 0.0003},
    {"key": "havo", "name": "Uzbekistan Havo Yo'llari", "ticker": "UZHA", "sector": "Transport", "basePrice": 13800, "vol": 0.020, "trend": 0.0005},
    # Qishloq xo'jaligi
    {"key": "uzagro", "name": "O'zagrokimyo", "ticker": "UZAGK", "sector": "Qishloq xo'jaligi", "basePrice": 3520, "vol": 0.020, "trend": 0.0002},
    {"key": "paxta", "name": "Paxtasanoat", "ticker": "PAXT", "sector": "Qishloq xo'jaligi", "basePrice": 4280, "vol": 0.022, "trend": -0.0001},
    # Oziq-ovqat
    {"key": "agrofood", "name": "Agrofood", "ticker": "AGRF", "sector": "Oziq-ovqat", "basePrice": 2340, "vol": 0.024, "trend": 0.0004},
    {"key": "milk", "name": "Milk House", "ticker": "MILK", "sector": "Oziq-ovqat", "basePrice": 1780, "vol": 0.026, "trend": 0.0003},
    {"key": "non", "name": "Toshkent non kombinati", "ticker": "NONK", "sector": "Oziq-ovqat", "basePrice": 1450, "vol": 0.020, "trend": -0.0002},
    # To'qimachilik
    {"key": "tekstil", "name": "O'ztekstil", "ticker": "UZTK", "sector": "To'qimachilik", "basePrice": 3980, "vol": 0.021, "trend": 0.0003},
    {"key": "ipakchilik", "name": "Ipakchilik", "ticker": "IPAK", "sector": "To'qimachilik", "basePrice": 2210, "vol": 0.023, "trend": 0.0002},
    # Farmatsevtika
    {"key": "farm", "name": "O'zfarmatsiya", "ticker": "UZFR", "sector": "Farmatsevtika", "basePrice": 6750, "vol": 0.018, "trend": 0.0005},
    {"key": "dori", "name": "Dori-darmon", "ticker": "DORI", "sector": "Farmatsevtika", "basePrice": 5210, "vol": 0.020, "trend": 0.0003},
    # Turizm
    {"key": "turizm", "name": "O'zturizm", "ticker": "UZTR", "sector": "Turizm", "basePrice": 3120, "vol": 0.025, "trend": 0.0004},
    # Moliya
    {"key": "fin", "name": "O'zmoliyasanoat", "ticker": "UZMS", "sector": "Moliya", "basePrice": 4860, "vol": 0.017, "trend": -0.0001},
    # Investitsiya
    {"key": "invest", "name": "Invest Finance", "ticker": "INFN", "sector": "Moliya", "basePrice": 3470, "vol": 0.019, "trend": 0.0004},
    # Boshqa
    {"key": "eco", "name": "Arbitra", "ticker": "ECOU", "sector": "Texnologiya", "basePrice": 5200, "vol": 0.030, "trend": 0.0010},
]

def seeded_rand(seed, min_v=0, max_v=1):
    h = hashlib.md5(str(seed).encode()).hexdigest()
    return min_v + (int(h[:8], 16) / 0xFFFFFFFF) * (max_v - min_v)

def generate_stock_data(meta, days=260):
    price = meta["basePrice"]
    trend = 1.0
    data = []
    now = date.today()
    from datetime import timedelta
    for i in range(days, -1, -1):
        d = date(now.year, now.month, now.day) - timedelta(days=i)
        if d.weekday() >= 5:
            continue
        seed = f"{meta['key']}_{d.isoformat()}"
        r1 = seeded_rand(seed + "_r1", -1, 1)
        r2 = seeded_rand(seed + "_r2", 0, 1)
        r3 = seeded_rand(seed + "_r3", 0, 1)
        if d.weekday() == 0:
            trend += (r1) * 0.006
            trend = max(0.6, min(1.4, trend))
        daily_vol = meta["vol"] * price * (0.5 + r2 * 1.5) * trend
        drift = price * meta["trend"] * trend + r1 * daily_vol * 0.3
        open_p = price
        close = round(price + drift, 2)
        half_range = daily_vol * (0.3 + r3 * 0.7)
        high = round(max(open_p, close) + half_range * r2, 2)
        low = round(min(open_p, close) - half_range * r3, 2)
        price = close
        volume = round((50000 + r2 * 300000) * trend * (1 + abs(drift) / (meta["vol"] * price or 1)))
        data.append({
            "time": d.isoformat(),
            "open": open_p, "high": high, "low": low, "close": close,
            "volume": max(1000, volume)
        })
    return data

def generate_current_stocks():
    stocks = []
    for meta in STOCK_META:
        hist = generate_stock_data(meta)
        last = hist[-1]
        first = hist[0]
        prev = hist[-2] if len(hist) > 1 else hist[-1]
        change = round(last["close"] - first["close"], 2)
        change_pct = round((change / first["close"]) * 100, 2)
        day_change = round(last["close"] - prev["close"], 2)
        day_change_pct = round((day_change / prev["close"]) * 100, 2)
        high_1y = max(d["high"] for d in hist)
        low_1y = min(d["low"] for d in hist)
        avg_vol = round(sum(d["volume"] for d in hist[-20:]) / 20)
        stocks.append({
            "key": meta["key"],
            "name": meta["name"],
            "ticker": meta["ticker"],
            "sector": meta["sector"],
            "price": last["close"],
            "change": day_change,
            "changePercent": day_change_pct,
            "changeYear": change,
            "changeYearPercent": change_pct,
            "high": high_1y,
            "low": low_1y,
            "volume": last["volume"],
            "avgVolume": avg_vol,
            "open": last["open"],
            "prevClose": prev["close"],
            "history": hist,
        })
    return stocks

def fetch_html(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")

def extract_plans(soup):
    plans = []
    table = soup.find("table")
    if not table:
        return plans
    rows = table.find_all("tr")
    if not rows:
        return plans
    header_cells = rows[0].find_all(["td", "th"])
    plan_names = [c.get_text(strip=True) for c in header_cells[1:]]
    for name in plan_names:
        plans.append({"name": name, "commissions": {}})
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        key_raw = cells[0].get_text(strip=True)
        if not key_raw or key_raw in ("\xa0", ""):
            continue
        key = re.sub(r"[^a-zA-Zа-яА-Я0-9\s]", "", key_raw).strip().lower()
        key = re.sub(r"\s+", "_", key)[:40]
        for i, val in enumerate([c.get_text(strip=True) for c in cells[1:]]):
            if i < len(plans) and val and val != "\xa0":
                plans[i]["commissions"][key] = val
    return plans

def extract_faq(soup):
    faq = []
    for item in soup.find_all("div", class_=re.compile("faq", re.I)):
        q_el = item.find(["h3", "h4", "strong", "b", "p", "span"], class_=re.compile("question|quest|title|quest", re.I))
        a_el = item.find(["div", "p"], class_=re.compile("answer|text|content|desc", re.I))
        if not q_el:
            q_el = item.find(["h3", "h4", "strong", "b"])
        if not a_el:
            ps = item.find_all(["div", "p"])
            a_el = ps[-1] if ps else None
        q = q_el.get_text(strip=True) if q_el else ""
        a = a_el.get_text(strip=True) if a_el else ""
        if q and a:
            faq.append({"question": q, "answer": a})
    for details in soup.find_all("details"):
        summary = details.find("summary")
        if summary:
            q = summary.get_text(strip=True)
            a = details.get_text(strip=True).replace(q, "", 1).strip()
            faq.append({"question": q, "answer": a})
    return faq

def extract_site_info(soup):
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        desc = meta.get("content", "")
    return {"name": "Bozor", "description": desc, "company": "MULTIBROKER MChJ"}

def get_fallback_plans():
    return [
        {"name": "Investor", "commissions": {"listing_aksiyalar": "0.31%", "listingdan_tashqari_aksiyalar": "0.41%", "gerb_yigimi": "0.01%", "broker_listing_aksiya": "0.63%"}},
        {"name": "Treyder", "commissions": {"listing_aksiyalar": "0.31%", "listingdan_tashqari_aksiyalar": "0.41%", "gerb_yigimi": "0.01%", "broker_listing_aksiya": "1%"}},
        {"name": "Pro", "commissions": {"listing_aksiyalar": "0.31%", "listingdan_tashqari_aksiyalar": "0.41%", "gerb_yigimi": "0.01%", "broker_listing_aksiya": "1%"}},
    ]

def parse_all():
    today = str(date.today())
    result = {
        "lastUpdated": today,
        "site": {"name": "Bozor", "description": "", "company": "MULTIBROKER MChJ"},
        "companies": [{"key": s["key"], "name": s["name"], "sector": s["sector"]} for s in STOCK_META],
        "stocks": generate_current_stocks(),
        "plans": get_fallback_plans(),
        "faq": [],
    }
    try:
        soup = fetch_html(f"{BASE_URL}/ru/")
        result["site"] = extract_site_info(soup)
    except requests.RequestException:
        pass
    try:
        soup_plans = fetch_html(f"{BASE_URL}/ru/plans/")
        plans = extract_plans(soup_plans)
        if plans:
            result["plans"] = plans
    except requests.RequestException:
        pass
    try:
        soup_faq = fetch_html(f"{BASE_URL}/ru/faq/")
        faq = extract_faq(soup_faq)
        if faq:
            result["faq"] = faq
    except requests.RequestException:
        pass
    return result

def save_data(data, path="data/bozor_data.json"):
    p = Path(__file__).parent / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {p} ({len(json.dumps(data))} chars)")
    return p

if __name__ == "__main__":
    data = parse_all()
    save_data(data)
