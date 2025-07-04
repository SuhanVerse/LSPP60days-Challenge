#![cfg(feature = "device")]
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use cortex_m_semihosting::hprintln;
use panic_halt as _; // panic handler
use stm32f103xx as pac;

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    dp.RCC.apb2enr.modify(|_, w| w.iopcen().enabled());
    dp.GPIOC.crh.modify(|_, w| {
        w.mode13().bits(0b10);
        w.cnf13().bits(0b00)
    });

    hprintln!("Day 23: RAW PAC blink demo").unwrap();

    loop {
        let odr = dp.GPIOC.odr.read().bits();
        dp.GPIOC.odr.write(|w| unsafe { w.bits(odr ^ (1 << 13)) });
        for _ in 0..8_000_000 {
            cortex_m::asm::nop()
        }
    }
}

