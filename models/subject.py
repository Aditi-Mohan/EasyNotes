class Subject:
    # primary key
    subject_id = None
    # foreign key
    uid = None

    subject_name = None
    faculty_name = None
    units = []
    color = None
    link = None

    def __init__(self, subject_id, subject_name, uid, fac_name, r, g, b, a, link):
        self.subject_id = subject_id
        self.uid = uid
        self.subject_name = subject_name
        self.faculty_name = fac_name
        self.color = (r, b, g, a)
        self.link = link

# relations participating in - 
# notes -> one to many
# topics -> many to many