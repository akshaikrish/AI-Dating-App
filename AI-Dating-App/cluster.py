import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import fetchUsers

n=1
def clustering(user_ID, data):
    global n
    # user_ID = 7

    # Extract the survey answers
    
    print("FUNCTION CALLED AGAIN " + str(n) +" times ")
    survey_answers = data.iloc[:, 1:]

    # Perform label encoding on the survey answers
    label_encoder = LabelEncoder()
    survey_answers_encoded = survey_answers.apply(label_encoder.fit_transform)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(survey_answers_encoded)

    # Add the cluster labels to the DataFrame
    data['Cluster'] = kmeans.labels_

    # Print the cluster assignments
    print(data[['surveyUserId', 'Cluster']])

    cluster_value = data.loc[data['surveyUserId'] == user_ID, 'Cluster'].values[0]
    cluster_data = data[data['Cluster'] == cluster_value]

    print(cluster_data.shape[0])
    # print("cluster data : ")
    # print(cluster_data)

    if cluster_data.shape[0] > 11:
        n += 1
        updated_cluster_data = clustering(user_ID, data=cluster_data)  # Recursive call
    else:
        updated_cluster_data = cluster_data  # Use the current cluster_data if the condition is not met


    if isinstance(updated_cluster_data, pd.DataFrame):
        updated_cluster_data = updated_cluster_data.drop(updated_cluster_data[updated_cluster_data['surveyUserId'] == user_ID].index)
        userID_list = updated_cluster_data['surveyUserId'].tolist()  # Convert the Series to a list
        # print("Printing updated_cluster_data:")
        # print(updated_cluster_data)
        # print("Printing userID_list:")
        # print(type(userID_list))
        return userID_list
    else:
        # Return the original cluster_data as a list if the recursive call returns a list
        return updated_cluster_data

# survey_data = fetchUsers.fetch_answers()
# clustering('ed8c023f-6886-453b-a778-9238fcf979e7', survey_data)
