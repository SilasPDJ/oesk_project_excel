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

    @staticmethod
    def walget_searpath(searched, initial_path=None):
        """
        # walk get searched path
        :param str searched: any string
        :param initial_path: any path...
        :return: first found though searched in path
        """
        if initial_path is None:
            initial_path = r'I:/OESK_CONTABIL'

        for (dirpath, dirnames, filenames) in os.walk(initial_path):
            if searched in dirpath:
                return dirpath

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
