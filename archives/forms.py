from django import forms
from archives.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content_type','object_id']
        widgets = {
            'content_type':forms.HiddenInput(attrs={'required':False}),
            'object_id':forms.HiddenInput(attrs={'required':False}),
        }
    def save(self,commit=True):
        return Report.objects.get_or_create(content_type=self.instance.content_type,object_id=self.instance.object_id)

