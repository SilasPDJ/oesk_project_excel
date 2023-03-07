from typing_extensions import override
import MySQLdb
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
import pandas as pd


class _StandardOrmMethods:
    # my porpoise is not to get any orm specific attributes  in here
    def __init__(self, orm, conn_obj: MySqlInitConnection):
        self.orm = orm
        self.conn_obj = conn_obj

    def generate_df_v2(self, start, end, step=1) -> pd.DataFrame:
        public_attributes = self.get_public_attributes(self.orm)
        queried_attributes = [
            getattr(self.orm, attribute) for attribute in public_attributes[start:end:step]]
        return self.conn_obj.pd_sql_query_select(
            *queried_attributes
        )

    @staticmethod
    def get_public_attributes(orm):
        return [attr for attr in dir(orm) if not attr.startswith("_")]


class DBInterface:
    def __init__(self, conn_obj: MySqlInitConnection) -> None:
        self.conn_obj = conn_obj
        self.engine = conn_obj.engine

    class EmpresasOrmOperations(_StandardOrmMethods):
        def __init__(self, conn_obj):
            self.orm = self.get_orm()
            super().__init__(self.orm, conn_obj)

        @staticmethod
        def get_orm():
            return SqlAchemyOrms.MainEmpresas

        def update_from_cnpj(self, cnpj: str, razao_social: str):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
                if empresa:
                    empresa.razao_social = razao_social
                    session.commit()
                    return True

        def generate_df(self) -> pd.DataFrame:

            df = self.conn_obj.pd_sql_query_select(
                self.orm.razao_social,
                self.orm.cnpj,
                self.orm.cpf,)
            return df

        def find_by_cnpj(self, cnpj):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
                return empresa

        def find_by_razao_social(self, rsoc):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter(self.orm.razao_social == rsoc).first()
                return empresa

        def filter_by_kwargs(self, **kwargs):

            with self.conn_obj.Session() as session:
                query = session.query(self.orm)
                for key, value in kwargs.items():
                    query = query.filter(getattr(self.orm, key) == value)
                return query.first()

    class ComptOrmOperations(_StandardOrmMethods):
        def __init__(self, conn_obj: MySqlInitConnection):
            self.orm = self.get_orm()
            super().__init__(self.orm, conn_obj)

        @staticmethod
        def get_orm():
            return SqlAchemyOrms.ClientsCompts

        # need to duplicate, otherwhise it won't highlight
        def filter_by_kwargs(self, **kwargs):
            with self.conn_obj.Session() as session:
                query = session.query(self.orm)
                for key, value in kwargs.items():
                    query = query.filter(getattr(self.orm, key) == value)
                return query.first()

        def filter_by_cnpj_and_compt(self, cnpj, compt):
            with self.conn_obj.Session() as session:
                query = session.query(self.orm).filter_by(compt=compt).join(
                    self.orm.main_empresas)\
                    .filter(SqlAchemyOrms.MainEmpresas.cnpj == cnpj)
                # return the last

                return query.first()

        def update_from_cnpj_and_compt(self, cnpj: str, values_obj: object, allowed=[]):
            """This abstraction updates the COMPTs table using cnpj, getting the other_values as parameter

            Args:
                cnpj (str): client_cnpj
                other_values (COMPT_ORM_OPERATIONS): object to be updated
                allowed (list, optional): If it's None, it'll update the full object. Defaults to [].

            Returns:
                boolean: True: things have been saved / False: error with DB
            """
            empresa = None

            # Filtered the object to be updated
            with self.conn_obj.Session() as session:
                empresa = session.query(self.orm).filter_by(compt=values_obj.compt).join(
                    self.orm.main_empresas)\
                    .filter(SqlAchemyOrms.MainEmpresas.cnpj == cnpj).one_or_none()

                if empresa:
                    update_dict = {
                        'declarado': values_obj.declarado,
                        'nf_saidas': values_obj.nf_saidas,
                        'entradas': values_obj.nf_entradas,
                        'sem_retencao': values_obj.sem_retencao,
                        'com_retencao': values_obj.com_retencao,
                        'valor_total': values_obj.sem_retencao + values_obj.com_retencao,
                        'anexo': values_obj.anexo,
                        'envio': values_obj.envio,
                        'imposto_a_calcular': values_obj.imposto_a_calcular
                    }
                    for key, value in update_dict.items():
                        if allowed != []:
                            if key in allowed:
                                setattr(empresa, key, value)
                        else:
                            setattr(empresa, key, value)

                    session.add(empresa)
                    session.commit()
                    return True

                return False
