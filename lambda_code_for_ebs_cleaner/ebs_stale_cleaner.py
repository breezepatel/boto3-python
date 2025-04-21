import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Step 1: Get all EBS snapshots owned by the account
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Step 2: Get all active EC2 instance IDs (optional — not directly used)
    instances_response = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    active_instance_ids = set()
    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Step 3: Iterate through each snapshot
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        # Case A: Snapshot has no associated volume
        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} — no volume associated.")
            continue

        # Case B: Check if the volume still exists
        try:
            volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
            volume = volume_response['Volumes'][0]

            # If the volume exists but is not attached to any instance
            if not volume['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} — volume {volume_id} not attached.")
        
        except ClientError as e:
            # If the volume does not exist (was deleted)
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} — volume {volume_id} not found.")
