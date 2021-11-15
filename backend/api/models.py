from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=20)
    age = models.IntegerField()
    nationality = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class News(models.Model):
    news_date = models.DateTimeField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    team_label = models.ManyToManyField(Team, blank=True)
    players_label = models.ManyToManyField(Player, blank=True)
    image = models.ImageField(upload_to='news_images')
    is_hot = models.BooleanField()
    def __str__(self):
        return self.title

class RegisteredUser(AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=20)

class ConfirmationCode(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    code = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)

class Video(models.Model):
    title = models.CharField(max_length=100)
    content = models.FileField(upload_to='Videos')
    image = models.ImageField(upload_to='Videos_image')
    team_label = models.ManyToManyField(Team, blank=True)
    players_label = models.ManyToManyField(Player, blank=True)
    def __str__(self):
        return self.title

class Match(models.Model):
    match_date = models.DateTimeField()
    host = models.ForeignKey(Team, related_name='host',on_delete=models.DO_NOTHING)
    guest = models.ForeignKey(Team, related_name='guest',on_delete=models.DO_NOTHING)
    host_score = models.IntegerField(default=0)
    guest_score = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    week = models.IntegerField()
    def __str__(self):
        return self.host.name + " - " + self.guest.name

class FavoriteTeams(models.Model):
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class RssLinks(models.Model):
    rss_link = models.CharField(max_length= 300, unique=True)
    def __str__(self):
        return self.rss_link