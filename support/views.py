from django.shortcuts import render, redirect
from django.db import IntegrityError

from .forms import ChatForm, MessageForm


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


def chat_view(request):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        message_form = MessageForm(request.POST)

        if chat_form.is_valid() and message_form.is_valid():
            chat = chat_form.save(commit=False)
            chat.user = user
            try:
                chat.save()
            except IntegrityError:
                pass
            else:
                message = message_form.save(commit=False)
                message.chat = chat
                try:
                    message.save()
                except IntegrityError:
                    pass
                else:
                    return render(request, 'accounts/success.html', context={
                        'title': 'Готово',
                        'lines': [
                            'Ваше сообщение успешно отправлено.',
                            'Проверьте Ваше сообщение в разделе "Мои сообщения".',
                        ],
                    })
    else:
        chat_form = ChatForm()
        message_form = MessageForm()

    context = dict()
    context['chat_form'] = chat_form
    context['message_form'] = message_form

    return render(request, 'support/chat.html', context=context)
