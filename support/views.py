from django.shortcuts import render, redirect
from django.db import IntegrityError

from pufiki190630.utilities import get_form_input_value, is_recaptcha_valid
from accounts.utilities import get_existing_user
from orders.forms import AnonymousUserForm
from .forms import MessageForm


SECTIONS = [
    ('product', 'Продукция', 'img/product_125px.png', [
        ('Какой наполнитель используется в продукции?', 'Да'),
        ('Почему кресло-мешок сплюснутый при распаковке?', 'Да'),
        ('Как почистить или постирать кресло-мешок?', 'Да'),
    ]),
    ('delivery', 'Доставка', 'img/truck_125px.png', [
        ('Сколько дней занимает доставка?', 'Да'),
        ('В какие города осуществляется доставка?', 'Да'),
    ]),
    ('payment', 'Оплата', 'img/money_125px.png', [
        ('Какие способы оплаты доступны?', 'Да'),
        ('Как обеспечивается безопасность оплаты банковской картой?', 'Да'),
    ]),
    ('return', 'Возврат или замена', 'img/refresh_125px.png', [
        ('Как заменить продукцию?', 'Да'),
        ('Как вернуть продукцию?', 'Да'),
    ]),
]


def support_view(request):
    context = dict()
    context['sections'] = SECTIONS

    return render(request, 'support/support.html', context=context)


def question_view(request, **kwargs):
    section_name = kwargs['section_name']
    question_index = kwargs['question_index']

    for section in SECTIONS:
        if section[0] == section_name:
            break
    else:
        return redirect('support:support')

    section_questions = section[3]

    try:
        question_index = int(question_index)
        question = section_questions[question_index]
    except (ValueError, IndexError):
        return redirect('support:support')

    context = dict()

    context['sections'] = SECTIONS
    context['section'] = section

    context['question_index'] = question_index
    context['question'] = question[0]
    context['answer'] = question[1]

    return render(request, 'support/question.html', context=context)


def message_view(request):
    user = request.user

    if request.method == 'POST':
        message_user = None
        if user.is_anonymous:
            form_email = get_form_input_value(request, 'email')
            existing_nonactive_user = get_existing_user(form_email, False)
            anonymous_user_form = AnonymousUserForm(request.POST, instance=existing_nonactive_user)
            if anonymous_user_form.is_valid():
                try:
                    message_user = anonymous_user_form.save()
                except IntegrityError:
                    message_user = None
        else:
            message_user = user
            anonymous_user_form = None

        message_form = MessageForm(request.POST)

        if message_user and message_form.is_valid() and (user.is_authenticated or is_recaptcha_valid(request)):
            message = message_form.save(commit=False)
            message.user = message_user
            message.save()

            return render(request, 'accounts/success.html', context={
                'body': 'Ваше сообщение успешно отправлено. <br> Наш менеджер скоро свяжется с Вами.'
            })
    else:
        anonymous_user_form = AnonymousUserForm() if user.is_anonymous else None
        message_form = MessageForm()

    context = dict()
    context['anonymous_user_form'] = anonymous_user_form
    context['message_form'] = message_form

    return render(request, 'support/message.html', context=context)
