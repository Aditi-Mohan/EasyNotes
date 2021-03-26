from datetime import datetime

class User:
    # primary key
    uid = None

    name = None
    password = None
    email = None
    college = None
    course = None
    semester = None
    total_session = None
    # unique
    token = None
    # unique
    homepage_url = None
    last_login = None

    def __init__(self, uid, name, email, college, course, semester, total_session, token, homepage_url, password, last_login):
        self.uid = uid
        self.name = name
        self.password = password
        self.email = email
        self.college = college
        self.course = course
        self.semester = semester
        self.total_session = total_session
        self.token = token
        self.homepage_url = homepage_url
        self.last_login = last_login # datetime.strptime(last_login, r'%Y-%m-%d %H:%M:%S')
    
def create_new_user():
    return User(None, None, None, None, None, None, None, None, None, None, None)

# relations partiipating in - 
# friends -> many to many
# subjects -> one to many
# notes (shared notes) -> one to one
# and more