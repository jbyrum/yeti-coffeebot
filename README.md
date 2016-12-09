# coffeebot
Coffeebot for Yeti's Slack

## Deploy to Heroku
1. Get your webhook url from Slack (see Incoming Webhook below)
2. Find your pyz time zone i.e. America/Los_Angeles
2. Press Deploy to Heroku below and enter the environment variables

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


## Set Up Slack Integrations
Fully functioning coffeebot relies on both incoming and outgoing webhooks.

Go to https://YOUR-TEAM.slack.com/apps/manage/custom-integrations

### Incoming Webhook
1. Click Incoming Webhooks
2. Add Configuration
3. Choose your channel and click Add Incoming Webhooks Integration
3. Update the name/image of coffeebot
4. Copy the webhook url. You will need to add this to Heroku when you deploy.

### Outgoing Webhook
1. Click Outgoing Webhooks
2. Add Configuration
3. Choose your channel and click Add Outgoing Webhooks Integration (Note: Outgoing Webhooks don't work with private channels)
4. Add the triggerword ('coffeebot')
5. Add your URL (http://example.herokuapp.com/coffee_prompt) - you'll get this after you deploy to Heroku.
6. Update name/image and save integration


## Setting up Arduino + Sparkfun WifiShield

We used Arduino Uno, the SparkFun Wifi Shield ESP8266, and the SparkFun Temperature Sensor TMP36. Place the temperature sensor near the water tank.
Download the Arduino code, and change the network settings so it includes your wifi network's name and password.
Then change the host to your heroku site. It should be example.herokuapp.com (do not include http). Upload this to the Arduino and enjoy Coffeebot!

## Commands
<code>coffeebot hi</code> OR <code>coffeebot hello</code>

greeting

<code>coffeebot [any sentence that contains coffee]</code>

Tells you when the most recent pot of coffee was brewes

<code>coffeebot stats</code>

How many pots of coffee have been brewed in the last week? In the last year?

<code>coffeebot fact</code>

"Fun" fact about coffee


