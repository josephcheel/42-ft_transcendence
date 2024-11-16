from django.db import models
from .status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
#try: 
#	from usermodel.models import User
#except:
#	def __str__(self):
#		return self.username
#	pass


if settings.DEBUG:

	from django.contrib.auth.models import AbstractUser
	class User(AbstractUser):
		lowercase_username = models.CharField(max_length=100, null=True)
		tournament_name = models.CharField(max_length=100, null=True)
		puntos = models.IntegerField(default=1000)
		puntos_reservados = models.IntegerField(default=0)
		ethereum_address = models.CharField(max_length=44, null=True)
		ethereum_private_key = models.CharField(max_length=66, null=True, blank=True)
		# Specify a unique related_name for the groups field
		groups = models.ManyToManyField(
			'auth.Group', related_name='users_db_Group', blank=True)
		user_permissions = models.ManyToManyField(
			'auth.Permission', related_name='users_db_Permission', blank=True)

User = get_user_model()

# Create your models here.

class Tournaments(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, null=True)
	player_id = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, related_name='tournaments_player')
	date_start = models.DateTimeField()
	last_match_date = models.DateTimeField()
	date_max_end = models.DateTimeField()
	max_players = models.IntegerField()
	cost = models.IntegerField(default=0)
	#points_collected = models.IntegerField()
	price_1 = models.IntegerField(default = 0)
	price_2 = models.IntegerField(default = 0)
	price_3 = models.IntegerField(default = 0)
	winning_points = models.IntegerField(default = 5, null = True)
	id_winner = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, related_name='tournaments_winner')
	id_second = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, related_name='tournaments_second')
	id_third = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, related_name='tournaments_third')
	status = models.CharField(
		max_length=8, choices=StatusTournaments.choices, default=StatusTournaments.OPEN_TOURNAMENT)
	current_round = models.IntegerField()
	hash_previus = models.CharField(max_length=256)
	hash = models.CharField(max_length=256)
#	groups = models.ManyToManyField('user_groups',related_name='users_db_Group', blank=True)
#	user_permissions = models.ManyToManyField('user_permissions',related_name='users_db_Permission', blank=True)


class Invitations(models.Model):
	tournament_id = models.ForeignKey(Tournaments, on_delete=models.CASCADE, null=True, related_name='invitations_tournament')
	player_id = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='invitations_player')
	status = models.CharField(max_length=8, choices=StatusInvitations.choices,
		default=StatusInvitations.INVITATION_IGNORED)

class Matches(models.Model):
	id = models.AutoField(primary_key=True)
	tournament_id = models.IntegerField(default=None,null=True)
	player_id_1 = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='matches_player_1')
	is_player1_in_room = models.BooleanField(default=False)
	player_id_2 = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='matches_player_2')
	is_player2_in_room = models.BooleanField(default=False)
	date_time = models.DateTimeField()
	winner_id = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='matches_winner')
	points_winner = models.IntegerField(default=0, null = True)
	looser_id = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='matches_looser')
	points_looser = models.IntegerField(default=0, null = True)
	round = models.CharField(max_length=11, choices=Rounds.choices, default=Rounds.QUALIFIED_ROUND.value, null = True)
	number_round = models.IntegerField()
	status = models.CharField(max_length=20, choices=StatusMatches.choices, default=StatusMatches.NOT_PLAYED.value)
