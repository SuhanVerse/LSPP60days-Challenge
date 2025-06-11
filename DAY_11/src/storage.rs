// src/storage.rs

use crate::todo::Todo;
use std::fs::OpenOptions;
use std::io::{BufReader, BufWriter};

const FILENAME: &str = "todos.json";

pub fn load_todos() -> Result<Vec<Todo>, Box<dyn std::error::Error>> {
    // Open (or create) the file without truncating existing data
    let file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(false)
        .open(FILENAME)?;

    // If the file is empty, return an empty list
    if file.metadata()?.len() == 0 {
        return Ok(Vec::new());
    }

    // Deserialize JSON into Vec<Todo>
    let reader = BufReader::new(file);
    let todos = serde_json::from_reader(reader)?;
    Ok(todos)
}

pub fn save_todos(todos: &[Todo]) -> Result<(), Box<dyn std::error::Error>> {
    // Open the file for writing, truncating existing contents
    let file = OpenOptions::new()
        .write(true)
        .truncate(true)
        .open(FILENAME)?;

    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, todos)?;
    Ok(())
}
