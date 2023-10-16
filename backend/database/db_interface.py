from datetime import datetime
from typing_extensions import override
import MySQLdb
from backend.models import SqlAchemyOrms
from backend.database import MySqlInitConnection

from typing import List, Type
import sqlalchemy as db
import pandas as pd
from default.sets import compt_to_date_obj


class _StandardOrmMethods:
    # my porpoise is not to get any orm specific attributes  in here
    def __init__(self, orm: SqlAchemyOrms, conn_obj: MySqlInitConnection):
        self.orm = orm
        self.conn_obj = conn_obj

    def generate_df_v2(self, start=None, end=None) -> pd.DataFrame:
        columns = self.select_columns_keys()
        queried_attributes = [
            getattr(self.orm, attribute) for attribute in columns[start:end]]
        return self.conn_obj.pd_sql_query_select_fields(
            *queried_attributes
        )

    def select_columns_keys(self) -> list:
        return [column.name for column in self.orm.__table__.columns]

    @staticmethod
    def generate_df_query_results_all(results) -> pd.DataFrame:
        records = [r.__dict__ for r in results]
        df = pd.DataFrame.from_records(records)
        df = df.drop(columns=["_sa_instance_state"])
        return df


class DBInterface:
    def __init__(self, conn_obj: MySqlInitConnection) -> None:
        self.conn_obj = conn_obj
        self.engine = conn_obj.engine

    def execute(self, query):
        with self.conn_obj.Session() as session:
            query = session.execute(db.text(query))
            return query.all()

    class EmpresasOrmOperations(_StandardOrmMethods):
        def __init__(self, conn_obj):
            self.orm = self.get_orm()
            super().__init__(self.orm, conn_obj)

        @staticmethod
        def get_orm() -> SqlAchemyOrms.MainEmpresas:
            return SqlAchemyOrms.MainEmpresas

        def get_ids_dictonary(self) -> dict:
            with self.conn_obj.Session() as session:
                empresas = session.query(
                    self.orm.id, self.orm.razao_social).all()
                return {e[0]: e[1] for e in empresas}

        def filter_by_kwargs(self, **kwargs):

            with self.conn_obj.Session() as session:
                query = session.query(self.orm)
                for key, value in kwargs.items():
                    query = query.filter(getattr(self.orm, key) == value)
                return query.first()

        def filter_by_cnpj(self, cnpj):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
                return empresa

        def filter_by_razao_social(self, rsoc):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter(self.orm.razao_social == rsoc).first()
                return empresa

        def query_all(self):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).all()
                return empresa

        def get_from_id(self, _id: int):
            with self.conn_obj.Session() as session:
                return session.query(self.orm).get(_id)

        def update_from_id(self, _id: int, form_values: dict):
            with self.conn_obj.Session() as session:
                record = session.query(self.orm).get(_id)
                for key, value in form_values.items():
                    setattr(record, key, value)
                session.commit()
                return True

        def update_from_cnpj(self, cnpj: str, razao_social: str):
            with self.conn_obj.Session() as session:
                empresa = session.query(
                    self.orm).filter_by(cnpj=cnpj).first()
                if empresa:
                    empresa.razao_social = razao_social
                    session.commit()
                    return True

        def insert(self, form_values: dict) -> int:
            with self.conn_obj.Session() as session:
                new_record = self.orm(**form_values)
                session.add(new_record)
                session.commit()
                return new_record.id

        def delete_from_id(self, _id: int):
            with self.conn_obj.Session() as session:
                record = session.query(self.orm).get(_id)
                if record is not None:
                    session.delete(record)
                    session.commit()
                    return True
                else:
                    return False

    class ComptOrmOperations(_StandardOrmMethods):
        def __init__(self, conn_obj: MySqlInitConnection):
            self.orm = self.get_orm()
            super().__init__(self.orm, conn_obj)

        @staticmethod
        def get_orm() -> SqlAchemyOrms.ClientsCompts:
            return SqlAchemyOrms.ClientsCompts

        def df_join_empresas(self, compt) -> pd.DataFrame:
            with self.conn_obj.Session() as session:
                query = session.query(SqlAchemyOrms.MainEmpresas, self.orm)\
                    .join(SqlAchemyOrms.MainEmpresas, self.orm.main_empresa_id == SqlAchemyOrms.MainEmpresas.id)
                query = query.filter(self.orm.compt == compt)
                df = pd.read_sql(query.statement, session.connection())
                return df

        def filter_by_kwargs(self, **kwargs):
            with self.conn_obj.Session() as session:
                query = session.query(self.orm)
                for key, value in kwargs.items():
                    query = query.filter(getattr(self.orm, key) == value)
                return query.first()

        def filter_by_cnpj_and_compt(self, cnpj, compt) -> SqlAchemyOrms.ClientsCompts:
            with self.conn_obj.Session() as session:
                query = session.query(self.orm).filter_by(compt=compt).join(
                    self.orm.main_empresas)\
                    .filter(SqlAchemyOrms.MainEmpresas.cnpj == cnpj)
                # return the last

                return query.first()

        def filter_all_by_compt(self, compt,) -> List[Type[SqlAchemyOrms.ClientsCompts]]:
            with self.conn_obj.Session() as session:
                query = session.query(self.orm).filter_by(compt=compt)
                # return the last
                return query.all()

        def filter_all_by_compt_order_by(self, compt, order_by_args=None) -> List[Type[SqlAchemyOrms.ClientsCompts]]:
            with self.conn_obj.Session() as session:
                query = session.query(self.orm).filter_by(compt=compt)
                if order_by_args is not None:
                    order_by_args = [db.text(arg) for arg in order_by_args]
                    query = query.order_by(*order_by_args)
                return query.all()

        def update_fieldict_from_cnpj_compt(self, cnpj: str, compt: datetime.date, field_value: dict) -> bool:
            from sqlalchemy import update
            with self.conn_obj.Session() as session:
                empresa = self.filter_by_cnpj_and_compt(cnpj, compt)
                if empresa:
                    session.execute(update(self.orm).
                                    where(self.orm.main_empresa_id == empresa.main_empresa_id).
                                    where(self.orm.compt == compt).
                                    values(field_value))
                    session.commit()
                    return True
            return False

        def update_from_cnpj_and_compt(self, cnpj: str, values_obj: SqlAchemyOrms.ClientsCompts, allowed=[]):
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

            with self.conn_obj.Session() as session:
                if empresa:
                    update_dict = {}

                    for key, value in vars(values_obj).items():
                        if not key.startswith("__"):
                            update_dict[key] = value

                    for key, value in update_dict.items():
                        if allowed != []:
                            if key in allowed:
                                setattr(empresa, key, value)
                        else:
                            setattr(empresa, key, value)

                    session.add(empresa)
                    # session.add means insert, merge means commit
                    # session.merge(empresa)
                    session.commit()
                    return True

                return False

        def update_from_cnpj_and_compt__dict(self, cnpj: str, update_dict: dict, allowed=[]):
            """This abstraction updates the COMPTs table using cnpj, getting the other_values as parameter

            Args:
                cnpj (str): client_cnpj
                other_values (COMPT_ORM_OPERATIONS): dictonary to be update
                allowed (list, optional): If it's None, it'll update the full object. Defaults to [].

            Returns:
                boolean: True: things have been saved / False: error with DB
            """
            empresa = None

            # Filtered the object to be updated
            with self.conn_obj.Session() as session:
                empresa = session.query(self.orm).filter_by(compt=update_dict['compt']).join(
                    self.orm.main_empresas)\
                    .filter(SqlAchemyOrms.MainEmpresas.cnpj == cnpj).one_or_none()
                if empresa:
                    for key, value in update_dict.items():
                        # Check if the key is allowed to be updated
                        if allowed != []:
                            if key not in allowed:
                                continue
                        # Update the value of the attribute
                        setattr(empresa, key, value)
                    session.merge(empresa)
                    # session.add means insert, merge means commit
                    session.commit()
                    return True

                return False

        def delete_from_id_empresa(self, _id_empresa: int, compt):
            """Deleta a competência a partir do _id_empresa
            Args:
                _id (int): _description_
                compt (_type_): _description_

            Returns:
            """
            with self.conn_obj.Session() as session:
                record = session.query(self.orm).join(SqlAchemyOrms.MainEmpresas,
                                                      self.orm.main_empresa_id == _id_empresa) \
                    .filter(self.orm.compt == compt).one_or_none()

                if record is not None:
                    session.delete(record)
                    session.commit()
                    return True
                else:
                    return False


