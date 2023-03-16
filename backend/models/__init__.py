from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import Integer, String, Numeric, Date
from backend.database import MySqlInitConnection as Connection


class SqlAchemyOrms(Connection):
    Base = declarative_base()

    class MainEmpresas(Base):
        __tablename__ = 'main_empresas'

        id = Column(Integer, primary_key=True)
        razao_social = Column(String(255))
        cnpj = Column(String(18), unique=True)
        cpf = Column(String(14))
        codigo_simples = Column(String(12))
        email = Column(String(255))
        gissonline = Column(String(500))
        giss_login = Column(String(50))
        ginfess_cod = Column(String(100))
        ginfess_link = Column(String(500))
        ha_procuracao_ecac = Column(String(15))

        clients_compts = relationship(
            "ClientsCompts", back_populates="main_empresas")

        def __repr__(self):
            return f"<MainEmpresas(cnpj='{self.cnpj}', razao_social='{self.razao_social}')>"

    class ClientsCompts(Base):
        __tablename__ = 'clients_compts'

        id = Column(Integer, primary_key=True)
        main_empresa_id = Column(Integer, ForeignKey('main_empresas.id'))
        main_empresas = relationship(
            "MainEmpresas", back_populates="clients_compts")
        # razao_social = Column(String(100))
        declarado = Column(Boolean())
        nf_saidas = Column(String(30))
        nf_entradas = Column(String(30))
        sem_retencao = Column(Numeric(precision=10, scale=2))
        com_retencao = Column(Numeric(precision=10, scale=2))
        valor_total = Column(Numeric(precision=10, scale=2))
        anexo = Column(String(3))
        envio = Column(Boolean())
        imposto_a_calcular = Column(String(7))
        possui_das_pendentes = Column(Boolean())
        compt = Column(Date())
        # pode_declarar =  Column(Boolean())
        # TODO: adicionar pode_declarar
