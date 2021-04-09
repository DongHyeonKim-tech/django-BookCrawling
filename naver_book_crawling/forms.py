from django import forms
from naver_book_crawling.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class BSModalForm(PopRequestMixin, forms.Form):
    pass


class BSModalModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    pass
