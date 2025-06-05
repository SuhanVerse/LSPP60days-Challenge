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

