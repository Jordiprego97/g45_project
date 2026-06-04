from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from classes.manufacturer import Manufacturer
from classes.model import Model
from classes.transaction import Transaction
from classes.gclass import Gclass

manufacturer_bp = Blueprint('manufacturers', __name__)

def gerar_grafico_fabricantes(fabricante):
    if not fabricante or not Manufacturer.lst:
        return None
        
    anos_contagem = fabricante.obter_contagem_por_ano()

    if not anos_contagem:
        return None

    anos_ordenados = sorted(anos_contagem.keys())
    valores = [anos_contagem[ano] for ano in anos_ordenados]

    fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
    bars = ax.bar(anos_ordenados, valores, color='#ffc107', edgecolor='#e0a800', width=0.5, linewidth=1)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(axis='both', colors='#555555', labelsize=9)
    ax.set_title("Evolução de Registos (Por Ano)", fontsize=10, fontweight='bold', color='#333333', pad=10)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='#444444')

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', transparent=True)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return plot_url

@manufacturer_bp.route('/manufacturers', methods=['GET', 'POST'])
def listar_manufacturers():
    modo = 'ver'
    
    if request.method == 'POST':
        acao = request.form.get('botao')
        modo_anterior = request.form.get('modo_atual', 'ver')

        if acao == 'First': Manufacturer.pos = 0
        elif acao == 'Previous':
            if Manufacturer.pos > 0: Manufacturer.pos -= 1
        elif acao == 'Next':
            if Manufacturer.pos < len(Manufacturer.lst) - 1: Manufacturer.pos += 1
        elif acao == 'Last': Manufacturer.pos = len(Manufacturer.lst) - 1
        elif acao == 'Insert': modo = 'inserir'
        elif acao == 'Edit': modo = 'editar'
        elif acao == 'Cancel': modo = 'ver'
        elif acao == 'Delete':
            if len(Manufacturer.lst) > 0:
                fabricante_atual = Manufacturer.obj[Manufacturer.lst[Manufacturer.pos]]
                id_a_apagar = fabricante_atual.manufacturer_id
                em_uso = any(t.manufacturer_id == id_a_apagar for t in Transaction.obj.values())
                
                if em_uso:
                    flash(f"Não pode apagar o Fabricante {id_a_apagar} porque tem transações vinculadas!", "danger")
                else:
                    Manufacturer.sqlexe(f'DELETE FROM "Manufacturer" WHERE "manufacturer_id" = {id_a_apagar}')
                    Manufacturer.reset()
                    Manufacturer.read(Gclass.path)
                    Manufacturer.pos = 0
                    flash("Fabricante removido com sucesso.", "success")
            modo = 'ver'
        elif acao == 'Save':
            m_name = request.form.get('manufacturer_name_input')
            mod_id = request.form.get('model_id_input')
            id_man = request.form.get('manufacturer_id_input')
            
            if modo_anterior == 'editar' and id_man: 
                Manufacturer.sqlexe(f'UPDATE "Manufacturer" SET "manufacturer_name" = "{m_name}", "model_id" = {mod_id} WHERE "manufacturer_id" = {id_man}')
                flash("Fabricante atualizado com sucesso.", "success")
            elif modo_anterior == 'inserir': 
                dt_hoje = datetime.date.today().strftime("%Y-%m-%d")
                Manufacturer.sqlexe(f'INSERT INTO "Manufacturer" ("manufacturer_name", "model_id", "created_date") VALUES ("{m_name}", {mod_id}, "{dt_hoje}")')
                flash("Fabricante inserido com sucesso.", "success")
                
            Manufacturer.reset()
            Manufacturer.read(Gclass.path)
            Manufacturer.pos = 0
            modo = 'ver'

    if modo != 'inserir' and len(Manufacturer.lst) > 0:
        if Manufacturer.pos >= len(Manufacturer.lst): Manufacturer.pos = 0
        fabricante_atual = Manufacturer.obj[Manufacturer.lst[Manufacturer.pos]]
    else:
        fabricante_atual = None

    modelos = Model.obj.values()
    
    m_name = "N/D"
    if fabricante_atual:
        m_obj = Model.obj.get(fabricante_atual.model_id)
        if m_obj: m_name = m_obj.model_info

    grafico_base64 = gerar_grafico_fabricantes(fabricante_atual)

    return render_template(
        'manufacturers.html', 
        active_page='manufacturers', 
        fabricante=fabricante_atual, 
        modelos=modelos, 
        m_name=m_name, 
        modo=modo,
        grafico=grafico_base64
    )