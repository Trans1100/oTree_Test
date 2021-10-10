from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
Quiz for investment game understanding
"""

class Constants(BaseConstants):
    name_in_url = 'Quiz_Investment'
    players_per_group = None
    num_rounds = 1
    sol1 = cu(30)
    sol2 = cu(0)
    sol3 = cu(24)
    sol4 = cu(12)
    sol5 = 'A'
    factor = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer_1 = models.CurrencyField(label='')
    answer_2 = models.CurrencyField(label='')
    answer_3 = models.CurrencyField(label='')
    answer_4 = models.CurrencyField(label='')
    answer_5 = models.StringField(label='',
                                  widgets=widgets.RadioSelect,
                                  choices=['A', 'B'])
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
    return player.correct



# PAGES

class Instruction(Page):
    pass

class Question(Page):
    timeout_seconds = 300
    form_model = "player"
    form_fields = ['answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5']


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.correct = player_correct(player)
        player.payoff = player.correct * Constants.factor
        player.participant.vars['Quiz_Investment'+str(player.participant.id_in_session)+'p'] = player.payoff
        return {
            'Earnings': player.payoff,
            'Correct': player.correct
        }

page_sequence = [
    Instruction,
    Question,
    Results
]
