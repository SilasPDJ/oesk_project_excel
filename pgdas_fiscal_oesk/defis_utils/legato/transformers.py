import os
import pdf2image
from pdfminer.high_level import extract_text


def pdf2jpg(file, destiny):
    """
    :param file: file+path
    :param destiny: responsive => knows file as file and only destiny without file as path and increment file...
    :return:
    """
    mainext = '.jpg'
    pages = pdf2image.convert_from_path(file)

    for e_cont, page in enumerate(pages):
        # real = '\\'.join(os.path.realpath(__file__).split('\\')[:-1]),
        ext = destiny.split('\\')[-1]
        if '.' in ext:
            idest = destiny.index('.')
            f_destiny = destiny[:idest]
            # ext = destiny[idest:]
            fnamenow = f"{f_destiny}-pag{e_cont + 1}.{mainext}"
        else:
            file_only = os.path.basename(os.path.normpath(file))
            fnamenow = f'{destiny}\\-pag{file_only}{e_cont+1}.{mainext}'
        page.save(fnamenow, 'JPEG')

        yield fnamenow


def jpg2txt(img_path):
    """
    :return: jpg to txt
    """
    from pyperclip import paste
    # driver = self.driver

    class SbFConverter:
        """
        MUITO OBRIGADO, SENHOR

        # retorna copiada a imagem através do nome dela
        """

        def read(self, img_name):
            # self.convert_gray_scale(img_name)

            import pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = r"I:\NEVER\tesseract.exe"
            r = img_name
            text = pytesseract.image_to_string(r)
            return text

        def convert_gray_scale(self, img_name):
            img2 = img_name
            from PIL import Image
            # img = Image.open(img2).convert('LA')
            img = Image.open(img2)
            img.convert('RGB')
            img.save(img_name)

    # img = driver.find_element_by_id('div-img-captcha')
    # img_name = 'hacking.png'
    # img.screenshot(img_name)

    nm_img = img_path
    img_name = nm_img
    # VEIO DE ginfess_download
    version2 = SbFConverter()
    # version2.convert_gray_scale(nm_img)
    read = version2.read(nm_img)
    return read


def pdf2txt(pdf_file_path):
    """
    :param pdf_file_path:
    :return: PDF file to TXT
    # Finally
    """
    with open(pdf_file_path, 'rb') as f:
        return extract_text(f)
