#![no_std]
#![no_main]
#![feature(abi_avr_interrupt)]
#![allow(static_mut_refs, unused_unsafe, unused_mut)]

use arduino_hal::{delay_ms, entry, pac, pins};
use core::panic::PanicInfo;

// panic handler
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

// servo calibration (ticks @16 MHz/8)
const SERVO_MIN: u16 = 1600; // ~0.8 ms
const SERVO_MAX: u16 = 4400; // ~2.2 ms

fn angle_to_ticks(angle: u8) -> u16 {
    let span = SERVO_MAX - SERVO_MIN;
    SERVO_MIN + (span as u32 * angle as u32 / 180) as u16
}

static mut LED: Option<
    arduino_hal::hal::port::Pin<arduino_hal::hal::port::mode::Output, arduino_hal::hal::port::PB5>,
> = None;
static mut ANGLE: u8 = 0;

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    let mut pins = pins!(dp);

    // serial
    let mut serial = arduino_hal::default_serial!(dp, pins, 9600);
    ufmt::uwriteln!(&mut serial, "Day30: 0–180°, digits then #\r\n").ok();

    // heartbeat LED
    let mut led = pins.d13.into_output();
    led.set_low();
    unsafe { LED = Some(led) }
    dp.TC2.tccr2a.write(|w| w.wgm2().ctc());
    dp.TC2.tccr2b.write(|w| w.cs2().prescale_1024());
    dp.TC2.ocr2a.write(|w| w.bits(156));
    dp.TC2.timsk2.write(|w| w.ocie2a().set_bit());

    // servo PWM
    let _servo_pin = pins.d9.into_output();
    dp.TC1
        .tccr1a
        .write(|w| w.com1a().bits(0b10).wgm1().bits(0b10));
    dp.TC1
        .tccr1b
        .write(|w| w.wgm1().bits(0b11).cs1().prescale_8());
    dp.TC1.icr1.write(|w| unsafe { w.bits(40_000) });

    // keypad setup
    let mut rows = [
        pins.d8.into_output().downgrade(),
        pins.d7.into_output().downgrade(),
        pins.d6.into_output().downgrade(),
        pins.d5.into_output().downgrade(),
    ];
    for r in rows.iter_mut() {
        r.set_high()
    }

    let cols = [
        pins.d4.into_pull_up_input().downgrade(),
        pins.d3.into_pull_up_input().downgrade(),
        pins.d2.into_pull_up_input().downgrade(),
    ];

    // main scan loop
    loop {
        for r in 0..rows.len() {
            // strobe row
            for rr in rows.iter_mut() {
                rr.set_high()
            }
            rows[r].set_low();
            delay_ms(5);

            for (c, col) in cols.iter().enumerate() {
                if col.is_low() {
                    let key = match (r, c) {
                        (0, 0) => '1',
                        (0, 1) => '2',
                        (0, 2) => '3',
                        (1, 0) => '4',
                        (1, 1) => '5',
                        (1, 2) => '6',
                        (2, 0) => '7',
                        (2, 1) => '8',
                        (2, 2) => '9',
                        (3, 0) => '*',
                        (3, 1) => '0',
                        (3, 2) => '#',
                        _ => '?',
                    };

                    match key {
                        '#' => {
                            let angle = unsafe { ANGLE };
                            let ticks = angle_to_ticks(angle);
                            dp.TC1.ocr1a.write(|w| unsafe { w.bits(ticks) });
                            ufmt::uwriteln!(&mut serial, "→ {}°\r\n", angle).ok();
                            // blink LED twice
                            for _ in 0..2 {
                                unsafe { LED.as_mut().unwrap().toggle() };
                                delay_ms(100);
                                unsafe { LED.as_mut().unwrap().toggle() };
                                delay_ms(100);
                            }
                            unsafe { ANGLE = 0 };
                        }
                        '*' => {
                            unsafe { ANGLE = 0 };
                            ufmt::uwriteln!(&mut serial, "Cleared\r\n").ok();
                        }
                        d if d.is_ascii_digit() => {
                            unsafe {
                                ANGLE = ANGLE
                                    .saturating_mul(10)
                                    .saturating_add(d as u8 - b'0')
                                    .clamp(0, 180);
                            }
                            ufmt::uwriteln!(&mut serial, "Digit: {}\r\n", d).ok();
                        }
                        _ => {}
                    }

                    // release + debounce
                    while col.is_low() {}
                    delay_ms(50);
                }
            }
        }
    }
}

