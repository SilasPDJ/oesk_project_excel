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

    @staticmethod
    def treat_documents_values(*args):
        for arg in args:
            yield str(int(arg))
