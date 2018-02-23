import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('movies')
print(table.creation_date_time)
print(table.scan())