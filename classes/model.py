#Parte da Matilde
from classes.gclass import Gclass
class Model(Gclass):
   
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_model_id', '_model_info']
   
    header = 'Models'
   
    des = ['Model id', 'Model info']
   
    def __init__(self, model_id, model_info):
        id=Model.get_id(model_id)
        self._model_id = id
        self._model_info = model_info
        Model.obj[id]=self
        Model.lst.append(id)
       
    @property
    def model_id(self):
        return self._model_id
    @model_id.setter  
    def model_id(self,model_id):
        self._model_id=model_id
    @property
    def model_info(self):
        return self._model_info
    @model_info.setter
    def model_info(self,model_info):
        self._model_info=model_info