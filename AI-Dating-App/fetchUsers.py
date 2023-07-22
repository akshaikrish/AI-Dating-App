from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import cluster

# Create the database engine
engine = create_engine('')

# Create a session factory
Session = sessionmaker(bind=engine)

# Assuming you have a list of user IDs


# Create a session
session = Session()
data = cluster.clustering()
print(data)

for user_id in user_ids:
    # Assuming you have a User model mapped to the 'users' table
    User = Table('users', MetaData(bind=engine), autoload=True)
    
    # Fetch the user data using the user ID
    user_data = session.query(User).filter(User.c.user_id == user_id)

    # Process and utilize the fetched data
    # Example: Print the user data
    print(user_data)

# Close the session
session.close()

