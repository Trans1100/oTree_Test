import random

from otree.api import *

author = 'Tran_Luu'

doc = """
The survey also serves as a result calculation round 
"""

class Constants(BaseConstants):
    name_in_url = 'Survey'
    players_per_group = None
    num_rounds = 1
#   order = ['1', '2']
#   order = ['1', '2', '3', '4', '5', '6']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
#    random_round = models.StringField()
    pass

class Player(BasePlayer):
    payoff_quiz = models.CurrencyField()
    total = models.CurrencyField()
    money = models.CurrencyField()
    age = models.IntegerField(label='What is your age?', choices=range(15, 76), blank=True)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
        blank=True
    )
    major = models.StringField(
        label='What is your major?',
        blank=True
    )
    GPA = models.FloatField(
        label='What is your GPA?',
        blank=True
    )
    game1 = models.IntegerField(
        label='''
        How important was the amount returned in the Sender-Receiver Game}
               when choosing which group member to vote for?
               ''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    game2 = models.IntegerField(
        label='''How important was the value of Rate when investing
         when choosing which group member to vote for?''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    game3 = models.IntegerField(
        label='''How likely are you to vote in the next election?''',
        choices=[[1, 'Very Unlikely'], [2, 'Unlikely'], [3, 'Do not know'], [4,'Likely'],
                 [5, 'Very Likely']],
        widget=widgets.RadioSelect,
        blank=True
    )
    game4 = models.IntegerField(
        label='''How would you describe yourself politically?''',
        choices=[[1, 'Very Liberal'], [2, 'Liberal'], [3,  'Somewhat Liberal'], [4,  'Neutral/Moderate'],
                 [5, 'Somewhat Conservative'], [6, 'Conservative'], [7, 'Very Conservative']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion1 = models.IntegerField(
        label='''1) Stance on the minimum wage''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion2 = models.IntegerField(
        label='''2) Stance on abortion''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion3 = models.IntegerField(
        label='''3) Stance on union issues''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion4 = models.IntegerField(
        label='''4) Stance on LGTBQ issues''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion5 = models.IntegerField(
        label='''5) Stance on climate/environmental issues''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion6 = models.IntegerField(
        label='''6) Trustworthiness''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion7 = models.IntegerField(
        label='''7) Economic Acumen''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion8 = models.IntegerField(
        label='''8) General Competence''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion9 = models.IntegerField(
        label='''9) Religious commitment''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )
    opinion10 = models.IntegerField(
        label='''10) Personal Integrity''',
        choices=[[1, 'Not At All Important'], [2, 'Low Importance'], [3, 'Neutral'], [4, 'Somewhat Important'],
                 [5, 'Very Important']],
        widget=widgets.RadioSelect,
        blank=True
    )


# FUNCTIONS


# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'GPA']

class Game(Page):
    form_model = 'player'
    form_fields = ['game1', 'game2', 'game3', 'game4']

class Opinion(Page):
    form_model = 'player'
    form_fields = ['opinion1', 'opinion2', 'opinion3', 'opinion4', 'opinion5',
                   'opinion6', 'opinion7', 'opinion8', 'opinion9', 'opinion10']


class WaitResult(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    @staticmethod
    def after_all_players_arrive(group: Group):
#       group.random_round = random.choice(Constants.order)
        for player in group.get_players():
            participant = player.participant
            player.payoff_quiz = participant.vars['Quiz_Investment'+str(player.participant.id_in_session)+'p'] +\
                                 participant.vars['Quiz_Trust'+str(player.participant.id_in_session)+'p'] + \
                                 participant.vars['Leader_Random_Quiz'+str(player.participant.id_in_session)+'p'] + \
                                 participant.vars['Leader_Elected_Quiz'+str(player.participant.id_in_session)+'p']
            player.payoff = participant.vars['invest' + str(participant.id_in_session) + 'p']
            for r in range(1, 7):
#           r = player.group.random_round
                player.payoff += participant.vars['round' + str(r) + str(player.participant.id_in_session) + 'trust_p'] +\
                                 participant.vars['round' + str(r) + str(player.participant.id_in_session) + 'leader_p']
            player.total = player.payoff + player.payoff_quiz + cu(50)
            player.money = player.total * 0.1


class Result(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'payoff_quiz': player.payoff_quiz,
            'total': player.total
        }



page_sequence = [
    Demographics,
    Game,
    Opinion,
    WaitResult,
    Result]
