import json
import os
from datetime import timedelta

import random
import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from slack_integration.models import Temperature


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def responder(message):
    if message == 'hello' or message == 'hi':
        return "Hi! It's nice to meet new humans."
    elif message == 'help':
        return "coffeebot help\t\t\tshows this message\ncoffeebot hello/hi\t\t\tgreeting from coffeebot\ncoffeebot " \
               "[any sentence containing coffee]\t\t\tinformation on whether the most recent pot of coffee is fresh" \
               "\ncoffeebot stats\t\t\tfind out how much coffee has been consumed\ncoffeebot fact\t\t\tget a \"fun\"" \
               "fact about coffee"
    elif 'coffee' in message:
        last_coffee = Temperature.objects.latest('id')
        minutes = last_coffee.minutes_since_creation()
        if minutes < 60:
            return "It's been {} minutes since someone made a fresh pot of coffee." \
                   " There's probably still some left!".format(minutes)
        else:
            return "It's been over an hour since someone made a fresh pot of coffee. Go make one!"
    return "Sorry, I didn't understand!"


COFFEE_FACTS = [
    "Coffee is the world's second most valuable traded commodity, only behind petroleum. :dollar: :dollar: :dollar:",
    "Energy drinks still don't have as much caffeine as a Starbucks coffee.",
    "Coffee is most effective if consumed between 9:30 am and 11:30 am. :sunny:",
    "The world consumes close to 2.25 billion cups of coffee every day.",
    "In Korea and Japan, there is a Cat Cafe where you can go to drink coffee and hang out with cats for hours :cat:",
    "The first webcam was created in Cambridge to check the status of a coffee pot. :nerd_face:",
    "Coffee beans aren't beans. They are fruit pits. :apple:",
    "In the beginning, Starbucks spent more money on health insurance for its employees than on coffee beans.",
    "Instant Coffee was invented by a man called George Washington around 1910.",
    "Coffee doesn't taste like it smells because saliva wipes out half of the flavor.",
    "Drinking a cup of caffeinated coffee significantly improves blood flow. :partyparrot:",
    "New Yorkers drink almost 7 times more coffee than other cities in the US. :explodyparrot:",
    ":elephant: One of the world's most expensive coffee brands is made from the dung of Thai elephants. :elephant:",
    "54% of the Americans drink coffee every day. :flag-us:",
    "The word \"coffee\" comes from the Arabic for \"wine of the bean\". :wine:",
    "The Netherlands is the world's largest per capita consumer of coffee, averaging 2.4 cups of coffee per person per "
    "day. :coffee:",
    "Without its smell, coffee would have only a sour or bitter taste due to the organic acids.",
    "To study the health effects of coffee, King Gustav III of Sweden :crown: commuted the death sentences of a pair "
    "of twins on the condition that one drank 3 pots of coffee and the other tea for the rest of their lives.",
    "The name \"Cappuccino\" comes from the resemblance of the drink to the clothing of the Capuchin monks.",
    "Americans spend an average of $1,092 on coffee each year. :dollar: :dollar: :dollar:",
    "Drinking caffeine in the evening delays our brain's release of melatonin and interrupts our circadian rhythm by "
    "as much as 40 minutes. :sleeping:",
    "Starbucks has opened 2 stores per day since 1987.",
    "It has been estimated it would take 70 cups of coffee to kill a 154-pound (70 kg) person.",
    "Brazil has been the largest producer of coffee for the last 150 years.",
    "50% of the caffeine you've consumed may be cleared from your body within 5 hours, but it will take over a day "
    "to fully eliminate it from your system.",
    "Hamburg, Germany, has banned coffee pods from government-run buildings in 2016 because they create unnecessary "
    "waste and contain aluminum.",
    "Two cups of coffee a day were found to reduce the risk of alcohol-related cirrhosis by 43%. :beers:",
    "20% of office coffee mugs contain fecal bacteria. :poop: :scream: :poop:",
    "It takes about 37 gallons (140 liters) of water to grow the coffee beans and process them to make one cup of "
    "coffee. :coffee: :coffee: :coffee:",
    "Coffee has been found to reverse liver damage caused by alcohol. :beers: :champagne: :beer: :champagne: :beers:",
    "Drinking 2 to 4 cups of coffee daily has been found to drop the risk of suicide by 50% compared to non-coffee "
    "drinkers.",
    "In the 17th century Ottoman Empire, drinking coffee was punishable by death. :skull:",
    "The world's most expensive coffee is $600 a pound."

]

def responder(message):
    if message == 'hello' or message == 'hi':
        return "Hi! It's nice to meet new humans."
    elif 'coffee' in message:
        last_coffee = Temperature.objects.latest('id')
        minutes = last_coffee.minutes_since_creation()
        if minutes < 60:
            return "It's been {} minutes since someone made a fresh pot of coffee." \
                   " There's probably still some left!".format(minutes)
        else:
            return "It's been over an hour since someone made a fresh pot of coffee. Go make one!"
    elif message == 'stats':
        total_pots = Temperature.objects.count()
        week_pots = Temperature.objects.filter(brew_date__gte=timezone.now()-timedelta(days=7)).count()
        fact = random.choice(COFFEE_FACTS)
        return "Coffee Stats\nBrews This Week: " + str(week_pots) + "\nTotal Brews: " + str(total_pots) + "\n" + fact
    elif message == 'fact':
        fact = random.choice(COFFEE_FACTS)
        return fact
    return "Sorry, I didn't understand!"


@csrf_exempt
def coffee_prompt(request):
    try:
        text = request.POST.get('text').split('coffeebot')[1].strip().lower()
        response_data = {'text': responder(text)}
    except AttributeError:
        response_data = {'text': 'I wasn\'t able to understand your message'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@csrf_exempt
def add_coffee(request):
    Temperature.objects.create(temperature=request.POST.get('temperature'))
    response = requests.post(WEBHOOK_URL, data=json.dumps({'text': request.POST.get('text')}))
    return HttpResponse()
