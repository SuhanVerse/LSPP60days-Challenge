// #![no_std]
// #![no_main]

// use arduino_hal::delay::Delay;
// use arduino_hal::port::mode::Output;
// use arduino_hal::{entry, interrupt, pac, prelude::*};
// use panic_halt as _;

// // Shared LED pin for ISR; actual type is inferred from pins.d13
// static mut LED: Option<arduino_hal::Pin<Output, _>> = None;

// #[entry]
// fn main() -> ! {
//     // 1) Grab the device peripherals
//     let dp = pac::Peripherals::take().unwrap();
//     // 2) Split PORTx registers into usable pins
//     let mut pins = arduino_hal::pins!(dp);

//     // 3) Configure D13 (PB5) as push-pull output
//     let led = pins.d13.into_output();
//     unsafe { LED = Some(led) };

//     // 4) Configure D2 (PD2/INT0) as input with pull-up
//     let _button = pins.d2.into_pull_up_input();

//     // 5) Set up the external interrupt on INT0 (PD2) for falling edge
//     dp.EXINT.eicra.modify(|_, w| w.isc0().bits(0b10)); // ISC01=1, ISC00=0
//     dp.EXINT.eimsk.modify(|_, w| w.int0().set_bit()); // enable INT0

//     // 6) Globally enable interrupts
//     unsafe { interrupt::enable() };

//     // 7) Main loop can sleep or do other work
//     let mut delay = Delay::new();
//     loop {
//         delay.delay_ms(1000u16);
//     }
// }

// /// Interrupt Service Routine for External Interrupt 0 (INT0)
// #[interrupt]
// fn INT0() {
//     unsafe {
//         if let Some(led) = LED.as_mut() {
//             led.toggle().void_unwrap();
//         }
//     }
// }

//----------------------------------------------------------------------------------

// #![no_std]
// #![no_main]

// use arduino_hal::port::mode::Output;
// use arduino_hal::port::portb::PB5;
// use avr_device::interrupt;
// use panic_halt as _;

// // Type alias for the LED pin
// type LedPin = arduino_hal::port::Pin<Output, PB5>;

// // Make LED accessible to ISR
// static mut LED: Option<LedPin> = None;

// #[arduino_hal::entry]
// fn main() -> ! {
//     // 1) Acquire peripherals
//     let dp = arduino_hal::Peripherals::take().unwrap();
//     let mut pins = arduino_hal::pins!(dp);

//     // 2) Configure D13 (PB5) as output and store in static
//     let led = pins.d13.into_output();
//     unsafe { LED = Some(led) };

//     // 3) Configure D2 (PD2/INT0) as input with pull-up
//     let _button = pins.d2.into_pull_up_input();

//     // 4) Set up INT0 on falling edge
//     let exti = dp.EXINT;
//     // ISC01=1, ISC00=0 => falling edge on INT0
//     exti.eicra.write(|w| w.isc0().bits(true).isc1().bits(false));
//     // Enable INT0
//     exti.eimsk.write(|w| w.int0().set_bit());

//     // 5) Enable global interrupts
//     unsafe { interrupt::enable() };

//     // 6) Sleep loop (or do other work)
//     loop {
//         arduino_hal::delay_ms(1000);
//     }
// }

// /// External Interrupt Request 0
// #[interrupt]
// fn INT0() {
//     // Toggle the LED
//     unsafe {
//         if let Some(led) = LED.as_mut() {
//             led.toggle().void_unwrap();
//         }
//     }
// }

//----------------------------------------------------------------------------------

#![no_std]
#![no_main]
#![feature(abi_avr_interrupt)]
use arduino_hal::hal::port::PB5;
#[warn(unused_imports)]
#[warn(unused_mut)]
#[warn(static_mut_refs)]
use arduino_hal::port::mode::Output;
use arduino_hal::{entry, pac};
use panic_halt as _;
static mut LED: Option<arduino_hal::port::Pin<Output, PB5>> = None;

#[entry]
fn main() -> ! {

    let dp = pac::Peripherals::take().unwrap();
    let  pins = arduino_hal::pins!(dp);
    let led = pins.d13.into_output();
    unsafe { LED = Some(led) };
    let _button = pins.d2.into_pull_up_input();
    dp.EXINT.eicra.modify(|_, w| w.isc0().bits(0b10));
    dp.EXINT.eimsk.modify(|_, w| w.int0().set_bit());

    unsafe { avr_device::interrupt::enable() };
    loop {
        arduino_hal::delay_ms(1000);
    }
}
#[avr_device::interrupt(atmega328p)]
fn INT0() {
    unsafe {
        if let Some(led) = LED.as_mut() {
            led.toggle();
        }
    }
}
