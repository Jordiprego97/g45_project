from flask import Blueprint, render_template, request, flash
import datetime
from classes.transaction import Transaction
from classes.manufacturer import Manufacturer
from classes.suplier import Suplier
from classes.gclass import Gclass
from classes.model import Model

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET', 'POST'])
def listar_transactions():
    modo = 'ver'
    transacao_atual = Transaction.obj[Transaction.lst[Transaction.pos]] if len(Transaction.lst) > 0 else None
    valor_simulado = None

    if request.method == 'POST':
        acao = request.form.get('botao')

       
        if acao == 'First':
            Transaction.pos = 0
        elif acao == 'Previous':
            if Transaction.pos > 0: 
                Transaction.pos -= 1
        elif acao == 'Next':
            if Transaction.pos < len(Transaction.lst) - 1: 
                Transaction.pos += 1
        elif acao == 'Last':
            Transaction.pos = len(Transaction.lst) - 1
            
        
        elif acao == 'Insert':
            modo = 'inserir'
            transacao_atual = None
        elif acao == 'Edit':
            modo = 'editar'
        elif acao == 'Cancel':
            modo = 'ver'
            
        
        elif acao == 'Delete':
            if transacao_atual:
                id_a_apagar = transacao_atual.transaction_id
                Transaction.sqlexe(f'DELETE FROM "Transaction" WHERE "transaction_id" = {id_a_apagar}')
                Transaction.reset()
                Transaction.read(Gclass.path)
                Transaction.pos = 0
                flash("Transação removida com sucesso.", "success")
                
       
        elif acao == 'Save':
            m_id = request.form.get('manufacturer_id_input')
            s_id = request.form.get('suplier_id_input')
            t_date = request.form.get('transaction_date_input')
            amount = request.form.get('amount_input')
            id_trans = request.form.get('transaction_id_input')
            
            if id_trans: 
                
                Transaction.sqlexe(f'UPDATE "Transaction" SET "manufacturer_id" = {m_id}, "suplier_id" = {s_id}, "transaction_date" = "{t_date}", "amount" = {amount} WHERE "transaction_id" = {id_trans}')
                flash("Transação atualizada com sucesso.", "success")
            else: 
                
                Transaction.sqlexe(f'INSERT INTO "Transaction" ("manufacturer_id", "suplier_id", "transaction_date", "amount") VALUES ({m_id}, {s_id}, "{t_date}", {amount})')
                flash("Transação registada com sucesso.", "success")
            
            Transaction.reset()
            Transaction.read(Gclass.path)
            Transaction.pos = 0
            modo = 'ver'

        
        elif acao == 'Apply Discount':
            pct = request.form.get('discount_percentage_input')
            if pct and transacao_atual:
                try:
                    pct = float(pct)
                    if 0 < pct <= 100:
                        
                        valor_simulado = transacao_atual.amount * (1 - pct / 100)
                        flash(f"Simulação: Desconto de {pct}% calculado com sucesso!", "success")
                    else:
                        flash("Insira uma percentagem de desconto entre 0 e 100.", "danger")
                except ValueError:
                    flash("Insira um valor numérico válido para o desconto.", "danger")
                    
        elif acao == 'Apply Tax':
            pct = request.form.get('tax_percentage_input')
            if pct and transacao_atual:
                try:
                    pct = float(pct)
                    if pct > 0:
                        
                        valor_simulado = transacao_atual.amount * (1 + pct / 100)
                        flash(f"Simulação: Taxa de {pct}% calculada com sucesso!", "success")
                    else:
                        flash("Insira uma percentagem de taxa maior que 0.", "danger")
                except ValueError:
                    flash("Insira um valor numérico válido para a taxa.", "danger")

   
    if modo != 'inserir' and len(Transaction.lst) > 0:
        transacao_atual = Transaction.obj[Transaction.lst[Transaction.pos]]

    
    fabricantes = list(Manufacturer.obj.values())
    fornecedores = list(Suplier.obj.values())
    
    
    data_formatada = ""
    if transacao_atual and transacao_atual.transaction_date:
        data_formatada = transacao_atual.transaction_date
    else:
        data_formatada = datetime.date.today().strftime("%Y-%m-%d")

    
    return render_template(
        'transactions.html', 
        transacao=transacao_atual, 
        modo=modo, 
        fabricantes=fabricantes, 
        fornecedores=fornecedores, 
        data_formatada=data_formatada,
        valor_simulado=valor_simulado
    )