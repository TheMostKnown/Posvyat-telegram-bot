import json
from typing import Optional

from telegram import Bot

from tgbot.handlers.spreadsheet_parser.spreadsheet_parser import get_data
from tgbot.handlers.utils import make_domain, make_tg_tag
from tgbot.models import (
    Organizer, Room, Guest, OrganizerSchedule, GuestSchedule,
    Level, Broadcast, Script, Button, Command
)


def get_init_data(
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str,
        bot: Optional[Bot] = None
) -> None:

    spreadsheet = get_data(
        spreadsheet_id,
        creds_file_name,
        token_file_name
    )

    # getting info about guests' levels
    levels_sheet = spreadsheet['Уровни']

    for i in range(1, len(levels_sheet)):
        level_num = int(levels_sheet[i][0])
        level_info = levels_sheet[i][1].strip()

        if level_num != '':
            level = Level.objects.filter(id=level_num)

            if len(level) > 0:
                level = level[0]

                level.level = level_info
                level.save()
            else:
                Level(
                    id=level_num,
                    level=level_info
                ).save()

    # getting info about commands for calling
    commands_sheet = spreadsheet['Команды']

    for i in range(1, len(commands_sheet)):
        name = commands_sheet[i][0].strip()
        arguments = commands_sheet[i][1].strip()
        desc = commands_sheet[i][2].strip()
        admin = True if commands_sheet[i][3] == '1' else False

        if name != '':
            command = Command.objects.filter(name=name)

            if len(command) > 0:
                command = command[0]

                command.arguments = arguments
                command.desc = desc
                command.admin = admin

                command.save()
            else:
                Command(
                    name=name,
                    arguments=arguments,
                    desc=desc,
                    admin=admin
                ).save()

    # getting info about broadcasting texts
    broadcasting_sheet = spreadsheet['Рассылки']

    for i in range(1, len(broadcasting_sheet)):
        title = broadcasting_sheet[i][0].strip()
        text = broadcasting_sheet[i][1].strip()
        levels = f'[{broadcasting_sheet[i][2]}]'

        if title != '':
            broadcast = Broadcast.objects.filter(title=title)

            if len(broadcast) > 0:
                broadcast = broadcast[0]

                broadcast.text = text
                broadcast.levels = levels

                broadcast.save()
            else:
                Broadcast(
                    title=title,
                    text=text,
                    levels=levels
                ).save()

    # getting info about admins
    admins_sheet = spreadsheet['Админы']
    for i in range(1, len(admins_sheet)):
        surname = admins_sheet[i][0].strip()
        name = admins_sheet[i][1].strip()
        tg_tag = admins_sheet[i][2].strip()

        if tg_tag != '':
            tg_tag = make_tg_tag(tg_tag)
            admin = Organizer.objects.filter(tg_tag=tg_tag)

            if len(admin) > 0:
                admin = admin[0]

                admin.surname = surname
                admin.name = name
                admin.is_admin = True

                admin.save()
            else:
                Organizer(
                    surname=surname,
                    name=name,
                    chat_id = 0,
                    is_admin=True,
                    tg_tag=tg_tag,
                    vk_link='',
                    phone='',
                    room='',
                    department=''
                ).save()

    # getting info about event organizers
    organizers_sheet = spreadsheet['Сетка Оргов']

    for i in range(2, len(organizers_sheet)):
        surname = organizers_sheet[i][0].strip()
        name = organizers_sheet[i][1].strip()
        tg_tag = organizers_sheet[i][2].strip()
        vk_link = organizers_sheet[i][3].strip()
        phone = organizers_sheet[i][4].strip()
        department = organizers_sheet[i][5].strip()
        room = organizers_sheet[i][6].strip()

        if tg_tag != '':
            tg_tag = make_tg_tag(tg_tag)
            organizer = Organizer.objects.filter(tg_tag=tg_tag)

            if organizer.count() > 0:
                organizer = organizer[0]

                organizer.surname = surname
                organizer.name = name
                organizer.vk_link = vk_link
                organizer.phone = phone
                organizer.room = room
                organizer.department = department

                organizer.save()
            else:
                Organizer(
                    surname=surname,
                    name=name,
                    chat_id = 0,
                    tg_tag=tg_tag,
                    vk_link=vk_link,
                    phone=phone,
                    room=room,
                    department=department,
                ).save()

    # getting info about participants
    guests_sheet = spreadsheet['Участники']

    for i in range(1, len(guests_sheet)):
        surname = guests_sheet[i][0].strip()
        name = guests_sheet[i][1].strip()
        patronymic = guests_sheet[i][2].strip()
        tg_tag = guests_sheet[i][24].strip()
        vk_link = guests_sheet[i][23].strip()
        phone = guests_sheet[i][22].strip()
        levels = json.loads(f'[{guests_sheet[i][30]}]') if guests_sheet[i][30] != '' else []
        room = guests_sheet[i][4].strip()
        team = guests_sheet[i][5].strip()

        if tg_tag != '':
            tg_tag = make_tg_tag(tg_tag)
            vk_link = make_domain(vk_link)

            guest = Guest.objects.filter(tg_tag=tg_tag)

            if len(guest) > 0:
                guest = guest[0]

                guest.surname = surname
                guest.name = name
                guest.patronymic = patronymic
                guest.tg_tag = tg_tag
                guest.vk_link = vk_link
                guest.phone = phone
                guest.room = room
                guest.team = team

                existing_levels = json.loads(guest.levels)

                text = ''

                if levels and len(levels) != len(levels):
                    guest.levels = json.dumps(levels)

                    # если есть новые группы -> нужно отправить уведомление об этом
                    # for level in levels:
                    #     if level not in existing_levels:
                    #         info = Notification.objects.filter(group_num=int(level))
                    #
                    #         if info:
                    #             text += f'{info.desc}\n'
                    #
                    # if len(text) != 0:
                    #     send_message(
                    #         vk=vk,
                    #         chat_id=guest.chat_id,
                    #         text=text
                    #     )
                guest.save()

            else:
                Guest(
                    surname=surname,
                    name=name,
                    patronymic=patronymic,
                    tg_tag=tg_tag,
                    vk_link=vk_link,
                    phone=phone,
                    levels=json.dumps(levels),
                    room=room,
                    texts=json.dumps([]),
                    team=team
                ).save()

    # getting info about organizers' schedule
    organizers_schedule_sheet = spreadsheet['Сетка Оргов']

    for i in range(2, len(organizers_schedule_sheet)):
        tg_tag = organizers_schedule_sheet[i][2].strip()
        tg_tag = make_tg_tag(tg_tag).strip()

        org_schedule = OrganizerSchedule.objects.filter(tg_tag=tg_tag)

        for j in range(9, len(organizers_schedule_sheet[i])):
            desc = organizers_schedule_sheet[i][j]

            if desc != '':

                date = organizers_schedule_sheet[0][j].strip()
                start_time = organizers_schedule_sheet[1][j].strip()
                finish_time = organizers_schedule_sheet[1][j+1].strip() \
                    if j + 1 < len(organizers_schedule_sheet[1]) \
                    else ''

                schedule_item = org_schedule.filter(start_time=start_time, date=date)

                if schedule_item.count() > 0:
                    schedule_item = schedule_item[0]

                    old_desc = schedule_item.desc

                    if old_desc != desc and tg_tag:
                        print('Пользователь c изменением и непустым тегом тг найден ')
                        print(tg_tag)
                        
                        try: 
                            user = Organizer.objects.get(tg_tag=tg_tag)
                            chat_id = user.chat_id
                                
                            print(tg_tag)
                            print(chat_id)
                            if bot and chat_id!=0:
                                bot.send_message(chat_id = chat_id, text = f"Расписание изменено c {start_time} до {finish_time} - {desc}")
                        except Exception:
                            print(f"Не отправилось сообщение об изменении расписания юзеру {tg_tag}")

                    schedule_item.desc = desc
                    schedule_item.date = date
                    schedule_item.start_time = start_time
                    schedule_item.finish_time = finish_time

                    schedule_item.save()
                else:
                    OrganizerSchedule(
                        desc=desc,
                        tg_tag=tg_tag,
                        date=date,
                        start_time=start_time,
                        finish_time=finish_time
                    ).save()

    # TODO waiting for table schema
    # getting info about guests' schedule
    # guests_schedule_sheet = spreadsheet['GuestSchedule']
    #
    # for i in range(1, len(guests_schedule_sheet)):
    #     desc = guests_schedule_sheet[i][0]
    #     start_time = guests_schedule_sheet[i][1]
    #     finish_time = guests_schedule_sheet[i][2]
    #
    #     guest_schedule = GuestSchedule.objects.filter(start_time=start_time)
    #
    #     if len(guest_schedule) > 0:
    #         guest_schedule = guest_schedule[0]
    #
    #         guest_schedule.desc = desc
    #         guest_schedule.start_time = start_time
    #         guest_schedule.finish_time = finish_time
    #
    #         guest_schedule.save()
    #     else:
    #         GuestSchedule(
    #             desc=desc,
    #             start_time=start_time,
    #             finish_time=finish_time
    #         ).save()

    # getting info about rooms
    rooms_sheet = spreadsheet['Комнаты']

    for i in range(1, len(rooms_sheet)):
        number = rooms_sheet[i][0].strip()
        capacity = rooms_sheet[i][1].strip()

        if number != '':
            room = Room.objects.filter(number=number)

            if len(room) > 0:
                room = room[0]

                room.capacity = capacity
                room.save()
            else:
                Room(
                    number=number,
                    capacity=capacity
                ).save()

    # getting info about scripts
    scripts_sheet = spreadsheet['Скрипты']

    for i in range(1, len(scripts_sheet)):
        title = scripts_sheet[i][0].strip()
        text = scripts_sheet[i][1].strip()

        if title != '':
            script = Script.objects.filter(title=title)

            if len(script) > 0:
                script = script[0]

                script.text = text
                script.save()
            else:
                Script(
                    title=title,
                    text=text
                ).save()

    # getting info about buttons
    buttons_sheet = spreadsheet['Кнопки']

    for i in range(1, len(buttons_sheet)):
        text = buttons_sheet[i][0].strip()
        title_from = buttons_sheet[i][1].strip()
        title_to = buttons_sheet[i][2].strip()

        if text is not None:
            button = Script.objects.filter(text=text)

            if len(button) > 0:
                button = button[0]

                button.title_from = title_from
                button.title_to = title_to

                button.save()
            else:
                Button(
                    text=text,
                    title_from=title_from,
                    title_to=title_to
                ).save()