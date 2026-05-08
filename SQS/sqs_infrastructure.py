import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

def create_video_jobs_queue():
    queue_name = 'Team24-Scheduling-Queue'
    print(f"Creating queue: '{queue_name}'...")
    
    try:
        response = sqs_client.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '0',
                'MessageRetentionPeriod': '86400'
            }
        )
        print("Queue Created Successfully")
        print(f"Queue Url: {response['QueueUrl']}")
        return response['QueueUrl']
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    queue_url = create_video_jobs_queue()