import re

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Movie, Genre, Country, Person, Comment
from .forms import UserForm

import arrow
import json
from collections import defaultdict


MOVIES_PER_PAGE = 15
simple_query = None
text = None
genre = None
year_period = None
rating = None


def make_pagination(request, movies):
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, MOVIES_PER_PAGE)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    return movies


def index(request, movies=None):
    if movies is None:
        movies = Movie.objects.all().order_by('-rating')

    context = {
        'movies': make_pagination(request, movies),
        'genres': Genre.objects.all().order_by('name'),
        'countries': Country.objects.all().order_by('country_zh')
    }

    return render(request, 'movies/index.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        data = defaultdict()
        data['author'] = User.objects.get(pk=request.user.id)
        data['movie'] = movie
        data['content'] = request.POST['message-text']
        data['grade'] = int(request.POST['grade'])
        data['date_time'] = arrow.arrow.datetime.now()
        Comment.objects.create(**data)

    Com = Comment.objects.filter(movie=movie)
    try:
        rate = round(sum([comment.grade for comment in Com])/len(Com), 1)
        movie.rating = rate
        movie.save()
    except ZeroDivisionError:
        pass
    new_comments = list(Com.order_by('-date_time'))[:6]
    hot_comments = list(Com.order_by('-up_votes'))[:6]

    context = {
        'movie': movie,
        'new_comments': new_comments,
        'hot_comments': hot_comments,
        'numbers': len(Com),
    }

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        is_in_likes = user.profile.liked_movies.filter(id=movie_id).count() == 1
        is_in_favourites = user.profile.favourite_movies.filter(id=movie_id).count() == 1
        is_in_watch_list = user.profile.watch_list.filter(id=movie_id).count() == 1

        context['is_in_likes'] = is_in_likes
        context['is_in_favourites'] = is_in_favourites
        context['is_in_watch_list'] = is_in_watch_list

    return render(request, 'movies/movie_detail.html', context)


def vote_comment(request, comment_id, choice):
    comment = Comment.objects.get(pk=comment_id)
    up_users = list(comment.up_users.all())
    down_users = list(comment.down_users.all())
    data = defaultdict()
    if request.user not in up_users+down_users:
        if choice == 'up':
            comment.up_users.add(request.user)
            comment.up_votes += 1
            comment.save()
        else:
            comment.down_users.add(request.user)
            comment.down_votes += 1
            comment.save()
        data.update({"res": "vote"})
    else:
        data.update({"res": "done"})
    ret = HttpResponse(json.dumps(data))
    ret['Content-Type'] = 'application/json;charset=utf-8'
    return ret


def simple_search(request):
    global simple_query
    tmp = request.GET.get('q')
    if tmp is not None:
        simple_query = tmp
    words = re.split(r'\s+', simple_query.strip())

    if len(words) == 0 or (len(words) == 1 and words[0] == ''):
        return redirect('movies:index')
    movies = Movie.objects.all()
    for word in words:
        movies = movies.filter(
            Q(title__icontains=word) |
            Q(description__icontains=word) |
            Q(director__last_name__icontains=word) |
            Q(director__first_name__icontains=word) |
            Q(director__full_name__icontains=word) |
            Q(key_actors__first_name__icontains=word) |
            Q(key_actors__last_name__icontains=word) |
            Q(key_actors__full_name__icontains=word)
        ).distinct()

    movies = movies.order_by('-rating')
    context = {
        'query': '"' + simple_query + '"',
        'genres': Genre.objects.all().order_by('name'),
        'countries': Country.objects.all().order_by('country_zh'),
        'movies': make_pagination(request, movies)
    }

    return render(request, 'movies/index.html', context)


def genre_search(request, genre_id):
    movies = Movie.objects.filter(genres__exact=genre_id).order_by('-rating')
    query = '"' + str(Genre.objects.get(id=genre_id)) + '" movies'

    context = {
        'movies': make_pagination(request, movies),
        'genres': Genre.objects.all().order_by('name'),
        'countries': Country.objects.all().order_by('country_zh'),
        'query': query
    }

    return render(request, 'movies/index.html', context)


def year_search(request, year):
    movies = Movie.objects.filter(year=year)
    query = 'movies from ' + str(year) + ' year'

    context = {
        'movies': make_pagination(request, movies),
        'query': query
    }

    return render(request, 'movies/index.html', context)


def country_search(request, country_id):
    movies = Movie.objects.filter(production_countries__id=country_id).order_by('-rating')
    query = 'movies from ' + str(Country.objects.get(id=country_id))

    context = {
        'movies': make_pagination(request, movies),
        'genres': Genre.objects.all().order_by('name'),
        'countries': Country.objects.all().order_by('country_zh'),
        'query': query
    }

    return render(request, 'movies/index.html', context)


def person_detail(request, person_id):
    movies = Movie.objects.filter(
        Q(director__id=person_id) | Q(key_actors__id=person_id)
    ).distinct()

    person = Person.objects.get(id=person_id)
    context = {
        'movies': make_pagination(request, movies),
        'person': person,
        'roles': ', '.join([str(r) for r in person.production_roles.all()])
    }

    return render(request, 'movies/person_detail.html', context)


def logout_user(request):
    logout(request)
    return redirect('movies:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('movies:index')
            else:
                return render(request, 'movies/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'movies/login.html', {'error_message': 'Invalid login'})
    return render(request, 'movies/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('movies:index')
    context = {
        "form": form,
    }
    return render(request, 'movies/register.html', context)


def user_profile(request, user_id):
    user = request.user

    if user.is_authenticated and user.id == int(user_id):
        liked_movies = user.profile.liked_movies.all()
        favourite_movies = user.profile.favourite_movies.all()
        watch_list = user.profile.watch_list.all()

        context = {
            'user': user,
            'liked_movies': make_pagination(request, liked_movies),
            'favourite_movies':  make_pagination(request, favourite_movies),
            'watch_list':  make_pagination(request, watch_list),
        }
        return render(request, 'movies/user_profile.html', context)
    else:
        raise Http404


# AJAX methods
def like_movie(request):
    user = request.user

    if user.is_authenticated:
        movie_id = int(request.POST.get('movie_id', None))

        data = ''
        if movie_id:
            movie = Movie.objects.get(id=movie_id)
            if movie is not None:
                if movie not in user.profile.liked_movies.filter(id=movie_id):
                    likes = movie.likes + 1
                    data = 'add'
                    user.profile.liked_movies.add(movie)

                else:
                    likes = movie.likes - 1
                    data = 'delete'
                    user.profile.liked_movies.remove(movie)
                movie.likes = 0 if likes < 0 else likes
                movie.save()

        return HttpResponse(data)
    else:
        return redirect('movies:index')


def add_to_favourites(request):
    user = request.user

    if user.is_authenticated:
        movie_id = int(request.POST.get('movie_id', None))
        data = ''
        if movie_id:
            movie = Movie.objects.get(id=movie_id)
            if movie is not None:
                if movie not in user.profile.favourite_movies.filter(id=movie_id):
                    favourites = movie.favourites + 1
                    data = 'add'
                    user.profile.favourite_movies.add(movie_id)
                else:
                    favourites = movie.favourites - 1
                    data = 'delete'
                    user.profile.favourite_movies.remove(movie_id)
                movie.favourites = 0 if favourites < 0 else favourites
                movie.save()

        return HttpResponse(data)
    else:
        return redirect('movies:index')


def add_to_watch_list(request):
    user = request.user

    if user.is_authenticated:
        movie_id = int(request.POST.get('movie_id', None))
        data = ''
        if movie_id:
            movie = Movie.objects.get(id=movie_id)
            if movie is not None:
                if movie not in user.profile.watch_list.filter(id=movie_id):
                    watches = movie.watches + 1
                    data = 'add'
                    user.profile.watch_list.add(movie_id)
                else:
                    watches = movie.watches - 1
                    data = 'delete'
                    user.profile.watch_list.remove(movie_id)
                movie.watches = 0 if watches < 0 else watches
                movie.save()

        return HttpResponse(data)
    else:
        return redirect('movies:index')
