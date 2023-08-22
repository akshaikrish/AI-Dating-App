from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table_name = 'SurveyPrompts-k2zzr3pxyzdyjdppvtdgwj2dxu-staging'  
table = dynamodb.Table(table_name)

def storeAnswers(ans):

    user_ID = ans[0]
    print(f'user : {user_ID}')
    p1, p2, p3, p4,p5 = ans[1:]  # separating the prompts from the 'ans' array

    response = table.get_item(Key={'id': user_ID})
    print(response)
    if 'Item' in response:
        # Update the answers if user ID already exists
        table.update_item(
            Key={'id': user_ID},
            UpdateExpression='SET Prompt1 = :p1, Prompt2 = :p2, Prompt3 = :p3, Prompt4 = :p4, Prompt5 = :p5',
            ExpressionAttributeValues={
                ':p1': p1,
                ':p2': p2,
                ':p3': p3,
                ':p4': p4,
                ':p5': p5
            }
        )
        print(f"Survey Prompts of {user_ID} updated")
    else:
        # Create a new entry if user ID doesn't exist
        item = {
            'id': user_ID,
            'Prompt1': p1,
            'Prompt2': p2,
            'Prompt3': p3,
            'Prompt4': p4,
            'Prompt5': p5
        }
        table.put_item(Item=item)
        print(f'New entry created for {user_ID}')


@app.route('/submitSurvey', methods=['POST'])
def submit_survey():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        print(answers)
        storeAnswers(answers)
      

        return jsonify({'message': 'Answers received successfully'}), 200
    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Error processing request'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
