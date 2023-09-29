from datetime import datetime as dt
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Now:

    @staticmethod
    def time():
        pass

    @staticmethod
    def hj():
        return dt.now().day

    @staticmethod
    def m():
        return dt.now().month

    @staticmethod
    def y():
        return dt.now().year

    @staticmethod
    def nome_mes(mes: int):
        nomes = """Janeiro 
        Fevereiro
        Março
        Abril
        Maio
        Junho
        Julho
        Agosto
        Setembro
        Outubro
        Novembro
        Dezembro
        """.strip().split()
        if mes > 0:
            return nomes[mes - 1]
        elif mes == 0:
            print('\033[1;31m Retornando janeiro')
            return nomes[0]
        else:
            return nomes[mes]

    @staticmethod
    def date2date_brazil(dd, sep='/'):
        try:
            dia = dd.day
            mes = dd.month
            ano = dd.year
        except (AttributeError, NameError) as e:
            raise e('Deu ruim!!! date2date_brazil')
        else:
            return f'{dia:02d}{sep}{mes:02d}{sep}{ano}'

    def first_and_last_day_compt(self, compt, sep='/', zdate_wontbe_greater=False):
        """
        ELE JÁ PEGA O ANTERIOR MAIS PROX
        :param str compt:(competencia or whatever). Defaults then call cls.get_compt_only() as default
        :param sep: separates month/year
        # É necessario o will_be pois antes dele é botado ao contrário
        # tipo: 20200430
        # ano 2020, mes 04, dia 30... (exemplo)
        :return: ÚLTIMO DIA DO MES
        """

        ill_split = ''.join([v for v in compt if v not in '0123456789'])
        mes, ano = compt.split(ill_split)
        mes, ano = int(mes), int(ano)
        #  - timedelta(days=1)
        # + relativedelta(months=1)

        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)
        first_now = date(ano, mes, 1)
        z, a = last_now, first_now

        if zdate_wontbe_greater:
            # last_only
            _check, _dia_hj = self.__check_date_greater_than_today(z)
            if _check:
                z = _dia_hj

        br1st = f'{a.day:02d}{sep}{a.month:02d}{sep}{a.year}'
        brlast = f'{z.day:02d}{sep}{z.month:02d}{sep}{z.year}'
        print(br1st, brlast)
        return br1st, brlast

    @staticmethod
    def __check_date_greater_than_today(self, mydt: date):
        dia_hj = dt.now()
        return mydt.day > dia_hj.day, dia_hj

    @staticmethod
    def get_last_business_day_of_month(mes=None, ano=None):
        dia_hj = dt.now()
        if mes is None:
            mes = dia_hj.month
        if ano is None:
            ano = dia_hj.year
        if mes > 12:
            mes = 12
        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)

        wkday = dt.weekday(last_now)
        while wkday >= 5:
            last_now -= timedelta(days=1)
            wkday = dt.weekday(last_now)
            print(wkday)
        return last_now

    @staticmethod
    def str_to_date(date_str: str, format_str: str) -> date:
        try:
            dt = datetime.strptime(date_str, format_str)
            return dt.date()
        except ValueError:
            raise ValueError(
                f"Invalid date string: {date_str}. Expected format: {format_str}")
