from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('DS8660_Module4', views.DS8660_Module4, name = 'DS8660_Module4'),
    path('Sentiment_Analyzer', views.Sentiment_Analyzer, name = 'Sentiment_Analyzer')
]

urlpatterns += staticfiles_urlpatterns()
