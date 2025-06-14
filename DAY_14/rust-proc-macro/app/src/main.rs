use derive_builder::Builder;
#[derive(Builder, Debug)]
#[allow(dead_code)]
pub struct Config {
    host: String,
    port: u16,
    use_tls: bool,
}

fn main() {
    let config = ConfigBuilder::default()
        .host("127.0.0.1".into())
        .port(8000)
        .use_tls(true)
        .build()
        .unwrap();

    println!("{:#?}", config);
}
