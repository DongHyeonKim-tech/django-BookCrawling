from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.shortcuts import render, redirect
from webdriver_manager.chrome import ChromeDriverManager

from naver_book_crawling.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm,
    CrawlingForm,
    isbnCrawlingForm,
    bidCrawlingForm
)
from .models import Book, BookCrawling, BidCrawling

# 크롤링 라이브러리
import re
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, HTTPError, URLError
from urllib.parse import quote_plus
from selenium import webdriver
import time
from sqlalchemy import create_engine
import pymysql
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import numpy as np
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os

# 검색
from django.contrib import messages
from django.db.models import Q


class Index(generic.ListView):
    model = BookCrawling
    paginate_by = 20
    context_object_name = 'books'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(boot_type=int(self.request.GET['type']))
        return qs

    # 페이징

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_number_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_number_range) * page_number_range
        end_index = start_index + page_number_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


def Detail(request, id):
    bookCrawling = BookCrawling.objects.get(pk=id)
    context = {
        'bookCrawling': bookCrawling,
    }
    return render(request, 'book/detail_book.html', context)


def BidDetail(request, bid):
    bidCrawling = BidCrawling.objects.get(pk=bid)
    context = {
        'bidCrawling': bidCrawling,
    }
    return render(request, 'book/bid_detail_book.html', context)


def get_text_list(tag_list):
    return [tag.text for tag in tag_list]


def crawling(request):

    return render(request, 'book/crawling_book.html')


def bidCrawler(request):

    return render(request, 'book/bidCrawling_book.html')


class bidIndex(generic.ListView):
    model = BidCrawling
    paginate_by = 20
    context_object_name = 'bids'
    template_name = 'bid_index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(boot_type=int(self.request.GET['type']))
        return qs

    # 페이징

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_number_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_number_range) * page_number_range
        end_index = start_index + page_number_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


