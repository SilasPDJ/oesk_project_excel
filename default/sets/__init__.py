from .pathmanager import Dirs
from .now import Now


class InitialSetting(Dirs, Now):
    @ classmethod
    def get_compt(cls, m_cont=-1, y_cont=0, past_only=True, sep='-'):
        from datetime import date
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        month = cls.m()
        year = cls.y()

        now_date = date(year, month, 1)

        if past_only:
            m_cont = m_cont * (-1) if m_cont > 0 else m_cont
            y_cont = y_cont * (-1) if y_cont > 0 else y_cont
            # force to be negative

        now_date = now_date + relativedelta(months=m_cont)
        now_date = now_date + relativedelta(years=y_cont)
        month, year = now_date.month, now_date.year
        compt = f'{month:02d}{sep}{year}'
        return compt

    @classmethod
    def files_pathit(cls, pasta_client, insyear=None, ano=None):
        from dateutil import relativedelta as du_rl
        from datetime import date

        """[summary]

        Args:
            pasta_client (str): client folder name
            insyear (str): inside year (competencia or whatever). Defaults then call cls.get_compt_only() as default
            ano (str,[optional]): year folder. Defaults to None.

        Returns:
            [type]: [description]
        """
        insyear = cls.get_compt() if insyear is None else insyear
        compt = insyear
        if ano is None:
            # ano = ''.join([insyear[e+1:] for e in range(len(insyear)) if insyear[e] not in '0123456789'])
            ill_split = ''.join([v for v in compt if v not in '0123456789'])
            mes, ano = compt.split(ill_split)
            try:
                int(ano)
            except ValueError:
                print(
                    f'if ano is None split ainda não encontrado,\n    ano = ano mês anterior')
                ano = date(cls.y(), cls.m(), 1) - du_rl.relativedelta(months=1)
                # Se ele não achar o ano vindo do split...

        excel_file_name = cls.getset_folderspath()
        # print(insyear, excel_file_name)
        __path = excel_file_name
        path_final = [*str(__path).split('\\'),
                      ano, insyear, pasta_client]
        salva_path = Dirs.pathit(*path_final)
        return salva_path

    @staticmethod
    def treat_documents_values(arg):
        return str(int(arg))
