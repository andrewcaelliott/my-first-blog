from django import forms
from .forms import SimpleChanceForm, ScreenChanceForm, SingleChanceForm
from .chance_utils import parse_probability, format_round_sigfigs
from .utils import getParamDefault

class ChanceCase():
    outcome_text = "hits"
    palette = "default"
    probability = "0.1"
    items = "100 trials"

    def set_params(self, params):
        self.probability = getParamDefault(params, "probability", getParamDefault(params, "number", "0.1"))
        self.items = getParamDefault(params, "items", "1000 trials")
        self.palette = getParamDefault(params, "palette_name", "default")


    def build_probability(self):
        return self.probability.replace(",", "|")

class SimpleChanceCase(ChanceCase):
    form_style = 'smp'
    form = SimpleChanceForm()

class SingleChanceCase(ChanceCase):
    form_style = 'sng'
    form = SingleChanceForm()

    def prepare_form(self):
        self.form.fields["probability"].initial = self.probability
        self.form.fields["probability"].label = "Chances?"
        self.form.fields["items"].initial = self.items
        self.form.fields["items"].label = "Trials?"
        self.form.fields["outcome_text"].initial = self.outcome_text
        self.form.fields["outcome_text"].label = "Outcomes?"
        self.form.fields["form_style"].initial = 'sng'
        self.form.fields['form_style'].widget = forms.HiddenInput()
        return self.form


class ScreenChanceCase(ChanceCase):
    form_style = 'scr'
    form = ScreenChanceForm()
    outcome_text = "true pos|false pos|false neg"
    palette = "screen"
    sensitivity = "0.9"
    specificity = "0.9"

    def set_params(self, params):
        self.probability = getParamDefault(params, "probability", getParamDefault(params, "number", "0.1"))
        self.sensitivity = getParamDefault(params, "probability_a", getParamDefault(params, "number", "0.9"))
        self.specificity = getParamDefault(params, "probability_b", getParamDefault(params, "number", "0.9"))
        self.items = getParamDefault(params, "items", "10000 trials")
        self.palette = getParamDefault(params, "palette_name", "screen")
        self.outcome_text = getParamDefault(params, "outcome_text", self.outcome_text)

    def prepare_form(self):
        self.form.fields["probability"].initial = self.probability
        self.form.fields["probability"].label = "Base Incidence?"
        self.form.fields["probability_a"].initial = self.sensitivity
        self.form.fields["probability_a"].label = "Sensitivity?"
        self.form.fields["probability_b"].initial = self.specificity
        self.form.fields["probability_b"].label = "Specificity?"
        self.form.fields["items"].initial = self.items
        self.form.fields["items"].label = "Cases?"
        self.form.fields["outcome_text"].initial = self.outcome_text
        self.form.fields["outcome_text"].label = "Outcomes?"
        self.form.fields["form_style"].initial = 'scr'
        self.form.fields['form_style'].widget = forms.HiddenInput()
        self.form.fields["palette_name"].initial = self.palette
        return self.form

    

    def build_probability(self):
        i = parse_probability(self.probability)
        p = parse_probability(self.sensitivity)
        n = parse_probability(self.specificity)
        print(i,p,n)
        ptp = i * p
        pfn = i * (1 - p)
        pfp = (1 - i) * (1 - n)
        ptn = (1 - i) * n
        print(ptp, pfp, pfn)
        # return '%s | %s | %s | %s' % (ptp, pfp, pfn, ptn)
        formatted = tuple((format_round_sigfigs(prob,4) for prob in (ptp, pfp, pfn)))
        print("Formatted=", formatted)
        return '%s | %s | %s ' % (formatted)

