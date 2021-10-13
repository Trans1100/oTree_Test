from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
Quiz for random leader game understanding
"""

class Constants(BaseConstants):
    name_in_url = 'Quiz_Leader_Elected'
    players_per_group = None
    num_rounds = 1
    flat_earning = cu(8)
    flat_invest = cu(4)
    endowment = cu(10)
    sol1 = 'A'
    factor = 2

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    answer_1 = models.StringField(label='',
                                  widgets=widgets.RadioSelect,
                                  choices=['A', 'B', 'C'])
    correct = models.IntegerField()



# FUNCTIONS

def player_correct(player: Player):
    player.correct = 0
    if player.answer_1 == Constants.sol1:
        player.correct += 1
    return player.correct



# PAGES

class Question(Page):
    timeout_seconds = 240
    form_model = "player"
    form_fields = ['answer_1']
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'remain': Constants.endowment - Constants.flat_invest,
            'total': Constants.flat_invest * 3,
            'earning': Constants.flat_earning
        }

class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.correct = player_correct(player)
        player.payoff = player.correct * Constants.factor
        player.participant.vars['Leader_Elected_Quiz'+str(player.participant.id_in_session)+'p'] = player.payoff
        return {
            'Earnings': player.payoff,
            'Correct': player.correct
        }

page_sequence = [
    Question,
    Results
]
