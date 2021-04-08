from models.user import User
from models.subject import Subject
from models.note import Note
from models.units import Units
from models.friend_requests import FriendRequests
from models.friend import Friend
from models.notificatins import Notitification
from models.share_request import ShareRequest
import asyncio
import dbconn as db
from datetime import datetime
from functions.write_transcript_to_notion import add_subpage_to_notion, add_unitpage_to_notion, verify_token

user = None
newuser = None
subjects = []
notes = {}
units = {}
latest_notes_loaded = False
latest_notes = []
quick_links_from_names_loaded = False
pending = []
friends = []
notifs = []
pending_shares = []
new_usernm = ''
pass_changed = False
signed_out = False

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

# async def add_user(name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login):
#     token_valid = await verify_token(token)
#     if token_valid:
#         url_valid = await verify_homepage_url(homepage_url)
#         if url_valid:
#             # verify email
#             q = 'insert into user (name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#             params = (name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login)
#             db.mycursor.execute(q, params)
#             db.mydb.commit()

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

async def add_note(sub_id, uid, unit_id, title, dt_of_creation, link, num_of_bookmarks, shared_from):
    q = 'insert into notes (note_title, uid, sub_id, unit_id, datetime_of_creation, link, num_of_bookmarks, shared_from) values(%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (title, uid, sub_id, unit_id, dt_of_creation, link, num_of_bookmarks, shared_from)
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
        q = 'drop view if exists {}'.format(viewname)
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

async def is_uid_valid(uid):
    q = 'select uid from user'
    db.mycursor.execute(q)
    res = db.mycursor.fetchall()
    print(uid in [x[0] for x in res])
    if uid in [x[0] for x in res]:
        return True
    else: return False

async def send_friend_request(req_to, comments, dt):
    q = 'select * from friend_requests where req_from=%s and req_to=%s'
    params = (user.uid, req_to)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) == 0:
        q = 'select * from friends where (user1=%s and user2=%s) or (user1=%s and user2=%s)'
        params = (user.uid, req_to, req_to, user.uid)
        db.mycursor.execute(q, params)
        res = db.mycursor.fetchall()
        if len(res) == 0:
            q = 'insert into friend_requests values(%s, %s, %s, %s)'
            params = (user.uid, req_to, dt, comments)
            db.mycursor.execute(q, params)
            db.mydb.commit()
        else:
            print('already friends')
    else:
        print('already requested')

async def get_pending_friend_requests():
    q = 'select p.req_from, p.sent_on, p.comments, u.name, u.college, u.course, u.semester from friend_requests p inner join user u on p.req_from=u.uid where p.req_to=%s'
    db.mycursor.execute(q, (user.uid,))
    res = db.mycursor.fetchall()
    global pending
    pending = [FriendRequests(*x) for x in res]

