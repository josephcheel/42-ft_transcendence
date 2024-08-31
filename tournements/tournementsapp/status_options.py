from enum import Enum

class StatusTournements(Enum):
	OPEN_TOURNEMENT = "open"
	CLOSED_TOURNEMENT = "closed"
	FINISHED_TOURNEMENT = "finished"

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
	STARTED = "sttarted"

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