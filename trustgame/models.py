
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""
import csv


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    with open('trustgame/multipliers.csv') as f:
        multipliers = list(csv.reader(f))[0]
    # number of rounds equal to the set of random numbers in csv
    num_rounds = len(multipliers)

    instructions_template = 'trustgame/instructions.html'

    # Initial amount allocated to each player
    endowment = c(10)


class Subsession(BaseSubsession):
    multiplier = models.FloatField()

    def creating_session(self):
        # We read the set of random numbers from csv and assign to each subsession based on the round number
        self.multiplier = float(Constants.multipliers[self.round_number - 1])
        for g in self.get_groups():
            if g.id_in_subsession % 2 == 1:
                g.treatment = 'X'
            else:
                g.treatment = 'Y'


class Group(BaseGroup):
    treatment = models.StringField()
    sent_amount = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=c(0),
    )

    def sent_back_amount_max(self):
        return self.sent_amount * self.subsession.multiplier

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * self.subsession.multiplier - self.sent_back_amount + 10

        p1.totalProfit = sum(p.payoff for p in p1.in_all_rounds())
        p2.totalProfit = sum(p.payoff for p in p2.in_all_rounds())


class Player(BasePlayer):
    q1 = models.IntegerField(
        label='Если вы в роли Участника А передадите Участнику Б 0 ECU. Какое максимальное количество ECU он сможет Вам передать на следующем этапе?')
    totalProfit = models.CurrencyField()

    def q1_error_message(self, value):
        if value != 0:
            return 'Проверьте Ваш ответ'

    q2 = models.IntegerField(
        label='Если вы в роли Участника А передадите Участнику Б 5 ECU, при передаче эта сумма увеличится в 7 раз и Участник Б передаст Вам 20 ECU. Сколько ECU вы получите по результату раунда?')
    totalProfit = models.CurrencyField()

    def q2_error_message(self, value):
        if value != 25:
            return 'Проверьте Ваш ответ'

    q3 = models.IntegerField(
        label='Сколько ECU получит Участник Б по результатам раунда, описанного в прошлом вопросе?')
    totalProfit = models.CurrencyField()

    def q3_error_message(self, value):
        if value != 25:
            return 'Проверьте Ваш ответ'

    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]
