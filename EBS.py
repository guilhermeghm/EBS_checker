import boto3

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

response = ec2.describe_volume_status(
    Filters=[
        {
            'Name': 'volume-status.status',
            'Values': [
                'impaired',
            ]
        },
    ]
)

VolumeIds=[]
for volume in response['VolumeStatuses']:
    VolumeIds.append(volume['VolumeId'])
VolumeIds_string = ','.join(VolumeIds)

if VolumeIds_string:
    response = sns.publish(
        TopicArn='arn:aws:sns:eu-west-1:xxxxxxxxxxxx:Teste',
        Message=" The following volumes are impaired: " + VolumeIds_string,
    )

print(VolumeIds_string)
