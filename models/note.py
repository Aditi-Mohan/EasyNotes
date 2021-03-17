from datetime import datetime as dt

class Note:
    # primary key
    note_id = None
    note_title = None
    # foreign key
    user_id = None
    # foreign key
    session_id = None
    # foreign key
    subject_id = None
    datetime_of_creation = None
    link = None
    topics = []

    def __init__(self, note_id, title, uid, sub_id, dt_of_creation, link):
        self.note_id = note_id
        self.note_title = title
        self.user_id = uid
        self.subject_id = sub_id
        self.datetime_of_creation = dt_of_creation

# one to many relationship - user -> notes
# one to many relationship - subject -> notes
# identifying relationship of shared notes