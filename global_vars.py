from models.subject import Subject
import asyncio
import dbconn as db

user = None
subjects = []
notes = []

async def get_subs(uid):
    q = 'select * from subject where uid=%s'
    db.mycursor.execute(q, (uid,))
    subs = db.mycursor.fetchall()
    print(subs)
    global subjects
    subjects = [Subject(*x) for x in subs]
    for each in subjects:
        print(each.subject_name)
    return