async def accept_friend_request(req_from, dt):
    q = 'insert into friends values(%s, %s, %s, %s, %s, %s)'
    params = (user.uid, req_from, dt, 0, 0, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'delete from friend_requests where req_from=%s and req_to=%s'
    params = (req_from, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = 'Friend Request Accepted by '+user.name
    params = (req_from, notif_title, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def reject_friend_request(req_from, dt):
    q = 'delete from friend_requests where req_from=%s and req_to=%s'
    params = (req_from, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = 'Friend Request Rejected by '+user.name
    params = (req_from, notif_title, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def get_friends():
    q = 'select f.user2, u.name, u.college, u.course, u.semester, f.added_on, f.notes_sent, f.notes_received, f.last_interaction from user u inner join friends f on u.uid=f.user2 where f.user1=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res1 = db.mycursor.fetchall()
    q = 'select f.user1, u.name, u.college, u.course, u.semester, f.added_on, f.notes_received, f.notes_sent, f.last_interaction from user u inner join friends f on u.uid=f.user1 where f.user2=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res2 = db.mycursor.fetchall()
    global friends
    friends = [Friend(*x) for x in res1]
    friends = [*friends, *[Friend(*x) for x in res2]]

async def remove_friend(fid, dt):
    q = 'delete from friends where (user1=%s and user2=%s) or (user1=%s and user2=%s)'
    params = (user.uid, fid, fid, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    # res = db.mycursor.fetchall()
    # print(res)
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = 'You were Unfriended by '+user.name
    params = (fid, notif_title, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def get_sent_from_fr(fid):
    q = 'select s.note_title, n.note_title, n.datetime_of_creation, s.link from notes n inner join notes s on s.note_id=n.shared_from where n.uid=%s and n.shared_from = any(select note_id from notes where uid=%s)'
    params = (fid, user.uid)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res

async def get_received_from_fr(fid):
    q = 'select s.note_title, n.note_title, n.datetime_of_creation, s.link from notes n inner join notes s on s.note_id=n.shared_from where n.uid=%s and n.shared_from = any(select note_id from notes where uid=%s)'
    params = (user.uid, fid)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res


async def get_notifications():
    q = 'select notif_title, dt from notifications where notif_for=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    global notifs
    notifs = [Notitification(*x) for x in res]

async def delete_notif(dt):
    q = 'delete from notifications where notif_for=%s and dt=%s'
    params = (user.uid, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def check_if_fid_friend(fid, note_id):
    q = 'select * from friends where (user1=%s and user2=%s) or (user1=%s and user2=%s)'
    params = (user.uid, fid, fid, user.uid)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) == 0:
        print('cannot share to people who are not friends')
    else:
        q = 'select * from share_request where req_to=%s and note_id=%s'
        params = (fid, note_id)
        db.mycursor.execute(q, params)
        res = db.mycursor.fetchall()
        if len(res) == 0:
            q = 'select * from notes where uid=%s and shared_from=%s'
            params = (fid, note_id)
            db.mycursor.execute(q, params)
            res = db.mycursor.fetchall()
            if len(res) == 0:
                q = 'select * from notes where uid=%s and note_id=%s and shared_from = any(select note_id from notes where uid=%s);'
                params = (user.uid, note_id, fid)
                db.mycursor.execute(q, params)
                res = db.mycursor.fetchall()
                if len(res) == 0:
                    return True
                else:
                    print('This note was sent to you by this user')
            else:
                print('already sent this note to this user')
        else:
            print('already sent shared request for this note to this user')

async def send_share_req(req_to, note_id, sub_name, unit_name, sent_on, note_title):
    q = 'insert into share_request values(%s, %s, %s, %s, %s, %s, %s, %s)'
    params = (req_to, user.uid, note_id, sub_name, unit_name, sent_on, note_title, user.name)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = user.name+' Wants to Share A Note With You'
    params = (req_to, notif_title, sent_on)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'update friends set last_interaction=%s where (user1=%s and user2=%s) or (user1=%s and user2=%s)'
    params = (sent_on, user.uid, req_to, req_to, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def get_pending_shares():
    q = 'select req_from, note_id, sub_name, unit_name, sent_on, note_title, friend_name from share_request where req_to=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    p = [ShareRequest(*x) for x in res]
    global pending_shares
    pending_shares = p

async def get_link_of_page(note_id):
    q = 'select link from notes where note_id=%s'
    params = (note_id,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res[0][0]

async def accept_share_request(sub_id, uid, unit_id, title, dt_of_creation, link, num_of_bookmarks, shared_from, req_dt, fid, og_title):
    await add_note(sub_id, uid, unit_id, title, dt_of_creation, link, num_of_bookmarks, shared_from)
    # delete from share_request and notification
    q = 'delete from notifications where notif_for=%s and dt=%s'
    params = (user.uid, req_dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'delete from share_request where req_to=%s and req_from=%s and note_id=%s'
    params = (user.uid, fid, shared_from)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    # send acceptance notification
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = og_title+' was Shared With '+user.name+' Successfully'
    params = (fid, notif_title, dt_of_creation)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    # inc count for notes received from that friend
    is_user1 = False
    q = 'select notes_received from friends where user1=%s and user2=%s'
    params = (user.uid, fid)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) == 1:
        is_user1 = True
        count = res[0][0]
    else:
        q = 'select notes_sent from friends where user1=%s and user2=%s'
        params = (fid, user.uid)
        db.mycursor.execute(q, params)
        res = db.mycursor.fetchall()
        count = res[0][0]
    count += 1
    print(count)
    if is_user1:
        q = 'update friends set notes_received=%s, last_interaction=%s where user1=%s and user2=%s'
        params = (count, dt_of_creation, user.uid, fid)
        db.mycursor.execute(q, params)
        db.mydb.commit()
    else:
        q = 'update friends set notes_sent=%s, last_interaction=%s where user1=%s and user2=%s'
        params = (count, dt_of_creation, user.uid, fid)
        db.mycursor.execute(q, params)
        db.mydb.commit()

async def reject_share_req(fid, dt, shared_from, og_title, dt1):
    # delete from share_request and notification
    q = 'delete from notifications where notif_for=%s and dt=%s'
    params = (user.uid, dt)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'delete from share_request where req_to=%s and req_from=%s and note_id=%s'
    params = (user.uid, fid, shared_from)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    # send rejection notification
    q = 'insert into notifications values(%s, %s, %s)'
    notif_title = user.name+' Rejected Share Request for '+og_title
    params = (fid, notif_title, dt1)
    db.mycursor.execute(q, params)
    db.mydb.commit()

async def get_list_of_subs_and_units():
    if len(subjects) == 0:
        await get_subs(user.uid)
    for each in subjects:
        if each.subject_name not in units.keys():
            await get_units_for(user.uid, each.subject_id, each.subject_name)
        print([x.unit_name for x in units[each.subject_name]])
    print([x.subject_name for x in subjects])

async def get_friend_token_url(fid):
    q = 'select token, homepage_url from user where uid=%s'
    params = (fid,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res[0]

async def get_nbm(note_id):
    q = 'select num_of_bookmarks from notes where note_id=%s'
    params = (note_id,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    return res[0][0]

async def delete_subject():
    return

# async def delete_unit(unit_id):
#     q = 'select note_id from notes where unit_id=%s'
#     params = (unit_id,)
#     db.mycursor.execute(q, params)
#     res = db.mycursor.fetchall()
#     for each in res:

#     return

async def delete_note(note_id):
    q = 'select * from share_request where note_id=%s'
    params = (note_id,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) > 0:
        print('There is a pending request for this note, You can\'t delete this note until the request is accepted or rejected')
    else:
        q = 'select note_id from notes where shared_from=%s'
        params = (note_id,)
        db.mycursor.execute(q, params)
        res = db.mycursor.fetchall()
        if len(res) > 0:
            print('changin ownership of a few notes...')
            for each in res:
                q = 'update notes set shared_from=0 where note_id=%s'
                params = (each[0],)
                db.mycursor.execute(q, params)
            db.mydb.commit()
        print('deleting...')
        q = 'delete from notes where uid=%s and note_id=%s'
        params = (user.uid, note_id)
        db.mycursor.execute(q, params)
        db.mydb.commit()
        return True
    return False
    # delete and remove shared from as well so that the other user now has ownership

# async def get_share_note_info(note_id):
#     q = 'select s.req_from, u.name, u.college, u.course, u.semester, s.note_id, s.note_title, s.sub_name, s.unit_name, s.sent_on from share_request s inner join user u on u.uid=s.req_from where s.req_to=%s and s.note_id=%s'
#     params = (user.uid, note_id)
#     db.mycursor.execute(q, params)
#     res = db.mycursor.fetchall()
#     return res[0]

# def get_name_of_fr(fid):
#     if len(friends) == 0:
#         fr = [x for x in friends if x.friend_id == fid][0]
#     return fr.name

async def check_username(nm):
    q = 'select name from user'
    db.mycursor.execute(q)
    res = db.mycursor.fetchall()
    if nm in [x[0] for x in res]:
        return False
    return True

async def create_user():
    q = 'insert into user (name, email, college, course, semester, total_sessions, token, homepage_url, password, last_login) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    params = (newuser.name, newuser.email, newuser.college, newuser.course, newuser.semester, 0, newuser.token, newuser.homepage_url, newuser.password, newuser.last_login.strftime(r"%Y-%m-%d %H:%M:%S"))
    db.mycursor.execute(q, params)
    db.mydb.commit()
    q = 'select * from user where uid = any( SELECT LAST_INSERT_ID());'
    db.mycursor.execute(q)
    res = db.mycursor.fetchall()
    print(res)
    global user
    user = User(*res[0])

async def check_if_summarised(note_id):
    q = 'select summarised from notes where note_id=%s'
    params = (note_id,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if res[0][0] == 0:
        return False
    return True

async def set_summarised(note_id):
    q = 'update notes set summarised=1 where note_id=%s'
    params = (note_id,)
    db.mycursor.execute(q, params)
    db.mydb.commit()

def signout():
    global signed_out
    signed_out = True

def reset():
    global user, newuser, subjects, notes, units, latest_notes_loaded, latest_notes, quick_links_from_names_loaded
    global pending, friends, notifs, pending_shares
    user = None
    newuser = None
    subjects = []
    notes = {}
    units = {}
    latest_notes_loaded = False
    latest_notes = []
    quick_links_from_names_loaded = False
    pending = []
    friends = []
    notifs = []
    pending_shares = []
    # new_usernm = ''

async def change_username(nnm):
    q = 'update user set name=%s where uid=%s'
    params = (nnm, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    global new_usernm
    new_usernm = nnm

async def set_password(npass):
    q = 'update user set password=%s where uid=%s'
    params = (npass, user.uid)
    db.mycursor.execute(q, params)
    db.mydb.commit()
    global pass_changed
    pass_changed = True

async def delete_account():
    if len(pending_shares) > 0:
        print('Your have pending share requests\nRejecting Requests...')
        # reject all pending requests
        for each in pending_shares:
            dt1 = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            await reject_share_req(each.req_from, each.sent_on, each.note_id, each.note_title, dt1)

    await get_friends()

    # delete share requests sent that are pending
    q = 'select req_to, sent_on from share_request where req_from=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) > 0:
        print('Cancelling all sent pending share requests...')
        for each in res:
            dq = 'delete from notifications where notif_for=%s and dt=%s'
            params = (each[0], each[1])
            db.mycursor.execute(dq, each)
        dq = 'delete from share_request where req_from=%s'
        params = (user.uid,)
        db.mycursor.execute(dq, params)
        db.mydb.fetchall()

    if len(friends) > 0:
        print('Unfriending Friends...')
        # remove from friends
        for each in friends:
            dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            await remove_friend(each.friend_id, dt)

    q = 'select note_id from notes where uid=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    # delete notes
    for each in res:
        await delete_note(each[0])

    # delete untis
    q = 'delete from units where uid=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    db.mydb.commit()

    # delete subjects
    q = 'delete from subject where uid=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    db.mydb.commit()

    # delete notifications for this user
    q = 'delete from notifications where notif_for=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    db.mydb.commit()

    # delete user
    q = 'delete from user where uid=%s'
    params = (user.uid,)
    db.mycursor.execute(q, params)
    db.mydb.commit()

    global signed_out
    signed_out = True

async def get_uid_for_nm(nm):
    q = 'select uid from user where name=%s'
    params = (nm,)
    db.mycursor.execute(q, params)
    res = db.mycursor.fetchall()
    if len(res) == 0:
        print('Username not valid')
        return None
    return res[0][0]