def crawlingBook(request):

    if request.method == 'POST':
        form = CrawlingForm(request.POST)

        if form.is_valid():
            plusUrl = form.cleaned_data['searchsubject']
            searchStartPage = form.cleaned_data['searchstartpage']
            searchEndPage = form.cleaned_data['searchendpage']

    baseUrl = 'https://book.naver.com/search/search_in.nhn?query='
    searchSubject = quote_plus(plusUrl)

    url = baseUrl + searchSubject + "&&"
    html = urlopen(url)
    # url = requests.get(baseUrl + searchSubject + "&&")
    # html = url.content
    soup = BeautifulSoup(html, "html.parser")

    # book_crawling 테이블 column
    search_list = []

    title_list = []

    intro_list = []

    author_intro_list = []

    category_top_list = []
    category_middle_list = []
    category_bottom_list = []

    ISBN_list = []

    writer_list = []

    translator_list = []

    painter_list = []

    publisher_list = []

    publish_date_list = []

    content_list = []

    bid_list = []

    image_list = []

    grade_list = []

    review_list = []

    # writer_info 테이블 column

    writer_name = []
    writer_link = []
    writer_num = []
    writer_book_title = []
    writer_bid = []
    writer_isbn = []

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.implicitly_wait(time_to_wait=5)

    # searchStartPage = ""
    # searchEndPage = ""

    searchStart = int(searchStartPage)
    searchEnd = int(searchEndPage)

    for k in range(searchStart, searchEnd+1):
        url_pre = (url+'pattern=0&orderType=rel.desc&viewType=list&searchType=bookSearch&serviceSm=service.basic&title=&author=&publisher=&isbn=&toc=&subject=&publishStartDay=&publishEndDay=&categoryId=&qdt=1&filterType=0&filterValue=&serviceIc=service.author&buyAllow=0&ebook=0&abook=0&page='+str(k))
        html_pre = urlopen(url_pre)
        # url_pre = requests.get(baseUrl + searchSubject + '&&'+'pattern=0&orderType=rel.desc&viewType=list&searchType=bookSearch&serviceSm=service.basic&title=&author=&publisher=&isbn=&toc=&subject=&publishStartDay=&publishEndDay=&categoryId=&qdt=1&filterType=0&filterValue=&serviceIc=service.author&buyAllow=0&ebook=0&abook=0&page='+str(k))
        # html_pre = url_pre.content
        soup_pre = BeautifulSoup(html_pre, "html.parser")

        title = ''
        title = get_text_list(soup_pre.select('dt'))[0:20]
        for i in range(0, len(title)):
            if '\xa0' in title[i]:
                title[i] = title[i][0:title[i].find(
                    '\xa0')].replace('\n', '')
            title_list.append(title[i])

        link_list = []

        try:
            for href in soup_pre.find("ul", id="searchBiblioList").find_all("dt"):
                link = href.find("a")["href"]
                bid = href.find("a")["href"].split('=')[1]
                link_list.append(link)
                bid_list.append(bid)
        except AttributeError:
            print('검색어에 대한 도서' + str(len(ISBN_list)) + '권 크롤링이 완료되었습니다.')
            driver.quit()

        for i in range(0, len(link_list)):
            # driver.get(link_list[i])
            url_det = link_list[i]
            html_det = urlopen(url_det)
            # url_det = requests.get(link_list[i])
            # html_det = url_det.content
            soup_det = BeautifulSoup(html_det, "html.parser")

            search_list.append(plusUrl)

            try:
                book_intro = soup_det.find('div', id='bookIntroContent')
                book_intro_text = book_intro.get_text().replace('\n', '')
                intro_list.append(book_intro_text)
            except AttributeError:
                book_intro_text = '없음'
                intro_list.append(book_intro_text)

            try:
                author_intro = soup_det.find(
                    'div', id='authorIntroContent')
                author_intro_text = author_intro.get_text().replace('\n', '')
                author_intro_list.append(author_intro_text)
            except AttributeError:
                author_intro_text = '없음'
                author_intro_list.append(author_intro_text)

            try:
                category_top = soup_det.find('li', class_='select')
                category_top_text = category_top.get_text().replace('\n', '')
                category_top_list.append(category_top_text)
            except AttributeError:
                category_top_text = '없음'
                category_top_list.append(category_top_text)

            try:
                category_middle = soup_det.find('li', class_='select2')
                category_middle_text = category_middle.get_text().replace('\n', '')
                category_middle_list.append(category_middle_text)
            except AttributeError:
                category_middle_text = '없음'
                category_middle_list.append(category_middle_text)

            try:
                category_bottom = soup_det.find('li', class_='select3')
                category_bottom_text = category_bottom.get_text().replace('\n', '')
                category_bottom_list.append(category_bottom_text)
            except AttributeError:
                category_bottom_text = '없음'
                category_bottom_list.append(category_bottom_text)

            grade = soup_det.find("div", class_="txt_desc").find(
                "strong").text[:-1]
            grade_list.append(grade)

            review = soup_det.find(
                "a", id="txt_desc_point").find_all("strong")[1].text
            review_list.append(review)

            book_info = soup_det.find('div', class_='book_info_inner')
            book_info_text = book_info.get_text()

            editor_exist = soup_det.find(
                "div", class_="book_info_inner").find_all("em")[0:3]

            if '저자' in book_info_text:
                writer_str = book_info_text.find('저자')+3
                writer_end = book_info_text.find('|', writer_str)
                writer = book_info_text[writer_str:writer_end]
            else:
                writer_str = book_info_text.find('글')+2
                writer_end = book_info_text.find('|', writer_str)
                writer = book_info_text[writer_str:writer_end]

            if '\xa0' in writer:
                writer = writer[0:int(writer.find('\xa0'))]

            writer_list.append(writer)

            if '편집' not in book_info_text:
                if ('그림' in book_info_text) and ('역자' in book_info_text):
                    painter_str = book_info_text.find('그림')+3
                    painter_end = book_info_text.find('|', painter_str)
                    painter = book_info_text[painter_str:painter_end]
                    painter_list.append(painter)

                    translator_str = book_info_text.find('역자')+3
                    translator_end = book_info_text.find(
                        '|', translator_str)
                    translator = book_info_text[translator_str:translator_end]
                    translator_list.append(translator)

                    publisher_str = translator_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

                elif ('그림' in book_info_text) and ('역자' not in book_info_text):
                    translator = '없음'
                    translator_list.append(translator)

                    painter_str = book_info_text.find('그림')+3
                    painter_end = book_info_text.find('|', painter_str)
                    painter = book_info_text[painter_str:painter_end]
                    painter_list.append(painter)

                    publisher_str = painter_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

                elif ('그림' not in book_info_text) and ('역자' in book_info_text):
                    painter = '없음'
                    painter_list.append(painter)

                    translator_str = book_info_text.find('역자')+3
                    translator_end = book_info_text.find(
                        '|', translator_str)
                    translator = book_info_text[translator_str:translator_end]
                    translator_list.append(translator)

                    publisher_str = translator_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

                elif '그림' and '역자' not in book_info_text:
                    translator = '없음'
                    translator_list.append(translator)

                    painter = '없음'
                    painter_list.append(painter)

                    publisher_str = writer_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

            elif '편집' in editor_exist:
                if ('그림' in book_info_text) and ('편집' in book_info_text):
                    painter_str = book_info_text.find('그림')+3
                    painter_end = book_info_text.find('|', painter_str)
                    painter = book_info_text[painter_str:painter_end]
                    painter_list.append(painter)

                    translator_str = book_info_text.find('편집')+3
                    translator_end = book_info_text.find(
                        '|', translator_str)
                    translator = book_info_text[translator_str:translator_end]
                    translator_list.append(translator)

                    publisher_str = translator_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

                elif ('그림' not in book_info_text) and ('편집' in book_info_text):
                    painter = '없음'
                    painter_list.append(painter)

                    translator_str = book_info_text.find('편집')+3
                    translator_end = book_info_text.find(
                        '|', translator_str)
                    translator = book_info_text[translator_str:translator_end]
                    translator_list.append(translator)

                    publisher_str = translator_end+1
                    publisher_end = book_info_text.find(
                        '\n', publisher_str)
                    publisher = book_info_text[publisher_str:publisher_end]
                    publisher_list.append(publisher)

                    publish_date_str = publisher_end+2
                    publish_date_end = book_info_text.find(
                        '\n', publish_date_str)
                    publish_date = book_info_text[publish_date_str:publish_date_end]
                    publish_date_list.append(publish_date)

            ISBN_str = book_info_text.find('ISBN')+6
            ISBN_end = book_info_text.find('|', ISBN_str)

            if ISBN_end == -1:
                ISBN_end = book_info_text.find('\n', ISBN_str)

            ISBN = book_info_text[ISBN_str:ISBN_end]

            if '\n' in ISBN:
                ISBN = ISBN[0:int(ISBN.find('\n'))]

            ISBN_list.append(ISBN)

            content = ''
            content = get_text_list(soup_det.select("div.book_cnt"))
            if content == []:
                content = ["없음"]
                content_list.append(content)
            else:
                content_list.append(content)

            for src in soup_det.find("div", class_="thumb_type").find_all("a"):
                bookImage = src.find("img")["src"]
                image_list.append(bookImage)

            writer_a = soup_det.find("div", class_="book_info_inner").find_all("div")[
                2].find_all("a")[:-1]
            writer_book = soup_det.find(
                "div", class_="book_info").find("a").text
            writer_book_bid = soup_det.find("div", class_="book_info").find("a")[
                "href"].split("=")[1]

            for w in range(0, len(writer_a)):
                writer_n = writer_a[w].text
                writer_name.append(writer_n)
                writer_href = writer_a[w]["href"]
                writer_link.append(writer_href)
                writer_split = writer_a[w]["href"].split("=")[3]
                writer_num.append(writer_split)
                writer_book_title.append(writer_book)
                writer_bid.append(writer_book_bid)
                writer_isbn.append(ISBN)

            if i == 19:
                break
        if k == searchEnd:
            print('검색어에 대한 도서 '+str(len(content_list))+'권 크롤링이 완료되었습니다.')
            driver.quit()
            break

    book_list = []
    for searchSubject, title, writer, translator, painter, publisher, publishDate, intro, content, authorIntro, categoryTop, categoryMiddle, categoryBottom, bid, ISBN, grade, review, image in zip(search_list, title_list, writer_list, translator_list, painter_list, publisher_list, publish_date_list, intro_list, content_list, author_intro_list, category_top_list, category_middle_list, category_bottom_list, bid_list, ISBN_list, grade_list, review_list, image_list):
        book = {"searchSubject": searchSubject, "title": title, "writer": writer, "translator": translator, "painter": painter, "publisher": publisher, "publishDate": publishDate, "intro": intro, "content": content,
                "authorIntro": authorIntro, "categoryTop": categoryTop, "categoryMiddle": categoryMiddle, "categoryBottom": categoryBottom, "bid": bid, "ISBN": ISBN, "grade": grade, "review": review, "image": image}
        book_list.append(book)

    writer_info_list = []
    for num, name, bookTitle, bid, isbn, link in zip(writer_num, writer_name, writer_book_title, writer_bid, writer_isbn, writer_link):
        writer_info = {"num": num, "name": name, "bookTitle": bookTitle,
                       "bid": bid, "isbn": isbn, "link": link}
        writer_info_list.append(writer_info)

    book_DF = pd.DataFrame(book_list)

    writer_DF = pd.DataFrame(writer_info_list)

    engine = create_engine(
        "mysql+pymysql://root:xkzlxkzl1!@127.0.0.1:3306/book?charset=utf8mb4", encoding='utf8')

    conn = engine.connect()

    book_DF.to_sql(name='book_crawling', con=engine,
                   if_exists='append', index=False)

    writer_DF.to_sql(name='writer_info', con=engine,
                     if_exists='append', index=False)

    conn.close()

    return HttpResponseRedirect(reverse_lazy('index'))


