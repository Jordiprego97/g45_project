from flask import Blueprint, render_template
from classes.model import Model
from classes.suplier import Suplier
from classes.manufacturer import Manufacturer
from classes.transaction import Transaction

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    stats = {
        'total_models': len(Model.lst),
        'total_suppliers': len(Suplier.lst),
        'total_manufacturers': len(Manufacturer.lst),
        'total_transactions': len(Transaction.lst),
        'total_amount': sum(t.amount for t in Transaction.obj.values() if hasattr(t, 'amount'))
    }
    
    recent_transactions = []
    # Inverte as transações para mostrar as mais recentes primeiro
    ids_recentes = list(Transaction.lst)[-5:][::-1]
    for tid in ids_recentes:
        t = Transaction.obj.get(tid)
        if t:
            m_obj = Manufacturer.obj.get(t.manufacturer_id)
            s_obj = Suplier.obj.get(t.suplier_id)
            recent_transactions.append({
                'id': t.transaction_id,
                'manufacturer_name': m_obj.manufacturer_name if m_obj else f"ID {t.manufacturer_id}",
                'suplier_title': s_obj.suplier_title if s_obj else f"ID {t.suplier_id}",
                'date': t.transaction_date,
                'amount': t.amount
            })
            
    return render_template('dashboard.html', active_page='dashboard', stats=stats, recent_transactions=recent_transactions)