// fn main() {
// let x = 34;
// if x % 2 == 0 {
// println!("{} is even", x);
// } else {
// println!("{} is odd", x);
// }
// }

// -----------------------------------------------------------

// **Example: `match` with patterns.**```rust
// fn main() {
//     let num = 2;
//     match num {
//         1 => println!("one"),
//         2 => println!("two"),
//         _ => println!("something else"),
//     }
// }

//-------------------------------------------------------------

// **Example: `match` with ranges.**```rust
// fn main() {
//     let num = 11;
//     match num {
//         1..=5 => println!("between 1 and 5"),
//         6..=10 => println!("between 6 and 10"),
//         _ => println!("something else"),
//     }
// }

// -------------------------------------------------------------

// **Example: `match` with guards.**```rust

// fn main() {
//     let num = 7;
//     match num {
//         1..=5 => println!("between 1 and 5"),
//         6..=10 if num % 2 == 0 => println!("between 6 and 10 and even"),
//         6..=10 => println!("between 6 and 10 and odd"),
//         _ => println!("something else"),
//     }
// }

// -------------------------------------------------------------

// **Example: `match` with destructuring.**```rust
// fn main() {
//     let point = (0, 4);
//     match point {
//         (0, 0) => println!("origin"),
//         (x, 0) => println!("on x-axis at {}", x),
//         (0, y) => println!("on y-axis at {}", y),
//         (x, y) => println!("point at ({}, {})", x, y),
//     }
// }

// -------------------------------------------------------------

// // **Example: `match` with enums.**```rust
// #[allow(dead_code)]
// enum Direction {
//     Up,
//     Down,
//     Left,
//     Right,
// }

// fn main() {
//     let dir = Direction::Up;
//     match dir {
//         Direction::Up => println!("going up"),
//         Direction::Down => println!("going down"),
//         Direction::Left => println!("going left"),
//         Direction::Right => println!("going right"),
//     }
// }

// -------------------------------------------------------------

// fn main() {
//     let mut count = 0;
//     loop {
//         count += 1;
//         if count == 3 {
//             println!("Reached 3, continuing.");
//             continue; // skip printing 3
//         }
//         println!("{}", count);
//         if count == 5 {
//             println!("Reached 5, breaking.");
//             break; // exit loop
//         }
//     }
// }

// -------------------------------------------------------------

// fn main() {
//     let a = 10;
//     let b = 3;
//     println!("a + b = {}", a + b);
//     println!("a / b = {}", a / b);
//     println!("a % b = {}", a % b);
// }

// -------------------------------------------------------------

// **Example: Comparison & Logical.**```rust
// fn main() {
//     let x = 5;
//     println!("x == 5: {}", x == 5);
//     println!("x != 5: {}", x != 5);
//     println!("0 < x < 10: {}", x > 0 && x < 10);
//     let a = true; let b = false;
//     println!("a AND b: {}", a && b);
//     println!("NOT a: {}", !a);
// }

// -------------------------------------------------------------

// **Example: Bitwise Operations.**```rust
// fn main() {
//     let x = 0b1010; // 10 in binary
//     let y = 0b0101; // 5 in binary
//     println!("x: {}", x);
//     println!("y: {}", y);
//     println!("x & y = {:b}", x & y); // AND
//     println!("x | y = {:b}", x | y); // OR
//     println!("x ^ y = {:b}", x ^ y); // XOR
//     println!("x << 1 = {:b}", x << 1); // shift left
// }

// -------------------------------------------------------------

// ## Symbols & Syntax
// Rust uses several punctuation symbols to define structure:
// - **`:`** – used in type annotations (e.g. `let x: i32 = 5` means `x` is an `i32`). It also appears in structs (`x: i32`) and labels (`'a: loop { ... }`).
// - **`->`** – appears in function signatures to denote the return type (e.g. `fn add(a: i32, b: i32) -> i32 { ... }`):contentReference[oaicite:11]{index=11}.
// - **`::`** – the path separator. Use it to access modules or enum variants, e.g. `std::io::stdin()`, `Option::Some`.
// - **`;`** – every statement ends with a semicolon:contentReference[oaicite:12]{index=12}, except the last expression in a block if you want it to return a value.
// - **`{}`** – braces define code blocks (for `fn`, `if`, loops, etc.) or struct literals. They group code or fields together.
// - **`()`** – parentheses group expressions, call functions, or enclose tuples/tuples-like parameters.
// - **`[]`** – brackets are used for array or slice literals and indexing, e.g. `let arr = [1,2,3]; println!("{}", arr[0]);`.

// **Example (combined syntax):**```rust
// mod greetings {
//     pub fn hello() {
//         println!("Hello!");
//     }
// }

// fn add(a: i32, b: i32) -> i32 {
//     a + b            // return value (no semicolon here, but semicolon would discard the value)
// }

// fn main() {
//     greetings::hello();            // `::` accesses module function
//     let result = add(2, 3);        // `()` for args, `;` ends statement
//     let arr = [10, 20, 30];        // `[]` for array
//     println!("result={}, arr[1]={}", result, arr[1]);
// }

// -------------------------------------------------------------

// pub struct Point {        // `pub`, `struct`, `{}`
//     x: i32,               // `:i32` (type annotation)
//     y: i32,
// }

// impl Point {             // implement methods for Point
//     pub fn new(x: i32, y: i32) -> Self {   // `fn`, `->`
//         Point { x, y }                    // struct literal
//     }
//     pub fn display(&self) {             // method, uses `&self`
//         println!("({}, {})", self.x, self.y);
//     }
// }

// fn main() {
//     let mut p = Point::new(3, 4);       // `let`, `mut`, `::`
//     p.display();
//     p.x = 5;                          // modify field
//     p.display();                      // display again
// }

// -------------------------------------------------------------

use rand::Rng;
use std::io;

fn main() {
    let secret = rand::thread_rng().gen_range(1..=48);
    println!("Guess the number between 1 and 48:");

    loop {
        let mut guess = String::new();
        io::stdin().read_line(&mut guess).expect("Failed to read");
        let guess: i32 = guess.trim().parse().expect("Enter a number");

        if guess < secret {
            println!("Too small!");
        } else if guess > secret {
            println!("Too big!");
        } else {
            println!("You got it!");
            break;
        }
    }
}
