import os

from dotenv import load_dotenv

from api import models
import telepot
from telepot.loop import MessageLoop
from api.handlers import start_context
from telepot.delegate import pave_event_space, per_chat_id, create_open, include_callback_query_chat_id

load_dotenv()


def super_generator(gen, *args, **kwargs):
    def new_gen(players):
        g = gen(players)
        for i in g:
            yield i
    return new_gen


@super_generator
def play(p):
    for v in p:
        yield v


class Chat(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Chat, self).__init__(*args, **kwargs)
        self.callback = start_context
        message = args[0][1]
        chat_pk = int(message["chat"]["id"])
        if message["from"].get("username", None) is None:
            bot.sendMessage(chat_pk, "Please set the username in your profile and try again")
            self.on_close(ValueError)
        else:
            if models.Player.objects.filter(username=message["from"]["username"], chat_id=chat_pk).count() == 0:
                self.player: models.Player = models.Player(username=message["from"]["username"], chat_id=chat_pk)
                self.player.save()
            else:
                self.player = models.Player.objects.get(username=message["from"]["username"], chat_id=chat_pk)
            self.player.chat_id = chat_pk
            self.player.save()

    def on_chat_message(self, msg):
        self.callback(self, msg)

    def on_callback_query(self, msg):
        self.callback(self, msg)

    @property
    def get_player(self):
        try:
            players = getattr(self, "cards")
        except AttributeError:
            self.cards = play(list(models.Player.objects.filter(is_active=True, game=self.player.game)))
            players = self.cards
        try:
            return next(players)
        except StopIteration:
            self.cards = play(list(models.Player.objects.filter(is_active=True, game=self.player.game)))
            return next(self.cards)


TOKEN = os.environ.get("BOT_TOKEN")

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(types=['private']), create_open, Chat, timeout=600),
])
webhook = MessageLoop(bot)
webhook.run_as_thread()
