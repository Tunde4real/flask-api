# -- coding: utf-8 -
# written by Ibrahim Aderinto

'''
This is the python module from which the swagger api will call methods from.
'''

# Import system modules
import os
import random
import shutil
import string
from zipfile import ZipFile

# 3rd party modules
from flask import abort


# A global variable to house all ascii characters
ascii_ = string.ascii_letters + string.digits


def generate_id():
    ''' 
        This function is for responding to a request with path basepath/api/id.
        It generates a unique ID to represent a user.

        returns:       The unique ID generated.     
    '''

    # create the unique ID
    new_id = ''.join([random.choice(ascii_) for i in range(3)])

    # make a new directory with name of unique ID generated to store the data of the user.
    os.mkdir(f"data/{new_id}")

    return {'id': new_id}


def upload(id, upload_file):
    '''
        This function is for responding to a call with path basepath/api/upload_file.
        It uploads the metadatas of a user in csv format to the folder named with
        the user's unique ID.

        returns:        A json data of ID and names of files uploaded.
    '''

    # abort if ID does not exist
    if not os.path.exists(f'data/{id}'):
        abort(
            404, f"ID - {id} not found"
        )

    # create a zip file object to read the zip file uploaded.
    zip = ZipFile(upload_file)

    # Extracts all the files in the zip file to the data/ID folder.
    # This puts the entire directory of the zip file in the ID folder.
    # In the form ID/zip_name/file
    zip.extractall(f'data/{id}')
    names = []

    # For every file extracted:
    for name in zip.namelist():
        # move the file one tree up
        shutil.copy(f"data/{id}/{name}", f'data/{id}')
        ind = name.index('/')
        # store the name of the file.
        names += [name[ind+1:]]
    
    # remove the folder ID/zip_name
    shutil.rmtree(f"data/{id}/{name[:ind]}")

    return {"id": id, "uploaded_files" : ', '.join(names)}

