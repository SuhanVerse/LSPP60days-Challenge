**60‑Day Embedded Rust & AI/ML Leapfrog Challenge**

Welcome to the ISPP60days-Challenge repository! Over the first 30 days, we explored embedded Rust on ARM Cortex‑M and AVR (Arduino Uno) platforms. For the next 30 days, we’ll dive into Python for AI and deep learning.

---

## 📁 Repository Structure

```
├── DAY_1 ... DAY_24       # ARM Cortex‑M embedded Rust exercises (blinky, no_std, PAC, HAL, RTIC, low‑power, debug)
├── DAY_25 ... day-30      # AVR/Arduino Uno Rust exercises (timers, interrupts, PWM, keypad, servo, sensor)
├── day-31 ... day-60      # Upcoming Python AI/ML exercises (to be created)
├── .gitignore             # ignore target/, artifacts
├── .gitattributes         # hide vendored files from GitHub stats
├── Cargo.toml             # workspace / template settings
└── README.md              # this document
```

## 🛠️ Prerequisites

* **Rust toolchain** (1.87+): `rustup component add rustfmt clippy`
* **ARM targets**: `rustup target add thumbv7m-none-eabi thumbv7em-none-eabihf`
* **QEMU**: for Cortex‑M emulation
* **probe‑rs** or **OpenOCD/GDB**: for on‑chip debugging
* **AVR toolchain**: nightly Rust + `cargo install ravedude cargo-generate`
* **Hardware**: STM32/NXP dev board (or QEMU) & Arduino Uno + keypad + servo + jumper wires

---

## 🚀 How to Run the Embedded Rust Days

### ARM (Days 1–24)

1. Clone & enter a day:  `cd DAY_21`
2. Build for QEMU:      `cargo build --release`
3. Run in QEMU:        `cargo run`
4. (Optional) Debug:    `cargo run --target thumbv7m-none-eabi -- -S openocd.gdb`

### AVR/Arduino (Days 25–30)

1. Generate new AVR project:

   ```bash
   cargo generate --git https://github.com/Rahix/avr-hal-template.git
   ```
2. Enter directory (e.g. `cd day-25`) and build:

   ```bash
   cargo build --release
   ```
3. Flash via ravedude & open serial console:

   ```bash
   cargo run --release
   ```

---

## 📝 Daily Highlights

* **Day 21–24**: `#![no_std]`, custom linker scripts, PAC vs HAL, timers, interrupts, RTIC, low‑power, semihosting & RTT logging
* **Day 25**: Arduino Uno Rust blinky using `avr-hal-template` & `ravedude`
* **Day 26**: External interrupts theory & practice on ATmega328P
* **Day 27**: PAC (`avr-device`) & embedded-hal traits, peripheral register access, RTIC on Arduino
* **Day 28**: Hardware PWM (Timer1) for servo control on D9
* **Day 29**: Keypad scanning + sleep/wake on `#` + heartbeat LED
* **Day 30**: Capstone: keypad‑driven servo control (0–180°) with timer/interrupt, serial feedback

---

## 🔭 What’s Next?

**Python AI/Deep Learning (Days 31–60)**
We’ll build on this embedded foundation by exploring:

* Data science fundamentals (NumPy, pandas, Matplotlib)
* Machine learning with scikit‑learn
* Deep learning with TensorFlow or PyTorch
* Simple robotics & control simulations in Python

Look for the new `day-31` directory in the coming days!

---

## 🤝 Contributing

* Feel free to open issues or PRs for clarity, bug fixes, or new examples.
* Tag your daily work with `#LSPPDayXX` on Twitter and link back here.

---

Happy hacking & learning! 🚀 #60DaysOfLearning2025
