from datetime import datetime

class Friend:
    # many to many relationship form user to user
    # primary key of user
    int user_id
    # primary key of user(friend)
    int friend_id

    # descriptive attributes
    int number_of_shared_notes
    datetime last_interaction
    double frequency
