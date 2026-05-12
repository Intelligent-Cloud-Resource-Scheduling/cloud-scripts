import boto3

ec2 = boto3.client('ec2', region_name='eu-north-1')

AMI_ID = 'ami-05d62b9bc5a6ca605'
MAX_ALLOWED_INSTANCES = 3 # change this to the maximum number of worker instances

def start_worker_instance(num_instances=1):
    print("Requesting to start a new worker instance...")

    if num_instances > MAX_ALLOWED_INSTANCES:
        print(f"Requested number of instances ({num_instances}) exceeds the maximum allowed ({MAX_ALLOWED_INSTANCES}). Starting {MAX_ALLOWED_INSTANCES} instance(s) instead.")
        num_instances = MAX_ALLOWED_INSTANCES

    try:
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType='t3.micro',
            MinCount=num_instances,
            MaxCount=num_instances,
            KeyName='apiWorker-key',
            InstanceInitiatedShutdownBehavior='terminate',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Team24-Video-Worker'}]
            }]
        ) 
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        print(f"Instance(s) started, ID(s): {instance_ids}")
        return instance_ids
    
    except Exception as e:
        print(f"Error: {e}")
        return None