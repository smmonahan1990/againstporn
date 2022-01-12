from django import forms
from archives.models import Report
from reactdev.logging_config import CustomLogger

logger = CustomLogger(__name__)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content_type','object_id','action']

from .helpers import choices

def CustomModelFormFactory(_model):

    class Meta:
        model = _model
        fields = ['title','author','submitted','selftext','fullsize','comments','score','flair','nsfw','status']
        widgets = {
           'flair': forms.Select(
               choices =(('', 'set flair...',),*choices(model)),
               attrs ={
                    'class':'form-control',
                    'style':'width: 200px;',
               }),
           'nsfw':forms.CheckboxInput(),
        }
    def is_valid(self):
        val = super(forms.ModelForm, self).is_valid()
        self.instance.title = self.get_initial_for_field(self.fields['title'],'title')
        return val

    def save(self, commit=True):
        update_fields = ['nsfw', 'flair', 'status']
        for key in update_fields:
            setattr(self.instance, key, self.cleaned_data.pop(key))
        for key in self.cleaned_data.keys():
            setattr(self.instance, key, self.initial[key])
        self.instance.save()
        self.instance.refresh_from_db()
        return self.instance

    def save_m2m(self,*args, **kwargs):
        pass

    attrs = {'__module__':'archives.forms',
             'Meta': Meta,
             'save': save,
             'is_valid': is_valid,
             'save_m2m': save_m2m,
    }
    name = '%sForm' % _model.__name__
    Form = type(name, (forms.ModelForm,), attrs)
    return Form

