// #![allow(dead_code)]
// #![allow(unused_variables)]
// enum Direction {
//     North,
//     South,
//     East,
//     West,
// }

// fn main() {
//     let dir1 = Direction::North;
//     let dir2 = Direction::East;

//     // Using a simple match
//     match dir1 {
//         Direction::North => println!("Going north"),
//         Direction::South => println!("Going south"),
//         Direction::East  => println!("Going east"),
//         Direction::West  => println!("Going west"),
//     }

//     // Using a match with a guard
//     match dir2 {
//         Direction::North => println!("Still going north"),
//         Direction::South => println!("Now going south"),
//         Direction::East  => {
//             if let Direction::East = dir2 {
//                 println!("Heading east");
//             }
//         },
//         Direction::West  => println!("Turning west"),
//     }

// }

//---------------------------------------------------------------------------------

// // Example of using enums in Rust with different variants
// #![allow(dead_code)]
// #![allow(unused_variables)]
// enum Message {
//     Quit,                          // no data
//     Move { x: i32, y: i32 },       // named fields (struct-like)
//     Write(String),                 // single String
//     ChangeColor(i32, i32, i32),    // three i32 values (tuple-like)
// }

// fn main() {
//     let m1 = Message::Quit;
//     let m2 = Message::Move { x: 10, y: -5 };
//     let m3 = Message::Write(String::from("Hello, world!"));
//     let m4 = Message::ChangeColor(255, 0, 0);

//     process_message(m2);
// }

// fn process_message(msg: Message) {
//     match msg {
//         Message::Quit => println!("Quit message"),
//         Message::Move { x, y } => println!("Move to ({}, {})", x, y),
//         Message::Write(text) => println!("Text message: {}", text),
//         Message::ChangeColor(r, g, b) => println!("Change color to ({}, {}, {})", r, g, b),
//     }
// }

//---------------------------------------------------------------------------------

// #[derive(Debug)]
// #[allow(dead_code)]
// enum Status {
//     Success,
//     Failure(String),
// }

// fn main() {
//     let s = Status::Failure(String::from("File not found"));
//     println!("Status: {:?}", s);
// }

//---------------------------------------------------------------------------------

// #![allow(dead_code)]
// enum Coin {
//     Penny,
//     Nickel,
//     Dime,
//     Quarter,
// }

// fn value_in_cents(coin: Coin) -> u8 {
//     match coin {
//         Coin::Penny   => 1,
//         Coin::Nickel  => 5,
//         Coin::Dime    => 10,
//         Coin::Quarter => 25,
//     }
// }

// fn main() {
//     let c = Coin::Dime;
//     println!("Value: {} cents", value_in_cents(c));
// }

//---------------------------------------------------------------------------------

// enum Message {
//     Move { x: i32, y: i32 },
//     Write(String),
//     Quit,
// }

// fn process_message(msg: Message) {
//     match msg {
//         Message::Move { x, y } => println!("Moving to ({}, {})", x, y),
//         Message::Write(text) => println!("Text: {}", text),
//         Message::Quit => println!("Quit"),
//     }
// }

// fn main() {
//     let m1 = Message::Move { x: 10, y: 20 };
//     let m2 = Message::Write(String::from("Hello, ISPP!"));
//     let m3 = Message::Quit;

//     process_message(m1);
//     process_message(m2);
//     process_message(m3);
// }

//---------------------------------------------------------------------------------

// enum Status {
//     Ok,
//     Err(String),
//     Unknown,
// }

// fn handle_status(status: Status) {
//     match status {
//         Status::Ok => println!("Everything is fine"),
//         Status::Err(msg) => println!("Error: {}", msg),
//         _ => println!("Other status"),
//     }
// }

// fn main() {
//     let status1 = Status::Ok;
//     let status2 = Status::Err(String::from("Something went wrong"));
//     let status3 = Status::Unknown;

//     handle_status(status1);
//     handle_status(status2);
//     handle_status(status3);
// }


//----------------------------------------------------------------------------------


// enum Shape {
//     Circle(f64),                // radius
//     Rectangle(f64, f64),       // width, height          
//     Triangle(f64, f64, f64),   // side1, side2, side3
// }

// fn area(shape: Shape) -> f64 {
//     match shape {
//         Shape::Circle(radius) => std::f64::consts::PI * radius * radius,
//         Shape::Rectangle(width, height) => width * height,
//         Shape::Triangle(a, b, c) => {
//             let s = (a + b + c) / 2.0; // semi-perimeter
//             (s * (s - a) * (s - b) * (s - c)).sqrt() // Heron's formula
//         },
//     }
// }

// fn main() {
//     let circle = Shape::Circle(5.0);
//     let rectangle = Shape::Rectangle(4.0, 6.0);
//     let triangle = Shape::Triangle(3.0, 4.0, 5.0);

