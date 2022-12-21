"""Main module for the bot"""

import app.log
import app.bot as bot

if __name__ == '__main__':
    bot_token: str = 'BotFather_provided_token'
    app = bot.build_basic_bot(bot_token)
    bot.add_actions_v1(app)
    bot.run_bot(app)
