from datetime import datetime

class Friend:
    # one to one relationship form user to user
    # primary key of user
    friend_id = None
    name = None
    college = None
    course = None
    semester = None
    added_on = None
    notes_sent = None
    notes_received = None
    last_interaction = None

    def __init__(self, friend_id, name, college, course, semester, added_on, notes_sent, notes_received, last_interaction):
        self.friend_id = friend_id
        self.name = name
        self.college = college
        self.course = course
        self.semester = semester
        self.added_on = added_on
        self.notes_sent = notes_sent
        self.notes_received = notes_received
        self.last_interaction = last_interaction

#  f.user2, u.name, u.college, u.course, u.semester, f.added_on, f.notes_sent, f.notes_received 