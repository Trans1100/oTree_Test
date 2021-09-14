from os import environ


SESSION_CONFIGS = [
    dict(
        name='Test_20p', app_sequence=['Quiz_Investment',
                                       'Investment_20p',
                                       'Quiz_Trust',
                                       'Trust_Game_20p_1st',
                                       'Quiz_Leader_Random',
                                       'Leader_20p_1st',
                                       'Trust_Game_20p_2nd',
                                       'Quiz_Leader_Elected',
                                       'Leader_20p_2nd',
                                       'Trust_Game_20p_3rd',
                                       'Leader_20p_3rd',
                                       'Trust_Game_20p_4th',
                                       'Leader_20p_4th',
                                       'Trust_Game_20p_5th',
                                       'Leader_20p_5th',
                                       'Trust_Game_20p_6th',
                                       'Leader_20p_6th',
                                       'Survey'], num_demo_participants=20
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'
POINTS_DECIMAL_PLACES = 2
ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '8556379831478'

INSTALLED_APPS = ['otree']
