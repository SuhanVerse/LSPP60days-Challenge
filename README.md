# 🚀 60‑Day Embedded Rust & AI/ML Leapfrog Challenge

Welcome to the **LSPP60days‑Challenge_2025** repository!  
This is a 60‑day technical journey exploring two key domains:

- **Days 1–30**: Embedded Rust on ARM Cortex‑M and AVR (Arduino Uno)  
- **Days 31–60**: Python‑based AI, Machine Learning, and Deep Learning

---

[![Crates.io](https://img.shields.io/crates/v/xrust_calclib.svg)](https://crates.io/crates/xrust_calclib)  
**xrust_calclib** — A simple Rust calculator library with add, sub, mul, div, and error handling

```bash
cargo add xrust_calclib
```

## 📁 Repository Structure

```text
├── DAY_01 … DAY_24       # ARM Cortex‑M embedded Rust (QEMU, PAC, HAL, RTIC, timers)
├── DAY_25 … day-30       # AVR/Arduino Uno: interrupts, keypad, servo, power‑saving
├── day_31 … day_60       # Python AI/ML journey (data prep, ML, DL, CLI/UI)
├── .gitignore            # Ignore build artifacts, venv, target directories
├── Cargo.toml            # Embedded Rust workspace settings
└── README.md             # This document
```

---

## 🛠️ Prerequisites

### Embedded Rust Recap (Days 1–30)

- **Rust toolchain 1.87+**:

  ```bash
  rustup component add rustfmt clippy
  rustup target add thumbv7m-none-eabi thumbv7em-none-eabihf
  ```

- **QEMU** for Cortex‑M emulation
- **On‑chip debugging**: probe‑rs, OpenOCD, or GDB

- **AVR support (Arduino Uno)**:

  ```bash
  rustup override set nightly
  cargo install ravedude cargo-generate
  ```

---

### Python AI/ML & Deployment (Days 31–60)

- **Python 3.10+** (preferably in a virtual environment or Conda)
- **Docker & Docker Compose**
- **VS Code** or your preferred IDE

---

## 🚀 Getting Started

### Embedded Rust

#### Example: Day 21 – Blink in QEMU

```bash
cd day_21
cargo run
```

**For AVR/Arduino (Days 25–30):**

```bash
# Generate template & flash
cargo generate --git https://github.com/Rahix/avr-hal-template.git
cd day-20
cargo run --release
```

---

### Python AI/ML Phase

```bash
# Create & activate virtualenv
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run a daily script or notebook
python day-34/eda.py
```

---

### Dockerized FastAPI (Day 60)

```bash
# Build & run the container
docker build -t lsp60-recommender:day60 -f day-60/Dockerfile .
docker run -d -p 8000:8000 --name lsp60-api lsp60-recommender:day60

# Health check
curl http://localhost:8000/health
```

---

## 🐳 Deployment

- **Deploy with Docker & Streamlit Cloud** for easy sharing and production use.

### 🐋 Docker Hub Images

- **Recommender API:** [`xenon6230/recommender-api`](https://hub.docker.com/r/xenon6230/recommender-api)
- **Sentiment Recommender:** [`xenon6230/sentiment-recommender`](https://hub.docker.com/r/xenon6230/sentiment-recommender)

---

## 📝 Daily Highlights

### Embedded Rust (Days 1–30)

- **Days 1–5**: Python refresher, control flow
- **Days 6–14**: Cortex‑M `#![no_std]`, panic handlers, semihosting
- **Days 15–24**: Linker scripts, PAC vs HAL, low‑power modes, tracing
- **Days 25–27**: AVR external interrupts, keypad scanning, servo PWM
- **Days 28–30**: Capstone – power‑optimized servo controller

---

### Python AI/ML & APIs (Days 31–60)

- **Days 31–40**: Data cleaning, EDA, baseline ML, regression & classification
- **Days 41–44**: TF‑IDF, sentiment analysis, content‑based recommender, evaluation
- **Days 45–54**: Deep learning (MLP, CNN, text CNN), collaborative filtering (SVD, kNN)
- **Days 55–58**: Hybrid recommender, NCF ranking & evaluation, BPR implementation
- **Day 59**: FastAPI service to serve multiple recommenders
- **Day 60**: Dockerize the API for production‑ready deployment

---

## 🚩 Next Milestones

- Pin exact dependency versions (`pip freeze`) for reproducibility
- CI/CD pipeline: automated Docker builds & tests
- Deploy to cloud (e.g., AWS ECS, DigitalOcean App Platform)
- Add unit & integration tests for each recommender endpoint

---

## 🤝 Contributing

- Tweet daily updates with `#LSPPDayXX` and tag [@lftechnology](https://twitter.com/lftechnology)

---

Happy hacking & learning! 🚀  
`#60DaysOfLearning2025 #RustEmbedded #PythonAI #LearningWithLeapfrog`
