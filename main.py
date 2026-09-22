import json
from abc import ABC, abstractmethod
import streamlit as st

class Usuario:
    def __init__(self, nome: str, email: str, senha: str):
        self.nome = nome
        self.email = email
        self.senha = senha

    def to_dict(self) -> dict:
        return {"nome": self.nome, "email": self.email, "senha": self.senha}

    @staticmethod
    def from_dict(dados: dict):
        return Usuario(dados["nome"], dados["email"], dados["senha"])


class Veiculo:
    def __init__(self, placa: str, modelo: str, ano: int):
        self.placa = placa
        self.modelo = modelo
        self.ano = ano

    def to_dict(self) -> dict:
        return {"placa": self.placa, "modelo": self.modelo, "ano": self.ano}

    @staticmethod
    def from_dict(dados: dict):
        return Veiculo(dados["placa"], dados["modelo"], int(dados["ano"]))


class UsuarioPersistenceStrategy(ABC):
    @abstractmethod
    def carregar(self) -> list:
        pass

    @abstractmethod
    def salvar(self, dados: list):
        pass


class JsonUsuarioPersistence(UsuarioPersistenceStrategy):
    def __init__(self, arquivo: str = "usuarios.json"):
        self.arquivo = arquivo

    def carregar(self) -> list:
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar(self, dados: list):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)


class UsuarioFactory:
    """
    GoF: Factory Method (Criacional)
    GRASP: Creator (Atribui a responsabilidade de criação de Usuario à Fábrica)
    """

    @staticmethod
    def criar_usuario(nome: str, email: str, senha: str) -> Usuario:
        return Usuario(nome, email, senha)


class UsuarioController:
    """
    GRASP: Controller (Coordenador dos eventos de negócio de Usuários)
    """

    def __init__(self, persistencia: UsuarioPersistenceStrategy):
        self.persistencia = persistencia

    def _carregar_todos(self) -> list:
        dados = self.persistencia.carregar()
        return [Usuario.from_dict(d) for d in dados]

    def _salvar_todos(self, usuarios: list):
        dados = [u.to_dict() for u in usuarios]
        self.persistencia.salvar(dados)

    def cadastrar(self, nome: str, email: str, senha: str) -> tuple[bool, str]:
        if not nome or not email or not senha:
            return False, "Todos os campos são obrigatórios."

        usuarios = self._carregar_todos()
        for u in usuarios:
            if u.email == email:
                return False, "Email já cadastrado."

        novo_usuario = UsuarioFactory.criar_usuario(nome, email, senha)
        usuarios.append(novo_usuario)
        self._salvar_todos(usuarios)
        return True, "Usuário cadastrado com sucesso!"

    def listar(self) -> list:
        return self._carregar_todos()

    def editar(self, email: str, novo_nome: str, nova_senha: str) -> tuple[bool, str]:
        usuarios = self._carregar_todos()
        for u in usuarios:
            if u.email == email:
                if novo_nome:
                    u.nome = novo_nome
                if nova_senha:
                    u.senha = nova_senha
                self._salvar_todos(usuarios)
                return True, "Usuário editado com sucesso!"
        return False, "Usuário não encontrado."

    def remover(self, email: str) -> tuple[bool, str]:
        usuarios = self._carregar_todos()
        for u in usuarios:
            if u.email == email:
                usuarios.remove(u)
                self._salvar_todos(usuarios)
                return True, "Usuário removido com sucesso!"
        return False, "Usuário não encontrado."


class VeiculoBuilder:
    """
    GoF: Builder (Criacional) - Facilita a construção passo a passo do objeto Veiculo.
    """

    def __init__(self):
        self.placa = ""
        self.modelo = ""
        self.ano = 0

    def com_placa(self, placa: str):
        self.placa = placa.upper().strip()
        return self

    def com_modelo(self, modelo: str):
        self.modelo = modelo.strip()
        return self

    def com_ano(self, ano: int):
        self.ano = ano
        return self

    def build(self) -> Veiculo:
        return Veiculo(self.placa, self.modelo, self.ano)


