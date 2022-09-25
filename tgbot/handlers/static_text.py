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
common_comands = "Список доступных команд\n" \
                "/support -- Обращение в Техподдержку\n" # need to fill
organizer_commands = "\nКоманды Организатора\n" \
                    "/depart <Отдел> -- список организаторов из указанного отдела\n" \
                    "/room <номер комнаты> -- полная информация о комнате\n" \
                    "/depart <Отдел> -- Список организоторов из Отдела\n" \
                    "/depart_now <Отдел> -- Список отдела с активными точками каждого организатора\n" \
                    "/schedule <Фамилия Имя|tg_tag|vklink|номер телефон> -- расписание организатора\n" \
                    "/guest <Фамилия Имя|tg_tag|vklink|номер телефон> -- полная информация о госте\n"
secret_admin_commands = "\n⚠️ Секретные команды администратора\n" \
                        "/stats - bot stats\n\n" \
                        "/get_iss - list of unsolved issues\n\n" \
                        "/get_iss <number> - full description of issue with user's contact\n\n" \
                        "/delete_issues - delete all solved issues from DB\n\n" \
                        "/delete_user <Tuple[arg1: str, arg2: str]> - забанить перечисленных юзеров по определенным причинам\n"\
                        "Пример: /delete_user @skuikness спам @ylptred возврат -> удалит пользователя с тегом @skuikness по причине спам и пользователя с тегом @ylptred по причине возврат билета\n" \
                        "Возможные значение arg2:\n" \
                        "спам\n" \
                        "возврат\n\n" \
                        "/get_logs now - получить логи\n\n" \
                        "/replace_org_tag <arg1: str, arg2: str> - заменить arg1 тег орга на arg2 тег орга\n" \
                        "Пример: /replace_org_tag @skuikness @ylptred -> заменит тег орга skuikness на ylptred\n\n" \
                        "/info_mailing < <arg1: str>, arg2: str> - отправить рассылку arg1 всем членам отдела arg2\n" \
                        "Пример: /info mailing <на входе нужно больше безов, выходят без курток> Безопасность -> отправит всем безам сообщение внутри кавычек < >\n\n" \
                        "Возможные значения arg2:\n" \
                        "Администрация - Коор + Зам Коора + Сервисный HR\n" \
                        "Конфликт - конфликт менеджер\n\n" \
                        "Далее: название отдела == значение arg2\n" \
                        "Админка\n" \
                        "Программа\n" \
                        "Игротехники\n" \
                        "Пиар\n" \
                        "Спонсорка\n" \
                        "Закупки\n" \
                        "Медиа\n" \
                        "Оформление\n" \
                        "Безопасность\n" \
                        "Площадка\n" \
                        "Финансы\n" \
                        "Атмосфера\n"



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

depart_no_argument = "Вы забыли ввести Отдел \n\nПример корректного ввода:\n /depart админка"
depart_mistake = "Ошибка в названии Отдела"
list_of_orgs_from = "Список организоторов из отдела"

org_not_found = "Организатор по этим параметрам не найден, возможно вы имели ввиду:\n"
guest_not_found = "Участник по этим параметрам не найден"
guest_no_arg = "Введите вместе с командой любой из следующих параметров:\n" \
                "Фамилия Имя | Тэг в ТГ(без @) | ссылка на ВК | Фамилия | Имя\n" \
                    "Например:\n/guest Иванов\n/guest gevorg_tsat"
guest_too_much_args = "Вы ввели слишком много данных\n"
