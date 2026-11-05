# Discord Partnership Announcement Bot

PartnerPulse is a Discord bot for posting partnership announcements to a configured channel, tagging the selected representative, and sharing partner details through a formatted embed.

## Install

1. Create a Discord application and bot in the Discord Developer Portal.
2. Invite the bot to your server with the `bot` and `applications.commands` scopes.
3. Grant the bot these permissions in the partnership channel:
   - View Channel
   - Send Messages
   - Embed Links
4. Install Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`.
6. Configure the environment variables:
   - `DISCORD_TOKEN`: your private Discord bot credential.
   - `PARTNERSHIP_CHANNEL_ID`: the Discord channel ID where announcements will be posted.
   - `GUILD_ID`: optional server ID for faster slash-command registration during development.
7. Start the bot:

   ```bash
   python main.py
   ```

## Use

1. Make sure the bot is online and can access the configured partnership channel.
2. In your Discord server, run:

   `/partnership representative partner_name invite_url details`

3. Select the representative member.
4. Enter the partner server or organization name.
5. Enter a Discord invite or external partnership website URL.
6. Optionally provide partnership details.
7. Users with the Manage Server permission can submit the command.
8. The bot posts a partnership embed in the configured channel, mentions the selected representative, and confirms the post privately to the command user.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/7b956145-6bc4-4518-a431-ec3c1ee4db91?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=7b956145-6bc4-4518-a431-ec3c1ee4db91
