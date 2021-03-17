from models.subject import Subject
from models.note import Note
from models.units import Units
import asyncio
import dbconn as db
from datetime import datetime
from functions.write_transcript_to_notion import add_subpage_to_notion, add_unitpage_to_notion

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

async def get_notes_for(uid, sub_id, unit_id, unit_name):
    q = 'select * from notes where uid=%s and sub_id=%s and unit_id=%s'
    db.mycursor.execute(q, (uid, sub_id, unit_id))
    res = db.mycursor.fetchall()
    print(len(res))
    nt = [Note(*x) for x in res]
    global notes
    notes[unit_name] = nt

async def add_subject(name, uid, fac_name, color):
    link = await add_subpage_to_notion(name)
    q = 'insert into subject values(%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (name, uid, fac_name, color[0], color[1], color[2], color[3], link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_unit(name, sub_name, sub_id, uid):
    link = await add_unitpage_to_notion(name, sub_name)
    q = 'insert into units (sub_id, uid, unit_name, link) values(%s, %s, %s, %s)'
    params = (sub_id, uid, name, link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_note(sub_id, uid, unit_id, note_id, title, link):
        q = 'insert into notes values(%s, %s, %s, %s, %s, %s, %s)'
        db.mycursor.execute(q, (note_id, title, uid, sub_id, unit_id, datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"), link))
        db.mydb.commit()