def bidCrawling(request):

    if request.method == 'POST':
        form = bidCrawlingForm(request.POST)

        if form.is_valid():
            searchStartBid = form.cleaned_data['searchstartbid']
            searchEndBid = form.cleaned_data['searchendbid']

    bidSearchStart = int(searchStartBid)
    bidSearchEnd = int(searchEndBid)

    engine = create_engine(
        "mysql+pymysql://root:xkzlxkzl1!@127.0.0.1:3306/book?charset=utf8mb4", encoding='utf8')
    torexe = os.popen(r'C:\Dev_program\Tor Browser\Browser\firefox.exe')
    profile = FirefoxProfile(
        r'C:\Dev_program\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path=r'C:\Dev_program\geckodriver.exe')

    driver.implicitly_wait(time_to_wait=5)

    searchCount = bidSearchEnd-bidSearchStart+1
    searchMok = int(np.ceil((bidSearchEnd-bidSearchStart+1)/50))

    taskId = 1

    while searchMok > 0:

        title_list = []
        intro_list = []
        author_intro_list = []
        category_top_list = []
        category_middle_list = []
        category_bottom_list = []
        ISBN_list = []
        writer_list = []
        translator_list = []
        painter_list = []
        publisher_list = []
        publish_date_list = []
        content_list = []
        bid_list = []
        image_list = []
        grade_list = []
        review_list = []
        writer_name = []
        writer_link = []
        writer_num = []
        writer_book_title = []
        writer_bid = []
        writer_isbn = []
        taskId_list = []
        taskContent_list = []
        str_list = []
        end_list = []
        complete_list = []
        errorDetail_list = []
        crawlerNum_list = []

        taskId_list.append(taskId)

        if (bidSearchStart+49) < bidSearchEnd:
            taskContent = str(bidSearchStart)+'~'+str(bidSearchStart+49)
        else:
            taskContent = str(bidSearchStart)+'~'+str(bidSearchEnd)

        taskContent_list.append(taskContent)
        str_now = datetime.datetime.now()
        str_time = str_now.strftime('%Y-%m-%d %H:%M:%S')
        str_list.append(str_time)

        for i in range(bidSearchStart, bidSearchStart+50):

            url_det = 'https://book.naver.com/bookdb/book_detail.nhn?bid=' + \
                str(i)
            try:
                html_det = urlopen(url_det)

            except (HTTPError, URLError, IndexError) as e:
                errorDetail_list.append(e)
                end_now = datetime.datetime.now()
                end_time = end_now.strftime('%Y-%m-%d %H:%M:%S')
                end_list.append(end_time)
                complete_list.append('error')
                crawlerNum_list.append(11)
                task_list = []

                for taskId, taskContent, str_time, end_time, complete, errorDetail, crawlerNum in zip(taskId_list, taskContent_list, str_list, end_list, complete_list, errorDetail_list, crawlerNum_list):
                    task = {"taskId": taskId, "taskContent": taskContent, "str_time": str_time, "end_time": end_time,
                            "complete": complete, "errorDetail": errorDetail, "crawlerNum": crawlerNum}
                    task_list.append(task)

                task_DF = ''
                task_DF = pd.DataFrame(task_list)

                conn = engine.connect()
                task_DF.to_sql(name='task', con=engine,
                               if_exists='append', index=False)
                conn.close()

                print(e)
                print('에러로 크롤링 종료')

                time.sleep(3)

                if bidSearchStart+50 > bidSearchEnd:
                    driver.quit()
                else:
                    continue
            else:
                soup_det = BeautifulSoup(html_det, "html.parser")

            if '책정보,  :' in soup_det.text:
                print(str(i), "번 제외(삭제 서지)")
                continue

            else:
                pass

            book_info = soup_det.find('div', class_='book_info_inner')

            try:
                book_info_text = book_info.get_text()

            except AttributeError:
                print(str(i), "번 제외(Attr 에러)")
                continue

            if driver.current_url == 'https://nid.naver.com/nidlogin.login?svctype=128&a_version=2&viewtype=2&url=http://book.naver.com&surl=http://book.naver.com':
                continue
            else:
                pass

            try:
                book_intro = soup_det.find('div', id='bookIntroContent')
                book_intro_text = book_intro.get_text().replace('\n', '')
                intro_list.append(book_intro_text)

            except AttributeError:
                book_intro_text = ''
                intro_list.append(book_intro_text)

            try:
                author_intro = soup_det.find('div', id='authorIntroContent')
                author_intro_text = author_intro.get_text().replace('\n', '')
                author_intro_list.append(author_intro_text)

            except AttributeError:
                author_intro_text = ''
                author_intro_list.append(author_intro_text)

            try:
                category_top = soup_det.find('li', class_='select')
                category_top_text = category_top.get_text().replace('\n', '')
                category_top_list.append(category_top_text)

            except AttributeError:
                category_top_text = ''
                category_top_list.append(category_top_text)

            try:
                category_middle = soup_det.find('li', class_='select2')
                category_middle_text = category_middle.get_text().replace('\n', '')
                category_middle_list.append(category_middle_text)

            except AttributeError:
                category_middle_text = ''
                category_middle_list.append(category_middle_text)

            try:
                category_bottom = soup_det.find('li', class_='select3')
                category_bottom_text = category_bottom.get_text().replace('\n', '')
                category_bottom_list.append(category_bottom_text)

            except AttributeError:
                category_bottom_text = ''
                category_bottom_list.append(category_bottom_text)

            try:
                grade = soup_det.find("div", class_="txt_desc").find(
                    "strong").text[:-1]

            except AttributeError:
                grade = ''
                grade_list.append(grade)

            try:
                review = soup_det.find(
                    "a", id="txt_desc_point").find_all("strong")[1].text

            except AttributeError:
                review = ''
                review_list.append(review)

            bookinfo_line1 = book_info.find_all("div")[2]

            rel_name = bookinfo_line1.text
            rel_list = []

            for rel in bookinfo_line1.find_all("em"):
                rel_cate = rel.text
                rel_list.append(rel_cate)

            for r in range(0, len(rel_list)):
                rel_name = rel_name.replace(rel_list[r], '')

            rel_name = rel_name.split('|')

            publish_date = rel_name[-1]

            if len(publish_date) == 4:
                publish_date = publish_date + ".01.01"
            elif len(publish_date) == 6:
                publish_date = publish_date[:4]+"."+publish_date[4:]+".01"
            elif publish_date == '':
                publish_date = '2025.01.01'

            if publish_date[0] != '1' and publish_date[0] != '2':
                publish_date = '2025.01.01'
                publish_date_list.append(publish_date)

            publisher = rel_name[-2]
            publisher_list.append(publisher)

            rel_name = rel_name[1:-2]

            rel_list = rel_list[1:]

            if (len(rel_list) and len(rel_name)) == 2:
                painter = rel_name[0].replace('\n', '')
                translator = rel_name[1].replace('\n', '')

            elif (len(rel_list) and len(rel_name)) == 1:
                if '역자' in rel_list:
                    translator = rel_name[0].replace('\n', '')
                    painter = ''
                else:
                    translator = ''
                    painter = rel_name[0].replace('\n', '')

            else:
                translator = ''
                painter = ''

            translator_list.append(translator)
            painter_list.append(painter)

            ISBN_str = book_info_text.find('ISBN')+6
            ISBN_end = book_info_text.find('|', ISBN_str)

            if ISBN_end == -1:
                ISBN_end = book_info_text.find('\n', ISBN_str)

            ISBN = book_info_text[ISBN_str:ISBN_end]

            if '\n' in ISBN:
                ISBN = ISBN[0:int(ISBN.find('\n'))]

            ISBN_list.append(ISBN)

            content = ''
            content = get_text_list(soup_det.select("div.book_cnt"))
            if content == []:
                content = [""]
                content_list.append(content)
            else:
                content_list.append(content)

            for src in soup_det.find("div", class_="thumb_type").find_all("a"):
                bookImage = src.find("img")["src"]
                image_list.append(bookImage)

            writer_a = soup_det.find("div", class_="book_info_inner").find_all("div")[
                2].find_all("a")[:-1]
            writer_book = soup_det.find(
                "div", class_="book_info").find("a").text
            writer_book_bid = soup_det.find("div", class_="book_info").find("a")[
                "href"].split("=")[1]

            bid_list.append(writer_book_bid)
            title_list.append(writer_book)

            writer = soup_det.find("div", class_="book_info_inner").find_all("div")[
                2].text.split("|")[0][3:].strip()
            writer_list.append(writer)

            for w in range(0, len(writer_a)):
                writer_n = writer_a[w].text
                writer_name.append(writer_n)
                writer_href = writer_a[w]["href"]
                writer_link.append(writer_href)
                writer_split = writer_a[w]["href"].split("=")[3]
                writer_num.append(writer_split)
                writer_book_title.append(writer_book)
                writer_bid.append(writer_book_bid)
                writer_isbn.append(ISBN)

            time.sleep(round(np.random.uniform(0.5, 1.4), 2))

            if i == bidSearchEnd:
                print('bid 번호에 대한 도서 '+str(searchCount)+'권 크롤링이 완료되었습니다.')
                driver.quit()
                break

        book_list = []
        book_DF = ''

        for title, writer, translator, painter, publisher, publishDate, intro, content, authorIntro, categoryTop, categoryMiddle, categoryBottom, bid, ISBN, grade, review, image in zip(title_list, writer_list, translator_list, painter_list, publisher_list, publish_date_list, intro_list, content_list, author_intro_list, category_top_list, category_middle_list, category_bottom_list, bid_list, ISBN_list, grade_list, review_list, image_list):
            book = {"title": title, "writer": writer, "translator": translator, "painter": painter, "publisher": publisher, "publishDate": publishDate, "intro": intro, "content": content,
                    "authorIntro": authorIntro, "categoryTop": categoryTop, "categoryMiddle": categoryMiddle, "categoryBottom": categoryBottom, "bid": bid, "ISBN": ISBN, "grade": grade, "review": review, "image": image}
            book_list.append(book)

        book_DF = pd.DataFrame(book_list)

        writer_info_list = []
        writer_DF = ''

        for num, name, bookTitle, bid, isbn, link in zip(writer_num, writer_name, writer_book_title, writer_bid, writer_isbn, writer_link):
            writer_info = {"num": num, "name": name, "bookTitle": bookTitle,
                           "bid": bid, "isbn": isbn, "link": link}
            writer_info_list.append(writer_info)

        writer_DF = pd.DataFrame(writer_info_list)

        end_now = datetime.datetime.now()
        end_time = end_now.strftime('%Y-%m-%d %H:%M:%S')
        end_list.append(end_time)
        complete = 'complete'
        complete_list.append(complete)
        errorDetail = ''
        errorDetail_list.append(errorDetail)
        crawlerNum_list.append(11)

        task_list = []

        task_DF = ''

        for taskId, taskContent, str_time, end_time, complete, errorDetail, crawlerNum in zip(taskId_list, taskContent_list, str_list, end_list, complete_list, errorDetail_list, crawlerNum_list):
            task = {"taskId": taskId, "taskContent": taskContent, "str_time": str_time, "end_time": end_time,
                    "complete": complete, "errorDetail": errorDetail, "crawlerNum": crawlerNum}
            task_list.append(task)

        task_DF = pd.DataFrame(task_list)

        conn = engine.connect()

        book_DF.to_sql(name='bid_crawling', con=engine,
                       if_exists='append', index=False)
        writer_DF.to_sql(name='writer_info', con=engine,
                         if_exists='append', index=False)
        task_DF.to_sql(name='task', con=engine,
                       if_exists='append', index=False)

        conn.close()

        searchMok -= 1
        bidSearchStart += 50
        taskId += 1

        time.sleep(1)

        return HttpResponseRedirect(reverse_lazy('bidIndex'))


class BookFilterView(BSModalFormView):
    template_name = 'book/filter_book.html'
    form_class = BookFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


class BookCreateView(BSModalCreateView):
    template_name = 'book/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = BookCrawling
    template_name = 'book/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


class BidBookUpdateView(BSModalUpdateView):
    model = BidCrawling
    template_name = 'book/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('bidIndex')


class BookReadView(BSModalReadView):
    model = BookCrawling
    template_name = 'book/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = BookCrawling
    template_name = 'book/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')


class BidBookDeleteView(BSModalDeleteView):
    model = BidCrawling
    template_name = 'book/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('bidIndex')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'book/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'book/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')


def books(request):
    data = dict()
    if request.method == 'GET':
        books = BookCrawling.objects.all()
        data['table'] = render_to_string(
            '_books_table.html',
            {'books': books},
            request=request
        )
        return JsonResponse(data)


def bids(request):
    data = dict()
    if request.method == 'GET':
        bids = BidCrawling.objects.all()
        data['table'] = render_to_string(
            '_bid_table.html',
            {'bids': bids},
            request=request
        )
        return JsonResponse(data)
