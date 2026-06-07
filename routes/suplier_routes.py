from flask import Blueprint, render_template, request, flash, redirect, url_for
from classes.suplier import Suplier
from classes.transaction import Transaction
from classes.gclass import Gclass

suplier_bp = Blueprint('supliers', __name__)

@suplier_bp.route('/supliers', methods=['GET', 'POST'])
def listar_supliers():
    modo = 'ver'
    fornecedor_atual = Suplier.obj[Suplier.lst[Suplier.pos]] if len(Suplier.lst) > 0 else None

    if request.method == 'POST':
        acao = request.form.get('botao')

        if acao == 'First':
            Suplier.pos = 0
        elif acao == 'Previous':
            if Suplier.pos > 0: Suplier.pos -= 1
        elif acao == 'Next':
            if Suplier.pos < len(Suplier.lst) - 1: Suplier.pos += 1
        elif acao == 'Last':
            Suplier.pos = len(Suplier.lst) - 1
        elif acao == 'Insert':
            modo = 'inserir'
            fornecedor_atual = None
        elif acao == 'Edit':
            modo = 'editar'
        elif acao == 'Delete':
            if fornecedor_atual:
                try:
                    id_a_apagar = int(fornecedor_atual.suplier_id)
                    em_uso = any(int(t.suplier_id) == id_a_apagar for t in Transaction.obj.values() if t.suplier_id)
                except (ValueError, TypeError):
                    em_uso = False
                
                if em_uso:
                    flash(f"Não pode apagar o Fornecedor {id_a_apagar} porque tem transações vinculadas!", "danger")
                    return redirect(url_for('supliers.listar_supliers'))
                else:
                    Suplier.sqlexe(f'DELETE FROM "Suplier" WHERE "suplier_id" = {id_a_apagar}')
                    Suplier.reset()
                    Suplier.read(Gclass.path)
                    Suplier.pos = 0
                    flash("Fornecedor removido com sucesso.", "success")
                    return redirect(url_for('supliers.listar_supliers'))
        elif acao == 'Save':
            s_title = request.form.get('suplier_title_input')
            s_cat = request.form.get('suplier_category_input')
            id_sup = request.form.get('suplier_id_input')
            if id_sup: 
                Suplier.sqlexe(f'UPDATE "Suplier" SET "suplier_title" = "{s_title}", "suplier_category" = "{s_cat}" WHERE "suplier_id" = {id_sup}')
            else: 
                Suplier.sqlexe(f'INSERT INTO "Suplier" ("suplier_title", "suplier_category") VALUES ("{s_title}", "{s_cat}")')
            Suplier.reset()
            Suplier.read(Gclass.path)
            Suplier.pos = 0
            modo = 'ver'
        elif acao == 'Cancel':
            modo = 'ver'

    if modo != 'inserir' and len(Suplier.lst) > 0:
        fornecedor_atual = Suplier.obj[Suplier.lst[Suplier.pos]]

    # --- LÓGICA DO GRÁFICO (Sem funções built-in) ---
    amounts_dict = {}
    for t_id in Transaction.lst:
        t = Transaction.obj[t_id]
        s_id = t.suplier_id
        amt = t.amount
        if s_id in amounts_dict:
            amounts_dict[s_id] += amt
        else:
            amounts_dict[s_id] = amt

    chart_labels = []
    chart_data = []
    for s_id in Suplier.lst:
        sup = Suplier.obj[s_id]
        name = sup.suplier_title
        
        amt = 0.0
        if s_id in amounts_dict:
            amt = amounts_dict[s_id]
            
        chart_labels.append(name)
        chart_data.append(amt)

    return render_template(
        'supliers.html', 
        active_page='suppliers', 
        fornecedor=fornecedor_atual, 
        modo=modo,
        chart_labels=chart_labels,
        chart_data=chart_data
    )