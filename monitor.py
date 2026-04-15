import sqlite3
import requests

# Replace 'your-unique-topic' with the name you picked in Step 1
TOPIC_NAME = "NtpdQ2nMXt3eywmK" 

def send_alert(job_name, error_msg):
    """Sends a notification to your phone/browser via ntfy.sh"""
    try:
        response = requests.post(
            f"https://ntfy.sh/{TOPIC_NAME}",
            data=f"🚨 Pipeline Failure: {job_name}\nError: {error_msg}".encode('utf-8'),
            headers={
                "Title": "Data Pipeline Alert",
                "Priority": "high",
                "Tags": "warning,skull"
            }
        )
        if response.status_code == 200:
            print(f"Notification sent for {job_name}!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def run_monitor():
    conn = sqlite3.connect('pipeline_logs.db')
    cursor = conn.cursor()

    # Look for Failed jobs that haven't been 'resolved' 
    # (For now, we'll just grab the latest ones)
    cursor.execute("SELECT job_name, error_message FROM logs WHERE status = 'Failed' LIMIT 1")
    failure = cursor.fetchone()
    
    if failure:
        job_name, error_msg = failure
        print(f"🚨 Found failure in {job_name}. Sending alert...")
        send_alert(job_name, error_msg)
    else:
        print("✅ No new failures.")

    conn.close()

if __name__ == "__main__":
    run_monitor()