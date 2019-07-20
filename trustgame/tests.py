from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Intro,
            yield Instructions,
            yield Question, {'q1': 0, 'q2': 25, 'q3': 25, }
        if self.player.id_in_group==1:
            yield Send, {'sent_amount': random.randint(0, Constants.endowment)}
        if self.player.id_in_group == 2:
            max_sent_back = int(self.group.sent_amount * self.subsession.multiplier)
            yield SendBack, {'sent_back_amount': random.randint(0, max_sent_back)}
        yield Results,
