fn main() {
    // 1. Creating a Vector
    let mut v: Vec<i32> = Vec::new();
    let v2 = vec![1, 2, 3];

    println!("Initial empty vector: {:?}", v);
    println!("Vector with initial values: {:?}", v2);

    // 2. Pushing and Popping Elements
    v.push(10);
    v.push(20);
    v.push(30);
    println!("After pushes: {:?}", v); // [10, 20, 30]

    if let Some(last) = v.pop() {
        println!("Popped: {}", last); // 30
    }
    println!("After pop: {:?}", v); // [10, 20]

    // 3. Accessing and Iterating
    let v3 = vec![100, 200, 300, 300, 400, 200];
    // Direct indexing (panics if out of bounds)
    println!("v3[1] = {}", v3[1]); // 200

    // Using get() returns Option<&T>
    match v3.get(5) {
        Some(val) => println!("Found: {}", val),
        None => println!("No element at index 5"),
    }

    // Immutable iteration
    for val in &v3 {
        println!("Got (immutable): {}", val);
    }

    // Mutable iteration: modify each element
    let mut v4 = vec![1, 2, 3];
    for x in &mut v4 {
        *x += 10; // dereference to change the value
    }
    println!("Modified (after mutable iteration): {:?}", v4); // [11, 12, 13]
}
