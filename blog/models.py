from django.db import models
from django.utils import timezone
from random import sample
from math import log10
from pint import UnitRegistry,UndefinedUnitError
from .fixer_io import convertToCurrency
from .convert import convertToDefault
from .convert import AMOUNT_UNITS
from .config import all_unit_choices
from .config import MEASURE_CHOICES,MULTIPLE_CHOICES,MULTIPLE_INVERSE
from .utils import num,sigfigs,getScaleFactor,output,currency_output,closeEnoughNumberFact,bracketNumber,getMultiple,country_code_list,resolve_country_code
ureg = UnitRegistry()
Q_=ureg.Quantity
UNIT_CHOICES = all_unit_choices


class NumberQuery(models.Model):

    text       = models.TextField()
    title      = models.CharField(max_length=50)
    number      = models.CharField(max_length=40)
    magnitude = models.CharField(max_length=20)
    scale = models.IntegerField()
    measure  = models.CharField(max_length=2, choices=MEASURE_CHOICES, default="co")
    location = models.CharField(max_length=2,choices=country_code_list(), default="GB")
    value    = models.DecimalField(max_digits=30, decimal_places=10)
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES, default="U")
    unit     = models.CharField(max_length=10, choices=UNIT_CHOICES)
    target_unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    subject = models.TextField()

    def setUnitChoices(self, choices):
        unit = models.CharField(max_length=10, choices=choices)

    def setScaleFactor(self):
        scale, factor = getScaleFactor(self.multiple)
        return factor

    def normalise(self):
        self.scale, factor = getScaleFactor(self.multiple)
        value = num(self.magnitude)
        while abs(value) > 1000:
            value = value / 1000
            self.scale = self.scale + 3
        while abs(value) < 1 and self.scale>=0:
            value = value * 1000
            self.scale = self.scale - 3
        self.multiple = MULTIPLE_INVERSE[self.scale]
        self.magnitude = str(value) 

    def getBrackets(self):
        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans = 0            
        n = convertToDefault(num_ans, self.unit)

        if n>1000000000000000000000:
            temp_scale = 21
            n = n / 1000000000000000000000.0
        elif n>1000000000000000000:
            temp_scale = 18
            n = n / 1000000000000000000.0
        elif n>1000000000000000:
            temp_scale = 15
            n = n / 1000000000000000.0
        elif n>1000000000000:
            temp_scale = 12
            n = n / 1000000000000.0
        elif n>1000000000:
            temp_scale = 9
            n = n / 1000000000.0
        elif n>1000000:
            temp_scale = 6
            n = n / 1000000.0
        elif n>1000:
            temp_scale = 3
            n = n / 1000.0
        else:
            temp_scale = 0

        print("Bracketing:", str(n), temp_scale, self.get_measure_display())
        brackets = bracketNumber(NumberFact, str(n), temp_scale, self.get_measure_display())
        print(brackets)
        return {"above":brackets[0], "below":brackets[1]}

    def getCloseMatches(self):
        #todo first convert to default unit

        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans = 0            
        n = convertToDefault(num_ans, self.unit)

        if n>1000000000000:
            temp_scale = 12
            n = n / 1000000000000.0
        elif n>1000000000:
            temp_scale = 9
            n = n / 1000000000.0
        elif n>1000000:
            temp_scale = 6
            n = n / 1000000.0
        elif n>1000:
            temp_scale = 3
            n = n / 1000.0
        else:
            temp_scale = 0

        closeEnough = closeEnoughNumberFact(NumberFact, n, temp_scale, 0.1, self.get_measure_display())
        closeMatches = []
        for fact in closeEnough:
            match = {"text":fact.render_folk_long, "link":fact.link}
            closeMatches.append(match)
#            closeMatches.append(":".join([fact.render,fact.link]))
#        closeMatches.append(" ".join([str(self.magnitude), str(scale), str(self.fields)]))
        if n==0:
            closeMatches.append({"text":"Invalid input", "link":"."})
