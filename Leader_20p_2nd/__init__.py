from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
A leader game with random leader. All start with 10 cu, the leader would have a flat earning 
and the members would have to 
invest a flat invest. The leader then can invest
 all the money from the member or embellish some for themselves. 
"""


class Constants(BaseConstants):
    name_in_url = 'Leader_20p_2nd'
    players_per_group = 4
    num_rounds = 1
    endowment = cu(10)
    flat_earning = cu(5)
    flat_invest = cu(2)
    prob = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50',
            '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
    about = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9', '10', '11', '12']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    invest = models.CurrencyField(initial=cu(0))
    take_for_myself = models.CurrencyField(initial=cu(0))
    rate = models.FloatField(initial=0)
    leader = models.IntegerField()

class Player(BasePlayer):
    rate = models.FloatField()
    rank = models.IntegerField()
    role_player = models.CharField()
    ranking = models.IntegerField(initial=0)
    invest = models.CurrencyField(choices=currency_range(cu(0), Constants.flat_invest*3, cu(1)), initial=cu(0))
    take_for_myself = models.CurrencyField(choices=currency_range(cu(0), Constants.flat_invest*3, cu(1)), initial=cu(0))
    id_A = models.IntegerField()
    id_B = models.IntegerField()
    id_C = models.IntegerField()
    choice_A = models.IntegerField(choices=[1, 2, 3])
    choice_B = models.IntegerField(choices=[1, 2, 3])
    choice_C = models.IntegerField(choices=[1, 2, 3])
    sent_A = models.CurrencyField()
    sent_B = models.CurrencyField()
    sent_C = models.CurrencyField()
    sent_back_A = models.CurrencyField()
    sent_back_B = models.CurrencyField()
    sent_back_C = models.CurrencyField()
#    trust_A = models.StringField()
#    trust_B = models.StringField()
#    trust_C = models.StringField()
    rate_A = models.FloatField()
    rate_B = models.FloatField()
    rate_C = models.FloatField()
    about_A = models.CurrencyField(choices=Constants.about)
    about_B = models.CurrencyField(choices=Constants.about)
    about_C = models.CurrencyField(choices=Constants.about)
    prob_A = models.StringField(choices=Constants.prob)
    prob_B = models.StringField(choices=Constants.prob)
    prob_C = models.StringField(choices=Constants.prob)

#FUNCTIONS


def creating_group(subsession: Subsession):
    group_1 = []
    group_2 = []
    group_3 = []
    group_4 = []
    group_5 = []
    matrix = []
    for p in subsession.get_players():
        p.rank = p.participant.vars['rank'+str(p.participant.id_in_session)]
        if p.rank in [2, 8, 13, 18]:
            group_1.append(p)
        elif p.rank in [1, 6, 12, 19]:
            group_2.append(p)
        elif p.rank in [5, 9, 11, 16]:
            group_3.append(p)
        elif p.rank in [3, 10, 14, 17]:
            group_4.append(p)
        else:
            group_5.append(p)
    matrix.append(group_1)
    matrix.append(group_2)
    matrix.append(group_3)
    matrix.append(group_4)
    matrix.append(group_5)
    subsession.set_group_matrix(matrix)


def choose_leader(group: Group):
    player_score = []
    leader_list = []
    for player in group.get_players():
        for other_player in player.get_others_in_group():
            if other_player.participant.id_in_session ==\
                    player.participant.vars['round2' + str(player.participant.id_in_session) + 'id'][0]:
                other_player.ranking += player.choice_A
            elif other_player.participant.id_in_session ==\
                    player.participant.vars['round2' + str(player.participant.id_in_session) + 'id'][1]:
                other_player.ranking += player.choice_B
            else:
                other_player.ranking += player.choice_C
    for player in group.get_players():
        player_score.append(player.ranking)
    winning_score = min(player_score)
    for player in group.get_players():
        if player.ranking == winning_score:
            leader_list.append(player.participant.id_in_session)
    group.leader = random.choice(leader_list)
    return group.leader


def player_role(player: Player):
    if player.participant.id_in_session == player.group.leader:
        player.role_player = 'Leader'
    else:
        player.role_player = 'Member'
    return player.role_player


def set_pay_off(player: Player):
    if player.role_player == 'Leader':
        player.payoff = Constants.endowment + Constants.flat_earning + player.group.take_for_myself
    if player.role_player == 'Member':
        player.payoff = Constants.endowment - Constants.flat_invest +\
                        (player.group.invest * (player.group.rate - 1) - player.group.take_for_myself)/3
    return player.payoff



#PAGES

class Instructions(Page):
    pass


class ShufflePage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        creating_group(subsession)


class LeaderChoice(Page):
    form_model = 'player'
    form_fields = ['invest', 'take_for_myself']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'c': Constants.flat_invest,
            '3c': Constants.flat_invest * 3
        }

    @staticmethod
    def error_message(player: Player, values):
        if values['invest'] + values['take_for_myself'] != Constants.flat_invest * 3:
            return 'The total amount must equal the group account'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.invest = cu(0)
            player.take_for_myself = cu(0)

class Leader(Page):

    form_model = 'player'
    form_fields = ['choice_A', 'choice_B', 'choice_C']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        other_player_rate = []
#        other_player_trust = []
        other_player_sent = []
        other_player_sent_back = []
        other_player_id = []
        for other_player in player.get_others_in_group():
            other_player_sent.append(other_player.participant.vars
                                     ['round2' + str(other_player.participant.id_in_session) + 'sent_amount'])
            other_player_sent_back.append(other_player.participant.vars
                                          ['round2' + str(other_player.participant.id_in_session) + 'sent_back_amount'])
#            other_player_trust.append(other_player.participant.vars
#                                      ['round2' + str(other_player.participant.id_in_session)+'t'])
            other_player_rate.append(other_player.participant.vars
                                     ['rate' + str(other_player.participant.id_in_session)])
            other_player_id.append(other_player.participant.id_in_session)
        player.participant.vars['round2' + str(player.participant.id_in_session) + 'id'] =\
            other_player_id
#        player.trust_A = "{:.0f}".format(other_player_trust[0])
#        player.trust_B = "{:.0f}".format(other_player_trust[1])
#        player.trust_C = "{:.0f}".format(other_player_trust[2])
        player.rate_A = other_player_rate[0]
        player.rate_B = other_player_rate[1]
        player.rate_C = other_player_rate[2]
        player.sent_A = other_player_sent[0]
        player.sent_B = other_player_sent[1]
        player.sent_C = other_player_sent[2]
        player.sent_back_A = other_player_sent_back[0]
        player.sent_back_B = other_player_sent_back[0]
        player.sent_back_C = other_player_sent_back[0]
        player.id_A = other_player_id[0]
        player.id_B = other_player_id[1]
        player.id_C = other_player_id[2]
        return {
#            'trustA': "{:.0f}".format(other_player_trust[0]),
#            'trustB': "{:.0f}".format(other_player_trust[1]),
#            'trustC': "{:.0f}".format(other_player_trust[2]),
            'rateA': other_player_rate[0],
            'rateB': other_player_rate[1],
            'rateC': other_player_rate[2],
            'sentA': other_player_sent[0],
            'sentB': other_player_sent[1],
            'sentC': other_player_sent[2],
            'sent_backA': other_player_sent_back[0],
            'sent_backB': other_player_sent_back[1],
            'sent_backC': other_player_sent_back[2]
        }

    @staticmethod
    def error_message(player: Player, values):
        if (values['choice_A'] == values['choice_B']) or \
                (values['choice_A'] == values['choice_C']) or \
                (values['choice_B'] == values['choice_C']):
            return 'Please enter different values!'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.choice_A = 1
            player.choice_B = 1
            player.choice_C = 1


class Trust(Page):
    form_model = 'player'
    form_fields = ['about_A', 'about_B', 'about_C', 'prob_A', 'prob_B', 'prob_C']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        other_player_rate = []
#       other_player_trust = []
        other_player_sent = []
        other_player_sent_back = []
        for other_player in player.get_others_in_group():
            other_player_sent.append(other_player.participant.vars
                                     ['round2' + str(other_player.participant.id_in_session) + 'sent_amount'])
            other_player_sent_back.append(other_player.participant.vars
                                          ['round2' + str(other_player.participant.id_in_session) + 'sent_back_amount'])
#           other_player_trust.append(other_player.participant.vars
#                                     ['round2' + str(other_player.participant.id_in_session)+'t'])
            other_player_rate.append(other_player.participant.vars
                                     ['rate' + str(other_player.participant.id_in_session)])
        return {
#            'trustA': "{:.0f}".format(other_player_trust[0]),
#            'trustB': "{:.0f}".format(other_player_trust[1]),
#            'trustC': "{:.0f}".format(other_player_trust[2]),
            'rateA': other_player_rate[0],
            'rateB': other_player_rate[1],
            'rateC': other_player_rate[2],
            'sentA': other_player_sent[0],
            'sentB': other_player_sent[1],
            'sentC': other_player_sent[2],
            'sent_backA': other_player_sent_back[0],
            'sent_backB': other_player_sent_back[1],
            'sent_backC': other_player_sent_back[2]
        }


class ResultWaitPage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.leader = choose_leader(group)
        for player in group.get_players():
            player.role_player = player_role(player)
            player.rate = player.participant.vars['rate'+str(player.participant.id_in_session)]
            if player.role_player == 'Leader':
                group.invest += player.invest
                group.take_for_myself += player.take_for_myself
                group.rate += player.rate
        for player in group.get_players():
            player.payoff = set_pay_off(player)


class Result(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['round2' + str(player.participant.id_in_session) + 'leader_p'] = player.payoff
        return {
            'earning': player.payoff,
            'role': player.role_player
        }


page_sequence = [
    Instructions,
    ShufflePage,
    LeaderChoice,
    Leader,
    Trust,
    ResultWaitPage,
    Result
    ]