#[avr_device::interrupt(atmega328p)]
fn TIMER2_COMPA() {
    unsafe { LED.as_mut().unwrap().toggle() }
}

//--------------------------------------------------------------------------

// #![no_std]
// #![no_main]
// #![feature(abi_avr_interrupt)]
// #![allow(static_mut_refs, unused_unsafe, unused_mut)]

// use arduino_hal::{delay_ms, entry, pac, pins};
// use avr_device::asm::sleep;
// use core::panic::PanicInfo;

// // ——————————————————————————————————————————————
// // 1) panic handler
// // ——————————————————————————————————————————————
// #[panic_handler]
// fn panic(_info: &PanicInfo) -> ! {
//     loop {}
// }

// static mut LED: Option<
//     arduino_hal::hal::port::Pin<arduino_hal::hal::port::mode::Output, arduino_hal::hal::port::PB5>,
// > = None;

// static mut ANGLE: u8 = 0;

// #[entry]
// fn main() -> ! {
//     // 1) Take peripherals
//     let dp = pac::Peripherals::take().unwrap();
//     let mut pins = pins!(dp);

//     // 2) Serial @9600
//     let mut serial = arduino_hal::default_serial!(dp, pins, 9600);
//     ufmt::uwriteln!(&mut serial, "Day30: Enter 0–180°, then '#'\r\n").ok();

//     // 3) Heartbeat LED on D13 via Timer2 CTC @1Hz
//     let mut led = pins.d13.into_output();
//     led.set_low();
//     unsafe { LED = Some(led) };
//     dp.TC2.tccr2a.write(|w| w.wgm2().ctc());
//     dp.TC2.tccr2b.write(|w| w.cs2().prescale_1024());
//     dp.TC2.ocr2a.write(|w| w.bits(156));
//     dp.TC2.timsk2.write(|w| w.ocie2a().set_bit());

//     // 4) Servo on D9 (OC1A): Fast-PWM mode 14, prescale=8
//     //    WGM13:12 = 11, WGM11:10 = 10 → 0b1110 = mode 14
//     let _servo_pin = pins.d9.into_output();
//     dp.TC1.tccr1a.write(|w| {
//         w.com1a()
//             .bits(0b10) // non-inverting OC1A
//             .wgm1()
//             .bits(0b10) // WGM11:10 = 10
//     });
//     dp.TC1.tccr1b.write(|w| {
//         w.wgm1()
//             .bits(0b11) // WGM13:12 = 11
//             .cs1()
//             .prescale_8() // prescaler = 8
//     });
//     dp.TC1.icr1.write(|w| unsafe { w.bits(40_000) }); // TOP = 40000 → 50 Hz

//     // 5) Keypad: rows D8–D5, cols D4, D3, D2–INT0
//     //    We “downgrade” each pin to the same erased‐type so they can live in one array.
//     let mut rows: [_; 4] = [
//         pins.d8.into_output().downgrade(),
//         pins.d7.into_output().downgrade(),
//         pins.d6.into_output().downgrade(),
//         pins.d5.into_output().downgrade(),
//     ];
//     for r in rows.iter_mut() {
//         r.set_high()
//     }

//     let cols: [_; 3] = [
//         pins.d4.into_pull_up_input().downgrade(),
//         pins.d3.into_pull_up_input().downgrade(),
//         pins.d2.into_pull_up_input().downgrade(), // ‘#’ confirm
//     ];

//     // 6) External interrupt on D2 (INT0) falling edge
//     dp.EXINT.eicra.write(|w| w.isc0().bits(0b10));
//     dp.EXINT.eimsk.write(|w| w.int0().set_bit());

