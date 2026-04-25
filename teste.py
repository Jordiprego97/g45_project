from classes.model import Model
from classes.suplier import Suplier
from classes.manufacturer import Manufacturer
from classes.transaction import Transaction

Model.read('data/dados_finais.db')
Suplier.read('data/dados_finais.db')
Manufacturer.read('data/dados_finais.db')
Transaction.read('data/dados_finais.db')

if len(Model.lst) == 0:
    m1 = Model(0, "Frigorífico Industrial XP")
    Model.insert(m1.model_id)

if len(Suplier.lst) == 0:
    s1 = Suplier(0, "Fornecedor de Metais", "Matéria Prima")
    Suplier.insert(s1.suplier_id)

if len(Manufacturer.lst) == 0:
    man1 = Manufacturer(0, "Fábrica Norte", "2024-05-20", 1)
    Manufacturer.insert(man1.manufacturer_id)

if len(Transaction.lst) == 0:
    t1 = Transaction(0, 1, 1, "2024-05-21", 5000.00)
    Transaction.insert(t1.transaction_id)

print("\n--- TESTE DE LIGAÇÕES ---")
for id in Transaction.lst:
    t = Transaction.obj[id]
    print(f"Transação {t.transaction_id}: Valor {t.amount}€ | Data: {t.transaction_date}")
