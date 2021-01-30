import random

colors = ['Black', 'Gray', 'Brown', 'Orange',
        'Yellow', 'Teal', 'Blue', 'Purple',
        'Pink', 'Red']
kivy_colors = {
    'Black': (1, 1, 1, 1),
    'Gray': (),
    'Brown': (),
    'Orange': (),
    'Yellow': (),
    'Teal': (),
    'Blue': (),
    'Purple': (),
    'Pink': (),
    'Red': ()
    }

def random_color():
    color = random.choice(colors)
    return color

def rgb_to_kivy(rgb):
    for each in rgb:
        

blue (55, 53, 47)
bluet rgb(11, 110, 153)
