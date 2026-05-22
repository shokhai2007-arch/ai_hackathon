import pytest
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

from main import (
    fetch_html,
    extract_plans,
    extract_faq,
    extract_site_info,
    parse_all,
    get_fallback_plans,
    save_data,
    generate_current_stocks,
    generate_stock_data,
    seeded_rand,
    STOCK_META,
    BASE_URL,
)

# ─── Sample HTML ───

SAMPLE_PLANS = """
<table>
  <tr><th>Parametr</th><th>Investor</th><th>Treyder</th><th>Pro</th></tr>
  <tr><td>Pokupka/prodazha listingovykh aktsiy</td><td>0,31%</td><td>0,31%</td><td>0,31%</td></tr>
  <tr><td>Brokerskaya (listing aktsii)</td><td>0,63%</td><td>1%</td><td>1%</td></tr>
  <tr><td>Gerbovyy sbor</td><td>0,01%</td><td>0,01%</td><td>0,01%</td></tr>
</table>
"""

SAMPLE_FAQ = """
<div class="faq-item">
  <h3 class="question">Chto takoe fondovyy rynok?</h3>
  <div class="answer">Fondovyy rynok — chast fin. rynka.</div>
</div>
<details>
  <summary>Chem otlichaetsya aktsiya?</summary>
  Aktsiya — dolya v kompanii.
</details>
"""

SAMPLE_HOME = '<html><head><meta name="description" content="Test Description"></head><body></body></html>'

# ─── Tests: seeded_rand ───

class TestSeededRand:
    def test_deterministic(self):
        assert seeded_rand("test", 0, 100) == seeded_rand("test", 0, 100)

    def test_different_seeds_different(self):
        assert seeded_rand("a", 0, 1) != seeded_rand("b", 0, 1)

    def test_within_range(self):
        for s in ["x", "y", "z"]:
            v = seeded_rand(s, 5, 10)
            assert 5 <= v <= 10


# ─── Tests: generate_stock_data ───

class TestGenerateStockData:
    def test_returns_list(self):
        data = generate_stock_data(STOCK_META[0], 10)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_entries_have_required_keys(self):
        data = generate_stock_data(STOCK_META[0], 5)
        for d in data:
            assert "time" in d
            assert "open" in d
            assert "high" in d
            assert "low" in d
            assert "close" in d
            assert "volume" in d

    def test_deterministic(self):
        a = generate_stock_data(STOCK_META[0], 10)
        b = generate_stock_data(STOCK_META[0], 10)
        assert a == b

    def test_no_weekends(self):
        data = generate_stock_data(STOCK_META[0], 30)
        for d in data:
            dt = __import__("datetime").datetime.fromisoformat(d["time"])
            assert dt.weekday() < 5

    def test_high_is_max(self):
        data = generate_stock_data(STOCK_META[0], 20)
        for d in data:
            assert d["high"] >= d["open"]
            assert d["high"] >= d["close"]
            assert d["high"] >= d["low"]

    def test_low_is_min(self):
        data = generate_stock_data(STOCK_META[0], 20)
        for d in data:
            assert d["low"] <= d["open"]
            assert d["low"] <= d["close"]
            assert d["low"] <= d["high"]


# ─── Tests: generate_current_stocks ───

class TestGenerateCurrentStocks:
    def test_returns_all_stocks(self):
        stocks = generate_current_stocks()
        assert len(stocks) >= 50

    def test_each_has_all_keys(self):
        required = ["key", "name", "ticker", "sector", "price", "change", "changePercent",
                     "changeYear", "changeYearPercent", "high", "low", "volume", "history"]
        for s in generate_current_stocks():
            for k in required:
                assert k in s, f"Missing key: {k}"

    def test_history_attached(self):
        for s in generate_current_stocks():
            assert len(s["history"]) > 0

    def test_prices_positive(self):
        for s in generate_current_stocks():
            assert s["price"] > 0
            assert s["high"] > 0
            assert s["low"] > 0


