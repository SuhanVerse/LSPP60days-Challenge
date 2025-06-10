// // src/main.rs

// /// A trait for anything that can “drive” (e.g., update position or altitude).
// pub trait Drive {
//     /// Update the object’s state.
//     fn update(&mut self);
// }

// /// A simple Robot struct implementing Drive.
// pub struct Robot {
//     name: String,
//     x: f64,
//     y: f64,
// }

// impl Drive for Robot {
//     fn update(&mut self) {
//         // Move diagonally by (1.0, 1.0)
//         self.x += 1.0;
//         self.y += 1.0;
//         println!("{} moved to ({}, {})", self.name, self.x, self.y);
//     }
// }

// /// An enum representing different vehicles, each implementing Drive.
// pub enum Vehicle {
//     Car { speed: f64 },
//     Drone { altitude: f64 },
// }

// impl Drive for Vehicle {
//     fn update(&mut self) {
//         match self {
//             Vehicle::Car { speed } => {
//                 *speed += 10.0;
//                 println!("Car now at speed {}", speed);
//             }
//             Vehicle::Drone { altitude } => {
//                 *altitude += 100.0;
//                 println!("Drone ascending to {}", altitude);
//             }
//         }
//     }
// }

// fn main() {
//     println!("— Demo: Drive trait on Robot —");
//     let mut bot = Robot {
//         name: "R2-D2".into(),
//         x: 0.0,
//         y: 0.0,
//     };
//     bot.update(); // prints: R2-D2 moved to (1.0, 1.0)

//     println!("\n— Demo: Drive trait on Vehicle::Car —");
//     let mut car = Vehicle::Car { speed: 50.0 };
//     car.update(); // prints: Car now at speed 60.0

//     println!("\n— Demo: Drive trait on Vehicle::Drone —");
//     let mut drone = Vehicle::Drone { altitude: 200.0 };
//     drone.update(); // prints: Drone ascending to 300.0
// }

//----------------------------------------------------------------------

// use std::cmp::PartialOrd;
// use std::fmt::Debug;

// /// 2.1 Generic Function: Find the largest element in a slice.
// fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
//     let mut largest = list[0];
//     for &item in list.iter().skip(1) {
//         if item > largest {
//             largest = item;
//         }
//     }
//     largest
// }

// /// 2.2 Generic Struct: A Point with any coordinate type.
// struct Point<T> {
//     x: T,
//     y: T,
// }

// impl<T> Point<T> {
//     fn new(x: T, y: T) -> Self {
//         Point { x, y }
//     }
// }

// /// 2.3 Debug‐only Pair Printer (fixed)
// fn print_pair<T: Debug, U: Debug>(t: T, u: U) {
//     // Now we only use {:?}, so Vec<T> works
//     println!("Pair: {:?} and {:?}", t, u);
// }

// /// Lifetime Annotation: Return the longer of two string slices.
// fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
//     if x.len() >= y.len() {
//         x
//     } else {
//         y
//     }
// }

// /// Demo all features in one main
// fn main() {
//     println!("🔍 Demo: generic function `largest`");
//     let nums = vec![3, 7, 2, 9, 4];
//     println!("Largest number: {}", largest(&nums));
//     let words = vec!["apple", "pear", "banana"];
//     println!("Longest word: {}", largest(&words));

//     println!("\n📐 Demo: generic struct `Point<T>`");
//     let int_point = Point::new(1, 2);
//     println!("Integer point: ({}, {})", int_point.x, int_point.y);
//     let float_point = Point::new(1.0, 4.5);
//     println!("Float point: ({}, {})", float_point.x, float_point.y);

//     println!("\n🔗 Demo: Debug‐only `print_pair`");
//     print_pair(42, vec![1, 2, 3]); // Vec<i32> is Debug
//     print_pair("hello", vec!["a", "b", "c"]);

//     println!("\n⏳ Demo: lifetime‐annotated `longest`");
//     let a = "short";
//     let b = "much longer string";
//     println!("The longest string is: {}", longest(a, b));
// }

//-----------------------------------------------------------------------------

// src/main.rs

mod math_generic;
mod traits_demo;

use math_generic::operate;
use traits_demo::{Article, Summary};

fn main() {
    // Trait demo
    let art = Article {
        title: "Rust Generics".into(),
        author: "Suhan".into(),
        content: "Deep dive".into(),
    };
    println!("Article summary: {}", art.summary());

    // Generic calculator demo
    let i = operate("add", 10i32, 20i32).unwrap();
    println!("10 + 20 = {}", i);

    let f = operate("div", 7.5f64, 2.5f64).unwrap();
    println!("7.5 / 2.5 = {}", f);
}
