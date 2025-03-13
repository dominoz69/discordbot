import discord
from discord.ext import commands
import random
import asyncio

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck = []
        self.card_values = {
            'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
        }
        
    def create_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
        
    def calculate_hand(self, hand):
        value = 0
        aces = 0
        
        for card in hand:
            rank = card[:-2]  # Remove suit emoji
            if rank == 'A':
                aces += 1
            else:
                value += self.card_values[rank]
                
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
                
        return value
        
    def format_hand(self, hand, hide_second=False):
        if hide_second and len(hand) > 1:
            return f"{hand[0]} 🂠"
        return ' '.join(hand)
        
    @commands.command()
    async def blackjack(self, ctx):
        """Play a game of Blackjack against the bot!"""
        self.deck = self.create_deck()
        player_hand = [self.deck.pop(), self.deck.pop()]
        dealer_hand = [self.deck.pop(), self.deck.pop()]
        
        async def show_game(hide_dealer=True):
            embed = discord.Embed(
                title="Blackjack",
                color=self.bot.colors['primary']
            )
            embed.add_field(
                name="Dealer's Hand",
                value=f"{self.format_hand(dealer_hand, hide_dealer)}\nValue: {'?' if hide_dealer else self.calculate_hand(dealer_hand)}",
                inline=False
            )
            embed.add_field(
                name="Your Hand",
                value=f"{self.format_hand(player_hand)}\nValue: {self.calculate_hand(player_hand)}",
                inline=False
            )
            return await ctx.send(embed=embed)
            
        message = await show_game()
        
        # Add hit/stand reactions
        await message.add_reaction('👊')  # hit
        await message.add_reaction('🛑')  # stand
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['👊', '🛑']
            
        while self.calculate_hand(player_hand) < 21:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                
                if str(reaction.emoji) == '👊':  # Hit
                    player_hand.append(self.deck.pop())
                    await message.delete()
                    message = await show_game()
                    await message.add_reaction('👊')
                    await message.add_reaction('🛑')
                else:  # Stand
                    break
                    
                await message.remove_reaction(reaction.emoji, user)
                
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Game Over",
                    description="Time's up! Game cancelled.",
                    color=self.bot.colors['error']
                )
                await message.edit(embed=embed)
                return
                
        player_value = self.calculate_hand(player_hand)
        
        # Dealer's turn
        while self.calculate_hand(dealer_hand) < 17:
            dealer_hand.append(self.deck.pop())
            
        dealer_value = self.calculate_hand(dealer_hand)
        
        # Show final hands
        await message.delete()
        message = await show_game(hide_dealer=False)
        
        # Determine winner
        if player_value > 21:
            result = "Bust! You lose! 💥"
            color = self.bot.colors['error']
        elif dealer_value > 21:
            result = "Dealer busts! You win! 🎉"
            color = self.bot.colors['success']
        elif player_value > dealer_value:
            result = "You win! 🎉"
            color = self.bot.colors['success']
        elif dealer_value > player_value:
            result = "Dealer wins! 💔"
            color = self.bot.colors['error']
        else:
            result = "It's a tie! 🤝"
            color = self.bot.colors['secondary']
            
        embed = discord.Embed(title="Game Over", description=result, color=color)
        await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
