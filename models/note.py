from datetime import datetime as dt

class Note:
    # primary key
    note_id = None
    note_title = None
    # foreign key
    user_id = None
    num_of_bookmarks = None
    subject_id = None
    unit_id = None

    datetime_of_creation = None
    link = None
    shared_from = None
    summarised = None
    topics = []

    def __init__(self, note_id, title, uid, sub_id, unit_id, dt_of_creation, link, num_of_bookmarks, shared_from, summarised):
        self.note_id = note_id
        self.note_title = title
        self.user_id = uid
        self.subject_id = sub_id
        self.unit_id = unit_id
        self.datetime_of_creation = dt_of_creation
        self.link = link
        self.num_of_bookmarks = num_of_bookmarks
        self.shared_from = shared_from
        self.summarised = summarised

# one to many relationship - user -> notes
# one to many relationship - subject -> notes
# identifying relationship of shared notes