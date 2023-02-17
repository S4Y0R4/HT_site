from flask import Blueprint, render_template
from contacts.forms import ContactsEditForm

contacts = Blueprint('contacts', __name__, template_folder='templates')


@contacts.route("/")
def my_contacts():
    form = ContactsEditForm()
    return render_template('contacts/my_contacts.html', title="Мои контакты")


# @contacts.route('/contacts_edit')
# def contacts_edit():
#     form = ContactsEditForm()
#     return render_template('contacts/contacts_edit.html', form=form, title='Редактирование моей контактной информации')
