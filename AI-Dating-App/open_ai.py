from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import cluster
import pandas as pd
import random
import ast
import fetchUsers

openai.api_key = "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"
app = Flask(__name__)
CORS(app)



# print(completion['choices'][0]['message']['content'])
def getProfiles(userIDs):
    profiles = []
    i= random.randint(10, 100)
    for _ in range(10):
        id = i +1
        i+=1
        name = random.choice(["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn"])
        age = random.randint(20, 35)
        interests = random.sample(["reading", "cooking", "hiking", "painting", "traveling", "dancing"], 2)
        favourite_food = random.choice(["pizza", "sushi", "chocolate", "pasta", "ice cream"])
        ambition = random.choice(["become a chef", "start my own business", "travel the world", "become an artist"])
        image = ''
        bio = ''
        gender = 'Female'
        lookingfor = 'Male'

        profile = {
            'id': id,
            'name': name,
            'age': age,
            'image':image,
            'bio' : bio,
            'gender' : gender,
            'lookingfor' : lookingfor
        }

        profiles.append(profile)
    return profiles

def sort_profiles(userID):
    # user_details is a dictionary containing the details of the user in question
    # profiles is a list of dictionaries, each representing a profile with details

    # Create a list to store the sorted profiles
    profiles = []
    sorted_profiles = []
    data = fetchUsers.fetch_answers()
    current_user_profile = fetchUsers.fetch_current_user(userID)
    # Call the clustering function from the cluster module
    clustered_userID_list = cluster.clustering(userID, data)

    # Extract content from userID_list 
    # content_to_pass = userID_list[0]  # Replace 'content_column_name' with the appropriate column name
    print(clustered_userID_list)

    profiles = fetchUsers.fetch_user_by_id(clustered_userID_list)

    
    user_name = current_user_profile['name']['S']
    user_age = current_user_profile['age']['S']
    user_interests = current_user_profile.get('interests', {}).get('S', '')  # Handle possible missing attributes
    user_favourite_food = current_user_profile.get('favouritefood', {}).get('S', '')  # Handle possible missing attributes
    user_ambition = current_user_profile.get('ambition', {}).get('S', '') 

    content_to_pass = f"My name is {user_name}. I am {user_age} years old. My interests are {user_interests}. My favourite food is {user_favourite_food}, " \
                      f"and my ambition is {user_ambition}. With the list of profiles I have sent you, I need you to " \
                      "select 3 profiles and sort them in the order of those more likely to match comes first. " \
                      "arr is an integer array containing IDs [provided with each profile] of the profiles in sorted order. Your Response should be just arr = [whatever is the solution]\n\n" + "\n\n"

    # List to store the formatted profile messages
    profile_messages = []
    print(content_to_pass)


    # Iterate through each profile and generate chat messages
    for profile in profiles:
        id = profile['id']['S']
        name = profile['name']['S']
        age = profile['age']['S']
        interests = profile.get('interests', {}).get('S', '')  # Handle possible missing attributes
        favourite_food = profile.get('favouritefood', {}).get('S', '')  # Handle possible missing attributes
        ambition = profile.get('ambition', {}).get('S', '')  # Handle possible missing attributes

        # Construct the profile message
        profile_message = f"(ID: {id}) My name is {name}. I am {age} years old. My interests are {interests}. " \
                        f"My favourite food is {favourite_food}, and my ambition is to {ambition}."
        
        print(profile_message)
        # Append the profile message to the list
        profile_messages.append(profile_message)

    # Construct the full messages list for OpenAI API
    messages = [
        {'role': 'user', 'content': content_to_pass},  # User message
        
        # Add profile messages as user messages with a unique identifier
        *[{'role': 'user', 'content': f"Profile {i+1}: {message}"} for i, message in enumerate(profile_messages)]
    ]

    # Add profile messages to the messages list
   
    # Call the OpenAI API for chat completions
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0
    )

#         # Extract the response from GPT-3
    response = completion['choices'][0]['message']['content']

    # print("response ", response)
    response_list_str = response.split('arr = ')[1].split('\n')[0]
    profile_ids_str = response_list_str.strip('[]').split(', ')  # Remove surrounding brackets and split into separate IDs

    sorted_id_list = profile_ids_str
    print(sorted_id_list)
    # sorted_id_list will contain the profile IDs
    return sorted_id_list

    


@app.route('/get_sorted_profiles', methods=['POST'])
def get_sorted_profiles():
    # Receive the user ID from the request
    user_ID = request.json['user_ID']

    # Generate random profiles for the user
    profiles = sort_profiles(user_ID)
    print("Suitable profiles : ", profiles)

    # Sort the profiles using sort_profiles_by_matching function
    sorted_profiles = fetchUsers.fetch_user_by_id(profiles)

    # Return the sorted profiles as a JSON response
    print("Sending profiles")
    return jsonify(sorted_profiles)

   

# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
# sort_profiles('424ce5f1-e976-4663-81e3-52f5b8b77113')




