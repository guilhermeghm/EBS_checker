import boto3

from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
sns = boto3.client('sns')


def lambda_handler(event, context):

    try:
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
    except ClientError as e:
        print("Some error has occurred! ", str(e))
        exit(-1)
    else:
        VolumeIds=[]
        for volume in response['VolumeStatuses']:
            VolumeIds.append(volume['VolumeId'])
        VolumeIds_string = ','.join(VolumeIds)

        if VolumeIds_string:
            response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:777996869152:Teste',
                Message=" The following volumes are impaired: " + VolumeIds_string,
            )

        print(VolumeIds_string)
