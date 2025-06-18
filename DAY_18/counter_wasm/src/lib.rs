use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct Counter {
    count: u32,
}

#[wasm_bindgen]
impl Counter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Counter {
        Counter { count: 0 }
    }

    pub fn increment(&mut self) {
        self.count += 1;
    }

    // Add this reset method
    pub fn reset(&mut self) {
        self.count = 0;
    }

    pub fn get(&self) -> u32 {
        self.count
    }
}
