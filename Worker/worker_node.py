import boto3
import time

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/009075573477/Team24-Scheduling-Queue'

def process_video_jobs():
    print("Worker instance started")
    
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=15
            )

            if 'Messages' not in response:
                continue

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

if __name__ == "__main__":
    process_video_jobs()