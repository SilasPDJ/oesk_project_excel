import win32com.client
import os


import os
import platform
import ctypes
import ctypes.wintypes


def get_documents_folder_location():
    if platform.system() == 'Windows':
        shell = win32com.client.Dispatch("WScript.Shell")
        my_documents = shell.SpecialFolders("MyDocuments")
        # print(my_documents)
    else:
        my_documents = os.path.expanduser("~/Documents")
    return my_documents


my_documents = get_documents_folder_location()
print(my_documents)
