from django import forms
from .models import Proceso
class ProcesoForm(forms.ModelForm):

    id_proceso = forms.IntegerField(min_value=0, max_value=999)
    class Meta:
        model = Proceso
        fields = ('id_proceso','nombre','descripcion')

    
    def __init__(self, *args, **kwargs):
        super(ProcesoForm,self).__init__(*args,**kwargs)
        self.fields['id_proceso'].required = True
        self.fields['nombre'].required = True
        
        

