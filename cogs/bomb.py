import discord
from discord.ext import commands
from discord import app_commands

import random
from datetime import timedelta

class bomb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bomb", description="bomb")
    @app_commands.allowed_installs(guilds=True, users=False)
    async def bomb(self, interaction: discord.Interaction, user: discord.Member):
        if not await self.bot.setting_manager.get_guild_setting(interaction.guild, ("fun", "bomb")):
            return await interaction.response.send_message("This guild has this command disabled.", ephemeral=True)
        
        roles_get = await self.bot.setting_manager.get_guild_setting(interaction.guild, ("fun", "bomb_role_exception"))
        if type(roles_get) is not list:
            roles_get = [e] if (e := roles_get) is not None else []

        for role in interaction.user.roles:
            if role.id in roles_get:
                return await interaction.response.send_message("ur just not fun", ephemeral=False)
        for role in user.roles:
            if role.id in roles_get:
                return await interaction.response.send_message("That person is immune to be being bombed.", ephemeral=True)


        chance = 2
        if random.randint(1, chance) == chance:
            try:
                await interaction.user.timeout(timedelta(minutes=5))
            except discord.Forbidden:
                return await interaction.response.send_message("wow you are so unfun", ephemeral=False)
            
            return await interaction.response.send_message("gg ur getting slimed", ephemeral=False)
        
        try:
            await user.timeout(timedelta(minutes=1))
        except discord.Forbidden:
            return await interaction.response.send_message("I cannot timeout that user.", ephemeral=False)
        await interaction.response.send_message(f"{user.mention} You have been bombed by {interaction.user.mention}.", ephemeral=False)

async def setup(bot):
    await bot.add_cog(bomb(bot))