#![allow(unused_macros)]

/// Say hello.
#[macro_export]
macro_rules! say_hello {
    () => {
        println!("Hello from a macro!");
    };
}

/// Tuple struct generator.
#[macro_export]
macro_rules! create_tuple {
    ($name:ident, $ty:ty) => {
        struct $name($ty, $ty);
    };
}

/// Vec<String> builder.
#[macro_export]
macro_rules! vec_of_strings {
    ( $( $s:expr ),* ) => {
        {
            let mut v = Vec::new();
            $(
                v.push($s.to_string());
            )*
            v
        }
    };
}

/// Log macro with optional level.
#[macro_export]
macro_rules! log {
    ($level:ident, $msg:expr) => {
        println!(concat!("[", stringify!($level), "] {}"), $msg);
    };
    ($msg:expr) => {
        log!(INFO, $msg);
    };
}

#[cfg(test)]
mod tests {
    #[test]
    fn demo_macros() {
        say_hello!();
        create_tuple!(Pair, f64);
        let p = Pair(1.5, 2.5);
        assert_eq!(p.0 + p.1, 4.0);

        let v = vec_of_strings!("rust", "macros");
        assert_eq!(v, vec!["rust".to_string(), "macros".to_string()]);

        log!("default log");
        log!(ERROR, "explicit error");
    }
}
