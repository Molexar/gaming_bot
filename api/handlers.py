import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from api import models
import api.loop


def message(msg):
    return msg.get("text") or msg.get("message")["text"]


def super_context(func, *args, **kwargs):
    def wrapper(chat, msg):
        if message(msg) == "/start":
            start_context(chat, msg)
        elif message(msg) == "/edit":
            edit(chat, msg)
        elif message(msg) == "/disable":
            disable(chat, msg)
        elif message(msg) == "/enable":
            enable(chat, msg)
        elif message(msg) == "/search":
            search(chat, msg)
        else:
            func(chat, msg)
    return wrapper


def start_context(chat, msg):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=game[1], callback_data=game[0])] for game in models.Game.choices
    ])
    chat.sender.sendMessage("Choose your favorite game from the list below:", reply_markup=keyboard)
    chat.callback = game_choosing_context


@super_context
def game_choosing_context(chat, msg):
    if telepot.flavor(msg) == 'callback_query':
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        chat.player.game = query_data
        chat.player.save()
        chat.callback = steam
        chat.sender.sendMessage("Please type your steam nickname")
    else:
        chat.sender.sendMessage("Please choose one of the games below")


@super_context
def steam(chat, msg):
    chat.player.steam = message(msg)
    chat.player.save()
    chat.callback = bio
    chat.sender.sendMessage("Now please type smth about yourself")


@super_context
def bio(chat, msg):
    chat.player.bio = message(msg)
    chat.player.is_active = True
    chat.player.save()
    chat.sender.sendMessage("Your profile is filled! Now you can search comrades")
    chat.callback = continue_search


def disable(chat, msg):
    chat.player.is_active = False
    chat.player.save()
    chat.sender.sendMessage("You are not online now")
    chat.callback = continue_search


def enable(chat, msg):
    chat.player.is_active = True
    chat.player.save()
    chat.sender.sendMessage("You are online")
    chat.callback = continue_search


def get_card(player: models.Player):
    return f"{player.steam}\n{player.get_game_display()}\n{player.bio}"


def search(chat, msg):
    next_player = chat.get_player
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="I found you!", callback_data=f"OK {next_player.chat_id}"),
         InlineKeyboardButton(text="Next player", callback_data="NEXT")]
    ])
    chat.sender.sendMessage(get_card(next_player), reply_markup=keyboard)
    chat.callback = continue_search


@super_context
def continue_search(chat, msg):
    if telepot.flavor(msg) == "callback_query":
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data.split(" ")[0] == "OK":
            api.loop.bot.sendMessage(int(query_data.split(" ")[1]), f"Your card was liked by @{chat.player.username}!")
            chat.callback = continue_search
        elif query_data.split(" ")[0] == "NEXT":
            search(chat, msg)
    else:
        chat.sender.sendMessage("Please choose option from the list")


def edit(chat, msg):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Game", callback_data="Game")],
        [InlineKeyboardButton(text="Steam", callback_data="steam")],
        [InlineKeyboardButton(text="Bio", callback_data="bio")]
    ])
    chat.sender.sendMessage("Choose info what you want to change", reply_markup=keyboard)
    chat.callback = edit_field


@super_context
def edit_field(chat, msg):
    if telepot.flavor(msg) == "callback_query":
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        chat.sender.sendMessage(f"Type new {query_data}")
        if query_data == 'steam':
            chat.callback = edit_bio
        elif query_data == 'bio':
            chat.callback = edit_steam
        elif query_data == "game":
            start_context(chat, msg)
    else:
        chat.sender.sendMessage("Please select option from list")


@super_context
def edit_bio(chat, msg):
    setattr(chat.player, "bio", message(msg))
    chat.player.save()
    chat.callback = edit_field


@super_context
def edit_steam(chat, msg):
    setattr(chat.player, "steam", message(msg))
    chat.player.save()
    chat.callback = edit_field





