// src/todo.rs
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Todo {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub created_at: DateTime<Utc>,
}

impl Todo {
    pub fn new(id: u32, title: String) -> Self {
        Todo {
            id,
            title,
            completed: false,
            created_at: Utc::now(),
        }
    }
}
