import os
from flask import Flask, render_template

from classes.gclass import Gclass


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
Gclass.path = os.path.join(BASE_DIR, 'data', 'dados_finais.db')

print(f"--> A apontar para a Base de Dados em: {Gclass.path}")


from classes.model import Model
from classes.manufacturer import Manufacturer
from classes.suplier import Suplier
from classes.transaction import Transaction

app = Flask(__name__, template_folder='classes/templates')

def carregar_dados_da_bd():
    """Garante o reload limpo dos dados da BD respeitando as chaves estrangeiras."""
    try:
        Model.reset()
        Suplier.reset()
        Manufacturer.reset()
        Transaction.reset()

        # RESOLUÇÃO: Passar o caminho correto para dentro do método read()
        Model.read(Gclass.path)
        Suplier.read(Gclass.path)
        Manufacturer.read(Gclass.path)
        Transaction.read(Gclass.path)
    except Exception as e:
        print(f"Erro ao ler base de dados: {e}")


@app.route('/')
def dashboard():
    carregar_dados_da_bd()
    
    stats = {
        'total_models': len(Model.lst),
        'total_suppliers': len(Suplier.lst),
        'total_manufacturers': len(Manufacturer.lst),
        'total_amount': sum(t.amount for t in Transaction.obj.values())
    }
    
    recentes = []
    todas_transacoes = list(Transaction.obj.values())
    for t in todas_transacoes[-5:]:
        m_obj = Manufacturer.obj.get(t.manufacturer_id)
        s_obj = Suplier.obj.get(t.suplier_id)
        recentes.append({
            'id': t.transaction_id,
            'manufacturer_name': m_obj.manufacturer_name if m_obj else "Desconhecido",
            'suplier_title': s_obj.suplier_title if s_obj else "Desconhecido",
            'date': t.transaction_date,
            'amount': t.amount
        })
    recentes.reverse()
    
    return render_template('dashboard.html', active_page='dashboard', stats=stats, recent_transactions=recentes)

from flask import request, redirect, url_for  

@app.route('/models', methods=['GET', 'POST'])
def listar_models():
    if not Model.lst:
        carregar_dados_da_bd()
    
    modelo_atual = Model.current()
    modo = 'ver'

    if request.method == 'POST':
        acao = request.form.get('botao')
        
        if acao == 'First':
            Model.first()
            modelo_atual = Model.current()
        elif acao == 'Previous':
            Model.previous()
            modelo_atual = Model.current()
        elif acao == 'Next':
            Model.nextrec()  
            modelo_atual = Model.current()
        elif acao == 'Last':
            Model.last()
            modelo_atual = Model.current()

        elif acao == 'Delete':
            if modelo_atual:
                id_a_apagar = modelo_atual.model_id
                
                Model.sqlexe(f'DELETE FROM "Model" WHERE "model_id" = {id_a_apagar}')
                

                Model.reset()
                Model.read(Gclass.path)
                Model.first()
                modelo_atual = Model.current()

        elif acao == 'Edit':
            modo = 'editar' 

        elif acao == 'Insert':
            modo = 'inserir'
            modelo_atual = None 

        elif acao == 'Save':
            info = request.form.get('model_info_input')
            id_model = request.form.get('model_id_input')
            
            if id_model: 
                Model.sqlexe(f'UPDATE "Model" SET "model_info" = "{info}" WHERE "model_id" = {id_model}')
            else: 
                Model.sqlexe(f'INSERT INTO "Model" ("model_info") VALUES ("{info}")')
            
            Model.reset()
            Model.read(Gclass.path)
            Model.first()
            modelo_atual = Model.current()
            modo = 'ver'

        elif acao == 'Cancel':
            modo = 'ver'
            modelo_atual = Model.current()

    return render_template('models.html', active_page='models', modelo=modelo_atual, modo=modo)

@app.route('/supliers', methods=['GET', 'POST'])
def listar_supliers():
    if not Suplier.lst:
        carregar_dados_da_bd()
    
    if request.method == 'POST':
        acao = request.form.get('botao')
        
        if acao == 'First':
            Suplier.first()
        elif acao == 'Previous':
            Suplier.previous()
        elif acao == 'Next':
            Suplier.nextrec()  
        elif acao == 'Last':
            Suplier.last()
            
        fornecedor_atual = Suplier.current()
        return render_template('supliers.html', active_page='supliers', fornecedor=fornecedor_atual)

    fornecedor_atual = Suplier.current()
    return render_template('supliers.html', active_page='supliers', fornecedor=fornecedor_atual)

@app.route('/manufacturers', methods=['GET', 'POST'])
def listar_manufacturers():
    if not Manufacturer.lst:
        carregar_dados_da_bd()
    
    if request.method == 'POST':
        acao = request.form.get('botao')
        
        if acao == 'First':
            Manufacturer.first()
        elif acao == 'Previous':
            Manufacturer.previous()
        elif acao == 'Next':
            Manufacturer.nextrec()  
        elif acao == 'Last':
            Manufacturer.last()
            
        fabricante_atual = Manufacturer.current()
        
        mod = Model.obj.get(fabricante_atual.model_id) if fabricante_atual else None
        model_info = mod.model_info if mod else "N/D"
        
        return render_template('manufacturers.html', active_page='manufacturers', fabricante=fabricante_atual, model_info=model_info)

    fabricante_atual = Manufacturer.current()
    mod = Model.obj.get(fabricante_atual.model_id) if fabricante_atual else None
    model_info = mod.model_info if mod else "N/D"
    
    return render_template('manufacturers.html', active_page='manufacturers', fabricante=fabricante_atual, model_info=model_info)

@app.route('/transactions', methods=['GET', 'POST'])
def listar_transactions():
    if not Transaction.lst:
        carregar_dados_da_bd()
    
    if request.method == 'POST':
        acao = request.form.get('botao')
        
        if acao == 'First':
            Transaction.first()
        elif acao == 'Previous':
            Transaction.previous()
        elif acao == 'Next':
            Transaction.nextrec()  
        elif acao == 'Last':
            Transaction.last()
            
        transacao_atual = Transaction.current()
        
        m_obj = Manufacturer.obj.get(transacao_atual.manufacturer_id) if transacao_atual else None
        s_obj = Suplier.obj.get(transacao_atual.suplier_id) if transacao_atual else None
        
        m_name = m_obj.manufacturer_name if m_obj else f"ID {transacao_atual.manufacturer_id}"
        s_title = s_obj.suplier_title if s_obj else f"ID {transacao_atual.suplier_id}"
        
        return render_template('transactions.html', active_page='transactions', transacao=transacao_atual, manufacturer_name=m_name, suplier_title=s_title)

    transacao_atual = Transaction.current()
    m_obj = Manufacturer.obj.get(transacao_atual.manufacturer_id) if transacao_atual else None
    s_obj = Suplier.obj.get(transacao_atual.suplier_id) if transacao_atual else None
    
    m_name = m_obj.manufacturer_name if m_obj else "N/D"
    s_title = s_obj.suplier_title if s_obj else "N/D"
    
    return render_template('transactions.html', active_page='transactions', transacao=transacao_atual, manufacturer_name=m_name, suplier_title=s_title)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)