from otree.api import *
import random
from decimal import Decimal
author = 'Tran Luu'

doc = """
An investment app that gives information about portfolio to test the ability of the players.
The app will take data from an Excel spreadsheet and the players will give money into potfolio with   
"""

class Constants(BaseConstants):
    name_in_url = 'Investment_8p'
    players_per_group = None
    num_rounds = 1
    r_A = 2.5
    r_B = 1.5
    r_C = 1
    r_D = 1
    r_E = 2
    p_A = 1
    p_B = 0.5
    p_C = 0.5
    p_D = 0.5
    p_E = 0.5
    question_A_1 = '-10.5p + r = -8'
    question_A_2 = '1.5p + r = 4'
    question_B_1 = '-9.5p + 0.5r = -4'
    question_B_2 = '2.5p + 0.5r = 2'
    question_C_1 = '-6p + 0.5r = -2.5'
    question_C_2 = '5p + 0.5r = 3'
    question_D_1 = '11p + 0.5r = -5'
    question_D_2 = '5p + 0.5r = 3'
    question_E_1 = '-13r + 0.5p = -5.5'
    question_E_2 = '10r + 0.5p = 6'
    endowment = cu(10)
    order = [1, 2, 3, 4, 5]
    order_2 =['E', 'D', 'C', 'B', 'A']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    invest_A = models.CurrencyField(min=cu(0), max=Constants.endowment, initial=cu(0))
    invest_B = models.CurrencyField(min=cu(0), max=Constants.endowment, initial=cu(0))
    invest_C = models.CurrencyField(min=cu(0), max=Constants.endowment, initial=cu(0))
    invest_D = models.CurrencyField(min=cu(0), max=Constants.endowment, initial=cu(0))
    invest_E = models.CurrencyField(min=cu(0), max=Constants.endowment, initial=cu(0))
    answer_p_A = models.StringField(initial='', blank=True)
    answer_p_B = models.StringField(initial='', blank=True)
    answer_p_C = models.StringField(initial='', blank=True)
    answer_p_D = models.StringField(initial='', blank=True)
    answer_p_E = models.StringField(initial='', blank=True)
    answer_r_A = models.StringField(initial='', blank=True)
    answer_r_B = models.StringField(initial='', blank=True)
    answer_r_C = models.StringField(initial='', blank=True)
    answer_r_D = models.StringField(initial='', blank=True)
    answer_r_E = models.StringField(initial='', blank=True)
    r_p_A = models.FloatField()
    r_p_B = models.FloatField()
    r_p_C = models.FloatField()
    r_p_D = models.FloatField()
    r_p_E = models.FloatField()
#    total_earnings = models.CurrencyField()
    rank = models.IntegerField()
    rate = models.FloatField()



# FUNCTIONS

def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.r_p_A = random.randint(0, 1)
        player.r_p_B = random.randint(0, 1)
        player.r_p_C = random.randint(0, 1)
        player.r_p_D = random.randint(0, 1)
        player.r_p_E = random.randint(0, 1)


def player_payoff(player: Player):
    player.payoff = Constants.endowment
    if player.r_p_A <= Constants.p_A:
        player.payoff += player.invest_A * (Constants.r_A - 1)
    if player.r_p_B <= Constants.p_B:
        player.payoff += player.invest_B * (Constants.r_B - 1)
    if player.r_p_C <= Constants.p_C:
        player.payoff += player.invest_C * (Constants.r_C - 1)
    if player.r_p_D <= Constants.p_D:
        player.payoff += player.invest_D * (Constants.r_D - 1)
    if player.r_p_E <= Constants.p_E:
        player.payoff += player.invest_E * (Constants.r_E - 1)
    return player.payoff


def rank_player(player: Player):
    sorted_players = sorted(
        player.subsession.get_players(),
        key=lambda x: x.payoff
    )
    player.rank = len(player.get_others_in_subsession()) + 1 - sorted_players.index(player)
    player.participant.vars[str(player.participant.id_in_session)+'rank'] = player.rank
    return player.rank


def rate_player(player: Player):
    if player.rank <= 5:
        player.rate = 2.6
    elif player.rank <= 10:
        player.rate = 2.1
    elif player.rank <= 15:
        player.rate = 1.6
    else:
        player.rate = 1.1
    return player.rate

# PAGES

class Instruction(Page):
    pass


class Question(Page):
    form_model = "player"
    form_fields = ['invest_A', 'invest_B', 'invest_C', 'invest_D', 'invest_E',
                   'answer_p_A', 'answer_p_B', 'answer_p_C', 'answer_p_D', 'answer_p_E',
                   'answer_r_A', 'answer_r_B', 'answer_r_C', 'answer_r_D', 'answer_r_E']
    timeout_seconds = 240

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['order2'] = Constants.order_2.copy()
        player.participant.vars[str(player.participant.id_in_session) + 'order'] = \
            random.sample(Constants.order, len(Constants.order))
        return {
                'A1': Constants.question_A_1,
                'A2': Constants.question_A_2,
                'B1': Constants.question_B_1,
                'B2': Constants.question_B_2,
                'C1': Constants.question_C_1,
                'C2': Constants.question_C_2,
                'D1': Constants.question_D_1,
                'D2': Constants.question_D_2,
                'E1': Constants.question_E_1,
                'E2': Constants.question_E_2,
                'order': player.participant.vars[str(player.participant.id_in_session)+'order'],
                'order_2': player.participant.vars['order2']
        }

    @staticmethod
    def error_message(player: Player, values):
        if values['invest_A'] + values['invest_B'] + values['invest_C'] + values['invest_D'] + \
                values['invest_E'] > Constants.endowment:
            return 'The total amount invested must not be larger than the endowment!'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.invest_A = cu(0)
            player.invest_B = cu(0)
            player.invest_C = cu(0)
            player.invest_D = cu(0)
            player.invest_E = cu(0)


class ResultWaitPage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience'

    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.payoff = player_payoff(player)



class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.rank = rank_player(player)
        player.rate = rate_player(player)
        player.participant.vars['invest'+str(player.participant.id_in_session)+'p'] = player.payoff
        player.participant.vars['rank'+str(player.participant.id_in_session)] = player.rank
        player.participant.vars['rate'+str(player.participant.id_in_session)] = player.rate
        return {
            'Earnings': player.participant.vars['invest'+str(player.participant.id_in_session)+'p'],
            'Rank': player.participant.vars['rank'+str(player.participant.id_in_session)],
            'Rate': player.participant.vars['rate'+str(player.participant.id_in_session)]
        }

page_sequence = [
    Instruction,
    Question,
    ResultWaitPage,
    Results
]
