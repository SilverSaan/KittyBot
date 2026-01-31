import os
import json
from datetime import datetime, timezone
import aiohttp
from pathlib import Path
from dateutil import parser


from discord.ext import commands
import discord

class LunarUtils(commands.Cog):

    BASE_URL = "https://craigchamberlain.github.io/moon-data/api/moon-phase-data/{year}/index.json"

    def __init__(self, bot):
        self.bot = bot
        # Folder for cached JSON files
        self.json_folder = Path(__file__).parent.parent / "jsons" / "moons"
        self.json_folder.mkdir(parents=True, exist_ok=True)


    @commands.hybrid_command()
    async def lunar_phase(self, ctx, date_str):
        """
        Takes a date string (day/month/year format), parses it (assumes UTC if no timezone),
        loads Chamberlain JSON for that year, finds surrounding phases,
        returns phase name.
        """

        try:
            # Force day-first parsing (European format: DD/MM/YYYY)
            dt = parser.parse(date_str, dayfirst=True)
        except (ValueError, TypeError):
            await ctx.send("Date is not valid, try again")
            return
        
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        year = dt.year

        json_file = self.json_folder / f"{year}.json"

        if json_file.exists():
            with open(json_file, "r") as f:
                moon_data = json.load(f)
            online_sourced = False
        else:
            # Fetch from Chamberlain
            url = self.BASE_URL.format(year=year)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(f"Failed to fetch lunar data for {year}")
                        return
                    moon_data = await resp.json()

            # Save for later
            with open(json_file, "w") as f:
                json.dump(moon_data, f, indent=2)
            online_sourced = True

        # Convert Chamberlain datetimes to datetime objects (make them timezone-aware)
        moon_data_dt = [
            {
                "datetime": datetime.fromisoformat(e["Date"]).replace(tzinfo=timezone.utc),
                "phase": e["Phase"]
            } for e in moon_data
        ]

        # Find the two surrounding phase events (any phase, not just new moons)
        prev_phase = None
        next_phase = None

        for i, e in enumerate(moon_data_dt):
            if e["datetime"] <= dt:
                prev_phase = e
            elif e["datetime"] > dt and next_phase is None:
                next_phase = e
                break

        if prev_phase is None or next_phase is None:
            await ctx.send("Unable to determine lunar phase for this date")
            return

        # Determine phase name based on which phases we're between
        prev_p = prev_phase["phase"]
        next_p = next_phase["phase"]

        # Calculate how close we are to each phase event
        time_since_prev = (dt - prev_phase["datetime"]).total_seconds()
        time_until_next = (next_phase["datetime"] - dt).total_seconds()

        # Give major phases a ~1 day window (±12 hours from exact moment)
        PHASE_WINDOW = 12 * 3600  # 12 hours in seconds

        phase_names_map = {0: "New Moon", 1: "First Quarter", 2: "Full Moon", 3: "Last Quarter"}

        # Check if we're within the window of the previous phase
        if time_since_prev < PHASE_WINDOW:
            phase_name = phase_names_map.get(prev_p, "Unknown")
        # Check if we're within the window of the next phase
        elif time_until_next < PHASE_WINDOW:
            phase_name = phase_names_map.get(next_p, "Unknown")
        # Otherwise, we're between phases
        elif prev_p == 0 and next_p == 1:  # New → First Quarter
            phase_name = "Waxing Crescent"
        elif prev_p == 1 and next_p == 2:  # First Quarter → Full
            phase_name = "Waxing Gibbous"
        elif prev_p == 2 and next_p == 3:  # Full → Last Quarter
            phase_name = "Waning Gibbous"
        elif prev_p == 3 and next_p == 0:  # Last Quarter → New
            phase_name = "Waning Crescent"
        else:
            phase_name = "Unknown"

        msg = f"Lunar phase on {dt.date()}: {phase_name}"
        msg = f"\nOnline sourced, confirm if needed"
        if online_sourced:
            msg += "\n(Cached for future use)"
        await ctx.send(msg)