from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from naver_book_crawling.forms import BSModalModelForm, BSModalForm
from naver_book_crawling.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Book, BookCrawling


class BookFilterForm(BSModalForm):
    type = forms.ChoiceField(choices=Book.BOOK_TYPES)

    class Meta:
        fields = ['type', 'clear']


class BookModelForm(BSModalModelForm):
    # publishdate = forms.DateField(
    #     error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    # )

    class Meta:
        model = BookCrawling
        exclude = ['searchsubject']
        labels = {
            "searchsubject": "검색어",
            "title": "제목",
            "categorytop": "카테고리1",
            "categorymiddle": "카테고리2",
            "categorybottom": "카테고리3",
            "writer": "저자",
            "translator": "역자",
            "painter": "그림",
            "publisher": "출판사",
            "publishdate": "출판일",
            "intro": "책 소개",
            "content": "목차",
            "authorintro": "저자 소개",
            "bid": "BID 번호",
            "isbn": "ISBN 번호",
            "grade": "별점",
            "review": "리뷰건수",
            "image": "이미지 링크"
        }


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


def pageNum_validator(value):
    if type(value) != int:
        raise forms.ValidationError('숫자를 입력해주세요.')


class CrawlingForm(forms.Form):
    searchsubject = forms.CharField(label='searchsubject')
    searchstartpage = forms.IntegerField(
        label='searchstartpage', validators=[pageNum_validator])
    searchendpage = forms.IntegerField(
        label='searchendpage', validators=[pageNum_validator])


class isbnCrawlingForm(forms.Form):
    isbnValue = forms.CharField(label='isbnValue')


def bidNum_validator(value):
    if type(value) != int:
        raise forms.ValidationError('숫자를 입력해주세요.')
    if value == None:
        raise forms.ValidationError('범위를 입력해주세요')


class bidCrawlingForm(forms.Form):
    searchstartbid = forms.IntegerField(
        label='searchstartbid', validators=[bidNum_validator])
    searchendbid = forms.IntegerField(
        label='searchendbid', validators=[bidNum_validator])
