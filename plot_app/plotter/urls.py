from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plot/', views.plot, name='plot'),
    path('plot_result/', views.plot_result, name='plot_result'),
    path('display_data/', views.display_data, name='display_data'),
]
