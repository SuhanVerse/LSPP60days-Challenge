use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};

type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

struct Worker {
    _id: usize,
    handle: Option<thread::JoinHandle<()>>,
}

impl ThreadPool {
    /// Create a new ThreadPool with the given size.
    /// Panics if size == 0.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            let receiver_clone = Arc::clone(&receiver);
            let handle = thread::spawn(move || {
                loop {
                    let message = receiver_clone.lock().unwrap().recv();
                    match message {
                        Ok(job) => job(),
                        Err(_) => break, // channel closed
                    }
                }
            });

            workers.push(Worker {
                _id: id,
                handle: Some(handle),
            });
        }

        ThreadPool { workers, sender }
    }

    /// Execute a task on the thread pool.
    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        // When ThreadPool is dropped, sender is dropped automatically,
        // closing the channel and allowing worker threads to exit.
        for worker in &mut self.workers {
            if let Some(handle) = worker.handle.take() {
                handle.join().unwrap();
            }
        }
    }
}