#        elif len(closeMatches)==0:
#            closeMatches.append({"text":"No close matches found", "link":"."})
        return closeMatches

    def getComparisons(self, references):
        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans=0
        n = convertToDefault(num_ans, self.unit)
        comparisons = []
        if (n == 0):
            comparisons.append({"factor":0, "render":"Invalid input"})
        for reference in references:
            fact = NumberFact.objects.get(title=reference[0])
            factNumber = float(fact.value)*10**fact.scale
            comparisonNumber = n  / factNumber
            if (comparisonNumber <= 1000000) and (comparisonNumber >= 0.0001):
                times = sigfigs(comparisonNumber,4);
                fraction = sigfigs(1/comparisonNumber,3);
                percent = sigfigs(times,6) * 100;
                if comparisonNumber >=0.32:
                    if comparisonNumber >=10:
                        comparisonRender = reference[1].replace(".2f", ".0f").format(times=times, fraction=fraction, percent=percent)
                    else:
                        comparisonRender = reference[1].format(times=times, fraction=fraction, percent=percent)
                #to do? 2/3, 3/4, 2/5, 3/5, 4/5
                elif comparisonNumber >=0.1 or len(reference)<4:
                    comparisonRender = reference[2].format(times=times, fraction=fraction, percent = percent)
                else:
                    comparisonRender = reference[3].format(times=times, fraction=fraction, percent = percent)
                comparison ={"factor":comparisonNumber, "render": comparisonRender+" ("+fact.render_number+")", "link":fact.link}
                comparisons.append(comparison)
        return comparisons

    def getDynamicComparisons(self, factpacks, year=None):
        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans=0
        n = num_ans
#        n = convertToDefault(num_ans, self.unit, year=year)
        comparisons = []
        if (n == 0):
            comparisons.append({"factor":0, "render":"Invalid input"})
        for factpack in factpacks:
            fact = factpack[0]
            factNumber = float(fact.value)*10**fact.scale
            comparisonNumber = n  / factNumber
            if (comparisonNumber <= 10000000) and (comparisonNumber >= 0.0000001):
                times = sigfigs(comparisonNumber,6);
                fraction = sigfigs(1/comparisonNumber,3);
                percent = sigfigs(times,6) * 100;
                if comparisonNumber >=0.5:
                    comparisonRender = factpack[1].format(times=times, fraction=fraction, percent=percent)
                elif comparisonNumber >=0.1 or len(factpack)<4:
                    comparisonRender = factpack[2].format(times=times, fraction=fraction, percent = percent)
                else:
                    comparisonRender = factpack[3].format(times=times, fraction=fraction, percent = percent)
                comparison ={"factor":comparisonNumber, "render": comparisonRender.replace(" i ", " "), "link":None}
                comparisons.append(comparison)
        return comparisons

    def getConversions(self, conversions, year=None):
        conversion_answers = []
        self.normalise()
        num_ans = num(self.magnitude) * self.setScaleFactor()
        print(self.measure)
        if (self.measure.find("a")==0):
            for conversion in conversions:
                n = convertToCurrency(num_ans, self.unit, conversion, year=year)
                mag = round(n,2)
                conversion_answers.append(" ".join([currency_output(mag), conversion]))
        else:
            quantity = Q_(" ".join([str(num_ans), self.unit]))
            for conversion in conversions:
                conv_q = quantity.to(conversion)
                mag = sigfigs(conv_q.magnitude,6)
                conversion_answers.append(" ".join([output(mag), conversion]))
        return conversion_answers


    
    def _display(self):
        line = " ".join([self.title,":",self.magnitude, self.get_multiple_display(), self.unit]).replace(" unit ", " ").replace(" - ", " ")
        line=(line+".").replace(" i.", ".")[:-1]
        return line

    def __str__(self):
        return self.title        

    render = property(_display)

class NumberFact(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    date = models.DateTimeField(null = True)
    location = models.TextField()
    magnitude = models.CharField(max_length=20)
    scale = models.IntegerField()
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES)
    location = models.CharField(max_length=100)