# ─── Tests: extract_plans ───

class TestExtractPlans:
    def test_extracts_three_plans(self):
        plans = extract_plans(BeautifulSoup(SAMPLE_PLANS, "html.parser"))
        assert len(plans) == 3
        assert plans[0]["name"] == "Investor"

    def test_commission_values(self):
        plans = extract_plans(BeautifulSoup(SAMPLE_PLANS, "html.parser"))
        broker = [k for k in plans[0]["commissions"] if "broker" in k.lower()][0]
        assert plans[0]["commissions"][broker] == "0,63%"

    def test_empty_html(self):
        assert extract_plans(BeautifulSoup("<html></html>", "html.parser")) == []

    def test_no_table(self):
        assert extract_plans(BeautifulSoup("<div></div>", "html.parser")) == []


# ─── Tests: extract_faq ───

class TestExtractFaq:
    def test_extracts_from_divs(self):
        faq = extract_faq(BeautifulSoup(SAMPLE_FAQ, "html.parser"))
        assert len(faq) >= 1

    def test_extracts_from_details(self):
        faq = extract_faq(BeautifulSoup(SAMPLE_FAQ, "html.parser"))
        details = [f for f in faq if "aktsiya" in f.get("question", "").lower()]
        assert len(details) >= 1

    def test_empty_html(self):
        assert extract_faq(BeautifulSoup("<html></html>", "html.parser")) == []


# ─── Tests: extract_site_info ───

class TestExtractSiteInfo:
    def test_description(self):
        info = extract_site_info(BeautifulSoup(SAMPLE_HOME, "html.parser"))
        assert info["description"] == "Test Description"

    def test_default_company(self):
        info = extract_site_info(BeautifulSoup("<html></html>", "html.parser"))
        assert info["company"] == "MULTIBROKER MChJ"


# ─── Tests: parse_all ───

class TestParseAll:
    def test_returns_expected_keys(self):
        result = parse_all()
        for k in ["lastUpdated", "site", "companies", "stocks", "plans", "faq"]:
            assert k in result

    def test_stocks_present(self):
        result = parse_all()
        assert len(result["stocks"]) >= 50

    def test_companies_present(self):
        result = parse_all()
        assert len(result["companies"]) >= 50

    def test_fallback_plans_on_network_error(self, monkeypatch):
        def fail(url):
            raise requests.ConnectionError("fail")
        import main
        monkeypatch.setattr(main, "fetch_html", fail)
        result = main.parse_all()
        assert len(result["plans"]) == 3


# ─── Tests: get_fallback_plans ───

class TestFallbackPlans:
    def test_three_plans(self):
        assert len(get_fallback_plans()) == 3

    def test_names(self):
        names = [p["name"] for p in get_fallback_plans()]
        assert "Investor" in names
        assert "Treyder" in names


# ─── Tests: save_data ───

class TestSaveData:
    def test_saves_json(self, tmp_path):
        p = save_data({"a": 1}, str(tmp_path / "out.json"))
        assert Path(p).exists()
        assert json.loads(Path(p).read_text(encoding="utf-8")) == {"a": 1}

    def test_creates_dirs(self, tmp_path):
        p = save_data({"x": "y"}, str(tmp_path / "a" / "b" / "n.json"))
        assert Path(p).exists()

    def test_utf8(self, tmp_path):
        save_data({"t": "so'm"}, str(tmp_path / "u.json"))
        assert "so'm" in Path(tmp_path / "u.json").read_text(encoding="utf-8")


# ─── Tests: fetch_html ───

class TestFetchHtml:
    def test_returns_soup(self):
        soup = fetch_html(f"{BASE_URL}/ru/")
        assert isinstance(soup, BeautifulSoup)

    def test_raises_on_bad_url(self):
        with pytest.raises(Exception):
            fetch_html("https://nonexistent.example.test")

    def test_has_title(self):
        soup = fetch_html(f"{BASE_URL}/ru/")
        assert soup.title is not None
