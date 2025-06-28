#![no_std]
#![no_main]
#![feature(abi_avr_interrupt)]
#![warn(
    unused_imports,
    unused_mut,
    static_mut_refs,
    unused_unsafe,
    unused_variables
)]

use arduino_hal::hal::port::PB1;
use arduino_hal::port::mode::Output;
use arduino_hal::{delay_ms, entry, pac};
use panic_halt as _;

// (Optional) stash the servo pin for an ISR if needed later
static mut SERVO: Option<arduino_hal::port::Pin<Output, PB1>> = None;

#[entry]
fn main() -> ! {
    // 1) Acquire peripherals and split pins
    let dp = pac::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);

    // 2) Configure D9/PB1 as output and stash it
    let pwm_pin = pins.d9.into_output();
    unsafe { SERVO = Some(pwm_pin) };

    // 3) Configure Timer1 for Fast‑PWM mode 14, OC1A non‑inverting, prescaler=8
    //    (WGM13:0 = 0b1110 → wgm11:10 = 0b10 in TCCR1A, wgm13:12 = 0b11 in TCCR1B)

    // TCCR1A: COM1A1:0 = 0b10 (non‑inverting), WGM11:10 = 0b10
    dp.TC1.tccr1a.write(|w| {
        w.com1a()
            .bits(0b10) // COM1A1=1, COM1A0=0
            .wgm1()
            .bits(0b10) // WGM11:10 = 10
    });

    // TCCR1B: WGM13:12 = 0b11, CS12:0 = 0b010 (clk/8)
    dp.TC1.tccr1b.write(|w| {
        w.wgm1()
            .bits(0b11) // WGM13=1, WGM12=1
            .cs1()
            .prescale_8() // prescaler = 8
    });
    dp.TC1.icr1.write(|w| w.bits(40_000));

    loop {
        for angle in (0..=180).step_by(5) {
            let duty = 2_000 + (angle as u32 * 2_000) / 180;
            dp.TC1.ocr1a.write(|w| w.bits(duty as u16));
            delay_ms(50u32);
        }
        for angle in (0..=180).rev().step_by(5) {
            let duty = 2_000 + (angle as u32 * 2_000) / 180;
            dp.TC1.ocr1a.write(|w| w.bits(duty as u16));
            delay_ms(50u32);
        }
    }
}
