#Parte Jordi Prego
from classes.gclass import Gclass
from classes.model import Model

class Manufacturer(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    
    att = ['_manufacturer_id', '_manufacturer_name', '_created_date', '_model_id']
    header = 'Manufacturers'
    des = ['Manufacturer id', 'Manufacturer name', 'Created date', 'Model Id']
    
    def __init__(self, manufacturer_id, manufacturer_name, created_date, model_id):
        super().__init__()
        
        model_id = int(model_id)
        if model_id in Model.lst:
            id = Manufacturer.get_id(manufacturer_id)
            self._manufacturer_id = id
            self._manufacturer_name = manufacturer_name
            self._created_date = created_date
            self._model_id = model_id
            
            Manufacturer.obj[id] = self
            Manufacturer.lst.append(id)
        else:
            print('Erro: Model ', model_id, ' não encontrado!')
        
    @property
    def manufacturer_id(self):
        return self._manufacturer_id
    
    @property
    def manufacturer_name(self):
        return self._manufacturer_name
    
    @manufacturer_name.setter
    def manufacturer_name(self, novo_nome):
        self._manufacturer_name = novo_nome
    
    @property
    def created_date(self):
        return self._created_date
    
    @created_date.setter
    def created_date(self, outro):
        self._created_date = outro

    @property
    def model_id(self):
        return self._model_id
    

    
