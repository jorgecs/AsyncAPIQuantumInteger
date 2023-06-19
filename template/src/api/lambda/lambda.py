import zipfile
import zlib
import boto3
import time
import shutil
import os

if not os.path.exists('./src/api/lambda/index.zip'):

    shutil.make_archive('./src/api/lambda/index',
                        'zip',
                        './src/api/lambda/',
                        'node_modules')

    zip = zipfile.ZipFile('./src/api/lambda/index.zip','a')

    zip.write('./src/api/lambda/index.js', os.path.basename('./src/api/lambda/index.js'))

    zip.close()

with open('./src/api/lambda/index.zip', 'rb') as f:
	zipped_code = f.read()


lambda_Client = boto3.client('lambda')
response = lambda_Client.create_function(
            Code=dict(ZipFile=zipped_code),
            Description='Lambda to send MQTT message with the result of the quantum computer.',
            Timeout=15,
            FunctionName='asyncapi_lambda',
            Handler='index.handler',
            Publish=True,
            {%- set lambda = asyncapi.ext('x-quantum-awslambda') %}
            Role='{{lambda.role_arn}}',
            Runtime='nodejs16.x',
        )

response = lambda_Client.get_function(FunctionName='asyncapi_lambda')
arn = response['Configuration']['FunctionArn']

sts = boto3.client("sts")
account_id = sts.get_caller_identity()["Account"]

response = lambda_Client.add_permission(
     FunctionName=arn,
     StatementId='1',
     Action='lambda:InvokeFunction',
     Principal='s3.amazonaws.com',
     SourceArn='arn:aws:s3:::'+'{{lambda.s3_bucket}}',
     SourceAccount=account_id
)


time.sleep(3)
     
lambda_Client = boto3.client('lambda')
response = lambda_Client.get_function(FunctionName='asyncapi_lambda')
arn = response['Configuration']['FunctionArn']


client = boto3.resource('s3')
bucket_name = '{{lambda.s3_bucket}}'
bucket_notification = client.BucketNotification(bucket_name)
response = bucket_notification.put(
    NotificationConfiguration={'LambdaFunctionConfigurations': [
        {
            'LambdaFunctionArn': arn,
            'Events': [
                's3:ObjectCreated:*'
            ],
        },
    ]}
)    
