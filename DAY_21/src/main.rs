#![no_std]
#![no_main]

use core::panic::PanicInfo;
use cortex_m::asm;
use cortex_m_rt::entry;
use cortex_m_semihosting::{debug, hprintln};

#[entry]
fn main() -> ! {
    // Print a debug message via semihosting
    hprintln!("Starting no_std debug demo");
    // Exit with success code (stops QEMU semihost session)
    debug::exit(debug::EXIT_SUCCESS);
    loop {
        asm::wfe();
    }
}

// Required when you do not pull in panic_semihosting:
// Define a minimal panic handler that just spins
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
