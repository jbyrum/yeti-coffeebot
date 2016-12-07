# coffeebot
Coffeebot for Yeti's Slack

## Set Up Slack Integrations
Fully functioning coffeebot relies on both incoming and outgoing webhooks.

Go to https://YOUR-TEAM.slack.com/apps/manage/custom-integrations

### Incoming Webhook
1. Click Incoming Webhooks
2. Add Configuration
3. Choose your channel and click Add Incoming Webhooks Integration
3. Update the name/image of coffeebot
4. Get the webhook url and add it to the django project.

### Outgoing Webhook
1. Click Outgoing Webhooks
2. Add Configuration
3. Choose your channel and click Add Outgoing Webhooks Integration (Note: Outgoing Webhooks don't work with private channels)
4. Add the triggerword ('coffeebot')
5. Add your URL (http://example.com/coffee_prompt)
6. Update name/image and save integration


## Commands
'<code>coffeebot hi</code> OR <code>coffeebot hello</code>

greeting

<code>coffeebot [any sentence that contains coffee]</code>

Tells you when the most recent pot of coffee was brewes

<code>coffeebot stats</code>

How many pots of coffee have been brewed in the last week? In the last year?

<code>coffeebot fact</code>

"Fun" fact about coffee


