from django.db import models

# Create your models here.
class Tournements(models.Model):
	name = models.CharField(max_length=30)
	Date = models.DateTimeField()
	max_players = models.IntegerField()
	price_1 = models.IntegerField()
	price_2 = models.IntegerField()
	price_3 = models.IntegerField()
	winner = models.CharField(max_length=30)
	second = models.CharField(max_length=30)
	third = models.CharField(max_length=30)
	hashprevius = models.CharField(max_length=256)
	hash = models.CharField(max_length=256)

class matches(models.Model):
	tournement = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player1 = models.CharField(max_length=30)
	player2 = models.CharField(max_length=30)
	date = models.DateTimeField()
	winner = models.CharField(max_length=30)
	round = models.IntegerField()

class players(models.Model):
	tournement = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	price = models.IntegerField()
	round = models.IntegerField()