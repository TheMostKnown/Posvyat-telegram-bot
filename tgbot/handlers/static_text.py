from tgbot.handlers.organizer import organizer


welcome = "Добро пожаловать!"
btn1 = "Кнопка №1"
btn2 = "Кнопка №2"
btn3 = "Кнопка №3"
pressed = "Вы нажали кнопку #"

go_back = "Вернуться"
confirm_broadcast = "Подтвердить"
decline_broadcast = "Отклонить"
secret_level = "Секретный уровень"
msg_sent = "Сообщение отослано"
share_location = "Позвольте мне узнать, откуда вы?"
thanks_for_location = "Спасибо за ваше местоположение!"
broadcast_command = '/broadcast'
broadcast_no_access = "Sorry, you don't have access to this function."
broadcast_header = "This message will be sent to all users.\n\n"
declined_message_broadcasting = "Рассылка сообщений отклонена❌\n\n"
error_with_markdown = "Невозможно обработать ваш текст в формате Markdown."
specify_word_with_error = " У вас ошибка в слове "
common_comands = "/help -- Список доступных команд\n" \
                "/support -- Обращение в Техподдержку\n" # need to fill
organizer_commands = "\nКоманды Организатора\n" \
                    "/room <номер комнаты> -- полная информация о комнате\n" \
                    "/departs -- Список отделов\n" \
                    "/depart <Отдел> -- Список организоторов из Отдела\n" \
                    "/depart_now <Отдел> -- Список отдела с активными точками каждого организатора\n" \
                    "/schedule <Фамилия Имя|tg_tag|vklink|номер телефон> -- расписание организатора\n" \
                    "/guest <Фамилия Имя|tg_tag|vklink|номер телефон> -- полная информация о госте\n" \
                    "/team <Номер команды> -- Спсиок участников из определенной команды\n"
secret_admin_commands = "\n⚠️ Секретные команды администратора\n" \
                        "/stats - bot stats\n" \
                        "/get_iss - list of unsolved issues\n" \
                        "/get_iss <number> - full description of issue with user's contact\n" \
                        "/delete_issues - delete all solved issues from DB\n"



support_start = "Опиши свою проблему ОДНИМ СООБЩЕНИЕМ или нажми /cancel если передумал"
support_send = "Ваша сообщение отправлено в техподдержки, с вами скоро свяжутся"
support_cancel = "Отправка сообщения в техподдержку отменена"
error_issue_arg = "Неверное значение аргумента. Убедитесь, что аргумент -- целое положительное число"
error_no_issue = "Нет сообщения с данным номером"
error_no_unsolved_issue = "Нет нерешенных проблем"
btn_not_fx = "Not solved"
btn_in_progress = "In Progress"
btn_fixed = "Fixed"
btn_all_from_user = "User's all issues"
no_unsolved_issue = "У пользователя нет нерешенных проблем"
issue_limit = "Ваши обращения дошли до нас. Не переживайте, с вами скоро свяжутся!"
users_issues_intro = "Все нерешенные проблемы пользователя:"

set_all_issues = "Fix user's all issues"
set_current_issue = "Fix only current"
set_all_success = "Статусы всех проблем user'a успешно изменены"

delete_issues_choose = "Вы уверены, что хотите удалить записи?"
delete_issues_success = "Записи успешно удалены"
delete_issues_declined = "Действие отменено"

room_not_found = "Комната с таким номером не найдена"
room_no_argument = "Вы забыли ввести номер комнаты.\n\nПример корректного ввода:\n/room 5"

depart_no_argument = "Вы забыли ввести Отдел \n\nПример корректного ввода:\n/depart админка"
depart_now_no_argument = "Вы забыли ввести Отдел \n\nПример корректного ввода:\n/depart_now админка"
depart_mistake = "Ошибка в названии Отдела"
list_of_orgs_from = "Список организоторов из отдела"

org_not_found = "Организатор по этим параметрам не найден\n"
guest_not_found = "Участник по этим параметрам не найден"
guest_no_arg = "Введите вместе с командой любой из следующих параметров:\n" \
                "Фамилия Имя | Тэг в ТГ(без @) | ссылка на ВК | Фамилия | Имя\n" \
                    "Например:\n/guest Иванов\n/guest gevorg_tsat"
guest_too_much_args = "Вы ввели слишком много данных\n"

team_no_arg = "Вы забыли ввести Номер команды.\n\nПример корректного ввода:\n/team 5"
team_not_found = "Команда с таким номером не найдена\n"