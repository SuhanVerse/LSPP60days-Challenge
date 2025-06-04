// Define a struct named Point with two fields: x and y
// struct Point {
//     x: f64,
//     y: f64,
// }

// fn main() {
//     // Instantiate a Point
//     let p = Point { x: 3.0, y: 4.0 };
//     println!("Point is at ({}, {})", p.x, p.y);
// }

//-----------------------------------------------------------------

// struct Point {
//     x: f64,
//     y: f64,
// }

// fn main() {
//     let mut p = Point { x: 0.0, y: 0.0 };
//     // let origin = Point { x: 0.0, y: 0.0 };
//     // let p2 = Point { y: 7.0, ..origin };
//     p.x = 5.0;
//     p.y = -2.0;
//     println!("Updated point: ({}, {})", p.x, p.y);
// }

//-----------------------------------------------------------------

// Define a Color type as three u8 values (RGB)
// struct Color(u8, u8, u8);

// fn main() {
//     let white = Color(255, 255, 255);
//     // Access via index syntax
//     println!("Red component: {}", white.0,white.1, white.2);
// }
//-----------------------------------------------------------------

// #[derive(Debug)]     // Derive Debug for easy printing
// struct Point {
//     x: f64,
//     y: f64,
// }

// impl Point {
//     // Associated function (constructor)
//     fn new(x: f64, y: f64) -> Self {
//         Point { x, y }
//     }

//     // Method taking &self: reads data without taking ownership
//     fn magnitude(&self) -> f64 {
//         (self.x.powi(2) + self.y.powi(2)).sqrt()
//     }

//     // Method taking &mut self: modifies the instance
//     fn translate(&mut self, dx: f64, dy: f64) {
//         self.x += dx;
//         self.y += dy;
//     }

//     // Method taking self by value: consumes the instance
//     fn consume(self) {
//         println!("Consuming point: ({}, {})", self.x, self.y);
//         // After this call, the original instance is no longer usable
//     }
// }

// fn main() {
//     // Using associated function new()
//     let mut p = Point::new(3.0, 4.0);
//     println!("Point: {:?}, magnitude = {}", p, p.magnitude());
//     p.translate(1.0, 2.0);
//     println!("Translated point: {:?}", p);
//     p.consume();
//     // println!("{:?}", p); // ERROR: p was moved by consume()
// }

//-----------------------------------------------------------------

// In library.rs or mod.rs
// pub struct User {
//     pub username: String, // field is public
//     email: String,        // field is private
// }

// impl User {
//     pub fn new(username: &str, email: &str) -> Self {
//         User {
//             username: username.to_string(),
//             email: email.to_string(),
//         }
//     }

//     pub fn email(&self) -> &str {
//         &self.email // provide a getter for private field
//     }
// }

// fn main() {
//     let user = User::new("Xenon62", "khsuhan100@gmail.com");
//     println!("Username: {}", user.username); // allowed
//                                              // println!("{}", user.email); // ERROR: `email` is private
//     println!("Email: {}", user.email()); // OK via getter method
// }

//-----------------------------------------------------------------


#[derive(Debug)]
struct Circle {
    radius: f64,
}

impl Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
}

fn main() {
    let c = Circle { radius: 2.0 };
    println!("Circle: {:?}", c);           
    println!("Area: {:.2}", c.area());      // Output with 2 decimal places
}