#    value = models.DecimalField(max_digits=30, decimal_places=10)
    value = models.FloatField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    measure = models.CharField(max_length=1, choices=MEASURE_CHOICES)
    subject = models.TextField()
    permlink = models.SlugField(db_index=True, unique=True)

    def display_folk_number(self, mag, mult, unit, measure):
        mag = str(sigfigs(num(self.magnitude),4))
        if (measure == "e"):
            measure = "extent"

        if measure.find("extent")>=0 and self.scale>0:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-3, measure=measure, unit="km", multiple=getMultiple(self.scale-3))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("extent")>=0 and self.scale==0 and num(self.magnitude)<1:
            newnumber = NumberFact(magnitude=str(sigfigs(num(self.magnitude)*1000,4)), scale=self.scale, measure=measure, unit="mm", multiple=getMultiple(self.scale))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude)*1000,4))

        if measure.find("extent")>=0 and self.scale<0 and num(self.magnitude)<1000:
            newnumber = NumberFact(magnitude=str(sigfigs(num(self.magnitude),4)), scale=self.scale+3, measure=measure, unit="mm", multiple=getMultiple(self.scale+3))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("area")>=0 and self.scale>=6:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-6, measure=measure, unit="km^2", multiple=getMultiple(self.scale-6))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("volume")>=0 and self.scale>=9:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-9, measure=measure, unit="km^3", multiple=getMultiple(self.scale-9))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure=="mass" and self.scale==0 and num(self.magnitude)<1:
            newnumber = NumberFact(magnitude=str(sigfigs(num(self.magnitude)*1000,4)), scale=self.scale, measure=measure, unit="g", multiple=getMultiple(self.scale))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude)*1000,4))

        if measure.find("mass")>=0 and self.scale<0 and num(self.magnitude)<1000:
            newnumber = NumberFact(magnitude=str(sigfigs(num(self.magnitude),4)), scale=self.scale+3, measure=measure, unit="g", multiple=getMultiple(self.scale+3))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure == "amount" and unit.find("USD")>=0:
            unit = "$"
        if measure == "amount" and unit.find("GBP")>=0:
            unit = "£"
                
        if measure.find("energy")>=0 and self.scale>0:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-3, measure=measure, unit="kJ", multiple=getMultiple(self.scale-3))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("energy")>=0 and self.scale>3:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-6, measure=measure, unit="MJ", multiple=getMultiple(self.scale-6))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("energy")>=0 and self.scale>6:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-9, measure=measure, unit="GJ", multiple=getMultiple(self.scale-9))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("energy")>=0 and self.scale>9:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-12, measure=measure, unit="TJ", multiple=getMultiple(self.scale-12))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if measure.find("energy")>=0 and self.scale>12:
            newnumber = NumberFact(magnitude=mag, scale=self.scale-15, measure=measure, unit="TJ", multiple=getMultiple(self.scale-15))
            mult = newnumber.multiple
            unit = newnumber.unit
            mag = str(sigfigs(num(self.magnitude),4))

        if mult=="thousand":
            newnumber = NumberFact(magnitude=str(sigfigs(num(self.magnitude)*1000,4)), multiple="unit", measure=measure, unit=unit)
            mag = str(sigfigs(num(self.magnitude)*1000,4))
            if len(mag)>3:
                mag = mag[:-3]+","+mag[-3:]
            mult = "unit"

        if measure=="count":
            if unit == "people":
                unit = ""
            else:
                unit = " "+unit
            response = "".join([mag, mult, unit])
            response = response.replace("billion ", "bn ").replace("thousand ", "th ").replace("Population", "Pop.")
        else:
            if unit == "$" or unit == "£":
                if mag[0] !="-":
                    response = "".join([unit, mag, mult])
                else:
                    response = "".join(["-", unit, mag.replace("-",""), mult])
            else:    
                response = " ".join([mag, mult, unit])
        return response.replace("unit", "").replace(" unknown", "").replace(" - ", " ").replace("  "," ")

    def normalise(self, round_to=None):
        value = num(self.magnitude)
        while abs(value) > 1000:
            value = value / 1000
            self.scale = self.scale + 3
        while abs(value) < 1 and self.scale>=0:
            value = value * 1000
            self.scale = self.scale - 3
        if round_to:
            value = round(value, round_to)
        self.multiple = MULTIPLE_INVERSE[self.scale]
        self.magnitude = str(value) 

    def getConversions(self, conversions, year=None):
        conversion_answers = []
        self.normalise()
        num_ans = num(self.magnitude) * 10** self.scale
        if (self.measure.find("amount")==0):
            if self.unit.find("/")>0:
                self.unit = self.unit[:self.unit.find("/")]
#        if self.unit in AMOUNT_UNITS: 
            for conversion in conversions:
                n = convertToCurrency(num_ans, self.unit, conversion, year=year)
                mag = round(n,2)
                nf = NumberFact(magnitude=mag / 10** self.scale, multiple=self.multiple, scale=self.scale, unit=conversion, measure = self.measure, title = self.title)
                nf.normalise()
                nf.value = num(nf.magnitude)
#                conversion_answers.append(" ".join([currency_output(mag), conversion]))
                conversion_answers.append(nf)
        else:
            quantity = Q_(" ".join([str(num_ans), self.unit]))
            for conversion in conversions:
                conv_q = quantity.to(conversion)
                mag = sigfigs(conv_q.magnitude,6)
