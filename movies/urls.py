from django.conf.urls import url
from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^simple_search/$', views.simple_search, name='simple-search'),

    url(r'^(?P<movie_id>[0-9]+)/$', views.movie_detail, name='movie-detail'),
    url(r'^comment/(?P<comment_id>[0-9]+)/(?P<choice>[a-zA-Z]+)/$', views.vote_comment, name='vote-comment'),
    url(r'^genre=(?P<genre_id>[0-9]+)/$', views.genre_search, name='genre-search'),
    url(r'^country=(?P<country_id>[0-9]+)/$', views.country_search, name='country-search'),
    url(r'^person=(?P<person_id>[0-9]+)/$', views.person_detail, name='person-detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login-user'),
    url(r'^logout_user/$', views.logout_user, name='logout-user'),
    url(r'^profile=(?P<user_id>[0-9]+)/$', views.user_profile, name='user-profile'),
    # url(r'^recommendations/$', views.recommendations, name='recommendations'),


    url(r'^like_movie/$', views.like_movie, name='like-movie'),
    url(r'^add_to_favourites/$', views.add_to_favourites, name='add-to-favourites'),
    url(r'^add_to_watch_list/$', views.add_to_watch_list, name='add-to-watch-list'),
]
