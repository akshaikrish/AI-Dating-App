import csv
import random

# Specify the number of rows and columns for your dataset
num_rows = 100  # Number of rows
num_columns = 5  # Number of columns

# Specify the headers for your dataset
headers = ["User ID", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]
my_list = ["Likely", "Unlikely", "Don't Know"]
columns = []

# Generate random data for each column
data = []
for _ in range(num_rows):
    row = [my_list[random.randint(0, 2)] for _ in range(num_columns)]
    data.append(row)


# Write the data to a CSV file
with open("survey.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for i, row in enumerate(data, start=1):
        writer.writerow([i] + row)
