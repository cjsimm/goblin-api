# Goblin API


# Todo and Bugs



# ZK Bot Setup

- generate the unique bot token inside telegram 

# Worker setup

- Ensure uvicorn remains set to 1 workers. Multiple workers will produce multiple lifetimes and introduce issues with telegram bot listening due to how the [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/index.html) update queue system works. 

# Development

## Telegram Bot

The telegram bot can receive updates from Telegram via either webhook or by polling for updates. Polling is easier for development as no extra security is required other than the Bot's secret token that's injected at setup. The webhook solution is overall better for production as it reduces the number of HTTP calls required and keeps a more efficient feedback loop.

## Using update polling for development

If the .env variable `TELEGRAM_WEBHOOK_KEY` is not set, a polling strategy is used by the bot to receive updates from telegram instead of the webhook


## Testing Telegram webhook loop locally

To run the Telegram bot using the FastAPI webhook endpoint, set the .env variable `TELEGRAM_WEBHOOK_KEY` to a private key that will be shared with Telegram at startup and arrive as the  `X-Telegram-Bot-Api-Secret-Token` header value that will arrive with each request to the endpoint. Telegram requires that HTTPS be used, so the header is encrypted with TLS to keep the key safe on the wire. This doesn't prevent the key from being logged inside infrastructure, however, so care must be taken.

FUTURE IMPROVEMENT: Restrict call origin to a telegram ip whitelist to further improve security

Localhost needs to be exposed to the internet to allow telegram to send webhook updates to the system using tunneling software such as [ngrok](https://ngrok.com/)

Localhost exposure must tunnel to an HTTPS url, and this url needs to be set in the `.env` file as the `API_PUBLIC_URL` environment variable

