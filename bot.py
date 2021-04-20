import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import random as r
#Библиотека для JSON
import json
#Библиотеки для работы переводчика
from ibm_watson import LanguageTranslatorV3

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#Авторизация в сервисе переводчика
authenticator = IAMAuthenticator('API_IBM')
language_translator = LanguageTranslatorV3 \
    (version='2018-05-01',
     authenticator=authenticator)

# ID группы и Ключ доступа для вашего сообщества (Для BotLongPool требуется еще ID группы)

vk_group = ('id VK группы', 'API группы')

# Авторизируемся на сервере ВКонтакте используя ключ доступа

vk = vk_api.VkApi(token=vk_group[1])

# Подключаемся к BotLongpool

longpoll = VkBotLongPoll(vk, vk_group[0])

#Функция переводчика
def Translate(text, lang):
    language_translator.set_service_url \
        ('ссылка на IBM')
    languages = language_translator.list_languages().get_result()
    translation = language_translator.translate \
        (text=text,
         model_id=lang).get_result()
    trans = json.dumps(translation, indent=2, ensure_ascii=False)
    formated_trans = json.loads(trans)
    result = formated_trans['translations'][0]['translation']

    return result


# Ждем событие от сервера VK API


for event in longpoll.listen():
            voprosi = str(event)
            msg = {}
            if 'message_new' in voprosi:
                msg['text'] = event.obj['message']['text'] # Текст сообщения
                msg['user'] = str(event.obj['message']['from_id']) # User, который отправил сообщения
                msg['random_id'] = r.randint(-2147483648,2147483647)

                try:

                    # Переводим сообщение пользователя на русский язык.

                    answer = Translate(msg['text'], lang='ru-en')

                    if answer.lower() == msg['text'].lower():
                        # и его необходимо перевести на английский язык.

                        answer = Translate(msg['text'], lang='en-ru')
                    # Отправка сообщения пользователю через метод messages.send

                    vk.method('messages.send', {'user_id': msg['user'], 'random_id': msg['random_id'], 'message': answer})

                except Exception as e:

                    # Отлавливание каких-либо ошибок и отправка сообщения о том, что перевод не удался.

                    vk.method('messages.send', {'user_id': msg['user'], 'random_id': msg['random_id'], 'message': 'Error'})