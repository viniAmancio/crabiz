from flask import Flask, render_template, session,  request, jsonify,redirect
from chat import Chat
from usuario import Usuario
from contato import Contato


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else: # POST
        nome = request.form['nome']
        senha = request.form['senha']
        telefone = request.form['telefone']

        usuario = Usuario()
        if usuario.cadastrar(telefone, nome ,senha):
            return "Usuario logado"
        else:
            return "Falha ao cadastrar"
        

@app.route('/logar', methods = ['GET','POST'])
def logar():
    if request.method =='GET':
        return render_template('login.html')
    else:
        senha = request.form['senha']
        telefone = request.form['telefone']
        usuario = Usuario()
        usuario.logar(telefone, senha)
        if  usuario.logado == True:
            session['usuario_logado'] = {"nome": usuario.nome,
                                    "telefone": usuario.tel}
            return redirect("/mensagem")
            
        else:
            session.clear()
            return redirect("/logar")
        

@app.route('/mensagem', methods = ['GET' , 'POST']) 
def mensagem():
    if request.method=='GET':
        return render_template("mensagem.html")
    else:
        chat = Chat()
        destinatarios = chat.retorna_contatos()
        contagem = 0
        for contato in destinatarios:
            print(contagem, " - ", contato.nome)
            contagem += 1
        destino = request.form['destinatario']  
        contato = destinatarios[destino]


@app.route("/cadastro_via_requisicao", methods = ['POST'])
def post_cadastro():
    dados_cadastro = request.get_json()
    nome = dados_cadastro['nome']
    telefone = dados_cadastro['telefone']
    senha = dados_cadastro['senha']
    
    usuario = Usuario()

    if usuario.cadastrar(telefone, nome ,senha):
        return jsonify({'mensagem': 'Cadastro com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao cadastrar'}), 500
    

@app.route("/get/usuarios")
def api_get_usuarios():
    nome_usuario = session['usuario_logado']["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retorna_contatos()
    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session['usuario_logado']["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    chat = Chat(nome_usuario, telefone_usuario)
    contato = Contato("", tel_destinatario)
    mensagens = chat.verificar_mensagem(0, contato)
    return jsonify(mensagens), 200

@app.route("/enviar_mensagem", methods=['GET', 'POST'])
def enviar_mensagem():
    dados = request.get_json()
    
    nome_usuario = session['usuario_logado']["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    destinatario = dados["tel"]
    mensagem = dados["mensagem"]

    chat = Chat(nome_usuario, telefone_usuario)
    contato = Contato("", destinatario)
    mensagens = chat.enviar_mensagem(mensagem, contato)
    return jsonify(mensagens), 200


app.run(host='0.0.0.0', port="8080")

        