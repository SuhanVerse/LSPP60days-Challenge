use final_web_server::ThreadPool;
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(format!("src/static/{}", filename))
        .unwrap_or_else(|_| String::from("<h1>Failed to read file</h1>"));

    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );

    stream.write_all(response.as_bytes()).unwrap();
}

fn main() {
    // Ensure static directory and files exist
    fs::create_dir_all("src/static").ok();
    fs::write("src/static/hello.html", "<h1>Welcome!</h1>").ok();
    fs::write("src/static/404.html", "<h1>Page Not Found</h1>").ok();

    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    println!("Listening on http://127.0.0.1:7878");

    let pool = ThreadPool::new(4);

    // Handle up to 100 connections then shut down
    for stream in listener.incoming().take(100) {
        let stream = stream.unwrap();
        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}
