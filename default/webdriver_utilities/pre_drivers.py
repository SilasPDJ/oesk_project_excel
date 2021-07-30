import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# continuar a desenvolver a def real_path, p/ driver


link = "Chromedriver/chromedriver.exe"
this_file_path = os.path.realpath(__file__)
path = os.path.dirname(this_file_path)
link = os.path.join(path, link)

# procura link chamado pela variável __file__


def default_qrcode_driver(path=''):
    """
    :param path: default path atual (downloads)
    :return: o driver para fechar no loop

    # sem perfil específico

    # new_path_set -> abre uma pasta para download especificada caso ela não exista ainda
    """
    def __profiles_main_folder(recria_padrao=False):
        """
        :param recria_padrao: True -> apaga arquivo e abre caixa de diálogo
        Create new profile
        """
        #
        with_title_name = 'PATH_PROFILES.txt'
        if recria_padrao:
            with open(with_title_name, 'w') as f:
                f.write('')
        try:
            value = open(with_title_name).read()
            if value == '':
                raise FileNotFoundError
        except FileNotFoundError:
            # IF FILE CONTAINING PATH NOT EXISTS, IT'LL DISPLAY A SELECTOR

            from tkinter import filedialog
            from tkinter import Tk
            root = Tk()
            root.withdraw()
            root = Tk()
            root.withdraw()
            while True:
                input(
                    'cheguei em onde estão as planilhas aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tiramee')
                way = filedialog.askdirectory(
                    title='SELECIONE ONDE ESTÃO SUAS PLANILHAS')

                # input(f'{fatiado_1} ;;;; {fatiado_2}')
                """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

                file = open(with_title_name, 'w')  # mt da hora
                file.write(way)
                file.close()
                value = open(with_title_name).read()
                if len(value) <= 0:
                    from tkinter import messagebox
                    resp = messagebox.askokcancel(
                        'ATENÇÃO!', message='Selecione uma pasta ou clique em CANCELAR.')
                    if not resp:
                        return
                else:
                    root.quit()
                    break
                root.mainloop()
        value = value.replace('/', '\\')
        return value

    __padrao = __profiles_main_folder()
    # path = SetPaths().new_path_set(path)
    # já está em mamae_download

    path = path.replace('/', '\\')
    # o try já tá dentro de replace

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument(f"user-data-dir={__padrao}")
    # carrega o perfil padrão com o qr_code
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        'profile.default_content_setting_values.automatic_downloads': 1

    })

    chromedriver = link

    # vindo do ginfess_driver [magic]

    driver = webdriver.Chrome(
        executable_path=chromedriver, options=chrome_options)
    return driver


def pgdas_driver(path=''):
    """
    :param path: default path atual
    :return: o driver para fechar no loop
    """

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    # profile chrome_options.add_argument("user-data-dir=C:\\Users\\AtechM_03\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        'profile.default_content_setting_values.automatic_downloads': 1

    })

    chromedriver = link
    # real_path_for_chromedriver()
    # vindo do ginfess_driver [magic]
    driver = webdriver.Chrome(
        executable_path=chromedriver, options=chrome_options)
    return driver


def ginfess_driver(path=''):
    """
    :param path: default path atual
    :return: o driver para fechar no loop

    "plugins.always_open_pdf_externally": True,
    download PDF automatic

    """
    print('\033[1;33m Headless\033[m')
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    # profile chrome_options.add_argument("user-data-dir=C:\\Users\\AtechM_03\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": True,
        'download.extensions_to_open': 'xml',
        "plugins.always_open_pdf_externally": True,
        # download PDF automaticamente acima
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    # options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_argument("safebrowsing-disable-extension-blacklist")
    # #################### Difference from above --> safe_browsing enabled
    chromedriver = link

    # real_path_for_chromedriver()

    driver = webdriver.Chrome(
        executable_path=chromedriver, options=chrome_options)
    # self.tags_wait('body', 'input', 'div')

    # sleep(5)
    return driver


def proffile_noqr_driver(path='', profile_path=''):
    """
    # Fazendo DEFIS
    # Driver que armazena perfil e recebi caminho para download

    :param path: default path atual (downloads)
    :param profile_path: caminho para o perfil
    :return: o driver.
    """

    __padrao = profile_path

    path = path.replace('/', '\\')
    # o try já tá dentro de replace

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument(f"user-data-dir={__padrao}")
    # carrega o perfil padrão com o qr_code
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
        'profile.default_content_setting_values.automatic_downloads': 1,


    })

    chromedriver = link
    # real_path_for_chromedriver()
    # vindo do ginfess_driver [magic]

    driver = webdriver.Chrome(
        executable_path=chromedriver, options=chrome_options)

    # self.tags_wait('body', 'input', 'div')

    # sleep(5)
    return driver


def jucesp_simple_driver():
    """
    # Fazendo DEFIS
    # Driver que armazena perfil e recebi caminho para download

    :return: o driver.
    """

    # __padrao = profile_path

    # o try já tá dentro de replace

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    # chrome_options.add_argument(f"user-data-dir={__padrao}")
    # carrega o perfil padrão com o qr_code
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    chromedriver = link
    # real_path_for_chromedriver()
    # vindo do ginfess_driver [magic]

    driver = webdriver.Chrome(
        executable_path=chromedriver, options=chrome_options)

    # self.tags_wait('body', 'input', 'div')

    # sleep(5)
    return driver