#                conversion_answers.append(" ".join([output(mag), conversion]))
                nf = NumberFact(magnitude=mag, multiple=self.multiple, scale=self.scale, unit=conversion, measure = self.measure, title = self.title)
                conversion_answers.append(nf)
        return conversion_answers


    def title_plus(self):
        if self.date != None:
            return self.title+" ("+str(self.date.year)+")"
        else:
            return self.title

    def _display0(self):
        return self.title_plus()

    def _display(self):
        return " ".join([self.title_plus(),":",self.magnitude, self.get_multiple_display(), self.unit]).replace(" unit ", " ").replace(" - ", " ").replace("iter", "itre")

    def _display2(self):
        return "".join([self.title_plus()," (",self.magnitude, " ", self.get_multiple_display(), " ",self.unit,")" ]).replace(" unit ", " ").replace(" - ", " ").replace("thousand", "th").replace("Population", "Pop.").replace("iter", "itre")

    def _display_folk(self):
        return "".join([self.title_plus()," (",
            self.display_folk_number(self.magnitude, self.get_multiple_display(), self.unit, self.measure),
            ")" ]).replace("Population", "Pop.").replace("thousand ", "th ")

    def _display_number(self):
        return "".join([
            self.display_folk_number(self.magnitude, self.get_multiple_display(), self.unit, self.measure)]).replace("thousand ", "th ").replace("iter", "itre")

    def _display_equals(self):
        title = self.title.replace("in "+resolve_country_code(self.location),"")
        title = title.replace("of "+resolve_country_code(self.location),"").replace("to "+resolve_country_code(self.location),"").replace("from "+resolve_country_code(self.location),"")
        return "".join([title," = ",
            self.display_folk_number(self.magnitude, self.get_multiple_display(), self.unit, self.measure)]).replace("thousand ", "th ").replace(" (2000)", "").replace(" people", "")

    def _display_folk_long(self):
        return "".join([self.title_plus()," (",
            self.display_folk_number(self.magnitude, self.get_multiple_display(), self.unit, self.measure),
            ")" ])

    def _link(self):
        return "/fact/"+self.permlink

    def _linkasunit(self):
        return "/factasunit/"+self.permlink

    def __str__(self):
        return self.title        

    render0 = property(_display0)
    render = property(_display)
    render2 = property(_display2)
    render_folk = property(_display_folk)
    render_number = property(_display_number)
    render_folk_long = property(_display_folk_long)
    render_equals = property(_display_equals)
    link = property(_link)
    linkasunit = property(_linkasunit)

class Comparison(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    numberFact1 = models.ForeignKey('NumberFact', default=0, related_name="primary")
    numberFact2 = models.ForeignKey('NumberFact', default=0)
    difference = models.DecimalField(max_digits=30, decimal_places=10)
    ratio = models.DecimalField(max_digits=30, decimal_places=20)

    def __str__(self):
        return self.title        

    def _display(self):
        return " ".join([self.title,":",self.numberFact1, self.numberFact2])

    def _display_folk(self):
        return " ".join([self.title,":",self.numberFact1, self.numberFact2])

    render = property(_display)
    render_folk = property(_display_folk)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    #text = models.TextField()
    numberFact = models.ForeignKey('NumberFact', default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ChanceQuery(models.Model):

    probability    = models.CharField(max_length=150)
    probability_a    = models.CharField(max_length=150)
    probability_b    = models.CharField(max_length=150)
    # chance_function    = models.CharField(max_length=150)
    item_text = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    exposed_items    = models.IntegerField()
    repetition_text       = models.CharField(max_length=200)
    repetitions = models.CharField(max_length=200)
    exposed_repetitions    = models.IntegerField()
    outcome_count = models.IntegerField()
    outcome_text       = models.CharField(max_length=200)
    repeat_mode = models.CharField(max_length=10, choices=[("repeats","repeats"), ("removes","removes")])
    calc_target = models.CharField(max_length=10, choices=[("probability", "probability"), ("items", "items"), ("repetitions", "repetitions"), ("hits", "hits")])
    palette_name = models.CharField(max_length=10)
    form_style = models.CharField(max_length=3)

class ChanceFact(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    probability    = models.CharField(max_length=150)
    # chance_function    = models.CharField(max_length=150)
    item_text       = models.CharField(max_length=200)
    exposed_items    = models.IntegerField()
    repetition_text       = models.CharField(max_length=200)
    exposed_repetitions    = models.IntegerField()
    outcome_text       = models.CharField(max_length=200)
    repeat_mode = models.CharField(max_length=10, choices=[("repeats","repeats"), ("removes","removes")])
    permlink = models.SlugField(db_index=True, unique=True)
    fact_type = models.CharField(max_length=10, choices=[("fact","fact"), ("example","example"), ("proportion","proportion")])
    page_type = models.CharField(max_length=10, choices=[("sng","sng"), ("smp","smp"), ("adv","adv"), ("scr","scr")])

    def _display_folk(self):
        if self.fact_type == 'fact':
            return "".join(["The chance of ", self.title, " is ", self.probability])
        elif self.fact_type == 'example':
            return "".join(["An example of ", self.title, " using ", self.probability])


    render_folk = property(_display_folk)
