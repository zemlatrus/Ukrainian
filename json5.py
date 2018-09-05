import os
import re
import json
from random import randint


# 1) To finish this, find a way to generate the d['children'] element outside of the loop
# 2) The problem is that 'path' gets renamed


#    H
#    |
# A --- B
# |     |
# A1 -- B1
# |     |
# F1 -- F1

# 1) Make overall dictionary
# 2) For each branch, go to each level, generate data, and then go to next level


left_side  = ['Nouns']
right_side = ['Verbs', 'Other']


not_this = ['(.*).py$', '(.*).numbers$', '(.*).key$']


def exclusion(to_parse, name):

    container = []

    excluded_values = ['.DS_Store', '(.*).py$', '(.*).numbers$', '(.*).key$', '(.*).csv', 'Scripts']

    if name == 'children':
        excluded_values += left_side
    elif name == 'parents':
        excluded_values += right_side

    for i in os.listdir(to_parse):
        counter = 0
        for j in excluded_values:
            if re.search(j, i):
                counter += 1
        if counter == 0:
            container.append(i)

    return container




def make_a_list_of_descendants(to_explore, name):
    
    descendants_list = []

    listed_directories = exclusion(to_explore, name)

    for i in listed_directories:   
        descendants = path_to_dict(os.path.join(to_explore, i), name)
        descendants_list.append(descendants)

    return descendants_list




def path_to_dict(path, name):

    remote_link = path.replace(home, '')

    if os.path.isfile(path):
        d = {}
        d['type'] = "file"
        d['name'] = os.path.splitext(os.path.basename(path))[0]
        d['id']   = 'AB-' + str(randint(10, 100000))
        d['link'] =  remote + remote_link
        # d['link'] =  os.path.abspath(path)
    
        return d

    if os.path.isdir(path):

        counter = 0
        for i in not_this:
            if re.search(i, path):
                counter += 1
        if counter == 0:
            d = {}
            d['type'] = "directory"
            d['name'] = os.path.basename(path)
            d['id']   = 'AB-' + str(randint(10, 100000))
            d[name]   = make_a_list_of_descendants(path, name)

            return d



home   = os.getcwd()
remote = 'https://rawgit.com/zemlatrus/Ukrainian/master'


final_container              = {}
final_container['type']      = "directory"
final_container['name']      = os.path.basename(home)
final_container['_children'] = [path_to_dict(os.path.join(home, i), '_children') for i in left_side]
final_container['_parents']  = [path_to_dict(os.path.join(home, j), '_parents') for j in right_side]

print(json.dumps(final_container, indent=2))












