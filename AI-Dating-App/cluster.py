import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

def clustering():
    user_ID = 2

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv('survey.csv')

    # Extract the survey answers
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
    print(data[['User ID', 'Cluster']])


    cluster_value = data.loc[data['User ID'] == user_ID, 'Cluster'].values[0]
    cluster_data = data[data['Cluster'] == cluster_value]
    updated_cluster_data = cluster_data.drop(cluster_data[cluster_data['User ID'] == user_ID].index)
    print(updated_cluster_data['User ID'])
    return updated_cluster_data

clustering()