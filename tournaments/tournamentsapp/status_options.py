from enum import Enum

class StatusTournaments(Enum):
	OPEN_TOURNAMENT = "open"
	CLOSED_TOURNAMENT = "closed"
	FINISHED_TOURNAMENT = "finished"

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]

class StatusInvitations(Enum): 
	INVITATION_IGNORED = "ignored"
	INVITATION_ACCEPTED = "accepted"
	INVITATION_REFUSED = "refused"

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]
	
class StatusMatches(Enum):
	NOT_PLAYED = "not played"
	PLAYED = "played"
	STARTED = "started"
	NEXT_ROUND_ASSIGNED = "assigned"
	WALKOVER = "walkover"
	WAITING_PLAYER1 = "waiting player 1"
	WAITING_PLAYER2 = "waiting player 2"

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]
	
class Rounds(Enum):
	FINAL_ROUND = "final"
	THIRD_PLACE_ROUND = "third place"
	SEMIFINAL_ROUND = "semifinal"
	QUALIFIED_ROUND = "qualified"

	@classmethod
	def choices(cls):
		return [(key.value, key.name) for key in cls]