//     println!("Area of circle: {}", area(circle));
//     println!("Area of rectangle: {}", area(rectangle));
//     println!("Area of triangle: {}", area(triangle));
// }

//---------------------------------------------------------------------------------


enum Message {
    Quit,
    Write(String),
    ChangeColor(i32, i32, i32),
}

//FULL MATCH
// let msg = Message::Write(String::from("Hello"));

// match msg {
//     Message::Write(text) => println!("Got text message: {}", text),
//     _                     => println!("Not a text message"),
// }

// Day 5, Section 2.4: Demonstrating `if let` for Concise Pattern Matching

// Define an enum with multiple variants. One variant holds a String.


fn main() {
    // Example 1: `msg` is the Write variant
    let msg = Message::Write(String::from("Hello"));

    // `if let` checks if `msg` matches the `Message::Write(text)` pattern.
    // If it does, it binds the inner String to `text` and enters the first block.
    // Otherwise, it runs the `else` block.
    if let Message::Write(text) = msg {
        println!("Got text message: {}", text);
    } else {
        println!("Not a text message");
    }

    // Example 2: `msg2` is the Quit variant
    let msg2 = Message::Quit;

    // Here, since `msg2` is not `Message::Write`, the `else` branch executes.
    if let Message::Write(text) = msg2 {
        println!("Got text message: {}", text);
    } else {
        println!("Not a text message");
    }

    // Example 3: Combining `if let` with `else if let` to check multiple variants
    let msg3 = Message::ChangeColor(255, 0, 0);

    if let Message::Write(text) = msg3 {
        println!("Write message: {}", text);
    } else if let Message::ChangeColor(r, g, b) = msg3 {
        println!("Change color to red={}, green={}, blue={}", r, g, b);
    } else {
        println!("Some other message variant");
    }
}


//---------------------------------------------------------------------------------


// fn get_third_element(v: &[i32]) -> Option<i32> {
//     if v.len() < 3 {
//         None
//     } else {
//         Some(v[2])
//     }
// }

// fn main() {
//     let nums = vec![10, 20, 30];
//     match get_third_element(&nums) {
//         Some(n) => println!("3rd element is {}", n),
//         None    => println!("No 3rd element"),
//     }
// }


//---------------------------------------------------------------------------------

// // Day 5, Section 2.5: Demonstrating `Option` Type and Methods
// // The `Option` type is used to represent a value that can be either `Some(value)` or `None`.
// #[allow(dead_code)]
// #[allow(unused_variables)]
// #[derive(Debug)]
// enum Option<T> {
//     Some(T),
//     None,
// }           
// // The `Option` type has several methods:
// // - `is_some()`: Returns `true` if the value is `Some(value)`,
// // - `is_none()`: Returns `true` if the value is `None`,
// // - `unwrap()`: Returns the inner value if it is `Some(value)`, or panics if it is `None`,
// // - `unwrap_or(default)`: Returns the inner value if it is `Some(value)`, or returns `default` if it is `None`,
// // - `map(func)`: Applies a function to the inner value if it is `Some(value)`, returning a new `Option`,
// // - `and_then(func)`: Similar to `map`, but the function must return an `Option`, allowing for chaining operations.
// // - `expect(message)`: Returns the inner value if it is `Some(value)`, or
// //   panics with a custom message if it is `None`.

// #[allow(dead_code)]
// fn main() {
//     let some_value = Option::Some(10);
//     let no_value = Option::None;
//     // Check if the option has a value
//     if let Option::Some(v) = some_value {
//         println!("Value is: {}", v);
//     } else {
//         println!("No value");
//     }
//     // Check if the option is None
//     if let Option::None = no_value {
//         println!("No value present");
//     } else {
//         println!("Value is present");
//     }
//     // Unwrapping the value
//     match some_value {
//         Option::Some(v) => println!("Unwrapped value: {}", v),
//         Option::None => println!("Cannot unwrap, no value present"),
//     }
//     // Using unwrap_or to provide a default value
//     let default_value = no_value.unwrap_or(0);
//     println!("Default value: {}", default_value);
//     // Using map to transform the value
//     let transformed_value = some_value.map(|v| v * 2);
//     match transformed_value {
//         Option::Some(v) => println!("Transformed value: {}", v),
//         Option::None => println!("No value to transform"),
//     }
//     // Using and_then to chain operations
//     let chained_value = some_value.and_then(|v| {
//         if v > 5 {
//             Option::Some(v + 5)
//         } else {
//             Option::None
//         }
//     });
//     match chained_value {
//         Option::Some(v) => println!("Chained value: {}", v),
//         Option::None => println!("No value after chaining"),
//     }
// }

//---------------------------------------------------------------------------------

