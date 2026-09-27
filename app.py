import streamlit as st
import streamlit.components.v1 as components
import time
from streamlit_autorefresh import st_autorefresh
from search import search_company
from llm import generate_brief
from crypto import get_crypto_prices

st.set_page_config(page_title="CompeteLens", page_icon="🔍", layout="centered")

# ---------- Custom Professional Styling (Tech Theme) ----------
st.markdown("""
    <style>
        .stApp {
            background-color: #0a0f1e;
            background-image: radial-gradient(rgba(56, 189, 248, 0.25) 1.2px, transparent 1.2px);
            background-size: 26px 26px;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { padding-top: 2rem; }

        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            text-align: center;
            color: #38bdf8;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
            margin-bottom: 0.1rem;
            font-family: 'Courier New', monospace;
            letter-spacing: 1px;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
            font-family: 'Courier New', monospace;
        }

        .crypto-bar {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 0.5rem;
        }
        .crypto-card {
            background-color: #111827;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 0.7rem 1.2rem;
            text-align: center;
            min-width: 100px;
        }
        .crypto-symbol {
            color: #38bdf8;
            font-weight: 700;
            font-size: 0.95rem;
            font-family: 'Courier New', monospace;
        }
        .crypto-price {
            color: #f1f5f9;
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 4px;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(17, 24, 39, 0.92);
            border: 1px solid #1e293b !important;
            border-radius: 16px !important;
            padding: 1.5rem;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.08);
        }
        .stTextInput > div > div > input {
            background-color: #0f172a;
            color: #f8fafc;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 0.7rem;
            font-size: 1rem;
        }
        .stTextInput label, .stSelectbox label {
            color: #e2e8f0 !important;
            font-weight: 600;
            font-size: 1rem;
        }
        .stButton > button {
            background: linear-gradient(90deg, #0ea5e9, #6366f1);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.5rem;
            font-weight: 700;
            width: 100%;
            font-size: 1rem;
            margin-top: 0.5rem;
        }
        .stButton > button:hover { opacity: 0.88; }

        .result-box {
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.2rem;
            margin-top: 1.2rem;
            color: #f1f5f9;
            font-size: 1rem;
            line-height: 1.6;
        }
        .brief-box {
            background-color: #0f172a;
            border: 1px solid #38bdf8;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1.2rem;
            color: #f1f5f9;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="main-title">🔍 CompeteLens</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Competitor Research Assistant</div>', unsafe_allow_html=True)

# ---------- Crypto Ticker (Auto-refresh every 60 sec) ----------
st_autorefresh(interval=60000, key="crypto_refresh")

prices = get_crypto_prices()

if prices:
    cards_html = '<div class="crypto-bar">'
    for coin in prices:
        if coin.get("is_percent"):
            display_value = f"{coin['price']:.2f}%"
        else:
            display_value = f"${coin['price']:,.2f}"
        cards_html += f'''
        <div class="crypto-card">
            <div class="crypto-symbol">{coin["symbol"]}</div>
            <div class="crypto-price">{display_value}</div>
        </div>'''
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align:center;color:#64748b;">Crypto prices load nahi ho sake.</div>', unsafe_allow_html=True)

# ---------- Live Ticking Countdown (JavaScript, har second update) ----------
unique_id = str(time.time()).replace(".", "")

components.html(
    f"""
    <div style="text-align:center; font-family:'Courier New', monospace; color:#64748b; font-size:0.85rem; margin-bottom:1.2rem;">
        ⏱ Next price update in: <span id="countdown_{unique_id}" style="color:#38bdf8; font-weight:700;">60</span>s
    </div>
    <script>
        (function() {{
            let seconds = 60;
            const el = document.getElementById("countdown_{unique_id}");
            const timer = setInterval(function() {{
                seconds -= 1;
                if (seconds <= 0) {{
                    clearInterval(timer);
                    if (el) el.innerHTML = "0";
                }} else {{
                    if (el) el.innerHTML = seconds;
                }}
            }}, 1000);
        }})();
    </script>
    """,
    height=40,
)

# ---------- Session state initialize karein ----------
if "results" not in st.session_state:
    st.session_state.results = None
if "brief" not in st.session_state:
    st.session_state.brief = None
if "error" not in st.session_state:
    st.session_state.error = None
if "llm_error" not in st.session_state:
    st.session_state.llm_error = None

# ---------- Input Card ----------
with st.container(border=True):
    company_name = st.text_input("Company ya Product ka naam likhein:", placeholder="e.g. Daraz, Foodpanda")

    language = st.selectbox(
        "Jawab kis zabaan me chahiye?",
        ["Auto", "English", "Roman Urdu", "Urdu"]
    )

    generate = st.button("🔎 Research Karein")

    if generate:
        if company_name.strip() == "":
            st.warning("Pehle koi naam likhein.")
        else:
            with st.spinner("Web se information dhoondi ja rahi hai..."):
                results, error = search_company(company_name)

            st.session_state.results = results
            st.session_state.error = error

            if results:
                with st.spinner("AI brief tayyar kar raha hai..."):
                    brief, llm_error = generate_brief(company_name, results, language)
                st.session_state.brief = brief
                st.session_state.llm_error = llm_error
            else:
                st.session_state.brief = None

    # ---------- Saved results dikhayein (session state se) ----------
    if st.session_state.results:
        if st.session_state.llm_error:
            st.error(f"AI summary banane me masla hua: {st.session_state.llm_error}")
        elif st.session_state.brief:
            st.markdown(f'<div class="brief-box">{st.session_state.brief}</div>', unsafe_allow_html=True)

        with st.expander("🔗 Raw Search Sources dekhein"):
            for r in st.session_state.results:
                st.markdown(
                    f'<div class="result-box"><b>{r["title"]}</b><br>'
                    f'<a href="{r["href"]}" target="_blank" style="color:#38bdf8;">{r["href"]}</a><br><br>'
                    f'{r["body"]}</div>',
                    unsafe_allow_html=True
                )
    elif st.session_state.error:
        st.error(f"Koi results nahi mile. Wajah: {st.session_state.error}")