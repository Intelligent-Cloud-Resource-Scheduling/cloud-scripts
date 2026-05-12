from flask import Flask, request, jsonify
import threading
import time
import requests
import os

app = Flask(__name__)

BACKEND_UPDATE_URL = "" # add url for backend update endpoint here

MAX_IDLE_SECONDS = 300
is_processing = False
last_job_finish_time = time.time()

def idle_watcher():
    global is_processing, last_job_finish_time
    
    while True:
        time.sleep(10)

        if not is_processing:
            idle_duration = time.time() - last_job_finish_time
            if idle_duration > MAX_IDLE_SECONDS:
                print(f"No jobs processed for {idle_duration} seconds. Shutting down the instance...")
                os.system("sudo shutdown -h now")
                break

def process_batch_in_background(batch_id, processes):
    print(f"\nStarting to process batch {batch_id} with {len(processes)} tasks in the background...")
    
    for process in processes:
        process_id = process.get('id')
        duration = process.get('duration', 5)
        
        print(f"Processing task {process_id} from batch {batch_id} (estimated time: {duration} seconds)...")
        time.sleep(duration)
        
        try:
            payload = {
                "batch_id": batch_id,
                "process_id": process_id,
                "status": "Completed"
            }
            response = requests.post(BACKEND_UPDATE_URL, json=payload)
            
            if response.status_code == 200:
                print(f"Process {process_id} from batch {batch_id} has been successfully updated to the backend.")
            else:
                print(f"Error updating process {process_id} from batch {batch_id}: {response.status_code}")
                
        except Exception as e:
            print(f"Error occurred while updating process {process_id} from batch {batch_id}: {e}")
            
    print(f"Finished processing batch {batch_id}.\n")
    
    is_processing = False
    last_job_finish_time = time.time()

@app.route('/process-batch', methods=['POST'])
def handle_batch():
    data = request.get_json()
    
    if not data or 'batch_id' not in data or 'processes' not in data:
        return jsonify({"error": "Invalid data format"}), 400
        
    batch_id = data['batch_id']
    processes = data['processes']
    
    is_processing = True
    
    thread = threading.Thread(target=process_batch_in_background, args=(batch_id, processes))
    thread.start()
    
    print(f"Received batch {batch_id} with {len(processes)} tasks. Processing will start in the background.")
    return jsonify({
        "message": "Batch processing started",
        "batch_id": batch_id,
        "status": "Processing Started"
    }), 200


if __name__ == '__main__':
    print("Starting API Worker...")
    watcher_thread = threading.Thread(target=idle_watcher, daemon=True)
    watcher_thread.start()
    app.run(host='0.0.0.0', port=5000)