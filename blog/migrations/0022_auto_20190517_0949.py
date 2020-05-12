# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20161111_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChanceFact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=50)),
                ('probability', models.CharField(max_length=50)),
                ('item_text', models.CharField(max_length=200)),
                ('exposed_items', models.IntegerField()),
                ('repetition_text', models.CharField(max_length=200)),
                ('exposed_repetitions', models.IntegerField()),
                ('outcome_text', models.CharField(max_length=200)),
                ('permlink', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChanceQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('probability', models.CharField(max_length=50)),
                ('item_text', models.CharField(max_length=200)),
                ('exposed_items', models.IntegerField()),
                ('repetition_text', models.CharField(max_length=200)),
                ('exposed_repetitions', models.IntegerField()),
                ('outcome_count', models.IntegerField()),
                ('outcome_text', models.CharField(max_length=200)),
                ('calc_target', models.CharField(max_length=10, choices=[('probability', 'probability'), ('items', 'items'), ('repetitions', 'repetitions'), ('hits', 'hits')])),
            ],
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='measure',
            field=models.CharField(max_length=1, choices=[('co', 'count'), ('am', 'amount'), ('ex', 'extent'), ('du', 'duration'), ('nu', 'number'), ('ma', 'mass'), ('ar', 'area'), ('vo', 'volume'), ('en', 'energy'), ('ca', 'capacity')]),
        ),
        migrations.AlterField(
            model_name='numberfact',
            name='unit',
            field=models.CharField(max_length=10, choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound'), ('J', 'joule'), ('erg', 'erg'), ('kWh', 'Kilowatt Hour'), ('MWh', 'Megawatt Hour'), ('GWh', 'Gigawatt Hour'), ('TWh', 'Terawatt Hour'), ('PWh', 'Petawatt Hour'), ('BTU', 'British Thermal Unit'), ('cal', 'Thermochemical calorie'), ('kcal', 'Food Calorie'), ('mL', 'millilitre'), ('L', 'litre'), ('kL', 'Kilolitre'), ('ML', 'Megalitre'), ('imperial_pint', 'imperial pint'), ('imperial_gallon', 'imperial gallon'), ('pint', 'US pint'), ('gallon', 'US gallon')]),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='location',
            field=models.CharField(max_length=2, default='GB', choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BR', 'Brazil'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CD', 'Democratic Republic of the Congo'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('TL', 'East Timor'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('PF', 'French Polynesia'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('CI', 'Ivory Coast'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KV', 'Kosovo'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Laos'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macau'), ('MK', 'Macedonia'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('KP', 'North Korea'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('CG', 'Republic of the Congo'), ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('SH', 'Saint Helena; Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('KR', 'South Korea'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syria'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('VI', 'United States Virgin Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis and Futuna Islands'), ('WB', 'West Bank'), ('EH', 'Western Sahara'), ('World', 'World'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='measure',
            field=models.CharField(max_length=2, default='co', choices=[('co', 'count'), ('am', 'amount'), ('ex', 'extent'), ('du', 'duration'), ('nu', 'number'), ('ma', 'mass'), ('ar', 'area'), ('vo', 'volume'), ('en', 'energy'), ('ca', 'capacity')]),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='target_unit',
            field=models.CharField(max_length=10, choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound'), ('J', 'joule'), ('erg', 'erg'), ('kWh', 'Kilowatt Hour'), ('MWh', 'Megawatt Hour'), ('GWh', 'Gigawatt Hour'), ('TWh', 'Terawatt Hour'), ('PWh', 'Petawatt Hour'), ('BTU', 'British Thermal Unit'), ('cal', 'Thermochemical calorie'), ('kcal', 'Food Calorie'), ('mL', 'millilitre'), ('L', 'litre'), ('kL', 'Kilolitre'), ('ML', 'Megalitre'), ('imperial_pint', 'imperial pint'), ('imperial_gallon', 'imperial gallon'), ('pint', 'US pint'), ('gallon', 'US gallon')]),
        ),
        migrations.AlterField(
            model_name='numberquery',
            name='unit',
            field=models.CharField(max_length=10, choices=[('km', 'kilometer'), ('m', 'meter'), ('cm', 'centimeter'), ('mm', 'millimeter'), ('mile', 'mile'), ('yard', 'yard'), ('foot', 'foot'), ('inch', 'inch'), ('i', 'item'), ('USD', 'US Dollars (USD)'), ('AUD', 'Australian Dollar (AUD)'), ('CAD', 'Canadian Dollar (CAD)'), ('CHF', 'Swiss Franc (CHF)'), ('EUR', 'Euros (EUR)'), ('GBP', 'UK Pounds (GBP)'), ('HKD', 'Hongkong Dollar (HKD)'), ('JPY', 'Japanese Yen (JPY)'), ('year', 'year'), ('month', 'month'), ('week', 'week'), ('day', 'day'), ('hour', 'hour'), ('minute', 'minute'), ('second', 'second'), ('t', 'metric_ton'), ('kg', 'kilogram'), ('g', 'gram'), ('ton', 'ton'), ('st', 'stone'), ('lb', 'pound'), ('J', 'joule'), ('erg', 'erg'), ('kWh', 'Kilowatt Hour'), ('MWh', 'Megawatt Hour'), ('GWh', 'Gigawatt Hour'), ('TWh', 'Terawatt Hour'), ('PWh', 'Petawatt Hour'), ('BTU', 'British Thermal Unit'), ('cal', 'Thermochemical calorie'), ('kcal', 'Food Calorie'), ('mL', 'millilitre'), ('L', 'litre'), ('kL', 'Kilolitre'), ('ML', 'Megalitre'), ('imperial_pint', 'imperial pint'), ('imperial_gallon', 'imperial gallon'), ('pint', 'US pint'), ('gallon', 'US gallon')]),
        ),
    ]
