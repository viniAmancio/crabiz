from conexao import Conexao
from hashlib import sha256



class Usuario:
    def __init__(self):
        self.tel = None
        self.nome = None
        self.senha = None
        self.logado = False
    def cadastrar(self, telefone, nome, senha):
        senha = sha256(senha.encode()).hexdigest()
        try:
            mydb = Conexao.conectar()


            mycursor = mydb.cursor()

            
            sql = f"INSERT INTO tb_usuario (tel, nome, senha) VALUES ('{telefone}', '{nome}', '{senha}')"
            
            mycursor.execute(sql)
            
            self.tel = telefone
            self.nome = nome
            self.senha = senha
            self.logado = True


            mydb.commit()

            print(mycursor.rowcount, "registro inserido")

            mycursor.execute("SELECT tel, nome FROM tb_usuario")

            ver = mycursor.fetchall()

            print(ver)

            mydb.close()
            return True
        except:
            return False

    def logar(self, telefone, senha):
            # criptografa a senha
            senha = sha256(senha.encode()).hexdigest()

            mydb = Conexao.conectar()

            mycursor = mydb.cursor()

            sql = f"SELECT tel, nome, senha FROM tb_usuario WHERE tel='{telefone}' AND senha='{senha}'"
            
            mycursor.execute(sql)
            ''
            resultado = mycursor.fetchone()
            print(resultado)
            if not resultado == None:
                 self.logado = True
                 self.nome = resultado[1]
                 self.tel = resultado[0]
                 self.senha = resultado[2]
            else:
                 self.logado = False

