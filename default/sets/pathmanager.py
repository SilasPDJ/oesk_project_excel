import os
import json
from json import decoder


class Dirs:
    @staticmethod
    def pathit(*directories, sep="\\"):
        """ make dirs with directories args, example: pathit('path', 'to', 'dir')
            that will return and create "path/to/dir"
        :param directories: "without "/" please
        :param sep: the separator

        Returns:
            str: path/to/dir
        """
        import os
        pathit = directories[0]

        for directory in directories[1:]:
            pathit += f'\\{directory}'
        if not os.path.exists(pathit):
            os.makedirs(pathit)
        pathit = pathit.replace('/', sep)
        return pathit

    def certifs_exist(self, startswith, at_least=2, endswith: bool = False):
        # if endswith is True, it will search for endswith instead
        arqs_search = self.files_get_anexos_v4(self.client_path, 'png')
        arqs_search += self.files_get_anexos_v4(self.client_path, 'pdf')
        # certificados gias são em PDF...
        arqs_search = [
            self.path_leaf(f, True) for f in arqs_search]
        if endswith is False:
            arqs_search = [f for f in arqs_search if f.startswith(startswith)]
        else:
            arqs_search = [f for f in arqs_search if f.endswith(startswith)]

        if len(arqs_search) >= at_least:
            return True
        return False

    @staticmethod
    def walget_searpath(searched, initial_path, whatis: int = 0):
        """
        # walk get searched path
        :param str searched: any string
        :param initial_path: any path...
        :param whatis: 0 = dirpath (defult); 1 = searches in dirnames; 2 = searches in filenames
        from os.walk  
        :return: first found though searched in path
        """
        if whatis > 2 or whatis < 0:
            raise ValueError("Try values between 2 and 0")
        for (dirpath, dirnames, filenames) in os.walk(initial_path):
            if whatis == 0:
                if searched in dirpath:
                    return dirpath
            elif whatis == 1:
                if searched in dirnames:
                    return dirnames
            elif whatis == 2:
                try:
                    listof = []
                    for filename in filenames:
                        if searched in filename:
                            listof.append(os.path.join(dirpath, filename))
                    return listof
                except IndexError:
                    return False

    @staticmethod
    def move_file(where_from, destiny):
        """[File/folder moved from a place[where_from] to another[destiny]]
        Args:
            where_from (str):
            destiny (str): 
        """
        from shutil import move
        move(where_from, destiny)

    @staticmethod
    def path_leaf(path, only_file=False):
        """
        :param path: Any path
        :param only_file: returns only file name
        :return: opposite of os.path.dirname, so returns the file path
        ps: returns False if path has no file
        """
        if not os.path.isfile(path):
            return False
        head, tail = os.path.split(path)
        if only_file:
            return tail

        # else
        return tail or os.path.basename(head)

    def files_get_anexos_v4(self, path, file_type='pdf', upload=True):
        """
        :param path: get anexos from the following path
        :param file_type: file annexed type
        :param compt: 10-2020; 02-2019 etc
        :param upload: False -> email it! True: upload it!
        :return: pdf_files or whatever

        # _files_path
        """
        from email.mime.application import MIMEApplication
        pdf_files = list()
        # Lucas Restaurante

        dir_searched_now = path
        list_checked_returned = [os.path.join(dir_searched_now, fname)
                                 for fname in os.listdir(dir_searched_now) if fname.lower().endswith(file_type)]

        for fname in list_checked_returned:
            if not upload:
                file_opened = MIMEApplication(open(fname, 'rb').read())
                fname_title = self.path_leaf(fname)
                file_opened.add_header(
                    'Content-Disposition', 'attachment', filename=fname_title)
                pdf_files.append(file_opened)
            else:
                pdf_files.append(f'{fname}')
        return pdf_files

    def unzip_folder(self, full_path, rm_zip=True):
        """
        :param full_path: caminho
        :param rm_zip: True -> remove zip, False, não remove
        :return: arquivo extraído e excluído o zip.
        Ele faz isso com todos os zip
        """
        from time import sleep
        from os import chdir, remove, listdir
        from zipfile import ZipFile, BadZipFile
        chdir(full_path)
        ls = listdir()
        for file in ls:
            print('Descompactando, ZIPs e excluíndo-os')
            if file.endswith('.zip'):
                try:
                    zf = ZipFile(file, mode='r')
                    zf.extractall()
                    zf.close()
                except BadZipFile:
                    print('Não deszipei')
                finally:
                    if rm_zip:
                        sleep(5)
                        remove(file)

    @staticmethod
    def sort_files_by_most_recent(folderpath):
        return sorted([os.path.join(folderpath, f)
                       for f in os.listdir(folderpath)],
                      key=lambda x: os.path.getmtime(
                          os.path.join(folderpath, x)),
                      reverse=True)

    @staticmethod
    def get_documents_folder_location():
        """
        :returns: user Documents folder location 
        """
        from platform import system
        import win32com
        import pythoncom
        if system() == 'Windows':
            pythoncom.CoInitialize()
            shell = win32com.client.Dispatch("WScript.Shell")
            my_documents = shell.SpecialFolders("MyDocuments")
            # print(my_documents)
        else:
            my_documents = os.path.expanduser("~/Documents")
        return my_documents


class HasJson:
    @staticmethod
    def load_json(file):
        """
        :param str file: file name
        :return: dict or list or tuple from json loaded
        """
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except (decoder.JSONDecodeError, FileNotFoundError) as e:
            # raise e
            return False

    @staticmethod
    def dump_json(objeto, file):
        """
        :param object objeto:
        :param file:
        # :param ensure_ascii: False -> utf-8, True -> ensure-it
        :return:

        # object engloba list, tuple, dict
        """
        with open(file, 'w', encoding='utf-8') as file:
            json.dump(objeto, file, ensure_ascii=False, indent=8)
