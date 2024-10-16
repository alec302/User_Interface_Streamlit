import streamlit as st
import pandas as pd
import requests

# Base URL for the backend API (Flask)
BASE_URL = "http://127.0.0.1:5000"

# Helper function to make API requests
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            st.error("Método HTTP não suportado.")
            return None

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        return None

# Streamlit App
st.title("Sistema de Aluguel de Bicicletas")
st.sidebar.header("Escolha a Função")

# Sidebar for different actions
action = st.sidebar.selectbox("Ação", [
    "Visualizar Bicicletas", 
    "Gerenciar Bicicletas",
    "Visualizar Usuários", 
    "Gerenciar Usuários",
    "Alugar Bicicleta", 
    "Devolver Bicicleta",
    "Ver Empréstimos"
])

#################################
# Visualizar Bicicletas
#################################
if action == "Visualizar Bicicletas":
    st.header("Bicicletas Disponíveis")

    # Fetch bikes from API
    bikes_data = fazer_requisicao("bikes", method="GET")

    if bikes_data:
        df_bikes = pd.DataFrame(bikes_data)
        st.dataframe(df_bikes)
    else:
        st.write("❌ Nenhuma bicicleta encontrada.")

#################################
# Gerenciar Bicicletas (Adicionar, Editar, Excluir)
#################################
if action == "Gerenciar Bicicletas":
    st.header("Gerenciar Bicicletas")

    # Add a new bike
    st.subheader("Adicionar Nova Bicicleta")
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    cidade = st.text_input("Cidade")
    status = st.selectbox("Status", ["disponivel", "em uso"])

    if st.button("Adicionar Bicicleta"):
        if marca and modelo and cidade:
            bike_data = {
                "marca": marca,
                "modelo": modelo,
                "cidade": cidade,
                "status": status
            }
            response = fazer_requisicao("bikes", method="POST", data=bike_data)
            if response:
                st.success("🚲 Bicicleta adicionada com sucesso!")
        else:
            st.error("⚠️ Todos os campos são obrigatórios.")

    # Update and delete bikes
    st.subheader("Editar ou Excluir Bicicletas Existentes")
    bikes_data = fazer_requisicao("bikes", method="GET")

    if bikes_data:
        bike_id = st.selectbox("Selecione uma Bicicleta para Editar ou Excluir", [bike["_id"] for bike in bikes_data])

        selected_bike = next((bike for bike in bikes_data if bike["_id"] == bike_id), None)
        if selected_bike:
            marca_edit = st.text_input("Marca", value=selected_bike['marca'])
            modelo_edit = st.text_input("Modelo", value=selected_bike['modelo'])
            cidade_edit = st.text_input("Cidade", value=selected_bike['cidade'])
            status_edit = st.selectbox("Status", ["disponivel", "em uso"], index=0 if selected_bike['status'] == "disponivel" else 1)

            if st.button("Atualizar Bicicleta"):
                update_data = {
                    "marca": marca_edit,
                    "modelo": modelo_edit,
                    "cidade": cidade_edit,
                    "status": status_edit
                }
                response = fazer_requisicao(f"bikes/{bike_id}", method="PUT", data=update_data)
                if response:
                    st.success("🚲 Bicicleta atualizada com sucesso!")

            if st.button("Excluir Bicicleta"):
                response = fazer_requisicao(f"bikes/{bike_id}", method="DELETE")
                if response:
                    st.success("🚲 Bicicleta excluída com sucesso!")

#################################
# Visualizar Usuários
#################################
if action == "Visualizar Usuários":
    st.header("Lista de Usuários")

    # Fetch users from API
    users_data = fazer_requisicao("usuarios", method="GET")

    if users_data:
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users)
    else:
        st.write("❌ Nenhum usuário encontrado.")

