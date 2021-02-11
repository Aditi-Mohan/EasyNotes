class Subject:
    # primary key
    int subject_id
    # foreign key
    int user_id

    string subject_name
    string units[]

# relations partiipating in - 
# notes -> one to many
# topics -> many to many