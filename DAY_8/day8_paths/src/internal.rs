/// Visible anywhere in this crate.
pub(crate) fn crate_helper() {
    println!("[internal] crate_helper called");
}

/// Visible only to the parent module (the binary root).
pub(super) fn parent_only() {
    println!("[internal] parent_only called");
}

/// Also visible everywhere in the crate (instead of trying pub(in …)).
pub(crate) fn math_only() {
    println!("[internal] math_only called");
}
