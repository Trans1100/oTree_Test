from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
Quiz for trust game understanding
"""

class Constants(BaseConstants):
    name_in_url = 'Quiz_Trust'
    players_per_group = None
    num_rounds = 1
    sol1 = cu(18)
    sol2 = cu(12)
    sol3 = cu(20)
    sol4 = cu(21)
    sol5 = cu(31)
    sol6 = cu(14)
    sol7 = cu(20)
    sol8 = cu(16)
    factor = 2
    endowment = cu(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer_1 = models.CurrencyField(label='')
    answer_2 = models.CurrencyField(label='')
    answer_3 = models.CurrencyField(label='')
    answer_4 = models.CurrencyField(label='')
    answer_5 = models.CurrencyField(label='')
    answer_6 = models.CurrencyField(label='')
    answer_7 = models.CurrencyField(label='')
    answer_8 = models.CurrencyField(label='')
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
    if player.answer_5 == Constants.sol5:
        player.correct += 1
    if player.answer_6 == Constants.sol6:
        player.correct += 1
    if player.answer_7 == Constants.sol7:
        player.correct += 1
    if player.answer_8 == Constants.sol8:
        player.correct += 1
    return player.correct



# PAGES

class Question(Page):
    form_model = "player"
    form_fields = ['answer_1', 'answer_2', 'answer_3', 'answer_4',
                   'answer_5', 'answer_6', 'answer_7', 'answer_8']


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.correct = player_correct(player)
        player.payoff = player.correct * Constants.factor
        player.participant.vars['Quiz_Trust'+str(player.participant.id_in_session)+'p'] = player.payoff
        return {
            'Earnings': player.payoff,
            'Correct': player.correct
        }

page_sequence = [
    Question,
    Results
]
