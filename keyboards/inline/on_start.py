from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

on_start = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text='💆‍♂️Перейти к правилам',
                                            callback_data='rules')
                                    ]
                                ])
