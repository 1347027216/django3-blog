from mdeditor.fields import MDTextFormField

from django import forms


class MDEditorForm(forms.Form):
    title = forms.CharField()
    # 选取前端模板配置
    content = MDTextFormField(config_name='form_config', min_length=5)
    category = forms.CharField()