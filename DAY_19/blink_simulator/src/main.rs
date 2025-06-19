// use std::thread;
// use std::time::Duration;

// /// Simulates blinking by printing "LED ON" / "LED OFF" at 1 Hz.
// fn main() {
//     loop {
//         println!("LED ON");
//         thread::sleep(Duration::from_millis(500));
//         println!("LED OFF");
//         thread::sleep(Duration::from_millis(500));
//     }
// }

use crossterm::{ExecutableCommand, cursor, event, terminal};
use std::thread;
use std::time::Duration;

fn main() {
    // Set up terminal
    std::io::stdout()
        .execute(terminal::EnterAlternateScreen)
        .unwrap();
    std::io::stdout().execute(cursor::Hide).unwrap();
    terminal::enable_raw_mode().unwrap();

    let mut led_on = false;

    loop {
        // Check for key press
        if event::poll(Duration::from_millis(0)).unwrap() {
            if let event::Event::Key(key) = event::read().unwrap() {
                match key.code {
                    event::KeyCode::Char('q' | 'Q') => break, // quit
                    event::KeyCode::Char('t' | 'T') => {
                        led_on = !led_on; // toggle
                    }
                    _ => {}
                }
            }
        }

        // Print state
        if led_on {
            println!("LED ON \t");
        } else {
            println!("LED OFF\t");
        }

        thread::sleep(Duration::from_millis(500));
        // Move cursor up to overwrite
        std::io::stdout().execute(cursor::MoveUp(1)).unwrap();
    }

    // Restore terminal
    terminal::disable_raw_mode().unwrap();
    std::io::stdout().execute(cursor::Show).unwrap();
    std::io::stdout()
        .execute(terminal::LeaveAlternateScreen)
        .unwrap();
}
