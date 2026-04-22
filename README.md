# Job Intelligence Engine

## Overview
A lightweight job intelligence engine built with Playwright for scraping structured job listings and visualizing them through a simple Streamlit dashboard.

The project focuses on building a clean, scalable data pipeline for job collection as the foundation for future AI-powered job analysis and automation systems.

---

## Features
- Web scraping with Playwright
- Structured job data extraction
- Modular scraper architecture
- CSV-based storage system
- Simple Streamlit dashboard for visualization

---

## Tech Stack
- Python
- Playwright
- Streamlit
- Pandas (optional)

---

## Architecture

Scraper → Parser → Job Model → CSV Storage → Dashboard

---

## Project Structure
- scraper/: data collection layer
- models/: data schema
- storage/: persistence layer
- dashboard/: UI layer
- data/: output files

---

## Roadmap

### Phase 1 (Current)
- [x] Basic Playwright scraper
- [x] CSV output
- [x] Simple dashboard

### Phase 2
- Multi-source scraping
- Data cleaning & normalization
- Deduplication

### Phase 3
- AI-based job classification
- Skill extraction
- Job scoring system

### Phase 4
- Full job intelligence platform
- API + SaaS features

---

## Purpose
This project is part of a larger AI Job Intelligence system aimed at building automation, job analytics, and intelligent job matching tools.