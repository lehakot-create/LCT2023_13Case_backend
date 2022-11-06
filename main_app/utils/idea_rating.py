"""
# Подсчет рейтинга идей и проектов на основание содержания текста комментариев
# Для работы необходимо установить следующие библиотеки:
#   torch torchvision torchaudio
#   transformers    
"""

import torch

from transformers import BertTokenizer, BertForSequenceClassification


# загружаем токен и модель
tokenizer = BertTokenizer.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')
model = BertForSequenceClassification.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')


# функция определения рейтинга комментария
def comment_rait(text):
    batch = tokenizer.encode(text, return_tensors='pt')
    outputs = model(batch)
    predict = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmin(predict, dim=1).numpy()
    return predicted[0]


# сейчас сгенерирован отдельный список комментариев, на проекте нужно будет этот список собирать из комментариев
comments = ['Очень интересная идея', "Плохо написанный проект", "Полное фуфло ваши идеи", "Редкое говно!",
            "Мне нравится Ваш подход!", "Очень хорошо", "Так держать!", "Вырви себе руки"]


# функция подсчета рейтинга идеи
def rating_idea(comments):
    idea_rating = 0
    for comment in comments:
        idea_rating += comment_rait(comment)
    return idea_rating
