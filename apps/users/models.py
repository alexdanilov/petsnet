import datetime
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from apps.utils import StdImageField
from apps.system.models import Regions



GENDER_CHOICES = (
    (u'm', _('gender-male')),
    (u'f', _('gender-female')),
)
class UserProfile(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    region = models.ForeignKey(Regions, verbose_name=_('region'), blank=True, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)
    birth_day = models.DateField(verbose_name=_('birth_day'), blank=True)
    avatar = StdImageField(upload_to='u/', sizes=((60, 60), (100, 100), (200, 250)), blank=True)

    contact_email = models.EmailField(verbose_name=_('contact_email'), blank=True)
    contact_phone = models.CharField(max_length=100, verbose_name=_('contact_phone'), blank=True)
    contact_skype = models.CharField(max_length=100, verbose_name=_('contact_skype'), blank=True)
    website = models.CharField(max_length=200, verbose_name=_('website'), blank=True)

    activity = models.TextField(verbose_name=_('activity'), blank=True)
    interests = models.TextField(verbose_name=_('interests'), blank=True)
    like_books = models.TextField(verbose_name=_('like_books'), blank=True)
    like_films = models.TextField(verbose_name=_('like_films'), blank=True)
    like_phrases = models.TextField(verbose_name=_('like_phrases'), blank=True)
    about = models.TextField(verbose_name=_('about'), blank=True)

    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, blank=True)
    balls = models.IntegerField(default=0, blank=True)
    last_login = models.DateTimeField(blank=True)
    activate = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % self.name

    @property
    def age(self):
        return int((datetime.datetime.now() - self.birth_day).days / 365)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def new_messages(self):
        return UserMessage.objects.filter(to_user=self, readed=False).count()

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('email', 'balance', 'balls', 'last_login', 'activate', 'birth_day')



class UserFriend(models.Model):
    user = models.ForeignKey(UserProfile, related_name='friend_user')
    friend = models.ForeignKey(UserProfile, related_name='friend_friend')
    accept = models.BooleanField(default=False, verbose_name=_('friend_accept'), db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s -> %s' % (self.user.full_name, self.to_user.full_name)

    class Meta:
        ordering = ['-created']
        db_table = 'user_friends'
        verbose_name = _("user_friend")
        verbose_name_plural = _("user_friends")



class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, related_name='message_user')
    author = models.ForeignKey(UserProfile, related_name='message_author')
    subject = models.CharField(max_length=255, blank=True, verbose_name=_('subject'))
    message = models.CharField(max_length=500, verbose_name=_('message'))
    readed = models.BooleanField(default=False, verbose_name=_('readed'), db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s -> %s' % (self.user.full_name, self.to_user.full_name)

    class Meta:
        ordering = ['-created']
        db_table = 'user_messages'
        verbose_name = _("user_message")
        verbose_name_plural = _("user_messages")



class UserWall(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_('user'))
    author = models.ForeignKey(UserProfile, related_name='author')
    message = models.TextField(verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.message

    class Meta:
        ordering = ['-created']
        db_table = 'user_wall'
        verbose_name = _("user_wall")
        verbose_name_plural = _("user_walls")