#################################
# Gerenciar Usuários (Adicionar, Editar, Excluir)
#################################
if action == "Gerenciar Usuários":
    st.header("Gerenciar Usuários")

    # Add a new user
    st.subheader("Adicionar Novo Usuário")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    data_nascimento = st.text_input("Data de Nascimento")

    if st.button("Adicionar Usuário"):
        if nome and cpf and data_nascimento:
            user_data = {
                "nome": nome,
                "cpf": cpf,
                "data_nascimento": data_nascimento
            }
            response = fazer_requisicao("usuarios", method="POST", data=user_data)
            
            # Check if the response is valid and contains the new user's _id
            if response and "_id" in response:
                st.success(f"👤 Usuário adicionado com sucesso! ID do Usuário: {response['_id']}")
            else:
                st.error("❌ Erro ao adicionar usuário. Verifique os dados ou tente novamente.")
        else:
            st.error("⚠️ Todos os campos são obrigatórios.")


    # Update and delete users
    st.subheader("Editar ou Excluir Usuários Existentes")
    users_data = fazer_requisicao("usuarios", method="GET")

    if users_data:
        user_id = st.selectbox("Selecione um Usuário para Editar ou Excluir", [user["_id"] for user in users_data])

        selected_user = next((user for user in users_data if user["_id"] == user_id), None)
        if selected_user:
            nome_edit = st.text_input("Nome", value=selected_user['nome'])
            cpf_edit = st.text_input("CPF", value=selected_user['cpf'])
            data_nascimento_edit = st.text_input("Data de Nascimento", value=selected_user['data_nascimento'])

            if st.button("Atualizar Usuário"):
                update_data = {
                    "nome": nome_edit,
                    "cpf": cpf_edit,
                    "data_nascimento": data_nascimento_edit
                }
                response = fazer_requisicao(f"usuarios/{user_id}", method="PUT", data=update_data)
                if response:
                    st.success("👤 Usuário atualizado com sucesso!")

            if st.button("Excluir Usuário"):
                response = fazer_requisicao(f"usuarios/{user_id}", method="DELETE")
                if response:
                    st.success("👤 Usuário excluído com sucesso!")

#################################
# Alugar Bicicleta
#################################
if action == "Alugar Bicicleta":
    st.header("Alugar uma Bicicleta")

    # Fetch users and available bikes
    users_data = fazer_requisicao("usuarios", method="GET")
    bikes_data = fazer_requisicao("bikes", method="GET")

    if users_data and bikes_data:
        available_bikes = [bike for bike in bikes_data if bike['status'] == 'disponivel']

        if available_bikes:
            selected_user = st.selectbox("Selecione o Usuário", [f"{user['_id']} - {user['nome']}" for user in users_data])
            selected_bike = st.selectbox("Selecione a Bicicleta", [f"{bike['_id']} - {bike['marca']} {bike['modelo']}" for bike in available_bikes])

            user_id = selected_user.split(" - ")[0]
            bike_id = selected_bike.split(" - ")[0]

            if st.button("Alugar Bicicleta"):
                loan_data = fazer_requisicao(f"emprestimos/usuarios/{user_id}/bikes/{bike_id}", method="POST")
                if loan_data:
                    st.success(f"Bicicleta alugada com sucesso! ID do empréstimo: {loan_data['_id']}")
                else:
                    st.error("❌ Falha ao alugar bicicleta.")
        else:
            st.write("❌ Nenhuma bicicleta disponível para aluguel.")
    else:
        st.write("❌ Não foi possível carregar dados de usuários ou bicicletas.")

#################################
# Devolver Bicicleta
#################################
if action == "Devolver Bicicleta":
    st.header("Devolver uma Bicicleta")

    loans_data = fazer_requisicao("emprestimos", method="GET")

    if loans_data:
        df_loans = pd.DataFrame(loans_data)
        st.dataframe(df_loans)
        
        loan_id = st.selectbox("Selecione o ID do Empréstimo para Devolver", df_loans["_id"])
        
        if st.button("Devolver Bicicleta"):
            return_data = fazer_requisicao(f"emprestimos/{loan_id}", method="DELETE")
            if return_data:
                st.success("Bicicleta devolvida com sucesso!")
            else:
                st.error("❌ Falha ao devolver bicicleta.")
    else:
        st.write("❌ Nenhum empréstimo encontrado.")

#################################
# Ver Empréstimos
#################################
if action == "Ver Empréstimos":
    st.header("Lista de Empréstimos Ativos")

    # Fetch loans from API
    loans_data = fazer_requisicao("emprestimos", method="GET")

    if loans_data:
        df_loans = pd.DataFrame(loans_data)
        st.dataframe(df_loans)
    else:
        st.write("❌ Nenhum empréstimo encontrado.")
