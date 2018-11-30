# Delete snapshots older than retention period

import boto3
from botocore.exceptions import ClientError

from datetime import datetime,timedelta

def delete_snapshot(snapshot_id):
    print "Deleting snapshot %s " % (snapshot_id)
    try:
        ec2resource = boto3.resource('ec2', region_name='AWS_REGION')
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        print "Caught exception: %s" % e

    return

def lambda_handler(event, context):

    # Get current timestamp in UTC
    now = datetime.now()

    # AWS Account ID
    account_id = 'YOUR_AWS_ACCOUNT_ID'

    # Define retention period in days
    retention_days_year = 365
    retention_days_over_year = 1825

    # Connect to region
    ec2 = boto3.client('ec2', region_name='AWS_REGION')

    # Filtering by snapshot timestamp comparison is not supported
    # User result var if you only want to filter snaps under your AWS account_id
    #result = ec2.describe_snapshots( OwnerIds=[account_id] )

    #Filter for going through a list of EBS snapshots with the following filters
    automated = ec2.describe_snapshots(Filters=[{"Name":"description","Values":["TEXT_IN_DESCRIPTION"]}, {"Name":"owner-id","Values":["YOUR_AWS_ACCOUNT_ID"]}])

    for snapshot in automated['Snapshots']:

        print "Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'],snapshot['StartTime'])

        # Remove timezone info from snapshot in order for comparison to work below
        snapshot_time = snapshot['StartTime'].replace(tzinfo=None)

        # Subtract snapshot time from now returns a timedelta
        # Check if the timedelta is greater than retention days
        if (now - snapshot_time) > timedelta(retention_days_year):
                #The latter if is for deleting all snapshots older than 1825 days / 5 years
                #if (now - snapshot_time) > timedelta(retention_days_over_year):
                    #print "Snapshot is older than 5 years so it will be deleted"
                    #delete_snapshot(snapshot['SnapshotId'])
                #else:
            if (snapshot_time.strftime("%d") != '01'):
                if (snapshot_time.strftime("%d") != '15'):
                    print "Snapshot %s is older than 1 year but not made on the 1st or 15th of the month so it will be deleted" % (snapshot['SnapshotId'])
                    delete_snapshot(snapshot['SnapshotId'])
                else:
                    print "Snapshot %s is made on the 15th of the month so it will not be deleted" % (snapshot['SnapshotId'])
            else:
                print "Snapshot %s is made on the 1st of the month, so it won't be deleted" % (snapshot['SnapshotId'])
        else:
            print "Snapshot %s is less than 1 year old so it won't be deleted" % (snapshot['SnapshotId'])
