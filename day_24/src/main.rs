#![no_std]
#![no_main]

use cortex_m_rt::entry;
use cortex_m_semihosting::hprintln;
use panic_halt as _;

use embedded_hal::digital::v2::OutputPin;
use stm32f1xx_hal::{delay::Delay, pac, prelude::*};

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    let cp = cortex_m::Peripherals::take().unwrap();

    let mut flash = dp.FLASH.constrain();
    let mut rcc = dp.RCC.constrain();
    let clocks = rcc.cfgr.freeze(&mut flash.acr);

    let mut gpioa = dp.GPIOA.split(&mut rcc.apb2);

    let mut led = gpioa.pa5.into_push_pull_output(&mut gpioa.crl);

    let mut delay = Delay::new(cp.SYST, clocks);

    loop {
        led.set_high().unwrap();
        hprintln!("LED ON");
        delay.delay_ms(1_000_u16);
        hprintln!("Waiting for 1 second...");
        led.set_low().unwrap();
        hprintln!("LED OFF");
        delay.delay_ms(1_000_u16);
        hprintln!("Waiting for 1 second...");
    }
}
