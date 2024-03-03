import boto3

# Create an S3 client
s3 = boto3.client('s3')

bucket_name = 'exploration-876679093433-ew1-initiative-grm-esg-sandbox'
object_key = 'takehome_assignment/customer_exposure.csv'

# Download the file
s3.download_file(bucket_name, object_key, 'customer_exposure.csv')