//     // 7) Enable interrupts
//     unsafe { avr_device::interrupt::enable() };

//     // 8) Main loop: scan keypad → build ANGLE → sleep until '#'
//     loop {
//         for r in 0..rows.len() {
//             // 1) set all rows HIGH
//             for r2 in rows.iter_mut() {
//                 r2.set_high();
//             }
//             // 2) pull just the r-th row LOW
//             rows[r].set_low();
//             delay_ms(5u32);
//             for (c, col_pin) in cols.iter().enumerate() {
//                 if col_pin.is_low() {
//                     let key = match (r, c) {
//                         (0, 0) => '1',
//                         (0, 1) => '2',
//                         (0, 2) => '3',
//                         (1, 0) => '4',
//                         (1, 1) => '5',
//                         (1, 2) => '6',
//                         (2, 0) => '7',
//                         (2, 1) => '8',
//                         (2, 2) => '9',
//                         (3, 0) => '*',
//                         (3, 1) => '0',
//                         (3, 2) => '#',
//                         _ => '?',
//                     };
//                     if key.is_ascii_digit() {
//                         unsafe {
//                             ANGLE = ANGLE
//                                 .saturating_mul(10)
//                                 .saturating_add(key as u8 - b'0')
//                                 .clamp(0, 180);
//                         }
//                         ufmt::uwriteln!(&mut serial, "Digit: {}\r", key).ok();
//                     }
//                     // wait release + debounce
//                     while col_pin.is_low() {}
//                     delay_ms(50u32);
//                 }
//             }
//         }
//         sleep();
//     }
// }

// // ——————————————————————————————————————————————
// // interrupts
// // ——————————————————————————————————————————————
// #[avr_device::interrupt(atmega328p)]
// fn TIMER2_COMPA() {
//     unsafe { LED.as_mut().unwrap().toggle() }
// }

// #[avr_device::interrupt(atmega328p)]
// fn INT0() {
//     // SAFETY: interrupt‐safe steal
//     let dp = unsafe { arduino_hal::pac::Peripherals::steal() };
//     let angle = unsafe { ANGLE };
//     let ticks = 2000 + (angle as u32 * 2000) / 180;
//     dp.TC1.ocr1a.write(|w| unsafe { w.bits(ticks as u16) });

//     // serial report
//     let mut pins = pins!(dp);
//     let mut serial = arduino_hal::default_serial!(dp, pins, 9600);
//     ufmt::uwriteln!(&mut serial, "Angle set to {}\r\n", angle).ok();

//     // reset
//     unsafe { ANGLE = 0 }
// }

//---------------------------------------------------------------------------------------

// #![no_std]
// #![no_main]
// #![feature(abi_avr_interrupt)]
// #![allow(static_mut_refs)]

// use arduino_hal::{delay_ms, entry, pac, pins};
// use avr_device::asm::sleep;
// use panic_halt as _;

// static mut LED: Option<
//     arduino_hal::hal::port::Pin<arduino_hal::hal::port::mode::Output, arduino_hal::hal::port::PB5>,
// > = None;

// static mut ANGLE: u8 = 0;

// #[entry]
// fn main() -> ! {
//     // ——————————————
//     // 1) Peripherals + Pins
//     let dp = pac::Peripherals::take().unwrap();
//     let mut pins = pins!(dp);

//     // 2) Serial @9600
//     let mut serial = arduino_hal::default_serial!(dp, pins, 9600);
//     ufmt::uwriteln!(&mut serial, "Day30: Enter 0–180°, then '#'\r").ok();
//     let mut led = pins.d13.into_output();
//     led.set_low();
//     unsafe { LED = Some(led) };
//     // Timer2 CTC @1Hz
//     dp.TC2.tccr2a.write(|w| w.wgm2().ctc());
//     dp.TC2.tccr2b.write(|w| w.cs2().prescale_1024());
//     dp.TC2.ocr2a.write(|w| w.bits(156));
//     dp.TC2.timsk2.write(|w| w.ocie2a().set_bit());

