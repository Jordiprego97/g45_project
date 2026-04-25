from classes.gclass import Gclass
class Suplier(Gclass):
    
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    
    att = ['_suplier_id', '_suplier_title', '_suplier_category']
    
    header = 'Supliers'
    
    des = ['Suplier id', 'Suplier title', 'Suplier Category']
    
    def __init__(self, suplier_id, suplier_title, suplier_category):
        
        super().__init__()
        id = Suplier.get_id(suplier_id)
        self._suplier_id = suplier_id
        self._suplier_title = suplier_title
        self._suplier_category = suplier_category
        
        Suplier.obj[id] = self
        Suplier.lst.append(id)
        
    @property
    def suplier_id(self):
        return self._suplier_id
    
    @property
    def suplier_title(self):
        return self._suplier_title
    
    @suplier_title.setter
    def suplier_title(self, outro):
        self._suplier_title = outro
    
    @property
    def suplier_category(self):
        return self._suplier_category
    
    @suplier_category.setter
    def suplier_category(self, outro):
        self._suplier_category = outro
    
