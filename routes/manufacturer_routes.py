from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime
from classes.manufacturer import Manufacturer
from classes.model import Model
from classes.transaction import Transaction
from classes.gclass import Gclass

manufacturer_bp = Blueprint('manufacturers', __name__)

@manufacturer_bp.route('/manufacturers', methods=['GET', 'POST'])
def listar_manufacturers():
    modo = 'ver'
    fabricante_atual = Manufacturer.obj[Manufacturer.lst[Manufacturer.pos]] if len(Manufacturer.lst) > 0 else None

    if request.method == 'POST':
        acao = request.form.get('botao')

        if acao == 'First':
            Manufacturer.pos = 0
        elif acao == 'Previous':
            if Manufacturer.pos > 0: Manufacturer.pos -= 1
        elif acao == 'Next':
            if Manufacturer.pos < len(Manufacturer.lst) - 1: Manufacturer.pos += 1
        elif acao == 'Last':
            Manufacturer.pos = len(Manufacturer.lst) - 1
        elif acao == 'Insert':
            modo = 'inserir'
            fabricante_atual = None
        elif acao == 'Edit':
            modo = 'editar'
        elif acao == 'Delete':
            if fabricante_atual:
                id_a_apagar = fabricante_atual.manufacturer_id
                em_uso = any(t.manufacturer_id == id_a_apagar for t in Transaction.obj.values())
                
                if em_uso:
                    flash(f"Não pode apagar o Fabricante {id_a_apagar} porque tem transações vinculadas!", "danger")
                    # Força a página a recarregar do zero de forma limpa, limpando os inputs
                    return redirect(url_for('manufacturers.listar_manufacturers'))
                else:
                    Manufacturer.sqlexe(f'DELETE FROM "Manufacturer" WHERE "manufacturer_id" = {id_a_apagar}')
                    Manufacturer.reset()
                    Manufacturer.read(Gclass.path)
                    Manufacturer.pos = 0
                    flash("Fabricante removido com sucesso.", "success")
                    return redirect(url_for('manufacturers.listar_manufacturers'))
        elif acao == 'Save':
            m_name = request.form.get('manufacturer_name_input')
            mod_id = request.form.get('model_id_input')
            id_man = request.form.get('manufacturer_id_input')
            if id_man: 
                Manufacturer.sqlexe(f'UPDATE "Manufacturer" SET "manufacturer_name" = "{m_name}", "model_id" = {mod_id} WHERE "manufacturer_id" = {id_man}')
            else: 
                dt_hoje = datetime.date.today().strftime("%Y-%m-%d")
                Manufacturer.sqlexe(f'INSERT INTO "Manufacturer" ("manufacturer_name", "model_id", "created_date") VALUES (\"{m_name}\", {mod_id}, "{dt_hoje}")')
            Manufacturer.reset()
            Manufacturer.read(Gclass.path)
            Manufacturer.pos = 0
            return redirect(url_for('manufacturers.listar_manufacturers'))
        elif acao == 'Cancel':
            return redirect(url_for('manufacturers.listar_manufacturers'))

    if modo != 'inserir' and len(Manufacturer.lst) > 0:
        fabricante_atual = Manufacturer.obj[Manufacturer.lst[Manufacturer.pos]]

    modelos = Model.obj.values()
    
    m_name = "N/D"
    if fabricante_atual:
        m_obj = Model.obj.get(fabricante_atual.model_id)
        if m_obj: m_name = m_obj.model_info

    return render_template('manufacturers.html', active_page='manufacturers', fabricante=fabricante_atual, modelos=modelos, m_name=m_name, modo=modo)