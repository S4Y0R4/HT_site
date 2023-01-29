from wtforms import Form, StringField, TextAreaField

class PostForm(Form):
    title = StringField('Название вакансии')
    city =StringField("Город")
    country =StringField("Страна")
    schedule =StringField("График")
    salary =StringField("Зарплата")
    contacts =StringField("Контакты")
    body = TextAreaField('Описание вакансии', render_kw={'class': 'form-control', 'rows': 15})
