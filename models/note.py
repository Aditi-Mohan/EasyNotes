from datetime import datetime as dt

class Note:
    # primary key
    int note_id
    # foreign key
    int user_id
    # foreign key
    int session_id
    # foreign key
    int subject_id
    
    string topics[]
    dt time_of_creation

# one to many relationship - user -> notes
# one to many relationship - subject -> notes
# identifying relationship of shared notes