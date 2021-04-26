from random import shuffle, randint
import discord

EMOJIS = ['🛁', '🚴', '🚀', '🚁', '🚂', '🚃', '🚌', '🚎', '🚑', '🚒', '🚓', '🦆', '🚕', '🦚', '🦞', '🚗',
         '🦑', '🚚', '🦢', '🦟', '🦠', '🦅', '🦀', '🦗', '🦋', '🚜', '🦇', '🦔', '🦓', '🚣', '🦒', '🦎',
         '🚶', '🛌', '🛒', '🛩', '🛰', '🛸', '🤔', '🤐', '🤓', '🤡', '🤫', '🥐', '🥕', '🥝', '🥦', '🥾']


# https://discord.gg/VSK6vZN5 - сервер с ботом
TOKEN = 'ODM2MjEzNzc1NzMyMTc4OTc0.YIauxA.qIGCX2O6PDgVHhM-PmPd3IPaP8M'


class CurrentPlay:
    def __init__(self):
        self.user = self.bot = 0
        self.num = 10  # обязательно четное! Иначе остается 1 эмодзи в конце игры
        self.smiles = EMOJIS.copy()
        shuffle(self.smiles)
        self.smiles = self.smiles[:self.num]

    def end_of_game(self):
        """Вовзращает результат игры и обнуляет счёт"""
        if self.user > self.bot:
            result = 'You Win!'
        elif self.user < self.bot:
            result = 'Bot Win!'
        else:
            result = 'Draw!'

        self.__init__()
        return result


class EmojiBot(discord.Client):
    # ключ - кортеж (сервер, канал), значение - состояние игры там
    games = {}

    async def on_message(self, message):
        if message.author == self.user:
            return

        text = message.content
        game = self.games.get((message.guild, message.channel), CurrentPlay())
        self.games[(message.guild, message.channel)] = game

        if not text.isdigit():
            await message.channel.send('Надо отправить число')
        elif text == '/stop':
            await message.channel.send(
                f'Game over.\nScore: You {game.score_user} - '
                f'Bot {game.score_bot}\n{game.end_of_game()}')
        else:
            user_s = game.smiles.pop(int(text) % len(game.smiles))
            bot_s = game.smiles.pop(randint(0, len(game.smiles) - 1))
            print(game.smiles)
            if user_s > bot_s:
                game.user += 1
            elif user_s < bot_s:
                game.bot += 1
            await message.channel.send(f'Your emoji:  {user_s}\n'
                                       f'Bot emoji:  {bot_s}\nScore: '
                                       f'You {game.user} - '
                                       f'Bot {game.bot}')
        if len(game.smiles) <= 1:
            await message.channel.send(
                f'Emoticons are over!\nScore: You {game.user} - '
                f'Bot {game.bot}\n{game.end_of_game()}')


if __name__ == "__main__":
    client = EmojiBot()
    client.run(TOKEN)
