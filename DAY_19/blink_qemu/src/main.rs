#![no_main]
#![no_std]

use cortex_m_rt::entry;
use cortex_m_semihosting::{debug, hprintln};
use panic_halt as _;

#[entry]
fn main() -> ! {
    hprintln!("Day 20: Simulated input & output via QEMU").ok();

    // Simulate 5 LED blinks
    for i in 1..=5 {
        hprintln!("Blink {}", i).ok();
        // simulate delay
        for _ in 0..1_000_000 {
            cortex_m::asm::nop();
        }
    }

    hprintln!("Done blinking. Halting now.").ok();
    debug::exit(debug::EXIT_SUCCESS); // Exit QEMU cleanly

    loop {}
}
