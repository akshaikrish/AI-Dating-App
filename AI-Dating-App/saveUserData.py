from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table_name = 'User-k2zzr3pxyzdyjdppvtdgwj2dxu-staging'  
table = dynamodb.Table(table_name)

def send_user_data(user):
    try:
        user_id = None
        user_attributes = {}
        
        # Extracting data from user_data list of dictionaries
        for item in user:
            label = item.get('label')
            value = item.get('value')
            if label == 'User ID':
                user_id = value
            else:
                user_attributes[label] = value
        
        if user_id:
            # Check if user ID already exists
            response = table.get_item(Key={'id': user_id})
            if 'Item' in response:
                # Update the user's attributes if user ID exists
                update_expression = 'SET ' + ', '.join([f'#attr_{attr} = :{attr}' for attr in user_attributes.keys()])
                expression_attribute_names = {f'#attr_{attr}': attr for attr in user_attributes.keys()}
                expression_attribute_values = {f':{attr}': user_attributes[attr] for attr in user_attributes.keys()}
                
                table.update_item(
                    Key={'id': user_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeNames=expression_attribute_names,
                    ExpressionAttributeValues=expression_attribute_values
                )
                print(f"User data of {user_id} updated")
            else:
                # Create a new entry if user ID doesn't exist
                user_attributes['id'] = user_id
                table.put_item(Item=user_attributes)
                print(f'New user entry created for {user_id}')
        else:
            print('User ID not found in user data')
        
        return True
    except Exception as e:
        print('Error:', e)
        return False

    


@app.route('/saveUser', methods=['POST'])
def save_user():
    try:
        data = request.get_json()
        user_data = data.get('user_data', [])
        send_user_data(user_data)
      

        return jsonify({'message': 'Answers received successfully'}), 200
    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Error processing request'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
