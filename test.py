import requests
import time

API_TOKEN = ""
CUSTOM_ID = "974"
TEAM_ID = "43231889"

print("=" * 60)
print("Step 1: Getting task info using custom_id")
print("=" * 60)

# Get task by custom_id to get the real task ID
url = f"https://api.clickup.com/api/v2/task/{CUSTOM_ID}?custom_task_ids=true&team_id={TEAM_ID}"
headers = {"Authorization": API_TOKEN}

resp = requests.get(url, headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    task_data = resp.json()
    real_task_id = task_data.get('id')
    task_name = task_data.get('name')
    print(f"✓ Task found: {task_name}")
    print(f"✓ Custom ID: {CUSTOM_ID}")
    print(f"✓ Real ID: {real_task_id}")
    
    print("\n" + "=" * 60)
    print("Step 2: Creating time entry (2 hours)")
    print("=" * 60)
    
    # Calculate time entry (2 hours = 120 minutes)
    duration_ms = 120 * 60 * 1000  # 2 hours in milliseconds
    end_time_ms = int(time.time() * 1000)
    start_time_ms = end_time_ms - duration_ms
    
    time_data = {
        "tid": real_task_id,
        "start": start_time_ms,
        "duration": duration_ms,
        "description": "Testing WorkPulse integration"
    }
    
    print(f"Request data:")
    print(f"  - Task ID: {real_task_id}")
    print(f"  - Duration: 120 minutes ({duration_ms} ms)")
    print(f"  - Start: {start_time_ms}")
    print(f"  - Description: Testing WorkPulse integration")
    
    time_resp = requests.post(
        f"https://api.clickup.com/api/v2/team/{TEAM_ID}/time_entries",
        headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
        json=time_data,
        timeout=10
    )
    
    print(f"\nTime Entry Status: {time_resp.status_code}")
    if time_resp.status_code in [200, 201]:
        print("✓ SUCCESS! Time entry created")
        print(f"Response: {time_resp.json()}")
    else:
        print("✗ FAILED!")
        print(f"Response: {time_resp.text}")
    
    print("\n" + "=" * 60)
    print("Step 3: Adding comment (optional)")
    print("=" * 60)
    
    comment_text = "Testing WorkPulse integration - 2h work completed"
    comment_resp = requests.post(
        f"https://api.clickup.com/api/v2/task/{real_task_id}/comment",
        headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
        json={"comment_text": comment_text},
        timeout=10
    )
    
    print(f"Comment Status: {comment_resp.status_code}")
    if comment_resp.status_code in [200, 201]:
        print("✓ Comment added successfully")
    else:
        print("✗ Comment failed")
        print(f"Response: {comment_resp.text}")
        
else:
    print(f"✗ Failed to get task: {resp.text}")