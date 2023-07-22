import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Users')

response = table.get_item(
    Key={
        'id': 3,
    }
)

if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    item = response['Item']
    print(item)
else:
    print('Failed to get item')
 