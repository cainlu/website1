#coding=utf-8
from django import forms

class UploadForm(forms.Form):
    context = forms.CharField(widget=forms.Textarea, required=True, error_messages={'invalid':u'文字内容提交错误'})
    image = forms.ImageField(required=False, error_messages={'invalid':u'图片提交错误'})
