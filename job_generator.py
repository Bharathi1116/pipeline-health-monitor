import sqlite3
import random
import time

def log_job(job_name, status, error_msg=None):
    """Inserts a single job record into the database."""
    conn = sqlite3.connect('pipeline_logs.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO logs (job_name, status, error_message) VALUES (?, ?, ?)",
        (job_name, status, error_msg)
    )
    
    conn.commit()
    conn.close()
    print(f"Logged: {job_name} | Status: {status}")

def run_simulation():
    # A list of fake data tasks a professional might have
    jobs = ["Daily_Sales_ETL", "User_Profile_Sync", "Inventory_Update", "Marketing_API_Pull"]
    
    while True:
        # Pick a random job
        job = random.choice(jobs)
        
        # 80% chance of success, 20% chance of failure
        if random.random() < 0.8:
            log_job(job, "Success")
        else:
            log_job(job, "Failed", "Connection Timeout: Server 404")
        
        # Wait 10 seconds before the next "job" runs
        print("Waiting for next job cycle...")
        time.sleep(10)

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")