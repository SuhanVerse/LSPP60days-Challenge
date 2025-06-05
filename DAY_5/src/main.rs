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

