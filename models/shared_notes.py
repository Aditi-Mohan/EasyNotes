from datetime import datetime

class SharedNote:
    # weak entity set
    # primary key of identifying entity set
    int note_id
    # foreign key
    int user_id_owner
    # foreign key
    int user_id_shared_to
    datetime datetime_of_sharing

    # discriminator
    # user_id_owner + datetime_of_sharing