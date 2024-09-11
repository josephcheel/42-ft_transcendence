from django.db import models
from .status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission

#try: 
#	from usermodel.models import User
#except:
#	def __str__(self):
#		return self.username
#	pass

class User(AbstractUser):
	groups = models.ManyToManyField(
		Group,
		# Añade un related_name único para evitar conflictos
		related_name='transcendence',
		blank=True,
		help_text='The groups this user belongs to.',
		verbose_name='groups',
	)
	user_permissions = models.ManyToManyField(
		Permission,
		related_name='transcendence',  # Añade un related_name único para evitar conflictos
		blank=True,
		help_text='Specific permissions for this user.',
		verbose_name='user permissions',
	)
	puntos = models.IntegerField(default=1000)
	puntos_reservados = models.IntegerField(default=0)
	def save_password(self, password):
		self.set_password(password)
		self.save()

# Create your models here.

class Tournaments(models.Model):
	id = models.AutoField(primary_key=True)
	player_id = models.IntegerField()
	date_start = models.DateTimeField()
	last_match_date = models.DateTimeField()
	date_max_end = models.DateTimeField()
	max_players = models.IntegerField()
	cost = models.IntegerField(default=0)
	#points_collected = models.IntegerField()
	price_1 = models.IntegerField(default = 0)
	price_2 = models.IntegerField(default = 0)
	price_3 = models.IntegerField(default = 0)
	id_winner = models.IntegerField(default = 0)
	id_second = models.IntegerField(default = 0)
	id_third = models.IntegerField(default=0)
	status = models.CharField(
		max_length=8, choices=StatusTournaments.choices, default=StatusTournaments.OPEN_TOURNAMENT)
	current_round = models.IntegerField()
	hash_previus = models.CharField(max_length=256)
	hash = models.CharField(max_length=256)

class Invitations(models.Model):
	tournament_id = models.IntegerField()
	player_id = models.IntegerField()
	status = models.CharField(max_length=8, choices=StatusInvitations.choices,
		default=StatusInvitations.INVITATION_IGNORED)

class Matches(models.Model):
	match_id = models.AutoField(primary_key=True)
	tournament_id = models.IntegerField()
	player_id_1 = models.IntegerField(default=0)
	player_id_2 = models.IntegerField(default=0)
	date_time = models.DateTimeField()
	winner_id = models.IntegerField(default=0)
	looser_id = models.IntegerField(default=0)
	round = models.CharField(max_length=11, choices=Rounds.choices, default=Rounds.QUALIFIED_ROUND.value)
	number_round = models.IntegerField()
	status = models.CharField(max_length=10, choices=StatusMatches.choices, default=StatusMatches.NOT_PLAYED.value)

class T_players(models.Model):
	tournament = models.IntegerField()
	player_id = models.IntegerField()
	price = models.IntegerField()	
	round = models.IntegerField()