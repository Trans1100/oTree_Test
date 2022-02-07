from otree.api import *
from decimal import Decimal

author = 'Tran_Luu'

doc = """
A trust game with two rounds
"""


class Constants(BaseConstants):
    name_in_url = 'Trust_Game_20p_6th'
    players_per_group = 2
    num_rounds = 2
    endowment = cu(10)
    multiplication_factor = 3



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_back_amount = models.CurrencyField(min=cu(0))
    sent_amount = models.CurrencyField(min=cu(0), max=Constants.endowment)


class Player(BasePlayer):
    earn_sender = models.CurrencyField()
    earn_receiver = models.CurrencyField()
    final_payoff = models.CurrencyField()


#FUNCTIONS


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.get_group_matrix()
        new_structure = [[7, 1], [6, 3], [17, 10], [15, 12], [5, 16],
                         [18, 9], [11, 13], [14, 19], [4, 2], [8, 20]]
        subsession.set_group_matrix(new_structure)
        subsession.get_group_matrix()
    if subsession.round_number == 2:
        subsession.get_group_matrix()
        new_structure = [[1, 7], [3, 6], [10, 17], [12, 15], [16, 5],
                         [9, 18], [13, 11], [19, 14], [2, 4], [20, 8]]
        subsession.set_group_matrix(new_structure)
        subsession.get_group_matrix()

def sent_back_amount_error_message(group: Group, value):
    if value > Constants.endowment + group.sent_amount * Constants.multiplication_factor:
        return 'Please enter within the amount of money being sent to you'

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
    p2.payoff = Constants.endowment + group.sent_amount * Constants.multiplication_factor -\
                group.sent_back_amount
    p1.earn_sender = p1.payoff
    p2.earn_receiver = p2.payoff




def total_payoff(player: Player):
    player.final_payoff = sum([p.payoff for p in player.in_all_rounds()])/2.0
    return player.final_payoff


#PAGES
class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']
    timeout_seconds = 300

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.sent_amount = cu(0)
        


class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return {
            'tripled_amount': group.sent_amount * Constants.multiplication_factor,
            'send_back_total': Constants.endowment + group.sent_amount * Constants.multiplication_factor
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.sent_back_amount = 0
        player.participant.vars['round6' + str(player.participant.id_in_session) + 'sent_amount'] =\
            player.group.sent_amount
        player.participant.vars['round6' + str(player.participant.id_in_session) + 'sent_back_amount'] =\
            player.group.sent_back_amount

class WaitForP1(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'



class ResultsWaitPage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


class Results(Page):
    pass


class ResultsSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        player_1 = player.in_round(1)
        player_2 = player.in_round(2)
        player.final_payoff = total_payoff(player)
        player.participant.vars['round6' + str(player.participant.id_in_session) + 'trust_p'] =\
            player.final_payoff
        return {
            'total_payoff': player.final_payoff,
            'payoff_1': player_1.payoff,
            'payoff_2': player_2.payoff
        }


page_sequence = [
    Welcome,
    Send,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results,
    ResultsSummary
]
