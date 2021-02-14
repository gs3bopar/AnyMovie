from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^results/', views.results, name='results'),
    path('movie/<str:t_id>/', views.movie),
    url(r'^favourite/save/$', views.favourite_save, name='favourite_save'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/password_reset/done', views.send_mail, name='send_mail'),
    url(r'^accounts/signup/', views.signup, name='signup'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
