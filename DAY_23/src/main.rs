#![no_std]
#![no_main]

use cortex_m_rt::entry;
use cortex_m_semihosting::hprintln;
use panic_halt as _; // provides the panic handler

// Import the PAC; the actual device module is `stm32f103xx::stm32f103`
use stm32f103xx as pac;

#[entry]
fn main() -> ! {
    // 1) Take ownership of the device peripherals
    let dp = pac::Peripherals::take().unwrap();

    // 2) Enable GPIOC clock (set IOPCEN in RCC.APB2ENR)
    dp.RCC.apb2enr.modify(|_, w| w.iopcen().enabled());

    // 3) Configure PC13 as 2 MHz push-pull output (CRH controls pins 8–15)
    dp.GPIOC.crh.modify(|_, w| {
        w.mode13().bits(0b10); // output @2 MHz
        w.cnf13().bits(0b00) // push-pull
    });

    hprintln!("Day 23: RAW PAC blink demo").unwrap();

    // 4) Blink PC13 in a loop
    loop {
        // Toggle PC13 by XOR-ing bit 13 of ODR
        let odr = dp.GPIOC.odr.read().bits();
        dp.GPIOC.odr.write(|w| unsafe { w.bits(odr ^ (1 << 13)) });

        // crude busy-wait
        for _ in 0..8_000_000 {
            cortex_m::asm::nop();
        }
    }
}
