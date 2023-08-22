import boto3
import pandas as pd

# Initialize a DynamoDB resource
region = 'eu-west-2'

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb', region_name=region)



# Replace 'YourTableName' with the actual name of your table
table = dynamodb.Table('User-k2zzr3pxyzdyjdppvtdgwj2dxu-staging')

def fetch_current_user(profile_id):
    try:
        response = dynamodb_client.get_item(
            TableName='User-k2zzr3pxyzdyjdppvtdgwj2dxu-staging',
            Key={'id': {'S': profile_id}}
        )

        item = response.get('Item', {})
        if item:
            print("Profile ID:", item.get('id', {}).get('S'))
            print("Name:", item.get('name', {}).get('S'))
            print("Age:", item.get('age', {}).get('S'))
            # Add more fields as needed
            
            print()  # Empty line for separation
            return item
        else:
            print("User not found")
            return None
    except Exception as e:
        print("Error fetching data:", e)


surveyTable = dynamodb.Table('Survey-k2zzr3pxyzdyjdppvtdgwj2dxu-staging')

def fetch_answers():
    try:
        response = surveyTable.scan()  # Use scan or query based on your needs
        items = response.get('Items', [])
        for item in items:
            print(item)
        df = pd.DataFrame(items)

        # Filter columns
        columns = ['surveyUserId', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']
        df = df[columns]
        print(df)
        return df
    except Exception as e:
        print("Error fetching data:", e)

def fetch_user_by_id(id_list):
    try:
        response = dynamodb_client.batch_get_item(
            RequestItems={
                'User-k2zzr3pxyzdyjdppvtdgwj2dxu-staging': {
                    'Keys': [{'id': {'S': profile_id}} for profile_id in id_list],
                }
            }
        )
        
        items = response.get('Responses', {}).get('User-k2zzr3pxyzdyjdppvtdgwj2dxu-staging', [])
        # print(items)
        for item in items:
            print("Profile ID:", item['id']['S'])
            print("Name:", item['name']['S'])
            print("Age:", item['age']['S'])
            # Add more fields as needed
            
            print()  # Empty line for separation
        return items
    except Exception as e:
        print("Error fetching data:", e)

# List of profile IDs you want to fetch
ids = ['ed8c023f-6886-453b-a778-9238fcf979e7', '424ce5f1-e976-4663-81e3-52f5b8b77113']
# fetch_user_by_id(ids)
# fetch_answers()
fetch_current_user('ed8c023f-6886-453b-a778-9238fcf979e7')