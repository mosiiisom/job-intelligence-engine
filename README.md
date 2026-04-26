# 🚀 Job Intelligence Engine

A lightweight job intelligence system that automatically collects, stores, and analyzes remote job postings using an automated data pipeline, structured database, and interactive dashboard.

---

## 🧠 Overview

This project started as a simple idea to avoid manually searching for remote jobs every day.

It gradually evolved into a small data pipeline system that:

- collects job postings automatically
- stores structured data in a database
- provides a query & filtering layer
- visualizes everything in a dashboard

---

## 🏗 Architecture

GitHub Actions (scheduled every hour)
↓
Playwright Scraper
↓
SQLite Database
↓
Query & Filter Layer
↓
Streamlit Dashboard

---

## ⚙️ Features

- 🔄 Automated scraping via GitHub Actions (hourly runs)
- 🗄 SQLite-based structured storage (migrated from CSV)
- 🔍 Keyword search across job listings
- 🧠 Flexible query and filtering system
- 🏷 Tag-based filtering support
- 📊 Interactive Streamlit dashboard
- 🎨 Card-based UI with responsive layout
- 🧩 Modular architecture (scraper / storage / UI separation)

---
## 📊 What It Does

1. GitHub Actions triggers the scraper automatically
2. Playwright collects job postings from remote job boards
3. Data is stored in a structured SQLite database
4. Query layer handles filtering and search operations
5. Streamlit dashboard visualizes results in real time UI
---

## 🧰 Tech Stack

- Python
- Playwright
- Streamlit
- SQLite
- Pandas
- GitHub Actions

---

## 🚀 Installation
```bash
git clone https://github.com/mosiiisom/job-intelligence-engine
cd job-intelligence-engine

pip install -r requirements.txt
playwright install chromium
```
---

## ▶️ Run
```bash
python main.py
streamlit run dashboard/app.py
```

---

## 📡 Updates

Job data is automatically updated every 1 hour using GitHub Actions.

No manual execution required for data collection.

---

## 🧠 Roadmap

- AI job ranking system
- CV matching engine
- semantic search
- multi-source scraping
- notifications system

---

## 🤝 Contributing

This is an early-stage system project.
Contributions, ideas, and improvements are welcome.

---
## 📄 License

MIT License

---

## 🔗 Live Demo

https://job-intelligence.streamlit.app/