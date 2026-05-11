import boto3
import time
import os

sqs = boto3.client('sqs', region_name='eu-north-1')
QUEUE_URL = 'https://sqs.eu-north-1.amazonaws.com/143326172801/Team24-Scheduling-Queue'

def process_video_jobs():
    print("Worker instance started")
    
    idle_counter = 0
    MAX_IDLE_TRIES = 5

    while idle_counter < MAX_IDLE_TRIES:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=15
            )

            if 'Messages' not in response:
                idle_counter += 1
                print(f"No message detected, total tries: ({idle_counter}/{MAX_IDLE_TRIES})")
                continue

            idle_counter = 0

            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            video_data = message['Body']
            
            print(f"New message: {video_data}")
            print("Processing video...")
            
            time.sleep(10) 
            
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=receipt_handle
            )
            
            print("Video processed and deleted from queue.\n")

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
    print("No more tasks in the queue. Shutting down the instance...")
    os.system("sudo shutdown -h now")
    
if __name__ == "__main__":
    process_video_jobs()