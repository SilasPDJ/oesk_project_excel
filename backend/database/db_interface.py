import MySQLdb
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
import pandas as pd


class StandardOrmMethods:
    def __init__(self, orm: SqlAchemyOrms, conn_obj: MySqlInitConnection):
        self.orm = orm
        self.conn_obj = conn_obj

    def generate_df_v2(self, start, end, step=1) -> pd.DataFrame:
        from sqlalchemy.sql import text, column
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

    class EmpresasOrmOperations(StandardOrmMethods):
        def __init__(self, conn_obj):
            super().__init__(self.get_orm(), conn_obj)

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
                self.orm.cnpj,
                self.orm.razao_social,
                self.orm.cpf,)
            return df

        def find_by_cnpj(self, cnpj):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
                return empresa

    class ComptOrmOperations(StandardOrmMethods):
        def __init__(self, conn_obj: MySqlInitConnection):
            super().__init__(self.get_orm(), conn_obj)

        @staticmethod
        def get_orm():
            return SqlAchemyOrms.ClientsCompts

        def update_values_from_cnpj_and_compt(self, cnpj, compt):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
