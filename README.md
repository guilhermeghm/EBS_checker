# EBS_Checker

This is a simple Python Script to be executed using a Lambda function to monitor the EBS Volume Status.


**HOW TO USE**

On the AWS console, you can check the status of your volume. However, you are not able to create a Cloud Watch event to trigger an action when a volume is impaired. In this article, I'm using the Cloud Watch event to call a Lambda function to monitor the volumes on your account and publish this information in an SNS topic.

More information about this resource: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-volume-status.html

The steps are:

  1 - First, create and an SNS topic, as described here:
        - https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html

      After the creation, save the ARN of the SNS.

  2 - Create a Lambda function with the following code; remember to change the ARN of the SNS topic.
      - https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html

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
                    TopicArn='arn:aws:sns:region:AWS-Account:SNS-Name',
                    Message=" The following volumes are impaired: " + VolumeIds_string,
                )


  3 - To be executed correctly, the Lambda will need to have some permissions, create a new IAM policy with the following permissions. To be more restrictive, you can change the SNS policy to allow permission only on the SNS topic that you will send the message.

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                  "ec2:DescribeInstances",
                  "ec2:DescribeImages",
                  "ec2:DescribeTags",
                  "ec2:DescribeSnapshots",
                  "ec2:DescribeVolumes",
                  "ec2:DescribeVolumeStatus",
                  "SNS:Publish"
                ],
                "Resource": "*"
            }
        ]
    }

  4 - In the role created to be used by this Lambda, add the above policy.

  5 - Create a Cloud Watch Event with the Lambda as the target. You can configure it to run in a scheduled way every 5 minutes.

Some observations about this solution/code:
  - This is a simple code and doesn't have implemented exponential backoff or retries. This means that it might fail in accounts with many volumes.
  - It is region-based, if you want to monitor more than one region, you can deploy the same code in each region, or you can change the code to get information in more than one region.


More information: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_volume_status

