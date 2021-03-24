from datetime import datetime

class FriendRequests:
    # foreign key
    req_from = None
    sent_on = None
    comments = None
    name = None
    college = None
    course = None
    semester = None

    def __init__(self, req_from, sent_on, comments, name, college, course, semester):
        self.req_from = req_from
        self.sent_on = sent_on
        self.name = name
        self.comments = comments
        self.college = college
        self.course = course
        self.semester = semester