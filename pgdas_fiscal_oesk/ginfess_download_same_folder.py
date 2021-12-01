# dale
import openpyxl
from default.sets import InitialSetting
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


class DownloadGinfessGuiSameFolder(InitialSetting, WDShorcuts):

    # only static methods from JsonDateWithDataImprove

    def __init__(self, *dados, compt,  show_driver=False):
        # driver
        __r_social, __cnpj, _ginfess_cod, link = dados

        self.compt = compt
        # mesma coisa de self.any_to_str, só que ele aceita args desempacotados
        self.future_path = self.files_pathit('NOTA_DE_SERVICOS', self.compt)
        self.client_path = self.files_pathit(__r_social.strip(), self.compt)