class InitNewCompt:
    def __init__(self, compt, setup=True) -> None:
        """Initialize a new compt if it not exists

        Args:
            compt_str (str): "%mm-yyyy"
            setup (bool): runs setup or not
        """
        self.conn_obj = MySqlInitConnection()
        self.engine = self.conn_obj.engine
        self.orm = SqlAchemyOrms.ClientsCompts
        self.compt = compt
        if setup:
            self.setup()

    def setup(self) -> None:
        from sqlalchemy import and_, desc
        from datetime import timedelta

        with self.conn_obj.Session() as session:
            # get the most recent row in the table
            most_recent_row = session.query(self.orm).order_by(
                desc(self.orm.compt)).first()
            # get the row(s) you want to duplicate
            rows_to_duplicate = session.query(self.orm).filter(
                self.orm.compt == most_recent_row.compt,
                # assuming pode_declarar is a boolean
            )

            # create the new compt datetime object
            compt_datetime = datetime.strptime(self.compt, '%m-%Y')

        with self.conn_obj.Session() as session:
            # check if the row already exists
            row_exists = session.query(self.orm).filter(
                self.orm.compt == compt_datetime).first()
            if not row_exists:
                print("Init new compt: ", self.compt, '-------')
                # create new rows with incremented date

                for row in rows_to_duplicate:
                    _envio = True if str(
                        row.imposto_a_calcular) == 'LP' else False
                    _declarado = True if str(
                        row.imposto_a_calcular) == 'LP' else False

                    def status_imports_g5(
                        campo): return campo if campo.upper() != 'OK' else ''

                    new_row = self.orm(
                        main_empresa_id=row.main_empresa_id,
                        declarado=_declarado,
                        nf_saidas=status_imports_g5(row.nf_saidas),
                        nf_entradas=status_imports_g5(row.nf_entradas),
                        sem_retencao=0.00,
                        com_retencao=0.00,
                        valor_total=0.00,
                        anexo=row.anexo,
                        imposto_a_calcular=row.imposto_a_calcular,
                        compt=compt_datetime,
                        envio=_envio,
                        pode_declarar=False  # set to False
                    )
                    session.add(new_row)
                session.commit()

    def add_new_client(self, empresa_id, imposto_a_calcular):
        # Vou utilizar anexo sugerido...
        if imposto_a_calcular == 'ICMS':
            anexo_sugerido = 'I'
        elif imposto_a_calcular == 'ISS':
            anexo_sugerido = 'III'
        else:
            anexo_sugerido = ''

        compt_datetime = self.compt

        with self.conn_obj.Session() as session:
            exists = session.query(self.orm).filter_by(
                compt=compt_datetime, main_empresa_id=empresa_id).first()

            if not exists:
                _envio = True if str(
                    imposto_a_calcular) == 'LP' else False
                _declarado = True if str(
                    imposto_a_calcular) == 'LP' else False
                new_row = self.orm(
                    main_empresa_id=empresa_id,
                    declarado=_declarado,
                    nf_saidas='',
                    nf_entradas='',
                    sem_retencao=0.00,
                    com_retencao=0.00,
                    valor_total=0.00,
                    anexo=anexo_sugerido,
                    imposto_a_calcular=imposto_a_calcular,
                    compt=compt_datetime,
                    envio=_envio,
                    pode_declarar=False  # set to False
                )
                session.add(new_row)
                session.commit()
                return True
            return False
