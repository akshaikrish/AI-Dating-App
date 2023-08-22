import boto3
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize a DynamoDB resource
region = 'eu-west-2'

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb', region_name=region)

app2 = Flask(__name__)
CORS(app2)

# Replace 'YourTableName' with the actual name of your table
table = 'Likes'

def check_if_match(userID_1, userID_2):
    try:
        response = dynamodb_client.get_item(
            TableName=table,
            Key={
                'userUD': {'S': userID_1}
            }
        )   
        current_liked_users_list = response.get('Item', {}).get('LikedUsers', {}).get('L', [])
       
        if any(user.get('S') == userID_2 for user in current_liked_users_list):
            print(f"{userID_2} exists in the liked users list.")
            # return
        else:
            updated_liked_users_list = current_liked_users_list + [{'S': userID_2}]
            dynamodb.update_item(
                TableName=table,  # Replace with your table name
                Key={'userUD': {'S': userID_1}},
                UpdateExpression='SET likedUsers = :new_liked_users',
                ExpressionAttributeValues={':LikedUsers': {'L': updated_liked_users_list}}
            )
        response = dynamodb_client.get_item(
            TableName=table,
            Key={
                'userUD': {'S': userID_2}
            }
        )
        current_liked_user_2_list = response.get('Item', {}).get('LikedUsers', {}).get('L', []) 
        if any(user.get('S') == userID_1 for user in current_liked_user_2_list):
            print(f"{userID_2} and {userID_1} is a match")
            return True
        else:
            print("Not a match")
            return False
        
    except Exception as e:
        print("Error fetching data:", e)

    

# check_if_match('ed8c023f-6886-453b-a778-9238fcf979e7','424ce5f1-e976-4663-81e3-52f5b8b77113')
@app2.route('/check_match', methods=['POST'])
def check_match():
    userID_A = request.json['userID_1']
    userID_B = request.json['userID_2']

    isMatch = check_if_match(userID_A,userID_B)
    print(isMatch)
    return isMatch

if __name__ == '__main__':
    app2.run(host='0.0.0.0', port=5002)