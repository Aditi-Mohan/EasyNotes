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
latest_notes_loaded = False
latest_notes = []
quick_links_from_names_loaded = False


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
    print('select * from units where uid={} and sub_id={}'.format(uid, sub_id))
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
    link = await add_subpage_to_notion(user.token, user.homepage_url, name)
    q = 'insert into subject (sub_name, uid, fac_name, r, g, b, a, link) values(%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (name, uid, fac_name, color[0], color[1], color[2], color[3], link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_unit(name, sub_name, sub_id, uid):
    link = await add_unitpage_to_notion(user.token, user.homepage_url, name, sub_name)
    q = 'insert into units (sub_id, uid, unit_name, link) values(%s, %s, %s, %s)'
    params = (sub_id, uid, name, link)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def add_note(sub_id, uid, unit_id, title, dt_of_creation, link, num_of_bookmarks):
    q = 'insert into notes (note_title, uid, sub_id, unit_id, datetime_of_creation, link, num_of_bookmarks) values(%s, %s, %s, %s, %s, %s, %s)'
    params = (title, uid, sub_id, unit_id, dt_of_creation, link, num_of_bookmarks)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    global latest_notes, latest_notes_loaded
    await clean_up()
    latest_notes_loaded = False
    latest_notes = []
    # print('insert into notes values({}, {}, {}, {}, {}, {})'.format(title, uid, sub_id, unit_id, dt_of_creation, link))

async def put_last_active(dt):
    q = 'update user set last_login=%s where uid=%s'
    params = (dt, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def get_latest_notes():
    global latest_notes_loaded
    if not latest_notes_loaded:
        q = 'create view latest_notes_%s as select * from notes where uid=%s order by datetime_of_creation desc limit 10;'
        db.mycursor.execute(q, (user.uid, user.uid))
        db.mydb.commit()
        latest_notes_loaded = True
    viewname = 'latest_notes_'+str(user.uid)
    q = 'select * from {}'.format(viewname)
    db.mycursor.execute(q)
    res = db.mycursor.fetchall()
    nt = [Note(*x) for x in res]
    global latest_notes
    latest_notes = nt

async def clean_up():
    if latest_notes_loaded:
        viewname = 'latest_notes_'+str(user.uid)
        q = 'drop view {}'.format(viewname)
        db.mycursor.execute(q)
        db.mydb.commit()
    # viewname = 'quick_links_from_names_'+str(user.uid)
    # q = 'drop view {}'.format(viewname)
    # db.mycursor.execute(q)
    # db.mydb.commit()

def get_color_for_sub(sub_id):
    for each in subjects:
        if each.subject_id == sub_id:
            return each.color

def get_name_for_sub(sub_id):
    for each in subjects:
        if each.subject_id == sub_id:
            return each.subject_name

async def get_name_for_unit(sub_id, sub_name, unit_id):
    if sub_name not in units.keys():
        await get_units_for(user.uid, sub_id, sub_name)
    for each in units[sub_name]:
        if each.unit_id == unit_id:
            return each.unit_name

async def get_link_for_latest(sub_id, unit_id, note_id):
    q = 'select link from latest_notes_%s where sub_id=%s and unit_id=%s and note_id=%s'
    params = (user.uid, sub_id, unit_id, note_id)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res[0][0]

async def get_quick_links_from_names(sub_name, unit_name, note_title):
    global quick_links_from_names_loaded
    if not quick_links_from_names_loaded:
        q = 'create view quick_links_from_names_%s as select s.sub_name, u.unit_name, n.note_title, n.link from notes n inner join units u on n.unit_id=u.unit_id inner join subject s on s.sub_id=u.sub_id where s.uid=%s;'
        db.mycursor.execute(q, (user.uid, user.uid))
        db.mydb.commit()
        quick_links_from_names_loaded = True
    q = 'select * from quick_links_from_names_%s where sub_name=%s and unit_name=%s and note_title=%s'
    params = (user.uid, sub_name, unit_name, note_title)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    print(res)
    if len(res) == 1:
        print(res)
    else:
        print('couldn\'t determine')
