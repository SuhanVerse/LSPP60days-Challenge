// use std::thread;
// use std::time::Duration;

// fn main() {
//     //Spawn 5 threads
//     let mut handles = Vec::new();
//     for i in 1..=5 {
//         let handle = thread::spawn(move || {
//             println!("Thread {} : starting", i);
//             thread::sleep(Duration::from_millis(500 * i));
//             println!("Thread {} : done", i);
//         });
//         handles.push(handle);
//     }

//     //Wait for all the threads to finish
//     for handle in handles {
//         handle.join().unwrap();
//     }
//     println!("All threads have completed...");
// }

//------------------------------------------------------------------------

// use std::sync::{Arc, Mutex};
// use std::thread;

// fn main() {
//     let counter = Arc::new(Mutex::new(0));
//     let mut handles = Vec::new();

//     for _ in 0..10 {
//         let counter_clone = Arc::clone(&counter);
//         let handle = thread::spawn(move || {
//             let mut num = counter_clone.lock().unwrap();
//             *num += 1;
//         });
//         handles.push(handle);
//     }

//     for handle in handles {
//         handle.join().unwrap();
//     }

//     println!("Result: {}", *counter.lock().unwrap()); // Should print 10
// }

//-------------------------------------------------------------------------------------

// use std::sync::mpsc;
// use std::thread;

// fn main() {
//     // Create a channel
//     let (sender, receiver) = mpsc::channel();

//     // Spawn producer threads
//     for id in 1..=3 {
//         let thread_sender = sender.clone();
//         thread::spawn(move || {
//             let msg = format!("Message from thread {}", id);
//             thread_sender.send(msg).unwrap();
//         });
//     }

//     // Drop the original sender to close channel when clones are done
//     drop(sender);

//     // Consumer: receive messages
//     for received in receiver {
//         println!("Got: {}", received);
//     }
//     println!("All messages received.");
// }

//-------------------------------------------------------------------------------------------

use std::sync::{Arc, Mutex, mpsc};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;
#[allow(dead_code)]
struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

impl ThreadPool {
    fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.send(job).unwrap();
    }
}

#[allow(dead_code)]
struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let job = receiver.lock().unwrap().recv().unwrap();
                println!("Worker {id} got a job; executing.");
                job();
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}

fn main() {
    let pool = ThreadPool::new(4);

    for i in 0..8 {
        pool.execute(move || {
            println!("Running task {}", i);
        });
    }

    // Give threads some time to print before exiting
    thread::sleep(std::time::Duration::from_secs(1));
}
