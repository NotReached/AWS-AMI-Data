import boto3
import json
import botocore.exceptions
import sys

ec2client = boto3.client('ec2')

#Exception Handling
try:
    testaccess = ec2client.describe_instances()
except botocore.exceptions.NoCredentialsError as error:
    print('No credentials detected in  ~/.aws/credentials')
    print('   Learn more here https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html')
    sys.exit(1)
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'UnauthorizedOperation':
        print('You are not authorized to perform this operation. Please check with your IAM Administrator.')
    else:
        raise error
    sys.exit(1)

#Add all AMIs in use on the account to the list 'account_amis'
account_amis = []
ami_sorting = ec2client.describe_instances()
for reservation in ami_sorting["Reservations"]:
    for ami in reservation["Instances"]:
        account_amis.append(ami["ImageId"])

#Pulls image data filtered by 'account_amis'
response = ec2client.describe_images(
    Filters=[
        {
            'Name': 'image-id',
            'Values': account_amis
        },
    ],
)

#This creates a dictionary with the keys being AMIS and the values being lists of instanceIds
instance_dict = {'null': ['null']}
instance_count = len(account_amis)
iterator=0
while iterator < instance_count:
    iterative_ami = ami_sorting['Reservations'][iterator]['Instances'][0]['ImageId']
    iterative_instance = ami_sorting['Reservations'][iterator]['Instances'][0]['InstanceId']
    if iterative_ami in instance_dict:
        instance_dict[iterative_ami].append(iterative_instance)
    else:
        instance_dict[iterative_ami] = [iterative_instance]
    iterator += 1

#This is the AMI + data output loop
image_count = len(response['Images'])
iterator=0
while iterator < image_count:
    for line in response['Images'][iterator]['ImageId']:
        ami_validate = response['Images'][iterator]['ImageId']
        if ami_validate in instance_dict:
            instance_id_validate = instance_dict[ami_validate]
        else:
            instance_id_validate = 'null'
        images_dict = {ami_validate: {
                    'ImageDescription': response['Images'][iterator]['Description'],
                    'ImageName': response['Images'][iterator]['Name'],
                    'ImageLocation': response['Images'][iterator]['ImageLocation'],
                    'OwnerId': response['Images'][iterator]['OwnerId'],
                    'InstanceIds': instance_id_validate
                     }
                 }
    json_formatter = json.dumps(images_dict, indent=2)
    print(json_formatter)
    iterator += 1