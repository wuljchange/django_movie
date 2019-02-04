import time
import datetime

from django.test import TestCase
from .models import Genre, ProductionRole, Country, Person, Movie


def create_movie(i):
    genre = Genre.objects.create(
        name='test_genre' + str(i)
    )

    person = Person.objects.create(
        first_name='test fn' + str(i),
        last_name='test ln' + str(i),
        date_of_birth='2001-11-11',
        photo='test_photo.jpg',
        country=Country.objects.get(country='GB'),
    )
    person.production_roles.add(ProductionRole.objects.get(title='Actor'))
    person.production_roles.add(ProductionRole.objects.get(title='Director'))
    person.save()

    movie = Movie.objects.create(
        title='test title' + str(i),
        year=i,
        description='test',
        rating=10,
        trailer='test_link',
        cover='test cover',
        duration=datetime.timedelta(hours=1, minutes=30),
        director=person
    )
    movie.production_countries.add(Country.objects.get(country='GB'))
    movie.genres.add(genre)
    movie.key_actors.add(person)
    movie.save()

    return movie


class AverageLoadTest(TestCase):
    def setUp(self):
        ProductionRole.objects.create(title='Actor')
        ProductionRole.objects.create(title='Director')
        Country.objects.create(country='GB')
        self.n = 1000

        self.shows = []
        start = time.time()
        for i in range(self.n):
            show = create_movie(i)

            self.shows.append(show)
        end = time.time()

        print('Inserting {} genres, countries, people, movies: {:.0f} s'.format(self.n, end - start))

    def tearDown(self):
        start = time.time()

        for show in self.shows:
            show.delete()

        end = time.time()

        print('Deleting {} genres, countries, people, movies: {:.0f} s'.format(self.n, end - start))

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movies' in response.context)
        self.assertEqual(len([show.id for show in response.context['movies']]), self.n)


class MaxLoadTest(TestCase):
    def setUp(self):
        ProductionRole.objects.create(title='Actor')
        ProductionRole.objects.create(title='Director')
        Country.objects.create(country='GB')
        self.n = 10000

        self.shows = []
        start = time.time()
        for i in range(self.n):
            show = create_movie(i)

            self.shows.append(show)
        end = time.time()

        print('Inserting {} genres, countries, people, movies: {:.0f} s'.format(self.n, end - start))

    def tearDown(self):
        start = time.time()

        for show in self.shows:
            show.delete()

        end = time.time()

        print('Deleting {} genres, countries, people, movies: {:.0f} s'.format(self.n, end - start))

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movies' in response.context)
        self.assertEqual(len([show.id for show in response.context['movies']]), self.n)
