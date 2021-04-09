from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('filter/', views.BookFilterView.as_view(), name='filter_book'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
    path('bidUpdate/<int:pk>', views.BidBookUpdateView.as_view(),
         name='bid_update_book'),
    path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_book'),
    path('bidDelete/<int:pk>', views.BidBookDeleteView.as_view(),
         name='bid_delete_book'),
    path('books/', views.books, name='books'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('crawling/', views.crawlingBook, name='crawling_book'),
    path('bidcrawler/', views.bidCrawler, name='crawler_bid'),
    path('crawlingbook/', views.crawling, name='crawling'),
    path('detail/<int:id>', views.Detail, name='detail'),
    path('bidDetail/<int:bid>', views.BidDetail, name='bid_detail'),
    path('bidIndex/', views.bidIndex.as_view(), name='bidIndex'),
    path('bidCrawling', views.bidCrawling, name='bid_Crawling'),
]
