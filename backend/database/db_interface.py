import MySQLdb
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection
import pandas as pd


Empresas = SqlAchemyOrms.MainEmpresas


# conn_obj = MySqlInitConnection()

Empresas = SqlAchemyOrms.MainEmpresas


class DBInterface:
    def __init__(self, conn_obj: MySqlInitConnection) -> None:
        self.conn_obj = conn_obj
        self.engine = conn_obj.engine

    @staticmethod
    def get_public_attributes(orm):
        return [attr for attr in dir(orm) if not attr.startswith("_")]

    class EmpresasOrmOperations:
        ORM = SqlAchemyOrms.MainEmpresas

        def __init__(self, conn_obj: MySqlInitConnection) -> None:
            self.conn_obj = conn_obj

        def update_from_cnpj(self, cnpj: str, razao_social: str):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.ORM).filter_by(cnpj=cnpj).first()
                if empresa:
                    empresa.razao_social = razao_social
                    session.commit()
                    return True

        def generate_df(self) -> pd.DataFrame:
            df = self.conn_obj.pd_sql_query_select(
                self.ORM.cnpj,
                self.ORM.razao_social,
                self.ORM.cpf,)
            return df

        def generate_df_v2(self, start, end, step=1) -> pd.DataFrame:
            from sqlalchemy.sql import text, column
            public_attributes = DBInterface.get_public_attributes(self.ORM)
            queried_attributes = [
                getattr(self.ORM, attribute) for attribute in public_attributes[start:end:step]]
            for q in queried_attributes:
                print(q)
            return self.conn_obj.pd_sql_query_select(
                *queried_attributes
            )

        def find_by_cnpj(self, cnpj):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.ORM).filter_by(cnpj=cnpj).first()
                return empresa

    class ComptOrmOperations:
        ORM = SqlAchemyOrms.MainEmpresas

        def __init__(self, conn_obj: MySqlInitConnection) -> None:
            self.conn_obj = conn_obj

        def update_values_from_cnpj_and_compt(self, cnpj, compt):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.ORM).filter_by(cnpj=cnpj).first()
