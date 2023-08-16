#######################
Используемые модули
#######################

Здесь описаны все модели для базы данных, которые мы использовали

``class Worksheet (models.Model)`` - модель для хранения анкет. Хранит следующие параметры: title,
image, author, tags, description, likes, dislikes, date.

* метод ``save()`` - сохраняет данные анкеты


``class Chat (models.Model)`` - модель для хранения чата.

``class Message (models.Model)`` - Модель для хранения сообщений. Хранит следующие параметры: message,
author, recipient, date.

``class SocialMedia (models.Model)`` - модель для хранения социальных сетей пользователя. Хранит
следующие параметры: profile, instagram, vk, github, codewars.

``class Like (models.Model)`` - модель для хранения лайков

``class Dislike (models.Model)`` - модель для хранения дизлайка

``class Comment (models.Model)`` - модель для хранения комментариев к анкете. Хранит следующие
параметры: text_message, author, worksheet, date
