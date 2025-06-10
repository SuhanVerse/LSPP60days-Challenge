// src/traits_demo.rs

pub trait Summary {
    fn summary(&self) -> String;
}

pub struct Article {
    pub title: String,
    pub author: String,
    pub content: String,
}

impl Summary for Article {
    fn summary(&self) -> String {
        format!("{} into {} by {}", self.content, self.title, self.author)
    }
}
