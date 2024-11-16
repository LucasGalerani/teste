from scripts.conexao import Conexao

def validar_dados(user, senha):
    minha_conexao = Conexao()
    query = "SELECT * FROM usuario WHERE nome = %s AND senha = %s"
    minha_conexao.cursor.execute(query, (user, senha))
    resultado = minha_conexao.cursor.fetchone()
    if resultado is None:
        return False
    else:
        return True
