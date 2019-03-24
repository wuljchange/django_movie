from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='类别')

    class Meta:
        db_table = 'genre'
        verbose_name_plural = '类别'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductionRole(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='角色')

    class Meta:
        db_table = 'production_role'
        verbose_name_plural = '角色'
        ordering = ['title']

    def __str__(self):
        return self.title


class Country(models.Model):
    country = CountryField(unique=True, verbose_name='国家或地区(英文)')
    country_zh = models.CharField(max_length=50, default='', verbose_name='国家或地区(中文)')

    class Meta:
        db_table = 'country'
        verbose_name_plural = '国家或地区'
        ordering = ['country']

    def __str__(self):
        return str(self.country_zh)


class Person(models.Model):
    first_name = models.CharField(max_length=30, default='', verbose_name='名')
    last_name = models.CharField(max_length=30, default='', verbose_name='姓')
    full_name = models.CharField(max_length=60, default='', verbose_name='全名')
    date_of_birth = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.", verbose_name='出生日期')
    date_of_death = models.DateField(
        null=True,
        blank=True,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
        verbose_name='逝世日期'
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        verbose_name='头像'
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='people',
        verbose_name='国家或地区'
    )
    production_roles = models.ManyToManyField(
        ProductionRole,
        blank=True,
        related_name='people',
        verbose_name='电影中的角色'
    )
    description = models.CharField(max_length=1000, default='', verbose_name='简介')

    class Meta:
        db_table = 'person'
        verbose_name_plural = '人物'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name='题目')
    year = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='上映日期'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='简介'
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='评分'
    )
    trailer = models.URLField(verbose_name='预告片地址')
    cover = models.ImageField(verbose_name='电影封面')
    link_to_watch = models.URLField(
        null=True,
        blank=True,
        verbose_name='完整观看地址'
    )
    date_added = models.DateField(auto_now_add=True, verbose_name='添加到后台日期')
    duration = models.DurationField(help_text='Format HH:MM:SS', verbose_name='时长')

    likes = models.IntegerField(default=0, blank=True)
    favourites = models.IntegerField(default=0, blank=True)
    watches = models.IntegerField(default=0, blank=True)

    director = models.ManyToManyField(
        Person,
        blank=True,
        related_name='directed_movies',
        limit_choices_to={'production_roles': ProductionRole.objects.filter(title='导演').get().pk},
        verbose_name='导演'
    )
    production_countries = models.ManyToManyField(
        Country,
        related_name='movies',
        verbose_name='国家或地区'
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='movies',
        verbose_name='类别'
    )
    key_actors = models.ManyToManyField(
        Person,
        blank=True,
        limit_choices_to={'production_roles': ProductionRole.objects.filter(title='演员').get().pk},
        related_name='acted_movies',
        verbose_name='主演',
    )

    class Meta:
        db_table = 'movie'
        verbose_name_plural = '电影'
        ordering = ['-date_added']

    def __str__(self):
        return self.title + ', ' + str(self.year)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='author_comment',
        verbose_name='author of comment',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movie_comment',
        verbose_name='movie of comment',
    )
    content = models.CharField(max_length=1000)
    date_time = models.DateTimeField()
    grade = models.IntegerField(default=5)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    up_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='up_user_comment',
        verbose_name='up_vote of comment',
    )
    down_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='down_user_comment',
        verbose_name='down_user of comment',
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    liked_movies = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='users_liked',
        verbose_name='liked movies'
    )
    disliked_movies = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='users_disliked',
        verbose_name='disliked movies'
    )
    favourite_movies = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='users_favourite',
        verbose_name='favourite movies'
    )
    watch_list = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='users_added_watch_list',
        verbose_name='watch list'
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        db_table = 'profile'
