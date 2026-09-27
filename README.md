# 🔍 CompeteLens — AI-Powered Competitor Research Assistant

**🌐 Live App:** [https://competelens-ai.streamlit.app/](https://competelens-ai.streamlit.app/)

---

## 📖 Overview

**CompeteLens** is an AI-powered web application that automates competitor and market research. Given any company or product name, it searches the public web, gathers relevant information (company overview, recent news, and online presence), and uses a Large Language Model (LLM) to generate a clean, structured, professional **Competitor Research Brief** — complete with source citations.

This tool is built to solve a real, time-consuming problem faced by marketing and business teams: **manual competitor research**, which normally takes hours, is reduced here to a matter of minutes.

---

## ✨ Key Features

- 🔎 **Automated Web Research** — Searches the live web for any company/product using the Serper.dev (Google Search) API.
- 🤖 **AI-Generated Brief** — Uses Groq's LLM (`openai/gpt-oss-120b`) to synthesize raw search data into a structured, professional report.
- 🌐 **Multilingual Support** — Automatically detects and responds in **English**, **Urdu**, or **Roman Urdu** based on user input, or lets the user manually select a language.
- 📑 **Source-Cited Results** — Every brief is backed by real, clickable source links — no hallucinated data.
- 💹 **Live Market Ticker (Value-Added Feature)** — A real-time cryptocurrency ticker displaying **BTC, ETH, SOL prices**, and **BTC Dominance (BTC.D)**, powered by the CoinMarketCap API. Prices auto-refresh every 60 seconds with a live visual countdown timer — giving the dashboard a professional, market-intelligence feel relevant to business/finance research contexts.
- 🎨 **Modern, Professional UI** — A custom-designed, tech-themed dark interface built entirely with Streamlit, styled for a polished, production-ready look.
- 🆓 **100% Free & Open Stack** — No paid APIs, no credit card requirements. Built entirely on free-tier services.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.13 |
| **Frontend / App Framework** | Streamlit |
| **Web Search** | Serper.dev API (Google Search results) |
| **AI / LLM Summarization** | Groq API (`openai/gpt-oss-120b`) |
| **Live Crypto Data** | CoinMarketCap API |
| **Web Scraping** | BeautifulSoup4, Requests |
| **Auto-Refresh Component** | streamlit-autorefresh |
| **Environment Management** | python-dotenv |
| **Deployment** | Streamlit Community Cloud |

---

## 🧠 How It Works

User Input (Company/Product Name)
│
▼
Serper.dev Search API ──► Retrieves top web results (news, overview, links)
│
▼
Groq LLM (gpt-oss-120b) ──► Synthesizes results into a structured brief
│
▼
Streamlit UI ──► Displays brief + sources + live crypto ticker

---

## 📂 Project Structure
competelens-ai/
│
├── app.py # Main Streamlit application (UI + logic)
├── search.py # Web search & scraping functions (Serper API)
├── llm.py # AI brief generation logic (Groq API)
├── crypto.py # Live crypto ticker data (CoinMarketCap API)
├── requirements.txt # Python dependencies
├── .gitignore # Excludes .env, venv, and cache files
└── README.md # Project documentation

---

## ⚙️ Setup & Installation (Run Locally)

1. **Clone the repository**
```bash
   git clone https://github.com/ttajirs-nom/competelens-ai.git
   cd competelens-ai
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   
5. **Run the app**
```bash
   streamlit run app.py

---

## 🎯 Use Case & Value Proposition

Marketing and business teams routinely spend hours manually researching competitors — checking company websites, searching for recent news, and compiling findings into a report. **CompeteLens automates this entire workflow**, turning a multi-hour manual task into a **30-second automated process**, while keeping every claim grounded in real, cited web sources (no AI hallucination).

The added **live market ticker** (BTC/ETH/SOL/BTC.D) reflects the tool's positioning as a lightweight **business & market intelligence dashboard** — not just a research tool, but a glanceable snapshot of both competitor landscape and market conditions in one place.

---

## 🔒 Notes on Data & Limitations

- All information is sourced live from public web search results — no scraping of private or authenticated data.
- API keys are securely managed via environment variables / Streamlit Secrets and are never exposed in the codebase.
- Search result quality depends on public data availability; the system includes graceful error handling for cases with limited information.

---

## 📌 Status

✅ Fully functional and deployed — [Live Demo](https://competelens-ai.streamlit.app/)

---

## 👤 Noman

Developed as a final project submission — showcasing practical application of Generative AI (RAG-style summarization), API integration, and full-stack deployment using a completely free technology stack.