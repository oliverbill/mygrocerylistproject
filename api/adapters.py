import ast

# import boto3
# from botocore.exceptions import ClientError

# class GCloudServices:
#     from google.cloud import storage
#     from google.cloud.api.api import
#
#     def get_gcp_secret(self):
#

class AwsServices():
    def get_aws_secret(secret_name):
        region_name = "us-east-1"
        session = boto3.session.Session()
        client = session.client(
            aws_access_key_id = 'AKIA22TA45G7EQIKXLSW',
            aws_secret_access_key= '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',
            service_name='secretsmanager',
            region_name=region_name,
        )
        try:
            secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            elif e.response['Error']['Code'] == 'DecryptionFailure':
                print("The requested secret can't be decrypted using the provided KMS key:", e)
            elif e.response['Error']['Code'] == 'InternalServiceError':
                print("An error occurred on service side:", e)
        else:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary, only one of these fields will be populated
            if 'SecretString' in secret_value_response:
                text_secret_data = secret_value_response['SecretString']

        dict_response = ast.literal_eval(text_secret_data)
        return dict_response

# get_aws_secret('rds!db-dd27cb78-20f7-4a97-bf98-2cdd9939be9c')