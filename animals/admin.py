from django.contrib import admin
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from animals.models import *


# Auto completes
class BreedAutocomplete(AutocompleteSettings):
    search_fields = ('^name',)

class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city_name_ru', '^city_name_en')


class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(AnimalType, AnimalTypeAdmin)


class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'visibility']
    list_filter = ['type', 'visibility']
    search_fields = ['name']

admin.site.register(Breed, BreedAdmin)


class AnimalAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'type', 'breed', 'region', 'birth_day', 'died']
    list_filter = ['type', 'gender', 'died']
    search_fields = ['name']

admin.site.register(Animal, AnimalAdmin)
autocomplete.register(Animal.breed, BreedAutocomplete)
autocomplete.register(Animal.region, RegionAutocomplete)
