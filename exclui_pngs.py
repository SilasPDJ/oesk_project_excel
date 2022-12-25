import pathlib
from __backend import COMPT, main_folder, main_file
from default.sets import InitialSetting

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
                        # COM ESSA CONVERSÃO, será anexado para o e-mail...
                        try:
                            pdf_filename = os.path.splitext(filename)[0]+'.pdf'
                            InitialSetting.convert_img2pdf(
                                filename, pdf_filename, dirpath)
                            # png2pdf
                            print(dirpath)
                        except:
                            pass
                        # TODO: ceck-up da quantidade de anexos para envio 2 ou 4?? Pois agora incrementou

# try to always use F5
# ChangePng('SimplesNacional', 0)


ChangePng('ginfessDone', 1)
