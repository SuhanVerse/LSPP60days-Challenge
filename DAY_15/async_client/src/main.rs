use reqwest::Error;
use tokio::task;

/// Asynchronously fetches the given URL and returns its byte length.
async fn fetch_url(url: &str) -> Result<usize, Error> {
    let response = reqwest::get(url).await?;         // .await the HTTP GET
    let bytes    = response.bytes().await?;          // .await the body bytes
    Ok(bytes.len())
}

#[tokio::main]
async fn main() {
    // 1. List of URLs to fetch
    let urls = vec![
        "https://www.rust-lang.org/",
        "https://crates.io/",
        "https://docs.rs/",
    ];

    // 2. Spawn one Tokio task per URL
    let mut handles = Vec::with_capacity(urls.len());
    for url in urls {
        let url_string = url.to_string();
        let handle = task::spawn(async move {
            match fetch_url(&url_string).await {
                Ok(len) => println!("{} -> {} bytes", url_string, len),
                Err(err) => eprintln!("Error fetching {}: {}", url_string, err),
            }
        });
        handles.push(handle);
    }

    // 3. Await all tasks to complete
    for handle in handles {
        let _ = handle.await;
    }
}
