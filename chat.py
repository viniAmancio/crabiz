from usuario import Usuario
from mensagem import Mensagem
from conexao import Conexao
from contato import Contato

class Chat:
    def __init__(self, nome: str , telefone: str):
        self.nome_usuario = nome
        self.telefone_usuario = telefone
    
    
    def enviar_mensagem(self, conteudo:str, destinatario: Contato) -> bool:
        """Método para enviar mensagens do usuário"""
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()
        sql = (f"INSERT INTO tb_mensagem (mensagem, tel_remetente, tel_destinatario) VALUES ('{conteudo}', '{self.telefone_usuario}', '{destinatario.tel}')")

        mycursor.execute(sql)
        mydb.commit()
    

        

    def verificar_mensagem(self, quantidade: int, contato: Contato):
        """Método para verificar mensagens do usuário"""
        mydb = Conexao.conectar()   
        mycursor = mydb.cursor()

        sql = f"SELECT tel_remetente, mensagem, nome, tel_destinatario FROM tb_mensagem INNER JOIN tb_usuario ON tb_usuario.tel = tb_mensagem.tel_remetente WHERE tel_destinatario='{contato.tel}' AND tel_remetente='{self.telefone_usuario}' OR tel_destinatario='{self.telefone_usuario}' AND tel_remetente = '{contato.tel}'"
        
        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        mensagens = []
        for i in resultado:
            mensagem = {"mensagem":i[1], "nome":i[2]}
            mensagens.append(mensagem) #acrecenta a var mensagem na lista mensagens
        return(mensagens)
    
    

    def retorna_contatos(self):
        mydb = Conexao.conectar()     
        mycursor = mydb.cursor()

        sql = "SELECT nome, tel FROM tb_usuario"
        
        mycursor.execute(sql)
        lista = mycursor.fetchall()
        cont = 0
        usuarios = []
        for i in lista:
            usuario = { "nome":i[0],"telefone":i[1]}
            usuarios.append(usuario) #acrecenta a var mensagem na lista mensagens
            cont += 1
        return(usuarios)
    