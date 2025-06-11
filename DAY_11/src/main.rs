mod storage;
mod todo;

use crate::storage::{load_todos, save_todos};
use crate::todo::Todo;
use std::env;

fn print_usage(program: &str) {
    eprintln!("Usage:");
    eprintln!("  {} list", program);
    eprintln!("  {} add <title>", program);
    eprintln!("  {} done <id>", program);
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage(&args[0]);
        std::process::exit(1);
    }

    let mut todos = load_todos()?;
    let cmd = args[1].as_str();

    match cmd {
        "list" => {
            if todos.is_empty() {
                println!("No TODOs yet!");
            } else {
                for todo in &todos {
                    println!(
                        "{}. [{}] {} (created {})",
                        todo.id,
                        if todo.completed { "x" } else { " " },
                        todo.title,
                        todo.created_at.format("%Y-%m-%d %H:%M")
                    );
                }
            }
        }
        "add" => {
            let title = args[2..].join(" ");
            let next_id = todos.iter().map(|t| t.id).max().unwrap_or(0) + 1;
            let new_todo = Todo::new(next_id, title);
            todos.push(new_todo);
            save_todos(&todos)?;
            println!("Added TODO #{}", next_id);
        }
        "done" => {
            let id: u32 = args
                .get(2)
                .and_then(|s| s.parse().ok())
                .expect("Please provide a valid id");
            match todos.iter_mut().find(|t| t.id == id) {
                Some(t) => {
                    t.completed = true;
                    save_todos(&todos)?;
                    println!("Marked TODO #{} as done", id);
                }
                None => println!("No TODO with id {}", id),
            }
        }
        _ => {
            print_usage(&args[0]);
            std::process::exit(1);
        }
    }

    Ok(())
}
