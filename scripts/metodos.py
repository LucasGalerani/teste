from scripts.conexao import Conexao
from scripts.modelo import *

class UsuarioDAO:  
    @staticmethod
    def buscar_todos() -> list:
        with Conexao() as conexao:
            conexao.cursor_dict.execute("SELECT * FROM usuario")
            usuarios_data = conexao.cursor_dict.fetchall()
        return usuarios_data

    
    @staticmethod
    def salvar_usuario(usuario: Usuario):
        with Conexao() as conexao:
            sql = "INSERT INTO usuario (nome, senha, cpf, email, data_nasc, data_entrada, numero_matricula) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (usuario.nome, usuario.senha, usuario.cpf, usuario.email, usuario.data_nasc, usuario.data_entrada, usuario.numero_matricula)
            conexao.cursor.execute(sql, valores)
            conexao.mydb.commit()

    @staticmethod
    def buscar_id_por_nome(nome: str) -> list:
        with Conexao() as conexao:
            query = "SELECT * FROM usuario WHERE nome = %s"
            conexao.cursor_dict.execute(query, (nome,))
            pergunta_data = conexao.cursor_dict.fetchall()
            
        if pergunta_data:
            return pergunta_data[0]["numero_matricula"]
        else:
            return None


class PerguntaDAO:  
    @staticmethod
    def buscar_todos() -> list:
        with Conexao() as conexao:
            conexao.cursor_dict.execute("SELECT * FROM pergunta")
            pergunta_data = conexao.cursor_dict.fetchall()
        return pergunta_data
    
    @staticmethod
    def buscar_por_categoria(categoria) -> list:
        with Conexao() as conexao:
            query = "SELECT * FROM pergunta WHERE categoria = %s"
            conexao.cursor_dict.execute(query, (categoria,))
            pergunta_data = conexao.cursor_dict.fetchall()
        return pergunta_data
    
    @staticmethod
    def buscar_por_id(idpergunta) -> list:
        with Conexao() as conexao:
            query = "SELECT * FROM pergunta WHERE idpergunta = %s"
            conexao.cursor_dict.execute(query, (idpergunta,))
            pergunta_data = conexao.cursor_dict.fetchall()
        return pergunta_data

    @staticmethod
    def salvar_pergunta(pergunta: Pergunta):
        with Conexao() as conexao:
            sql = "INSERT INTO pergunta (idpergunta, titulo, pergunta, estudante, categoria) VALUES (%s, %s, %s, %s, %s)"
            valores = (pergunta.idpergunta, pergunta.titulo, pergunta.pergunta, pergunta.estudante, pergunta.categoria)
            conexao.cursor.execute(sql, valores)
            conexao.mydb.commit()

class RespostaDAO:  
    @staticmethod
    def buscar_todos() -> list:
        with Conexao() as conexao:
            conexao.cursor_dict.execute("SELECT * FROM resposta")
            resposta_data = conexao.cursor_dict.fetchall()
        return resposta_data
    
    @staticmethod
    def salvar_resposta(resposta: Resposta):
        with Conexao() as conexao:
            sql = "INSERT INTO resposta (idresposta, pergunta_referente, texto, estudante) VALUES (%s, %s, %s, %s)"
            valores = (resposta.idresposta, resposta.pergunta_referente, resposta.texto, resposta.estudante)
            conexao.cursor.execute(sql, valores)
            conexao.mydb.commit()

    @staticmethod
    def buscar_por_idpergunta(idpergunta) -> list:
        with Conexao() as conexao:
            query = "SELECT * FROM resposta WHERE pergunta_referente = %s"
            conexao.cursor_dict.execute(query, (idpergunta,))
            pergunta_data = conexao.cursor_dict.fetchall()
        return pergunta_data