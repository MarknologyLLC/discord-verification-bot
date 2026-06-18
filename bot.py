"""
Marknology Discord Verification Bot
Handles TikTok Shop creator applications via private ticket channels.

Commands:
  /approve @member  -- grant verified role (staff)
  /close            -- close and delete ticket channel (staff)
  /export_creators  -- export applications to JSON (admin)

Flow:
  1. Bot posts verification panel in VERIFICATION_CHANNEL_ID
  2. Applicant clicks "Create ticket" -> private channel opens
  3. Bot asks questions one at a time (email, name, TikTok, referral)
  4. TikTok handle validated (@username or profile URL)
  5. Completed application saved to creators.json (gitignored)
  6. Application posted to STAFF_LOG_CHANNEL_ID
  7. Staff runs /approve @member to grant VERIFIED_ROLE_ID
  8. Staff runs /close to clean up ticket channel
"""

import discord
import json
import os
import re
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
VERIFICATION_CHANNEL_ID = int(os.getenv("VERIFICATION_CHANNEL_ID", "0"))
STAFF_LOG_CHANNEL_ID = int(os.getenv("STAFF_LOG_CHANNEL_ID", "0"))
VERIFIED_ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID", "0"))
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID", "0"))

CREATORS_FILE = Path("creators.json")  # gitignored -- contains applicant emails
QUESTIONS = [
    ("email", "What is your email address?"),
    ("name", "What is your first and last name?"),
    ("tiktok", "What is your TikTok handle? (e.g. @username or full profile URL)"),
    ("referral", "How did you hear about us?"),
]

# ── TikTok handle validation ────────────────────────────────────────────────
TIKTOK_PATTERN = re.compile(
    r"^(@[A-Za-z0-9._]+|https?://(www\.)?tiktok\.com/@[A-Za-z0-9._]+/?)$"
)

def valid_tiktok(value: str) -> bool:
    return bool(TIKTOK_PATTERN.match(value.strip()))


# ── In-memory session state ─────────────────────────────────────────────────
# { channel_id: { "user_id": int, "step": int, "answers": {} } }
sessions: dict[int, dict] = {}


# ── Bot setup ───────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


# ── Verification panel ──────────────────────────────────────────────────────
class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apply as a Creator", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user

        # One active ticket per user
        for ch in guild.text_channels:
            if ch.name == f"apply-{member.name.lower()}":
                await interaction.response.send_message(
                    "You already have an open application channel.", ephemeral=True
                )
                return

        # Create private channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        channel = await guild.create_text_channel(
            f"apply-{member.name.lower()}",
            overwrites=overwrites
        )

        sessions[channel.id] = {"user_id": member.id, "step": 0, "answers": {}}
        await interaction.response.send_message(f"Ticket opened: {channel.mention}", ephemeral=True)
        await channel.send(
            f"Hi {member.mention}, welcome to the Marknology creator application.

"
            f"{QUESTIONS[0][1]}"
        )


# ── Message handler -- walks applicant through questions ────────────────────
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    session = sessions.get(message.channel.id)
    if not session or message.author.id != session["user_id"]:
        await bot.process_commands(message)
        return

    step = session["step"]
    key, _ = QUESTIONS[step]
    answer = message.content.strip()

    # Validate TikTok handle
    if key == "tiktok" and not valid_tiktok(answer):
        await message.channel.send(
            "That doesn't look right. Please use @username or a full TikTok profile URL "
            "(e.g. https://www.tiktok.com/@username)."
        )
        return

    session["answers"][key] = answer
    session["step"] += 1

    if session["step"] < len(QUESTIONS):
        await message.channel.send(QUESTIONS[session["step"]][1])
    else:
        await complete_application(message, session)

    await bot.process_commands(message)


async def complete_application(message: discord.Message, session: dict):
    answers = session["answers"]
    guild = message.guild
    member = guild.get_member(session["user_id"])

    # Save to creators.json (gitignored)
    entry = {
        "discord_id": str(session["user_id"]),
        "discord_username": str(member),
        "applied_at": datetime.utcnow().isoformat(),
        **answers
    }
    creators = json.loads(CREATORS_FILE.read_text()) if CREATORS_FILE.exists() else []
    creators.append(entry)
    CREATORS_FILE.write_text(json.dumps(creators, indent=2))

    # Post to staff log
    log_channel = guild.get_channel(STAFF_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title="New Creator Application", color=0xfe5b27)
        embed.add_field(name="Discord", value=str(member), inline=True)
        embed.add_field(name="Email", value=answers.get("email", "-"), inline=True)
        embed.add_field(name="Name", value=answers.get("name", "-"), inline=True)
        embed.add_field(name="TikTok", value=answers.get("tiktok", "-"), inline=True)
        embed.add_field(name="Referral", value=answers.get("referral", "-"), inline=False)
        embed.set_footer(text=f"Channel: #{message.channel.name}")
        await log_channel.send(embed=embed)

    await message.channel.send(
        "Application submitted. A staff member will review it and get back to you here. "
        "You can leave this channel open until then."
    )
    del sessions[message.channel.id]


# ── Slash commands ───────────────────────────────────────────────────────────
@tree.command(name="approve", description="Grant verified role to an applicant (staff only)")
@app_commands.describe(member="The member to approve")
async def approve(interaction: discord.Interaction, member: discord.Member):
    role = interaction.guild.get_role(VERIFIED_ROLE_ID)
    if not role:
        await interaction.response.send_message("Verified role not configured.", ephemeral=True)
        return
    await member.add_roles(role)
    await interaction.response.send_message(f"{member.mention} approved and granted {role.name}.")


@tree.command(name="close", description="Close and delete this ticket channel (staff only)")
async def close(interaction: discord.Interaction):
    await interaction.response.send_message("Closing ticket...")
    await interaction.channel.delete()


@tree.command(name="export_creators", description="Export creator applications to JSON (admin only)")
async def export_creators(interaction: discord.Interaction):
    admin_role = interaction.guild.get_role(ADMIN_ROLE_ID)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message("Admin only.", ephemeral=True)
        return
    if not CREATORS_FILE.exists():
        await interaction.response.send_message("No applications yet.", ephemeral=True)
        return
    await interaction.response.send_message(
        "Exporting...",
        file=discord.File(str(CREATORS_FILE), filename="creators-export.json"),
        ephemeral=True
    )


# ── Startup ──────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    # Post or refresh verification panel
    channel = bot.get_channel(VERIFICATION_CHANNEL_ID)
    if channel:
        await channel.send(
            embed=discord.Embed(
                title="Marknology Creator Application",
                description=(
                    "Want to create content for Marknology brands on TikTok Shop?\n\n"
                    "Click the button below to start your application. "
                    "We will review it and get back to you in the ticket."
                ),
                color=0xfe5b27
            ),
            view=VerifyButton()
        )
    print(f"Bot ready as {bot.user}")


bot.run(DISCORD_TOKEN)
