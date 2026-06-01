from flask import Blueprint, render_template, request, flash
from classes.model import Model
from classes.manufacturer import Manufacturer
from classes.gclass import Gclass

model_bp = Blueprint('models', __name__)

@model_bp.route('/models', methods=['GET', 'POST'])
def listar_models():
    modo = 'ver'
    modelo_atual = Model.obj[Model.lst[Model.pos]] if len(Model.lst) > 0 else None

    if request.method == 'POST':
        acao = request.form.get('botao')

        if acao == 'First':
            Model.pos = 0
        elif acao == 'Previous':
            if Model.pos > 0: Model.pos -= 1
        elif acao == 'Next':
            if Model.pos < len(Model.lst) - 1: Model.pos += 1
        elif acao == 'Last':
            Model.pos = len(Model.lst) - 1
        elif acao == 'Insert':
            modo = 'inserir'
            modelo_atual = None
        elif acao == 'Edit':
            modo = 'editar'
        elif acao == 'Delete':
            if modelo_atual:
                id_a_apagar = modelo_atual.model_id
                # VALIDAÇÃO PEDIDA PELO PROFESSOR:
                em_uso = any(m.model_id == id_a_apagar for m in Manufacturer.obj.values())
                
                if em_uso:
                    flash(f"Não pode apagar o Modelo {id_a_apagar} porque está a ser usado por Fabricantes!", "danger")
                else:
                    Model.sqlexe(f'DELETE FROM "Model" WHERE "model_id" = {id_a_apagar}')
                    Model.reset()
                    Model.read(Gclass.path)
                    Model.pos = 0
                    flash("Modelo apagado com sucesso.", "success")
        elif acao == 'Save':
            m_info = request.form.get('model_name_input')
            id_model = request.form.get('model_id_input')
            if id_model: 
                Model.sqlexe(f'UPDATE "Model" SET "model_info" = "{m_info}" WHERE "model_id" = {id_model}')
            else: 
                Model.sqlexe(f'INSERT INTO "Model" ("model_info") VALUES ("{m_info}")')
            Model.reset()
            Model.read(Gclass.path)
            Model.pos = 0
            modo = 'ver'
        elif acao == 'Cancel':
            modo = 'ver'

    if modo != 'inserir' and len(Model.lst) > 0:
        modelo_atual = Model.obj[Model.lst[Model.pos]]

    return render_template('models.html', active_page='models', modelo=modelo_atual, modo=modo)