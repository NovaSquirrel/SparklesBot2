# SparklesBot2
A simple multi-platform bot using webhooks

This bot is designed around writing generic command logic, and then reusing it across multiple chat platforms. `bot.py` listens for webhooks for platforms that support webhooks, and routes the received information through the command logic, parsing the POSTs and formatting the output as necessary for each platform.

For platforms that don't support webhooks in response to bot commands (like Discord or IRC), a generic JSON endpoint is provided, and you can write a small bot (using whatever premade library makes it easiest) that POSTs bot commands to the endpoint to do the actual logic.
