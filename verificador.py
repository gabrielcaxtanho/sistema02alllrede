from flask import Flask, render_template, request, redirect, session, flash

class ONU:
    def __init__(self, usuario, cliente, equipamento, motivo, anotacoes, data):
        self.usuario = usuario
        self.cliente = cliente
        self.equipamento = equipamento
        self.motivo = motivo
        self.anotacoes = anotacoes
        self.data = data


onu1 = ONU("USER", "CLIENTE EXEMPLO", "EQUIPAMENTO EXEMPLO", "MOTIVO EXEMPLO",  "ANOTAÇOES EXEMPLO", "XX/XX/XXXX")
lista = [onu1]
class NOVOUSUARIO:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
gabriel = NOVOUSUARIO("LOGIN", "SENHA")
usuarios = [gabriel]
app = Flask(__name__)

app.secret_key = 'gabriel'

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    usuario = session['usuario_logado']
    user_onus = [onu for onu in lista if onu.usuario == usuario]

    return render_template("lista.html", titulo="Anotações", onus=user_onus)

###Filtrando ONU e usuarios para aparecer apenas os registros feito pelo usuario
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    return render_template("novo.html", titulo= "NOVA ANOTAÇAO")
#Usando o protocolo HTTP, conseguimos passar informações de um formulário pela Web.
#No caso do Flask, queremos receber informações e tratar usando Python.
@app.route('/criar', methods=['POST'])
def criar():
    cliente = request.form['cliente']
    equipamento = request.form['equipamento']
    motivo = request.form['motivo']
    anotacoes = request.form['anotacoes']
    data = request.form['data']
    usuario = session['usuario_logado']
    onu = ONU(usuario, cliente, equipamento, motivo, anotacoes, data)
    lista.append(onu)
    #fazendo redirecionamento para a pagina nao recarregar o formulario e ir para a pagina inicial chamada /
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    login_inserido = request.form['usuario']
    senha_inserida = request.form['senha']
    ### UTILIZANDO A SECTION DO FLASK PARA OS COKIEES CONSEGUIREM ARMAZENAREM INFORMAÇÕES

    for usuario in usuarios:
        if usuario.login == login_inserido and usuario.senha == senha_inserida:
            session['usuario_logado'] = request.form['usuario']
            flash(request.form['usuario'] + ' logou com sucesso!')
            return redirect('/')
    flash('usuario nao logado')
    return redirect('/login')

@app.route('/cadastrousuario')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    return render_template('cadastrousuario.html')

@app.route('/criarusuario', methods=['POST'])
def criarusuario():
    login = request.form['login']
    senha = request.form['senha']
    novousuario = NOVOUSUARIO(login, senha)
    usuarios.append(novousuario)
    return redirect('/')

@app.route('/listausuarios')
def listausuarios():
    return render_template("listausuarios.html", titulo="Lista de Usuários", usuarios=usuarios)
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')

if __name__ == "__main__":
    app.run()