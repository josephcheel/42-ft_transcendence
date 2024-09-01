from django.db import models
from .status_options import StatusTournements, StatusInvitations, StatusMatches, Rounds
from django.contrib.auth import get_user_model
try: 
	from usermodel.models import User
except:
	pass

# Create your models here.
User = get_user_model()

class Tournements(models.Model):
	id = models.AutoField(primary_key=True)
	player_id = models.IntegerField()
	date_start = models.DateTimeField()
	last_match_date = models.DateTimeField()
	date_max_end = models.DateTimeField()
	max_players = models.IntegerField()
	cost = models.IntegerField()
	points_collected = models.IntegerField()
	price_1 = models.IntegerField()
	price_2 = models.IntegerField()
	price_3 = models.IntegerField()
	id_winner = models.IntegerField()
	id_second = models.IntegerField()
	id_third = models.IntegerField()
	status = models.CharField(
		max_length=8, choices=StatusTournements.choices, default=StatusTournements.OPEN_TOURNEMENT)
	current_round = models.IntegerField()
	hash_previus = models.CharField(max_length=256)
	hash = models.CharField(max_length=256)

class Invitations(models.Model):
	tournement_id = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player_id = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=8, choices=StatusInvitations.choices,
		default=StatusInvitations.INVITATION_IGNORED)

class Matches(models.Model):
	match_id = models.AutoField(primary_key=True)
	tournement_id = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player_id_1 = models.IntegerField()
	player_id_2 = models.IntegerField()
	date_time = models.DateTimeField()
	winner_id = models.IntegerField()
	looser_id = models.IntegerField()
	round = models.CharField(max_length=11, choices=Rounds.choices, default=Rounds.QUALIFIED_ROUND)
	number_round = models.IntegerField()
	status = models.CharField(max_length=10, choices=StatusMatches.choices, default=StatusMatches.NOT_PLAYED)

class T_players(models.Model):
	tournement = models.ForeignKey(Tournements, on_delete=models.CASCADE)
	player_id = models.IntegerField()
	price = models.IntegerField()	
	round = models.IntegerField()