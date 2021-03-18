class Units:
    # primary key
    unit_id = None
    unit_name = None
    link = None

    # foreign key
    sub_id = None
    uid = None

    def __init__(self, unit_id, sub_id, uid, unit_name, link):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.link = link
        self.sub_id = sub_id
        self.uid = uid
