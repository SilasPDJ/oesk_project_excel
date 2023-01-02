class SbFConverter:
    """
    MUITO OBRIGADO, SENHOR

    # retorna copiada a imagem através do nome dela
    """

    def __init__(self, img_name, path=''):
        from pyperclip import copy
        self.convert_gray_scale(img_name)

        read = self.read(img_name)
        copy(read)

    def read(self, img_name):
        self.convert_gray_scale(img_name)

        import pytesseract
        from PIL import Image
        pytesseract.pytesseract.tesseract_cmd = r"O:\NEVER\tesseract.exe"
        r = img_name
        text = pytesseract.image_to_string(r)
        print(text)
        return text

    def convert_gray_scale(self, img_name):
        img2 = img_name
        from PIL import Image
        img = Image.open(img2).convert('LA')
        img.save(img_name)
