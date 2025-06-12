# calclib_rustx

A Rust calculator library with floating-point arithmetic and error handling.

[![crates.io](https://img.shields.io/crates/v/calclib_rustx.svg)](https://crates.io/crates/calclib_rustx)
[![docs.rs](https://docs.rs/calclib_rustx/badge.svg)](https://docs.rs/calclib_rustx)
[![license](https://img.shields.io/crates/l/calclib_rustx.svg)](LICENSE-APACHE)

## Overview

`calclib_rustx` provides basic and advanced arithmetic operations on `f64` values, with idiomatic Rust error handling.  
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
calclib_rustx = "0.1.0"


# with fancy output
calclib = { version = "0.1.1", features = ["fancy"] }