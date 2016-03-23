from application.models import *


def is_match_existing(user_Id, likes):
	is_match = Match.objects.filter(user_Id=likes, likes=user_Id).count()
	match = False
	if is_match > 0:
		match = True

	return match


def update_like(user_Id, likes, match):
	match = Match(user_Id, likes, match)
	match.save()