class VeiculoRepositorySingleton:
    """
    GoF: Singleton (Criacional) - Garante uma única instância do Repositório de Veículos.
    """
    _instance = None

    def __new__(cls, arquivo: str = "veiculos.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.arquivo = arquivo
        return cls._instance

    def carregar(self) -> list:
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar(self, dados: list):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)


class VeiculoController:
    """
    GRASP: Controller - Gerencia operações de negócio do cadastro de carros.
    GRASP: Information Expert - Consulta e gerencia a lógica das regras de Veiculo.
    """

    def __init__(self):
        self.repositorio = VeiculoRepositorySingleton()

    def _carregar_todos(self) -> list:
        dados = self.repositorio.carregar()
        return [Veiculo.from_dict(d) for d in dados]

    def _salvar_todos(self, veiculos: list):
        dados = [v.to_dict() for v in veiculos]
        self.repositorio.salvar(dados)

    def cadastrar(self, placa: str, modelo: str, ano: int) -> tuple[bool, str]:
        if not placa or not modelo or ano <= 1885:
            return False, "Dados inválidos para o veículo."

        veiculos = self._carregar_todos()
        placa_formatada = placa.upper().strip()
        for v in veiculos:
            if v.placa == placa_formatada:
                return False, "Veículo com esta placa já cadastrado."

        novo_veiculo = VeiculoBuilder() \
            .com_placa(placa) \
            .com_modelo(modelo) \
            .com_ano(ano) \
            .build()

        veiculos.append(novo_veiculo)
        self._salvar_todos(veiculos)
        return True, "Veículo cadastrado com sucesso!"

    def listar(self) -> list:
        return self._carregar_todos()

    def editar(self, placa: str, novo_modelo: str, novo_ano: int) -> tuple[bool, str]:
        veiculos = self._carregar_todos()
        placa_busca = placa.upper().strip()
        for v in veiculos:
            if v.placa == placa_busca:
                if novo_modelo:
                    v.modelo = novo_modelo
                if novo_ano > 1885:
                    v.ano = novo_ano
                self._salvar_todos(veiculos)
                return True, "Veículo atualizado com sucesso!"
        return False, "Veículo não encontrado."

    def remover(self, placa: str) -> tuple[bool, str]:
        veiculos = self._carregar_todos()
        placa_busca = placa.upper().strip()
        for v in veiculos:
            if v.placa == placa_busca:
                veiculos.remove(v)
                self._salvar_todos(veiculos)
                return True, "Veículo removido com sucesso!"
        return False, "Veículo não encontrado."

# Initialize controllers
if "user_ctrl" not in st.session_state:
    st.session_state.persistencia_usuario = JsonUsuarioPersistence("usuarios.json")
    st.session_state.user_ctrl = UsuarioController(st.session_state.persistencia_usuario)

if "car_ctrl" not in st.session_state:
    st.session_state.car_ctrl = VeiculoController()

user_ctrl = st.session_state.user_ctrl
car_ctrl = st.session_state.car_ctrl

st.set_page_config(page_title="Sistema de Gestão", page_icon="🚗", layout="wide")

st.title("🚗 Sistema de Gestão (Usuários & Veículos)")
st.sidebar.title("Menu de Navegação")
modulo = st.sidebar.radio("Escolha o Módulo:", ["Gerenciar Usuários", "Gerenciar Veículos"])

