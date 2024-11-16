from flask import Flask, jsonify, request
import metodos
from scripts.modelo import *

app = Flask(__name__)

userDAO = metodos.UsuarioDAO()
perguntasDAO = metodos.PerguntaDAO()
respostasDAO = metodos.RespostaDAO()

@app.route('/users', methods=['GET'])
def obter_usuarios():
    return jsonify(userDAO.buscar_todos())

@app.route('/questions', methods=['GET'])
def obter_perguntas():
    return jsonify(perguntasDAO.buscar_todos())

@app.route('/respost', methods=['GET'])
def obter_respostas():
    return jsonify(respostasDAO.buscar_todos())

@app.route('/users/<int:numero_matricula>', methods=['GET'])
def obter_usuarios_por_numero_matricula(numero_matricula):
    for user in userDAO.buscar_todos():
        if user.get('numero_matricula') == numero_matricula:
            return jsonify(user)
    return jsonify({"error": "Usuário não encontrado"}), 404

@app.route('/questions/<int:idpergunta>', methods=['GET'])
def obter_pergunta_por_id(idpergunta):
    for pergunta in perguntasDAO.buscar_todos():
        if pergunta.get('idpergunta') == idpergunta:
            return jsonify(pergunta)
    return jsonify({"error": "Pergunta não encontrada"}), 404

@app.route('/questions/<categoria>', methods=['GET'])
def obter_pergunta_por_categoria(categoria):
    perguntas = [
        pergunta for pergunta in perguntasDAO.buscar_todos()
        if pergunta.get('categoria') == categoria
    ]
    return jsonify(perguntas)

@app.route('/respost/<int:idpergunta>', methods=['GET'])
def obter_resposta_por_id_pergunta(idpergunta):
    for resposta in respostasDAO.buscar_todos():
        if resposta.get('idpergunta') == idpergunta:
            return jsonify(resposta)
    return jsonify({"error": "Pergunta não encontrada"}), 404

@app.route('/respost/<int:idresposta>', methods=['GET'])
def obter_resposta_por_id_resposta(idresposta):
    for resposta in respostasDAO.buscar_todos():
        if resposta.get('idresposta') == idresposta:
            return jsonify(resposta)
    return jsonify({"error": "Pergunta não encontrada"}), 404

@app.route('/users', methods=['POST'])
def incluir_novo_user():
    novo_user_request = request.get_json()
    novo_user = Usuario(
        senha=novo_user_request["senha"],
        nome=novo_user_request["nome"],
        cpf=novo_user_request["cpf"],
        email=novo_user_request["email"],
        data_nasc=novo_user_request["data_nasc"],
        data_entrada=novo_user_request["data_entrada"],
        numero_matricula=novo_user_request["numero_matricula"]
    )
    userDAO.salvar_usuario(novo_user)
    return jsonify(userDAO.buscar_todos()), 201

@app.route('/questions', methods=['POST'])
def incluir_nova_pergunta():
    nova_pergunta_request = request.get_json()
    nova_pergunta = Pergunta(
        idpergunta=nova_pergunta_request["idpergunta"],
        titulo=nova_pergunta_request["titulo"],
        pergunta=nova_pergunta_request["pergunta"],
        categoria=nova_pergunta_request["categoria"],
        estudante=nova_pergunta_request["estudante"]
    )
    perguntasDAO.salvar_pergunta(nova_pergunta)
    return jsonify(perguntasDAO.buscar_todos()), 201

@app.route('/respost', methods=['POST'])
def incluir_nova_resposta():
    nova_resposta_request = request.get_json()
    nova_resposta = Resposta(
        pergunta_referente=nova_resposta_request["pergunta_referente"],
        idresposta=nova_resposta_request["idresposta"],
        texto=nova_resposta_request["texto"],
        estudante=nova_resposta_request["estudante"]
    )
    respostasDAO.salvar_resposta(nova_resposta)
    return jsonify(respostasDAO.buscar_todos()), 201

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)