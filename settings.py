from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'trust',
        'display_name': "Trust Game",
        'num_demo_participants': 2,
        'app_sequence': ['trustgame'],
        'use_browser_bots': False,
    },
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'RUB'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ROOMS = [{'name': 'hse', 'display_name': 'hse'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4jozfsc+t7#v==^z_&2y7511qh1$8wkbp&*x34=j^lu#s3ns6u'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
