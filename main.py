import logging
import os
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("partnership-bot")


def get_required_int(name: str) -> int:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    try:
        return int(value)
    except ValueError as error:
        raise RuntimeError(f"{name} must be a Discord ID number") from error


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing required environment variable: DISCORD_TOKEN")

PARTNERSHIP_CHANNEL_ID = get_required_int("PARTNERSHIP_CHANNEL_ID")
GUILD_ID = os.getenv("GUILD_ID")


class PartnershipBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info("Synced %d application commands to guild %s", len(synced), GUILD_ID)
        else:
            synced = await self.tree.sync()
            logger.info("Synced %d global application commands", len(synced))

    async def on_ready(self) -> None:
        if self.user:
            logger.info("Logged in as %s (%s)", self.user, self.user.id)


bot = PartnershipBot()


@bot.tree.command(name="partnership", description="Post a partnership announcement and tag its representative.")
@app_commands.describe(
    representative="The representative to tag in the announcement",
    partner_name="The name of the partner server or organization",
    invite_url="A permanent invite or website URL",
    details="Optional details about the partnership",
)
@app_commands.checks.has_permissions(manage_guild=True)
async def partnership(
    interaction: discord.Interaction,
    representative: discord.Member,
    partner_name: str,
    invite_url: str,
    details: Optional[str] = None,
) -> None:
    channel = interaction.guild.get_channel(PARTNERSHIP_CHANNEL_ID) if interaction.guild else None
    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message(
            "The configured partnership channel could not be found.", ephemeral=True
        )
        return

    embed = discord.Embed(
        title=f"New Partnership: {partner_name}",
        description=details or "We are excited to announce this new partnership!",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow(),
    )
    embed.add_field(name="Partner", value=partner_name, inline=True)
    embed.add_field(name="Representative", value=representative.mention, inline=True)
    embed.add_field(name="Link", value=invite_url, inline=False)
    embed.set_footer(text=f"Posted by {interaction.user.display_name}")

    try:
        await channel.send(content=representative.mention, embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            "I do not have permission to post in the configured partnership channel.",
            ephemeral=True,
        )
        return

    await interaction.response.send_message(
        f"Partnership posted in {channel.mention} and {representative.mention} was tagged.",
        ephemeral=True,
    )


@partnership.error
async def partnership_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    if isinstance(error, app_commands.errors.MissingPermissions):
        message = "You need the Manage Server permission to use this command."
    else:
        logger.error("Partnership command failed", exc_info=error)
        message = "The partnership could not be posted. Check the bot configuration and try again."

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


bot.run(TOKEN)
