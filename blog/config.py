extent_references = [
    ('Length of trip from the Earth to the Sun','{times:20.2f} times the distance from the Earth to the Sun','1 / {fraction:20.0f} of the distance from the Earth to the Sun'),
    ('Length of trip from the Earth to the Moon','{times:20.2f} times the distance from the Earth to the Moon','1 / {fraction:20.0f} of the distance from the Earth to the Moon'),
    ('Length of trip around the equator','{times:20.2f} times the distance around the equator','1 / {fraction:20.0f} of the distance around the equator'),
    ('Length of trip from London to New York','{times:20.2f} times the distance from London to New York','1 / {fraction:20.0f} of the distance from London to New York'),
    ('Length of trip from London to Edinburgh','{times:20.2f} times the distance from London to Edinburgh','1 / {fraction:20.0f} of the distance from London to Edinburgh'),
    ('Length of a football pitch','{times:20.2f} football pitches end to end','1 / {fraction:20.0f} as long as a football pitch'),
    ('Length of a London bus','{times:20.2f} London buses end to end','1 / {fraction:20.0f} as long as a London bus'),
    ('Length of an iPhone 6',"{times:20.2f} iPhone 6's end to end",'1 / {fraction:20.0f} as long as an iPhone 6'),
]

count_references = [
    ('Population of World','{times:20.2f} for every person in the world','One for every {fraction:20.0f} people in the world'),
    ('Population of China','{times:20.2f} for every person in China','One for every {fraction:20.0f} people in China'),
    ('Population of United States','{times:20.2f} for every person in the USA','One for every {fraction:20.0f} people in the USA'),
    ('Population of United Kingdom','{times:20.2f} for every person in the UK','One for every {fraction:20.0f} people in the UK'),
]

amount_references = [
    ('GDP of United States','{times:20.2f} times the USA GDP','{percent:20.2f} percent of the USA GDP','1 /{fraction:20.0f} of the USA GDP'),
    ('GDP of United Kingdom','{times:20.2f} times the UK GDP','{percent:20.2f} percent of the UK GDP','1 /{fraction:20.0f} of the UK GDP'),
    ('Wealthiest Person','{times:20.2f} times the wealth of the wealthiest person','{percent:20.2f} percent of the wealth of the wealthiest person','1 /{fraction:20.0f} of the wealth of the wealthiest person'),
    ('Largest Win on a Lottery Ticket','{times:20.2f} times the largest-ever lottery win (per ticket)','{percent:20.2f} percent of the largest-ever lottery win (per ticket)','1 /{fraction:20.0f} of the largest-ever lottery win (per ticket)'),
] 

duration_references = [
    ('age of the universe','{times:20.2f} times the age of the universe','{percent:20.2f} percent of the age of the universe','1 /{fraction:20.0f} of the age of the universe'),
    ('first modern humans','{times:20.2f} times the period since the emergence of the first modern humans','{percent:20.2f} percent of the time since the emergence of the first modern humans','1 /{fraction:20.0f} of the time since the emergence of the first modern humans'),
    ('building of Great Wall of China','{times:20.2f} times the period since the building of the Great Wall of China','{percent:20.2f} percent of the time since the building of the Great Wall of China','1 /{fraction:20.0f} of the time since the building of the Great Wall of China'),
    ('lifespan of Galapagos giant tortoise','{times:20.2f} times the lifespan of a Galapagos giant tortoise','{percent:20.2f} percent of the lifespan of a Galapagos giant tortoise','1 /{fraction:20.0f} of the lifespan of a Galapagos giant tortoise'),
    ('human generation','{times:20.2f} human generations','{percent:20.2f} percent of a human generation','1 /{fraction:20.0f} of a human generation'),
    ('lifespan of rat','{times:20.2f} times the lifespan of a rat','{percent:20.2f} percent of the lifespan of a rat','1 /{fraction:20.0f} of the lifespan of a rat'),
] 

reference_lists = {
    'e': extent_references,
    'c': count_references,
    'a': amount_references,
    'd': duration_references,
}


EXTENT_UNIT_CHOICES= (
        ('km', 'kilometer'),
        ('m', 'meter'),
        ('cm', 'centimeter'),
        ('mm', 'millimeter'),
        ('mile', 'mile'),
        ('yard', 'yard'),
        ('foot', 'foot'),
        ('inch', 'inch'),
    )

COUNT_UNIT_CHOICES= (
        ('i', 'item'),
    )

AMOUNT_UNIT_CHOICES= (
        ('USD', 'US Dollars (USD)'),
        ('AUD', 'Australian Dollar (AUD)'),
        ('CAD', 'Canadian Dollar (CAD)'),
        ('CHF', 'Swiss Franc (CHF)'),
        ('EUR', 'Euros (EUR)'),
        ('GBP', 'UK Pounds (GBP)'),
        ('HKD', 'Hongkong Dollar (HKD)'),
        ('JPY', 'Japanese Yen (JPY)'),
    )

DURATION_UNIT_CHOICES= (
        ('year', 'year'),
        ('month', 'month'),
        ('week', 'week'),
        ('day', 'day'),
        ('hour', 'hour'),
        ('minute', 'minute'),
        ('second', 'second'),
    )

unit_choice_lists = {
    'e': EXTENT_UNIT_CHOICES,
    'c': COUNT_UNIT_CHOICES,
    'a': AMOUNT_UNIT_CHOICES,
    'd': DURATION_UNIT_CHOICES,
}

all_unit_choices = EXTENT_UNIT_CHOICES + COUNT_UNIT_CHOICES + AMOUNT_UNIT_CHOICES + DURATION_UNIT_CHOICES

quip_lists = {
    "e":"It's a long, long way to ...",
    "c":"Let me count ...",
    "a":"There's more to life than money",
    "d":"How many years can a mountain exist?",
}

extent_conversion_targets = [
    ('kilometer'),
    ('metre'),
    ('millimeter'),
    ('mile'),
    ('yard'),
    ('foot'),
    ('inch'),
]

amount_conversion_targets = [
    ('USD'),
    ('AUD'),
    ('CAD'),
    ('CHF'),
    ('EUR'),
    ('GBP'),
    ('HKD'),
    ('JPY'),
]

duration_conversion_targets = [
    ('year'),
    ('month'),
    ('fortnight'),
    ('week'),
    ('day'),
    ('hour'),
    ('minute'),
    ('second'),
]


conversion_target_lists = {
    'e': extent_conversion_targets,
    'a': amount_conversion_targets,
    'd': duration_conversion_targets,
}

conversion_quip_lists = {
    "e":"The long and winding road ...",
    "a":"Money makes the world go round ...",
    "d":"How long has it been ...",
}

MEASURE_CHOICES = (
    ('c', 'count'),
    ('a', 'amount'),
    ('e', 'extent'),
    ('d', 'duration'),
    ('n', 'number'),
)

MULTIPLE_CHOICES = (
    ('U', '-'),
    ('k', 'thousand'),
    ('M', 'million'),
    ('G', 'billion'),
    ('T', 'trillion'),
)
