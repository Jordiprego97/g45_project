#ParteSofia
from classes.gclass import Gclass
from classes.manufacturer import Manufacturer
from classes.suplier import Suplier

class Transaction(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_transaction_id', '_manufacturer_id', '_suplier_id', '_transaction_date', '_amount']
    header = 'Transactions'
    des = ['Transaction Id', 'Manufacturer Id', 'Suplier Id', 'Transaction Date', 'Amount']

    def __init__(self, transaction_id, manufacturer_id, suplier_id, transaction_date, amount):
        super().__init__()
        
        manufacturer_id = int(manufacturer_id)
        suplier_id = int(suplier_id)
        
        if manufacturer_id in Manufacturer.lst:
            if suplier_id in Suplier.lst:
                id = Transaction.get_id(transaction_id)
                self._transaction_id = id
                self._manufacturer_id = manufacturer_id
                self._suplier_id = suplier_id
                self._transaction_date = transaction_date
                self._amount = float(amount)
               
                Transaction.obj[id] = self
                Transaction.lst.append(id)
            else:
                print('Erro: Fornecedor ', suplier_id, ' não encontrado!')
        else:
            print('Erro: Fabricante ', manufacturer_id, ' não encontrado!')

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def manufacturer_id(self):
        return self._manufacturer_id
    
    @property
    def suplier_id(self):
        return self._suplier_id
    @property
    def transaction_date(self):
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        self._transaction_date = transaction_date

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
    
    def apply_discount(self, percentage):
        
        percentage = float(percentage)
        if 0 < percentage <= 100:
            desconto = self._amount * (percentage / 100)
            self.amount = self._amount - desconto 
            return True
        return False
    def apply_tax(self, percentage):
        
        percentage = float(percentage)
        if percentage > 0:
            taxa = self._amount * (percentage / 100)
            self.amount = self._amount + taxa
            return True
        return False
