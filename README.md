# 60‑Day Embedded Rust & AI/ML Leapfrog Challenge

Welcome to the **ISPP60days‑Challenge** repository!  
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

```
├── DAY_01 … DAY_24       # ARM Cortex‑M embedded Rust (QEMU, PAC, HAL, RTIC, timers)
├── DAY_25 … day-30       # AVR/Arduino Uno: interrupts, keypad, servo, power‑saving
├── day_31 … day_60       # Python AI/ML journey (data prep, ML, DL, CLI/UI)
├── .gitignore            # Ignore build artifacts, venv, target directories
├── Cargo.toml            # Embedded Rust workspace settings
└── README.md             # This document
```

## 🛠️ Prerequisites

### Embedded Rust (Days 1–30)

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

### Python AI/ML (Days 31–60)

- **Python >= 3.10**
- **VS Code** with Python extension
- **Recommended**: virtual environment (venv or conda)

## 🚀 How to Run

### ARM (Days 1–24)

```bash
cd DAY_21
cargo run               # Builds & runs in QEMU

# Optional debug:
cargo run --target thumbv7m-none-eabi -- -S openocd.gdb
```

### AVR/Arduino (Days 25–30)

```bash
cargo generate --git https://github.com/Rahix/avr-hal-template.git
cd day-25
cargo run --release     # Flashes via ravedude & opens serial console
```

### Python AI/ML Phase (Days 31–60)

- **Tools**: pandas, numpy, matplotlib, scikit-learn, tensorflow or pytorch, streamlit or flask

```bash
# Manage venv:
python -m venv .venv && source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

## 📝 Daily Highlights

### Embedded Rust

- **Days 1–14**: Blinky, `#![no_std]`, panic handlers, semihosting
- **Days 15–24**: Linker scripts, PAC vs HAL, timers, RTIC, low‑power, debug/tracing
- **Days 25–27**: Arduino Uno blinky, external interrupts, PAC & RTIC
- **Days 28–30**: Timer1 PWM for servo, keypad scanning, capstone servo controller

### Python AI/ML (In Progress)

- **Day 31**: Python refresher (data types, control flow)
- **Day 32**: Comprehensions & generators
- **Day 33**: Pandas data cleaning
- **Day 34**: Exploratory Data Analysis (histograms, scatter plots)
- …through **Day 60**: ML models, deep learning, CLI & Streamlit demos

## 🔭 What’s Next?

- Implement TF‑IDF and cosine similarity
- Build scikit‑learn classifiers (regression, SVM, clustering)
- Explore CNNs for image classification
- Capstone: Music recommender with CLI & Streamlit UI
- Deploy with Docker & Streamlit Cloud

## 🤝 Contributing

- Open an issue or submit a PR for clarity, bug fixes, or new examples
- Tweet daily updates with `#LSPPDayXX` and tag [@lftechnology](https://twitter.com/lftechnology)

Happy hacking & learning! 🚀  
`#60DaysOfLearning2025 #RustEmbedded #PythonAI #LearningWithLeapfrog`
