class Usuario:
    def __init__(self, nome, senha, cpf, email, data_nasc, data_entrada, numero_matricula):
        self.nome = nome
        self.senha = senha
        self.cpf = cpf
        self.email = email
        self.data_nasc = data_nasc
        self.data_entrada = data_entrada
        self.numero_matricula = numero_matricula

class Pergunta:
    def __init__(self, titulo, pergunta, estudante, categoria, idpergunta='default'):
        self.titulo = titulo
        self.pergunta = pergunta
        self.idpergunta = idpergunta
        self.estudante = estudante
        self.categoria = categoria

class Resposta:
    def __init__(self, pergunta_referente, estudante, texto, idresposta='default'):
        self.idresposta = idresposta
        self.pergunta_referente = pergunta_referente
        self.estudante = estudante
        self.texto = texto