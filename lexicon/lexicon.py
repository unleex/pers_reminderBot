LEXICON_RU: dict[str, str] = {
    'start_command_text': 'Привет! Это бот-напоминалка, с которым ты ничего не забудешь.' 
                        'Ты можешь создать расписание уроков, ДЗ и напоминания к ним! '
                        'Для ознакомления с функционалом отправь комманду /help',
            'info_command_text': 'Чтобы открыть главно меню, отправь "/menu".' 
                         'Чтобы посмотреть расписание на сегодня, так и '
                         'напиши: "Сегодня", или на завтра: "Завтра"\n'
                         'Чтобы добавить ДЗ, отправь сообщениеф формата:\n'
                         'дз &ltпредмет&gt - &ltзадание&gt\n'
                         'Пример:'
                         'дз англ уч. стр 15 номер 1\n'
                         '(подробнее в "Изменить расписание")',
            'edit_schedule_text': 'Измени или создай расписание'
                                'уроков.\n'
                                '1. Нажми на кнопку дня, на который хочешь'
                                'заполнить/изменить расписание\n'
                                '2. Пришли уроки, <b>каждый–с новой строки,без номеров и других доп. символов</b>!\n'
                                '3. Когда закончишь, не забудь нажать ✅'
                                'Создать',
            'edit_days_text': 'Присылай уроки, <b>каждый–с новой строки,'
                                'без номеров и других доп. символов</b>',
            'tasks_menu': 'Чтобы добавить задание, отправь сообщение формата:\n'
                'дз <i>&ltпредмет&gt &ltзадание&gt</i>\n'
                'Пример: <i>дз англ уч. стр 15 номер 1</i>\n'  
                'Чтобы поставить дедлайн на следующий урок, напишите в конце "след"'
                'Но можно добавить после "дз" день, и на него будет поставлен дедлайн\n'
                    'Пример: <i>дз пн англ уч. стр 15 номер 1</i>\n'
                'Также можно поставить на дату. Используйте формат ДД/ММ\n'
                    'Пример: <i>дз 25/01 англ уч. стр 15 номер 1</i>\n'
                'Чтобы уточнить время, напишите время в формате "ХХ:ХХ"'
                    'Пример: <i>дз  англ уч. стр 15 номер 1 пн 10:00</i>\n'
                    '<i>Используй двоеточие только для указания времени во избежание ошибок!</i>'
                '<b> Чтобы добавить дз, не обязательно находиться в этом меню!'
                'Ты можешь в любое время отправить боту дз и он добавит его!</b>\n'
                'Нажми на задание снизу, чтобы изменить/удалить его',
            'new_user_registered': 'Новый пользователь! Привет, name, спасибо, что выбрали этого бота! Удачного пользования)',
            'UnknownInstruction': 'Неверный формат сообщения.',
            'EmptySchedule': 'Здесь пока пусто(',
            'default_time_alert': 'Дедлайн сегодня',
            'pre_deadline_alert': "ДЕДЛАЙН СКОРО",
            "deadline_alert": "ДЕДЛАЙН"

}