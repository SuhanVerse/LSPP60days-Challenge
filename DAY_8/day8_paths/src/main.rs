// Declare modules for this binary crate
mod internal;
mod math;
mod utils;

fn main() {
    // Call the internal(super) helper via an absolute path
    crate::internal::parent_only();

    // Use the utils module
    utils::greet("Rustacean"); // prints greeting + calls crate_helper
    let fact5 = utils::factorial(5);
    println!("5! = {}", fact5);

    // Use math operations
    let sum = math::add(7, 3);
    let product = math::multiply(4, 6);
    println!("7 + 3 = {}, 4 * 6 = {}", sum, product);

    // Call the math-only internal helper via the math module
    math::run_math_helper();
}
