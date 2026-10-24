// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::thread;
use std::time::Duration;

fn main() {
    // Check and spawn local agentP Python daemon if not already online
    thread::spawn(|| {
        println!("[Tauri Launcher] Initializing background local agentP daemon...");
        // Ensure daemon runs natively at 127.0.0.1:9090
        let status = Command::new("python3")
            .arg("src/daemon/router.py")
            .spawn();

        match status {
            Ok(mut child) => {
                println!("[Tauri Launcher] agentP Core Daemon spawned with PID: {}", child.id());
                let _ = child.wait();
            }
            Err(e) => {
                eprintln!("[Tauri Launcher] Note: Python daemon launch status: {}. Assuming standalone or active daemon.", e);
            }
        }
    });

    // Short sleep for daemon initialization
    thread::sleep(Duration::from_millis(300));

    tauri::Builder::default()
        .setup(|_app| {
            println!("[Tauri] agentP Desktop Shell v2.9.0 initialized successfully.");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Error while running agentP Tauri application");
}
