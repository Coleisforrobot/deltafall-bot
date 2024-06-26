from discord.utils import get
from discord.ext import commands
import time
from discord.ext import tasks
import os

class yourenobody(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_time.start()
        self.guildid = 1198291214672347308
        self.stupidrole = 1233821393133768817
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for file in os.listdir("data/just_joined/"):
            with open(f"data/just_joined/{file}", "r") as f:
                time = float(f.readline())
                while time in self.cooldowns:
                    time += 1
                self.cooldowns[time] = int(file)
        self.cooldowns = dict(sorted(self.cooldowns.items()))

    @tasks.loop(seconds=30)
    async def check_time(self):
        if len(self.cooldowns) >= 1:
            if next(iter(self.cooldowns)) - time.time() < -172800: # 2 days 
                usr_id = self.cooldowns[next(iter(self.cooldowns))]
                guild = self.bot.get_guild(self.guildid)
                usr = guild.get_member(usr_id)
                await usr.remove_roles(get(guild.roles, id=self.stupidrole))

                os.remove(f"data/just_joined/{usr_id}")
                del self.cooldowns[next(iter(self.cooldowns))]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = get(member.guild.roles, id=self.stupidrole)
        await member.add_roles(role)
        
        with open(f"data/just_joined/{member.id}", "x") as file:
            file.write(str(time.time()))
            self.cooldowns[time.time()] = int(member.id)

async def setup(bot):
    await bot.add_cog(yourenobody(bot))