if modulo == "Gerenciar Usuários":
    st.header("👤 Módulo de Usuários")
    tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar", "Listar", "Editar", "Remover"])

    with tab1:
        st.subheader("Cadastrar Novo Usuário")
        with st.form("form_cad_usuario"):
            nome = st.text_input("Nome")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Cadastrar Usuário")

            if submitted:
                sucesso, msg = user_ctrl.cadastrar(nome, email, senha)
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)

    with tab2:
        st.subheader("Lista de Usuários Cadastrados")
        usuarios = user_ctrl.listar()
        if not usuarios:
            st.info("Nenhum usuário cadastrado.")
        else:
            data = [{"Nome": u.nome, "Email": u.email} for u in usuarios]
            st.dataframe(data, use_container_width=True)
    with tab3:
        st.subheader("Editar Usuário")
        usuarios = user_ctrl.listar()
        emails = [u.email for u in usuarios]

        if not emails:
            st.info("Não há usuários disponíveis para edição.")
        else:
            email_selecionado = st.selectbox("Selecione o Email do Usuário", emails)
            usuario_atual = next((u for u in usuarios if u.email == email_selecionado), None)

            with st.form("form_edit_usuario"):
                novo_nome = st.text_input("Novo Nome", value=usuario_atual.nome if usuario_atual else "")
                nova_senha = st.text_input("Nova Senha (deixe em branco para não alterar)", type="password")
                submit_edit = st.form_submit_button("Salvar Alterações")

                if submit_edit:
                    sucesso, msg = user_ctrl.editar(email_selecionado, novo_nome, nova_senha)
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with tab4:
        st.subheader("Remover Usuário")
        usuarios = user_ctrl.listar()
        emails = [u.email for u in usuarios]

        if not emails:
            st.info("Não há usuários disponíveis para remoção.")
        else:
            email_remover = st.selectbox("Selecione o Email para Remover", emails, key="remove_user_select")
            if st.button("Remover Usuário", type="primary"):
                sucesso, msg = user_ctrl.remover(email_remover)
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

elif modulo == "Gerenciar Veículos":
    st.header("🚘 Módulo de Veículos (Carros)")
    tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar", "Listar", "Editar", "Remover"])

    with tab1:
        st.subheader("Cadastrar Novo Veículo")
        with st.form("form_cad_veiculo"):
            placa = st.text_input("Placa (ex: ABC-1234)")
            modelo = st.text_input("Modelo")
            ano = st.number_input("Ano", min_value=1886, max_value=2100, value=2023, step=1)
            submitted_car = st.form_submit_button("Cadastrar Veículo")

            if submitted_car:
                sucesso, msg = car_ctrl.cadastrar(placa, modelo, int(ano))
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)

    with tab2:
        st.subheader("Lista de Veículos Cadastrados")
        veiculos = car_ctrl.listar()
        if not veiculos:
            st.info("Nenhum veículo cadastrado.")
        else:
            data_veiculos = [{"Placa": v.placa, "Modelo": v.modelo, "Ano": v.ano} for v in veiculos]
            st.dataframe(data_veiculos, use_container_width=True)

    with tab3:
        st.subheader("Editar Veículo")
        veiculos = car_ctrl.listar()
        placas = [v.placa for v in veiculos]

        if not placas:
            st.info("Não há veículos disponíveis para edição.")
        else:
            placa_selecionada = st.selectbox("Selecione a Placa do Veículo", placas)
            veiculo_atual = next((v for v in veiculos if v.placa == placa_selecionada), None)

            with st.form("form_edit_veiculo"):
                novo_modelo = st.text_input("Novo Modelo", value=veiculo_atual.modelo if veiculo_atual else "")
                novo_ano = st.number_input("Novo Ano", min_value=1886, max_value=2100,
                                           value=veiculo_atual.ano if veiculo_atual else 2023, step=1)
                submit_edit_car = st.form_submit_button("Salvar Alterações")

                if submit_edit_car:
                    sucesso, msg = car_ctrl.editar(placa_selecionada, novo_modelo, int(novo_ano))
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # Tab 4: Remover
    with tab4:
        st.subheader("Remover Veículo")
        veiculos = car_ctrl.listar()
        placas = [v.placa for v in veiculos]

        if not placas:
            st.info("Não há veículos disponíveis para remoção.")
        else:
            placa_remover = st.selectbox("Selecione a Placa para Remover", placas, key="remove_car_select")
            if st.button("Remover Veículo", type="primary"):
                sucesso, msg = car_ctrl.remover(placa_remover)
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
