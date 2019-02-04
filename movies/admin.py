import datetime

from django.contrib import admin
from django.contrib.auth.models import Group
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Genre, Movie, Person, Country, ProductionRole


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie


class MovieModelAdmin(ImportExportModelAdmin):
    resource_class = MovieResource
    list_display = ['title', 'year', 'rating', 'date_added']
    list_filter = ['date_added', 'rating', 'year', 'genres']
    search_fields = ['title', 'description', 'key_actors__first_name', 'key_actors__last_name',
                     'director__first_name', 'director__last_name']
    exclude = ['rating', 'likes', 'dislikes']    # comment

    class Meta:
        model = Movie


class PersonResource(resources.ModelResource):
    class Meta:
        model = Person


class PersonModelAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ['last_name', 'first_name', 'age', 'all_production_roles', 'country', 'movies_count']
    list_filter = ['production_roles', 'country']
    search_fields = ['first_name', 'last_name']

    class Meta:
        model = Person

    def age(self, person):
        born = person.date_of_birth
        today = datetime.date.today()
        is_alive = person.date_of_death is None
        if is_alive:
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        else:
            date_of_death = person.date_of_death
            return 'Died(age {})'.format(
                   str(date_of_death.year - born.year - ((date_of_death.month, date_of_death.day) < (born.month, born.day))))

    def all_production_roles(self, person):
        return ', '.join([role.title for role in person.production_roles.order_by('title').all()])

    def movies_count(self, person):
        return (person.acted_movies.all() | person.directed_movies.all()).distinct().count()


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class GenreModelAdmin(ImportExportModelAdmin):
    resource_class = GenreResource


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country


class CountryModelAdmin(ImportExportModelAdmin):
    resource_class = CountryResource


class ProductionRoleResource(resources.ModelResource):
    class Meta:
        model = ProductionRole


class ProductionRoleModelAdmin(ImportExportModelAdmin):
    resource_class = ProductionRoleResource


admin.site.site_header = 'Administration'
admin.site.name = 'MovieNet'
admin.site.site_title = 'MovieNet'

admin.site.unregister(Group)

admin.site.register(Movie, MovieModelAdmin)
admin.site.register(Person, PersonModelAdmin)
admin.site.register(Genre, GenreModelAdmin)
admin.site.register(Country, CountryModelAdmin)
admin.site.register(ProductionRole, ProductionRoleModelAdmin)
