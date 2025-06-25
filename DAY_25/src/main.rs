#![no_std]
#![no_main]

use arduino_hal::delay::Delay;
use arduino_hal::prelude::*;
use panic_halt as _;

#[arduino_hal::entry]
fn main() -> ! {
    // 1) Grab the peripherals
    let dp = arduino_hal::Peripherals::take().unwrap();
    let mut pins = arduino_hal::pins!(dp);

    // 2) Configure digital pin 13 (PB5) as output
    let mut led = pins.d13.into_output(&mut pins.ddr);

    // 3) Set up the hardware timer–based delay
    let mut delay = Delay::new();

    // 4) Blink loop: toggle, then wait 500 ms
    loop {
        // toggle LED state
        led.toggle().void_unwrap();

        // hardware delay (Timer0)
        delay.delay_ms(500u16);
    }
}
