

class Legato:
    def le_excel_each_one(self, msh):
        # msh = sheet_name inside sheet file
        dict_written = {}
        for en, header in enumerate(msh.columns):
            title = msh[header].name

            dict_written[title] = []
            # dicionário sh_name tem o  dicionário title que tem a lista com os valores, muito bom

            """
            try:
                list_written[title] = []
            except KeyError:
                ...
            """
            r_soc = msh[header].values
            # if title == "Razão Social":
            for name in r_soc:
                dict_written[title].append(name)
        return dict_written

    def readnew_lista(self, READ, print_values=False):
        """ TRANSFORMO EM DICIONÁRIO, CONTINUAR"""
        get_all = {}
        new_lista = []
        for k, lista in READ.items():
            for v in lista:
                v = str(v)
                v = v.replace(u'\xa0', u' ')
                v = v.strip()
                if str(v) == 'nan':
                    v = ''
                new_lista.append(v)
            get_all[k] = new_lista[:]
            new_lista.clear()
        if print_values:
            for k, v in get_all.items():
                print(f'\033[1;32m{k}')
                for vv in v:
                    print(f'\033[m{vv}')
        return get_all

    @staticmethod
    def readnew_lista_v_atual(json_part):
        """
        Surgiu em send_pgdasmail
        #        from smtp_project.init_email import JsonDateWithImprove as Jj
        #        json_file = Jj.load_json(fname)

        :param json_part: json_file.keys()
        # It contains dictionary
        """
        new_dict = {}

        for all_items in json_part:
            for k, v in all_items.items():
                new_dict[k] = v
        return new_dict

    def trata_money_excel(self, faturado):
        try:
            faturado = f'{float(faturado):,.2f}'
        except ValueError:
            print('Já é string')
        finally:
            faturado = faturado.lower().strip()
            if 'nan' in faturado or 'zerou' in faturado:
                faturado = 'SEM VALOR A PAGAR'
                return faturado
            faturado = faturado.replace('.', 'v')
            faturado = faturado.replace(',', '.')
            faturado = faturado.replace('v', ',')
            return faturado

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(v)

    @staticmethod
    def str_with_mask(elem, mask, msc=None):
        """
        # string with mask
        :param str elem: any element checked
        :param str mask: for checking by its length
        :param tuple msc: "mask should contain": None-> by default
        :return: string if its length equals to mask length, else False
        """
        elem.strip()
        anula_parco = ('.', ',', ';', ':', ')')

        if msc is None:
            check_mask = ('.', ',', ';', ':', '-',
                          '/', '_', '(', ')', '+', '$')
        else:
            check_mask = msc

        def trata_str(val1, valmask):
            if val1 in check_mask:
                return val1 == valmask
            elif valmask in check_mask:
                return val1 == valmask
            else:
                return None

        elem = elem[:-1] if elem.endswith(anula_parco) else elem
        if len(elem) == len(mask):
            for msk, el in zip(mask, elem):
                try:
                    int(el)
                    int(msk)
                    pass
                except ValueError:
                    dle = trata_str(el, msk)
                    if dle is False:
                        return False
                    else:
                        pass
            return elem
        else:
            return False

    def parse_sh_name(self, tup, data_required=True):
        """
        :param tup: compt and excel_file_name from self._atual_compt_and_file
        :param data_required: data_Required
        :return:
        """
        import pandas as pd
        compt, excel_file_name = tup
        xls = pd.ExcelFile(excel_file_name)
        sheet_names = iter(xls.sheet_names)
        for e, sh in enumerate(sheet_names):
            # if e > 0:
            if data_required:
                yield xls.parse(sh, dtype=str)
            else:
                yield sh

    @staticmethod
    def trata_sendvals(val):
        # ex: 1400,03 = 140003
        try:
            int(val)
        except ValueError:
            return val
        else:
            a = int(val) == float(val)
            if a:
                return val + "00"
            else:
                return val
