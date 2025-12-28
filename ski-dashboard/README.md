# Ski Lift & Slope Status Dashboard

A Python-based scraping and monitoring system that collects ski lift and slope opening statuses from local ski resort websites (Vaud & Valais, Switzerland) and visualizes them using Grafana.

The system is designed for **low-frequency scraping (2–3× per day)**, high reliability, and visually rich dashboards with dark themes, gauges, and status indicators.

---

## 🏗️ Architecture Overview

Ski Resort Websites
↓
Python Selenium Scrapers
↓
Orchestrator / Scheduler
↓
PostgreSQL Database
↓
Grafana Dashboards


---

## 🧱 Components

### 1️⃣ Scraper Layer (Python + Selenium)
- One scraper module per resort
- Handles JavaScript-heavy pages
- Normalizes lift and slope statuses
- Outputs structured data only (no DB logic)

**Responsibilities**
- Open resort status pages
- Parse lift and slope data
- Normalize names and statuses
- Return clean Python dictionaries

---

### 2️⃣ Orchestrator / Scheduler
- Controls when scraping runs
- Executes all enabled resort scrapers
- Handles retries, logging, and validation
- Writes results to the database

**Scheduling**
- 2–3 runs per day
- Implemented using:
  - Cron (recommended)
  - or APScheduler (optional)

---

### 3️⃣ Database (PostgreSQL)
Stores current and historical lift/slope statuses.

**Core Tables**
- `resorts`
- `lifts`
- `slopes`
- `statuses`

Supports:
- Historical tracking
- Grafana SQL queries
- Future expansion (snow depth, weather, alerts)

---

### 4️⃣ Grafana
- Read-only visualization layer
- Auto-refresh every 5–15 minutes
- Dark theme by default

**Panels**
- Status cards (open / closed)
- Gauges (% lifts open)
- Tables (per-resort breakdowns)

---

### 5️⃣ Optional API Layer (Future)
FastAPI service for:
- External access
- Mobile apps
- Public endpoints

Grafana connects directly to the database (API not required initially).

---

## 🗂️ Project Structure



ski-dashboard/
├── scraper/
│ ├── base/
│ │ ├── selenium_driver.py
│ │ ├── scraper_base.py
│ │ └── utils.py
│ ├── resorts/
│ │ ├── verbier.py
│ │ ├── villars.py
│ │ ├── leyson.py
│ │ └── crans_montana.py
│ └── run_scraper.py
│
├── orchestrator/
│ ├── scheduler.py
│ └── tasks.py
│
├── db/
│ ├── schema.sql
│ └── migrations/
│
├── grafana/
│ ├── dashboards/
│ └── provisioning/
│
├── docker/
│ ├── docker-compose.yml
│ ├── grafana/
│ └── postgres/
│
├── logs/
├── config/
│ └── settings.yaml
│
├── .env
├── README.md
└── requirements.txt


---

## 🔄 Data Flow

1. Scheduler triggers scraper
2. Selenium scrapes resort websites
3. Data is normalized and validated
4. Database is updated (UPSERT)
5. Grafana queries database
6. Dashboards refresh automatically

---

## 🐳 Deployment

- All services run via Docker
- Easy local development and cloud deployment
- Reproducible environment

---

## ⚠️ Notes & Best Practices

- Respect resort website terms of service
- Use reasonable delays and caching
- Log all scrape attempts
- Detect DOM changes and fail gracefully

---

## 🚀 Next Steps

- Implement base Selenium scraper
- Create database schema
- Configure Grafana data source
- Design first dashboard