//     dp.TC1
//         .tccr1a
//     dp.TC1
//         .tccr1a
//         .write(|w| w.com1a().bits(0b10).wgm1().bits(0b10));
//     dp.TC1
//         .tccr1b
//         .write(|w| w.wgm1().bits(0b1).wgm12().bits(0b1).cs1().prescale_8());
//     dp.TC1.icr1.write(|w| unsafe { w.bits(40_000) }); // TOP = 40k → 50 Hz
//     // Use only PORTB pins for rows and PORTD pins for columns to match types
//     let mut rows = [
//         { let mut p = pins.d8.into_output(); p.set_high(); p }, // PB0
//         { let mut p = pins.d9.into_output(); p.set_high(); p }, // PB1
//         { let mut p = pins.d10.into_output(); p.set_high(); p }, // PB2
//         { let mut p = pins.d11.into_output(); p.set_high(); p }, // PB3
//     ];
//     // Columns (D4, D3, D2=INT0) - all on PORTD
//     let cols = [
//         pins.d4.into_pull_up_input(), // PD4
//         pins.d3.into_pull_up_input(), // PD3
//         pins.d2.into_pull_up_input(), // PD2
//     ];
//     dp.EXINT.eicra.write(|w| w.isc0().bits(0b10));
//     dp.EXINT.eimsk.write(|w| w.int0().set_bit());

//     // 7) Enable interrupts
//     unsafe { avr_device::interrupt::enable() };
//     loop {
//         // Scan keypad: drive each row low, read columns
//         for (r, row) in rows.iter_mut().enumerate() {
//             // set row low, others high
//             for (i, r2) in rows.iter_mut().enumerate() {
//                 if i == r {
//                     r2.set_low();
//                 } else {
//                     r2.set_high();
//                 }
//             }
//             delay_ms(5u32);

//             for (c, col) in cols.iter().enumerate() {
//                 if col.is_low().unwrap() {
//                     // map (r,c) to char
//                     let key = match (r, c) {
//                         (0, 0) => '1',
//                         (0, 1) => '2',
//                         (0, 2) => '3',
//                         (1, 0) => '4',
//                         (1, 1) => '5',
//                         (1, 2) => '6',
//                         (2, 0) => '7',
//                         (2, 1) => '8',
//                         (2, 2) => '9',
//                         (3, 0) => '*',
//                         (3, 1) => '0',
//                         (3, 2) => '#',
//                         _ => '?',
//                     };
//                     // if digit, accumulate
//                     if key.is_ascii_digit() {
//                         unsafe {
//                             ANGLE = (ANGLE.saturating_mul(10))
//                                 .saturating_add(key as u8 - b'0')
//                                 .clamp(0, 180);
//                         }
//                         ufmt::uwriteln!(&mut serial, "Digit: {}\r", key).ok();
//                     }
//                     // wait for release
//                     while col.is_low().unwrap() {}
//                     delay_ms(50u32);
//                 }
//             }
//         }
//         // Sleep until confirm
//         sleep();
//         // INT0 ISR will handle moving servo & report
//     }
// }
// // Timer2 heartbeat
// #[avr_device::interrupt(atmega328p)]
// fn TIMER2_COMPA() {
//     unsafe {
//         LED.as_mut().unwrap().toggle();
//     }
// }

// // INT0: Confirm '#'
// #[avr_device::interrupt(atmega328p)]
// fn INT0() {
//     let dp = unsafe { pac::Peripherals::steal() };
//     let current_angle = unsafe { ANGLE };
//     // Convert 0–180 → 2_000–4_000 ticks
//     let ticks = 2_000 + (current_angle as u32 * 2_000) / 180;
//     dp.TC1.ocr1a.write(|w| unsafe { w.bits(ticks as u16) });

//     // Report and reset
//     let pins = unsafe { pins!(dp) };
//     let mut serial = arduino_hal::default_serial!(dp, pins, 9600);
//     ufmt::uwriteln!(&mut serial, "Angle set to {}\r", current_angle).ok();
//     unsafe {
//         ANGLE = 0;
//     }
// }
