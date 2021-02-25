class User:
    # primary key
    int user_id

    string user_name
    string email
    string college
    string course
    int semester
    int total_session
    # unique
    string token
    # unique
    string homepage_url

# relations partiipating in - 
# friends -> many to many
# subjects -> one to many
# notes (shared notes) -> one to one
# and more