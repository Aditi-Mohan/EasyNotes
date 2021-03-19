from models.subject import Subject
from models.note import Note
from models.units import Units
import asyncio
import dbconn as db
from datetime import datetime
from functions.write_transcript_to_notion import add_subpage_to_notion, add_unitpage_to_notion, verify_token

user = None
subjects = []
notes = {}
units = {}

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

async def get_units_for(uid, sub_id, sub_name):
    q = 'select * from units where uid=%s and sub_id=%s'
    db.mycursor.execute(q, (uid, sub_id))
    res = db.mycursor.fetchall()
    print(len(res))
    uts = [Units(*x) for x in res]
    global units
    units[sub_name] = uts

async def get_notes_for(uid, sub_id, unit_id, unit_name, sub_name):
    print('select * from notes where uid={} and sub_id={} and unit_id={}'.format(uid, sub_id, unit_id))
    q = 'select * from notes where uid=%s and sub_id=%s and unit_id=%s'
    db.mycursor.execute(q, (uid, sub_id, unit_id))
    res = db.mycursor.fetchall()
    print(len(res))
    nt = [Note(*x) for x in res]
    global notes
    if sub_name in notes.keys():
        notes[sub_name][unit_name] = nt
    else:
        notes[sub_name] = {unit_name: nt}
    print(notes)

async def add_user(name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login):
    token_valid = await verify_token(token)
    if token_valid:
        url_valid = await verify_homepage_url(homepage_url)
        if url_valid:
            # verify email
            q = 'insert into user (name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            params = (name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login)
            db.mycursor.execute(q, params)
            db.mydb.commit()

async def add_subject(name, uid, fac_name, color):
    link = await add_subpage_to_notion(name)
    q = 'insert into subject (sub_name, uid, fac_name, r, g, b, a, link) values(%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (name, uid, fac_name, color[0], color[1], color[2], color[3], link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_unit(name, sub_name, sub_id, uid):
    link = await add_unitpage_to_notion(name, sub_name)
    q = 'insert into units (sub_id, uid, unit_name, link) values(%s, %s, %s, %s)'
    params = (sub_id, uid, name, link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_note(sub_id, uid, unit_id, title, dt_of_creation, link):
    q = 'insert into notes (note_title, uid, sub_id, unit_id, datetime_of_creation, link) values(%s, %s, %s, %s, %s, %s)'
    params = (title, uid, sub_id, unit_id, dt_of_creation, link)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    print('insert into notes values({}, {}, {}, {}, {}, {})'.format(title, uid, sub_id, unit_id, dt_of_creation, link))
