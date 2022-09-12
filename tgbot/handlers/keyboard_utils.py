# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers import manage_data as md
from tgbot.handlers import static_text as st


def make_btn_keyboard():
    buttons = [
        [
            InlineKeyboardButton(st.go_back, callback_data=f'{md.BUTTON_BACK_IN_PLACE}'),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_start_command():
    buttons = [
        [
            InlineKeyboardButton(st.btn1, callback_data=f'{md.BTN_1}'),
        ],
        [
            InlineKeyboardButton(st.btn2, callback_data=f'{md.BTN_2}'),
            InlineKeyboardButton(st.btn3, callback_data=f'{md.BTN_3}'),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(st.confirm_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.CONFIRM_BROADCAST}'),
        InlineKeyboardButton(st.decline_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)

def keyboard_issue_set_status(status):
    buttons = [[]]
    if status != "N":
        buttons[0].append(InlineKeyboardButton(st.btn_not_fx, callback_data=md.SET_NOT_FIXED))
    if status != "P":
        buttons[0].append(InlineKeyboardButton(st.btn_in_progress, callback_data=md.SET_IN_PROGRESS))
    if status != "F":
        buttons[0].append(InlineKeyboardButton(st.btn_fixed, callback_data=md.SET_FIXED))
    return InlineKeyboardMarkup(buttons)

