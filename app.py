from flask import Flask, render_template, jsonify, request, redirect, make_response
from scripts.metodos import PerguntaDAO, RespostaDAO, UsuarioDAO
from scripts.modelo import Pergunta, Resposta, Usuario
from scripts.back_end import validar_dados

app = Flask(__name__)

'''
=============
     API
=============
'''

@app.route('/questions', methods=['GET'])
def obter_perguntas():
    return jsonify(PerguntaDAO.buscar_todos())

@app.route('/api/usuarios', methods=['GET'])
def obter_usuarios():
    return jsonify(UsuarioDAO.buscar_todos())

@app.route('/api/usuarios', methods=['POST'])
def incluir_novo_usuario():
    try:
        user = request.get_json()
        novo_usuario = Usuario(
            cpf=user["cpf"],
            data_entrada=user["data_entrada"],
            data_nasc=user["data_nasc"],
            email=user["email"],
            nome=user["nome"],
            numero_matricula=user["numero_matricula"],
            senha=user["senha"]
        )
        UsuarioDAO.salvar_usuario(novo_usuario)
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/questions', methods=['POST'])
def incluir_nova_pergunta():
    nova_pergunta_request = request.get_json()
    nova_pergunta = Pergunta(
        titulo=nova_pergunta_request["titulo"],
        pergunta=nova_pergunta_request["pergunta"],
        categoria=nova_pergunta_request["categoria"],
        estudante=request.cookies.get('numero_matricula')
    )
    PerguntaDAO.salvar_pergunta(nova_pergunta)
    return jsonify(PerguntaDAO.buscar_todos()), 201

@app.route('/api/perguntas/<categoria>', methods=['GET'])
def api_perguntas_por_categoria(categoria):
    perguntas = PerguntaDAO.buscar_por_categoria(categoria)
    return jsonify(perguntas)

@app.route('/questions/<int:idpergunta>', methods=['GET'])
def obter_pergunta_por_id(idpergunta):
    pergunta = PerguntaDAO.buscar_por_id(idpergunta)
    return jsonify(pergunta)

@app.route('/respost', methods=['GET'])
def obter_respostas():
    return jsonify(RespostaDAO.buscar_todos())

@app.route('/respost/<int:idpergunta>', methods=['GET'])
def obter_resposta_por_id_pergunta(idpergunta):
    respostas = RespostaDAO.buscar_por_idpergunta(idpergunta)
    return jsonify(respostas)

@app.route('/respost/<int:idpergunta>', methods=['POST'])
def incluir_nova_resposta(idpergunta):
    nova_resposta_request = request.get_json()
    nova_resposta = Resposta(
        pergunta_referente=idpergunta,
        texto=nova_resposta_request["texto"],
        estudante=request.cookies.get('numero_matricula')
    )
    RespostaDAO.salvar_resposta(nova_resposta)
    return jsonify(RespostaDAO.buscar_todos()), 201

'''
==================
     FRONT-END
==================
'''

@app.route('/home', methods=['GET'])
def home():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('index.html')
    else:
        return render_template("error.html")

@app.route('/info', methods=['GET'])
def info():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('perguntas.html', categoria='info')
    else:
        return render_template("error.html")

@app.route('/ali', methods=['GET'])
def ali():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('perguntas.html', categoria='ali')
    else:
        return render_template("error.html")

@app.route('/eletro', methods=['GET'])
def eletro():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('perguntas.html', categoria='eletro')
    else:
        return render_template("error.html")

@app.route('/mec', methods=['GET'])
def mec():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('perguntas.html', categoria='mec')
    else:
        return render_template("error.html")

@app.route('/div', methods=['GET'])
def div():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('perguntas.html', categoria='div')
    else:
        return render_template("error.html")

@app.route('/pergunta', methods=['GET'])
def pergunta():
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        return render_template('pergunta.html')
    else:
        return render_template("error.html")

@app.route('/pergunta_completa/<int:idpergunta>', methods=['GET'])
def pergunta_completa(idpergunta):
    user_number = request.cookies.get('numero_matricula')
    if user_number != None:
        pergunta = next(
            (p for p in PerguntaDAO.buscar_todos() if p['idpergunta'] == idpergunta),
            None
        )
        if not pergunta:
            return "Pergunta não encontrada", 404
        respostas = RespostaDAO.buscar_por_idpergunta(idpergunta)
        return render_template(
            'pergunta_completa.html',
            pergunta=pergunta,
            respostas=respostas
        )
    else:
        return render_template("error.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get("usuario")
    password = request.form.get("password")
    
    if validar_dados(user, password):
        user_number = UsuarioDAO.buscar_id_por_nome(user)
        
        if user_number:
            response = make_response(redirect('/home'))
            response.set_cookie('numero_matricula', str(user_number))
            return response
        else:
            return "Usuário não encontrado", 404
    return "Credenciais inválidas, tente novamente.", 401


@app.route('/registrar', methods=['GET'])
def registrar():
    return render_template('registrar.html')

if __name__ == '__main__':
    app.run(debug=True)
