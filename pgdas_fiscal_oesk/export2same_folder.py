# dale
from re import search
import openpyxl
# from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts
from default.interact import press_keys_b4, press_key_b4
from selenium.webdriver import Chrome

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *

from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from time import sleep
from default.webdriver_utilities.pre_drivers import ginfess_driver
from openpyxl import Workbook
from openpyxl.utils.cell import coordinate_from_string
from openpyxl.utils import get_column_letter as gcl
import pandas as pd
import os
from shutil import copy2

from pgdas_fiscal_oesk.contimatic import Contimatic


class Export2SameFolder(Contimatic):

    # extesions lowercase, always
    extensions = ['xml', 'csv']

    def __init__(self, *dados, compt):
        # driver
        __r_social, __cnpj = dados

        self.compt = compt
        # mesma coisa de self.any_to_str, só que ele aceita args desempacotados
        self.client_path = self.files_pathit(__r_social.strip(), self.compt)

        # Copia os arquivos com as seguintes extensões: self.extensions

    def icms(self):
        """
        * Não precisa de especificar o cliente, pois os ZIP estão fora da pasta deles

        """

        from zipfile import ZipFile, BadZipFile

        future_path = self.files_pathit('NOTA_DE_ICMS', self.compt)
        previous_path = "\\".join(future_path.split('\\')[:-1])

        filt_zips = filter(lambda file: file.endswith('.zip'),
                           os.listdir(previous_path))
        full_zips_path = [os.path.join(previous_path, nfzip)
                          for nfzip in filt_zips]

        for zipfile in full_zips_path:
            _file = ZipFile(zipfile, mode='r')

            removext = os.path.splitext(zipfile)[0]
            zipfile_name = os.path.basename(removext)

            unziped_path = os.path.join(
                future_path, os.path.basename(zipfile_name))

            _file.extractall(unziped_path)
            # _file.extract()
            # self.move_file(_file, future_path)
            _file.close()
            input('teste')
        print(*filt_zips)
