import sqlite3

def check_for_failures():
    """Queries the database for the most recent failed jobs."""
    conn = sqlite3.connect('pipeline_logs.db')
    cursor = conn.cursor()

    # We only want to find 'Failed' jobs. 
    # In a real system, we'd only look for NEW failures since the last check.
    query = "SELECT id, job_name, error_message, timestamp FROM logs WHERE status = 'Failed'"
    
    cursor.execute(query)
    failures = cursor.fetchall()
    
    conn.close()
    return failures

def run_monitor():
    print("--- Scanning for Pipeline Failures ---")
    failures = check_for_failures()
    
    if not failures:
        print("✅ All systems go. No failures detected.")
    else:
        print(f"🚨 ALERT: Found {len(failures)} failures!")
        for f in failures:
            print(f"ID: {f[0]} | Job: {f[1]} | Error: {f[2]} | Time: {f[3]}")

if __name__ == "__main__":
    run_monitor()