from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
Quiz for random leader game understanding
"""

class Constants(BaseConstants):
    name_in_url = 'Quiz_Leader_Random'
    players_per_group = None
    num_rounds = 1
    flat_earning = cu(5)
    flat_invest = cu(4)
    endowment = cu(10)
    sol1 = 1
    sol2 = flat_invest * 3
    sol3 = endowment + flat_earning + cu(11)
    sol4 = endowment - flat_invest + ((flat_invest * 3 - cu(11)) * 1.6)/3
    factor = 2

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    answer_1 = models.IntegerField(label='')
    answer_2 = models.CurrencyField(label='')
    answer_3 = models.CurrencyField(label='')
    answer_4 = models.CurrencyField(label='')
    correct = models.IntegerField()



# FUNCTIONS

def player_correct(player: Player):
    player.correct = 0
    if player.answer_1 == Constants.sol1:
        player.correct += 1
    if player.answer_2 == Constants.sol2:
        player.correct += 1
    if player.answer_3 == Constants.sol3:
        player.correct += 1
    if player.answer_4 == Constants.sol4:
        player.correct += 1
    return player.correct



# PAGES

class Question(Page):
    timeout_seconds = 300
    form_model = "player"
    form_fields = ['answer_1', 'answer_2', 'answer_3', 'answer_4']
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
        player.participant.vars['Leader_Random_Quiz'+str(player.participant.id_in_session)+'p'] = player.payoff
        return {
            'Earnings': player.payoff,
            'Correct': player.correct
        }

page_sequence = [
    Question,
    Results
]
