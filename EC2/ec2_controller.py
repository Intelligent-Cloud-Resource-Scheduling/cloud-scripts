import boto3

ec2 = boto3.client('ec2', region_name='eu-north-1')
sqs = boto3.client('sqs', region_name='eu-north-1')

QUEUE_URL = 'https://sqs.eu-north-1.amazonaws.com/143326172801/Team24-Scheduling-Queue'
AMI_ID = 'ami-05d62b9bc5a6ca605'
ROLE_NAME = 'Team24-Worker-Role'
MAX_ALLOWED_INSTANCES = 3 # change this to the maximum number of worker instances

def get_queue_jobs_count(num_instances=1):
    if num_instances > MAX_ALLOWED_INSTANCES:
        print(f"Instances reduced from: ({num_instances}) to ({MAX_ALLOWED_INSTANCES}).")
        num_instances = MAX_ALLOWED_INSTANCES

    response = sqs.get_queue_attributes(
        QueueUrl=QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

def start_worker_instance(num_instances=1):
    print("Requesting to start a new worker instance...")
    try:
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType='t3.micro',
            MinCount=num_instances,
            MaxCount=num_instances,
            IamInstanceProfile={'Name': ROLE_NAME},
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Team24-Video-Worker'}]
            }]
        ) 
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        print(f"Instance(s) started, ID(s): {instance_ids}")
        print(f"Instance started, ID: {instance_ids}")
        return instance_ids
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Checking the video jobs queue...")
    
    jobs = get_queue_jobs_count()
    print(f"Number of video jobs in the queue: {jobs}")

    if jobs > 0:
        start_worker_instance(jobs)
    else:
        print("No video jobs in the queue. No worker instances needed.")