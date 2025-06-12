# xrust_calclib

A Rust calculator library with floating-point arithmetic and error handling.

## Overview

`xrust_calclib` provides basic and advanced arithmetic operations on `f64` values, with idiomatic Rust error handling.  
It supports:

- Addition, subtraction, multiplication  
- Division and modulo with `Result`-based divide-by-zero checks  
- Exponentiation and square root (with negative-input checks)  
- Absolute value and factorial (integer-only factorial)  

---

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
xrust_calclib = "0.1.0"


# with fancy output
xrust_calclib = { version = "0.1.0", features = ["fancy"] }