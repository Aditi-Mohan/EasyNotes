from datetime import time, datetime

class Session:
    # primary key
    int session_id
    # foreign key
    int user_id
    # foreign key
    int subject_id
    # foreign key
    int note_id
    # foreign key - multivalued attribute
    int topic_ids[]

    datetime date
    time session_duration

# one to many relationship - user -> session