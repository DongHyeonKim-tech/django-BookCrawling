# import requests
import django
import re
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium import webdriver
import time
from sqlalchemy import create_engine
import pymysql
import os
import json
from django.http import HttpResponse

# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py 파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")

django.setup()


def get_text_list(tag_list):
    return [tag.text for tag in tag_list]

# branch Testing

def book(request):
    data = json.loads(request.body)

    baseUrl = 'https://book.naver.com/search/search_in.nhn?query='
    plusUrl = input('검색어 입력: ')
    searchSubject = quote_plus(plusUrl)

    url = baseUrl + searchSubject + "&&"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # 검색 페이지에서 정보 가져오기보 가져오기
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

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    chromedriver = 'C:/Dev_program/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver, options=options)

    driver.implicitly_wait(time_to_wait=5)

    searchStartPage = input('크롤링 시작 페이지(숫자): ')
    searchEndPage = input('크롤링 끝낼 페이지(숫자): ')

    searchStart = int(quote_plus(searchStartPage))
    searchEnd = int(quote_plus(searchEndPage))

    for k in range(searchStart, searchEnd+1):
        url_pre = (url+'pattern=0&orderType=rel.desc&viewType=list&searchType=bookSearch&serviceSm=service.basic&title=&author=&publisher=&isbn=&toc=&subject=&publishStartDay=&publishEndDay=&categoryId=&qdt=1&filterType=0&filterValue=&serviceIc=service.author&buyAllow=0&ebook=0&abook=0&page='+str(k))
        html_pre = urlopen(url_pre)
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
            for src in soup_pre.find("ul", id="searchBiblioList").find_all("div", class_="thumb type_search"):
                bookImage = src.find("img")["src"]
                image_list.append(bookImage)
        except AttributeError:
            print('검색어에 대한 도서' + str(len(ISBN_list)) + '권 크롤링이 완료되었습니다.')
            driver.quit()

        for i in range(0, len(link_list)):
            driver.get(link_list[i])
            url_det = link_list[i]
            html_det = urlopen(url_det)
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

    book_DF = pd.DataFrame(book_list)

    engine = create_engine(
        "mysql+pymysql://root:xkzlxkzl1!@127.0.0.1:3306/book?charset=utf8mb4", encoding='utf8')

    conn = engine.connect()

    book_DF.to_sql(name='book_crawling', con=engine,
                   if_exists='append', index=False)
    conn.close()

    return HttpResponse(''), 'book/crawling_book.html'
