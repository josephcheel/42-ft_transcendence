from django.db import models

# Create your models here.
class Tournements(models.Model):
	OPEN_TOURNEMENT = 0
	CLOSED_TOURNEMENT = 1
	FINISHED_TOURNEMENT = 2


	STATUS_CHOICES = [
		{OPEN_TOURNEMENT, "open"},
		{CLOSED_TOURNEMENT, "closed"},
		{FINISHED_TOURNEMENT, "finished"},
	]
	name = models.CharField(max_length=30)
	date = models.DateTimeField()
	max_players = models.IntegerField()
	price_1 = models.IntegerField()
	price_2 = models.IntegerField()
	price_3 = models.IntegerField()
	winner = models.CharField(max_length=30)
	second = models.CharField(max_length=30)
	third = models.CharField(max_length=30)
	status = models.CharField(
		max_length=8, choices=STATUS_CHOICES, default=OPEN_TOURNEMENT)
	hash_previus = models.CharField(max_length=256)
	hash = models.CharField(max_length=256)

class matches(models.Model):
	tournement = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player1 = models.CharField(max_length=30)
	player2 = models.CharField(max_length=30)
	date = models.DateTimeField()
	winner = models.CharField(max_length=30)
	round = models.IntegerField()

class T_players(models.Model):
	tournement = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player_id = models.CharField(max_length=30)
	price = models.IntegerField()
	round = models.IntegerField()