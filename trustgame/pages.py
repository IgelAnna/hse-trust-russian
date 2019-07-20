from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass
   # form_model = 'player'
   # form_fields = ['q1']
    def is_displayed(self):
        return self.round_number == 1


class Question(Page):
    form_model = 'player'
    form_fields = ['q1']
    form_fields = ['q2']
    form_fields = ['q3']
    
    def is_displayed(self):
        return self.round_number == 1
    



class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    body_text = 'Пожалуйста, ожидайте другого участника!'
    title_text = 'Пожалуйста, подождите!'

class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * self.subsession.multiplier
        tripled_amount_with_endowment = tripled_amount + 10

        return {
                'tripled_amount_with_endowment': tripled_amount_with_endowment,
                'tripled_amount': tripled_amount,
                'prompt': 'Пожалуйста, введите число от 0 до {}'.format(tripled_amount)}


class ResultsWaitPage(WaitPage):
    body_text = 'Пожалуйста, ожидайте другого участника!'
    title_text = 'Пожалуйста, подождите!'
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * self.subsession.multiplier
        }


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
