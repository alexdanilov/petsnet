import datetime
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models

from apps.system.models import Regions
from apps.users.models import UserProfile
from apps.utils import StdImageField


class AnimalType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = tinymce_models.HTMLField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'animals_types'
        verbose_name = _("animal-type")
        verbose_name_plural = _("animal-types")


class Breed(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    type = models.ForeignKey(AnimalType, verbose_name=_("type"))
    description = tinymce_models.HTMLField(blank=True, verbose_name=_("description"))
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"))

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.type)

    class Meta:
        db_table = 'animals_breeds'
        verbose_name = _("breed")
        verbose_name_plural = _("breeds")


ANIMAL_GENDERS = (
    (u'm', _('gender-male')),
    (u'f', _('gender-female')),
)
class Animal(models.Model):
    type = models.ForeignKey(AnimalType, verbose_name=_("type"))
    user = models.ForeignKey(UserProfile, verbose_name=_("user"))
    region = models.ForeignKey(Regions, verbose_name=_("region"))
    breed = models.ForeignKey(Breed, verbose_name=_("breed"))
    gender = models.CharField(max_length=1, choices=ANIMAL_GENDERS, verbose_name=_("gender"))
    birth_day = models.DateField(verbose_name=_("birth_day"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    weight = models.CharField(max_length=255, verbose_name=_("animal-weight"))
    height = models.CharField(max_length=255, verbose_name=_("animal-height"), blank=True)
    color = models.CharField(max_length=255, verbose_name=_("animal-color"), blank=True)
    history = models.TextField(verbose_name=_("animal-history"))
    description = models.TextField(verbose_name=_("animal-description"))
    it_like = models.CharField(max_length=255, verbose_name=_("animal-it-like"))
    it_not_like = models.CharField(max_length=255, verbose_name=_("animal-it-not-like"))
    loved_toy = models.CharField(max_length=255, verbose_name=_("animal-loved-toy"), blank=True)
    loved_eat = models.CharField(max_length=255, verbose_name=_("animal-loved-eat"), blank=True)
    can_do = models.CharField(max_length=255, verbose_name=_("animal-can-do"), blank=True)
    children = models.CharField(max_length=255, verbose_name=_("animal-children"))
    died = models.BooleanField(default=False, verbose_name=_("animal-died"))
    energy_level = models.IntegerField(default=1)
    intellect_level = models.IntegerField(default=1, verbose_name=_("intellect_level"))
    energy_level = models.IntegerField(default=1, verbose_name=_("energy_level"))
    friendly_level = models.IntegerField(default=1, verbose_name=_("friendly_level"))
    game_level = models.IntegerField(default=1, verbose_name=_("game_level"))
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"))
    deleted = models.BooleanField(default=False)

    @property
    def age(self):
        return (datetime.datetime.today() - self.birth_day).days / 365

    @property
    def avatar(self):
        try:
            image = AnimalImage.objects.filter(animal=self)[0].image.image1
        except Exception:
            image = None
        return image

    def __unicode__(self):
        return self.name

    @property
    def images(self):
        return AnimalImage.objects.filter(animal=self)

    class Meta:
        db_table = 'animals_animals'
        verbose_name = _("animal")
        verbose_name_plural = _("animals")


class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        exclude = ('site_id', 'user', 'visibility', 'deleted', 'region', 'birth_day')


class AnimalImage(models.Model):
    animal = models.ForeignKey(Animal, verbose_name=_('animal'))
    image = StdImageField(upload_to='a/', verbose_name=_('photo'), sizes=((100, 100), (240, 240), (500, 500)))

    def __unicode__(self):
        return self.image

    class Meta:
        db_table = 'animals_images'
        verbose_name = _("animals_image")
        verbose_name_plural = _("animals_images")
