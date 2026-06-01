from flask import Blueprint, render_template, request, flash
import datetime
from classes.model import Model
from classes.suplier import Suplier
from classes.manufacturer import Manufacturer
from classes.transaction import Transaction
from classes.gclass import Gclass

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET', 'POST'])
def listar_transactions():
    modo = 'ver'

    if len(Transaction.lst) > 0:
        if Transaction.pos >= len(Transaction.lst):
            Transaction.pos = len(Transaction.lst) - 1
        if Transaction.pos < 0:
            Transaction.pos = 0
        transacao_atual = Transaction.obj[Transaction.lst[Transaction.pos]]
    else:
        transacao_atual = None

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
        elif acao == 'Delete':
            if transacao_atual:
                id_trans = transacao_atual.transaction_id
                Transaction.sqlexe(f'DELETE FROM "Transaction" WHERE "transaction_id" = {id_trans}')
                Transaction.reset()
                Transaction.read(Gclass.path)
                Transaction.pos = 0
                flash("Transação eliminada com sucesso.", "success")
        elif acao == 'Save':
            man_id = request.form.get('manufacturer_id_input')
            sup_id = request.form.get('suplier_id_input')
            t_date = request.form.get('transaction_date_input')
            amount = request.form.get('amount_input')
            id_trans = request.form.get('transaction_id_input')
            
            if t_date:
                t_date = t_date.replace('-', '/')
            
            if id_trans: 
                Transaction.sqlexe(f'UPDATE "Transaction" SET "manufacturer_id" = {man_id}, "suplier_id" = {sup_id}, "transaction_date" = "{t_date}", "amount" = {amount} WHERE "transaction_id" = {id_trans}')
            else: 
                Transaction.sqlexe(f'INSERT INTO "Transaction" ("manufacturer_id", "suplier_id", "transaction_date", "amount") VALUES ({man_id}, {sup_id}, "{t_date}", {amount})')
            
            Transaction.reset()
            Transaction.read(Gclass.path)
            Transaction.pos = 0
            modo = 'ver'
        elif acao == 'Cancel':
            modo = 'ver'

    if modo != 'inserir' and len(Transaction.lst) > 0:
        if Transaction.pos >= len(Transaction.lst):
            Transaction.pos = len(Transaction.lst) - 1
        transacao_atual = Transaction.obj[Transaction.lst[Transaction.pos]]
    else:
        if modo == 'inserir':
            transacao_atual = None

    fabricantes = list(Manufacturer.obj.values())
    fornecedores = list(Suplier.obj.values())

    data_formatada = ""
    if transacao_atual and transacao_atual.transaction_date:
        data_str = str(transacao_atual.transaction_date).strip().split(" ")[0]
        if "/" in data_str:
            parts = data_str.split("/")
            if len(parts) == 3:
                if len(parts[0]) == 4:
                    data_formatada = f"{parts[0]}-{parts[1]}-{parts[2]}"
                elif len(parts[2]) == 4:  # Caso DD/MM/YYYY
                    data_formatada = f"{parts[2]}-{parts[1]}-{parts[0]}"
        elif "-" in data_str:
            parts = data_str.split("-")
            if len(parts) == 3:
                if len(parts[0]) == 4:    # Caso YYYY-MM-DD
                    data_formatada = data_str
                elif len(parts[2]) == 4:  # Caso DD-MM-YYYY
                    data_formatada = f"{parts[2]}-{parts[1]}-{parts[0]}"

    return render_template(
        'transactions.html', 
        active_page='transactions', 
        transacao=transacao_atual, 
        fabricantes=fabricantes, 
        fornecedores=fornecedores, 
        modo=modo,
        data_formatada=data_formatada
    )