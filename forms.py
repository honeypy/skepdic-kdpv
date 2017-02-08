from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, ValidationError, TextAreaField, SelectField, StringField
import imghdr

class UploadForm(Form):
    a = '#СловарьСкептика'
    b = '#новости'
    c = '#статьи'
    d = '#видео'
    e = '#цитаты'
    f = '#БиблиотекаСкептика'
    g = '#юмор'
    h = '#инфографика'
    j = '#репортаж'
    k = '#интервью'
    l = '#фрики'
    m = '#логика'
    n = '#анонсы'
    o = '#деградат'
    p = '#конкурс'
    r = '#познавательный'
    q = '#переводы'

    image_file_file = FileField('Загрузить картинку')
    image_file = StringField('Ссылка на картинку')
    tag = SelectField('Тег', choices=[(a, a), (b, b), (c, c), (d, d), (e, e), (f, f), (g, g), (h, h), (j, j), (k, k), (l, l),
                               (m, m), (n, n), (o, o), (p, p), (r, r), (q, q)])
    title = TextAreaField('Заголовок')
    subtitle = TextAreaField('Подзаголовок')
    submit = SubmitField('Создать картинку')
'''
    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() not in ('.jpg','.png'):
            raise ValidationError('Invalid file extension')
        if imghdr.what(field.data) != 'jpeg' and imghdr.what(field.data) != 'png':
            raise ValidationError('Invalid image format')
'''

class AnnounceUploadForm(Form):
    bckgrnd_file = FileField('Загрузить картинку фона')
    avatar_file = FileField('Загрузить портрет лектора')
    title = TextAreaField('Название мероприятия')
    date = TextAreaField('Дата')
    place = TextAreaField('Место')
    themes_content = TextAreaField('Основные темы')
    submit = SubmitField('Создать картинку')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() not in ('.jpg', '.png'):
            raise ValidationError('Invalid file extension')
        if imghdr.what(field.data) != 'jpeg' and imghdr.what(field.data) != 'png':
            raise ValidationError('Invalid image format')