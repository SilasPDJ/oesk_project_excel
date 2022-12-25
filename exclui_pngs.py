import pathlib
from __backend import COMPT, main_folder, main_file

import os
class ChangePng:
    def __init__(self, searched, option, path=os.path.join(main_folder, '..'), ext='.png'):


        for dirpath, dirnames, filenames in os.walk(path):
            for dirname in dirnames:
                if dirname.isnumeric() and len(dirname) == 4:
                    print(dirname)

            for filename in filenames:
                if searched in filename:
                    # print(dirpath)
                    # print(filename)
                    changed = os.path.join(dirpath, filename)
                    if option == 0:
                        try:
                            os.remove(changed)
                        except FileNotFoundError:
                            pass
                    elif option == 1:
                        
                        # png2pdf


        # try to always use F5



ChangePng('SimplesNacional', 0)

ChangePng('ginfessDone')