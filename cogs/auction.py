# Auction for Market and interaction, create the auction and modal for bids 

import discord
from discord.ext import commands

class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="auction", description="Start an auction for an item.")
    async def auction(self, ctx, item: str, starting_bid: float):
        """Starts an auction for a specified item with buttons for bidding."""
        starting_bid = round(starting_bid, 2)
        item = item.strip()
        Message = f"**Auction Started!**\nItem: {item}\nStarting Bid: {starting_bid}\n\nClick the button below to place your bid!"
        view = AuctionView(item, starting_bid)

        await ctx.send(Message, view=view)


class AuctionView(discord.ui.View):
    def __init__(self, item: str, starting_bid: float):
        super().__init__(timeout=None)
        self.item = item
        self.current_bid = starting_bid
        self.highest_bidder = None

    @discord.ui.button(label="Bid", style=discord.ButtonStyle.primary)
    async def bid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handles the bid button click."""

        await interaction.response.send_modal(BidModal(self))

    async def set_current_bid(self, bid: float, bidder: discord.User):
        """Updates the current bid and highest bidder."""
        self.current_bid = bid
        self.highest_bidder = bidder
    



class BidModal(discord.ui.Modal):
    def __init__(self, auction_view: AuctionView):
        super().__init__(title="Place Your Bid")
        self.auction_view = auction_view

        self.current_bid_display = discord.ui.Label(
            text=f"Current Bid: {self.auction_view.current_bid} by {self.auction_view.highest_bidder if self.auction_view.highest_bidder else "No Bidder yet"}", 
            component=discord.ui.TextInput(
            style=discord.TextStyle.short,
            max_length=256),
        )

        self.character_name = discord.ui.TextInput(
            label="Character Name",
            placeholder="Enter your character's name",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.character_name)

        self.bid_amount = discord.ui.TextInput(
            label="Bid Amount",
            placeholder=f"Enter a bid higher than {self.auction_view.current_bid}",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.bid_amount)

        

    async def on_submit(self, interaction: discord.Interaction):
        """Handles the submission of the bid modal."""
        try:
            bid_value = float(self.bid_amount.value)
            character_name = self.character_name.value.strip()
            if bid_value <= self.auction_view.current_bid:
                await interaction.response.send_message(
                    f"Your bid must be higher than the current bid of {self.auction_view.current_bid}.",
                    ephemeral=True
                )
                return

            await self.auction_view.set_current_bid(bid_value, character_name)

            await interaction.response.send_message(
                f"Bid accepted! Current highest bid is now {self.auction_view.current_bid} by {character_name}.",
                ephemeral=True
            )

        except ValueError:
            await interaction.response.send_message(
                "Invalid bid amount. Please enter a valid number.",
                ephemeral=True
            )