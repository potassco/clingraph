"""
Test Utils
"""
#pylint: disable=missing-function-docstring

import os
import shutil

def get_example_file(number):
    return os.path.join("examples","doc",f"example{number}",f"example{number}.lp")

def get_example_str(number):
    with open(get_example_file(number), 'r',encoding='utf-8') as lpfile:
        return lpfile.read()

def make_file(content):
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/test_tmp.lp', 'w',encoding='utf-8') as lpfile:
        lpfile.write(content)

    return 'out/test_tmp.lp'

def clean_out():
    folder = 'out'
    #pylint: disable=broad-except
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
