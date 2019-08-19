from django.shortcuts import render, redirect
from django.db import IntegrityError

from shop.views import HOME_META_DESCRIPTION
from .forms import ChatForm, MessageForm


SECTIONS = [
    ('product', 'Продукция', 'img/product_125px.png', [
        ('Какой наполнитель используется в продукции?',
         'Стандарт для нашей продукции является экологически чистый гранулированный пенополистирол. '
         'Главными его преимуществами являются гипоаллергенность и водооталкивающие свойства. '
         'Лишь спустя несколько лет активного использования пуфиков, бинбэгов и кресло-мешков наполнитель '
         'теряет начальную форму, но это легко исправить - наши кресло-мешки многоразовые и дополнить их можно '
         'у нас в магазине.'),
        ('Почему кресло-мешок сплюснутый при распаковке?',
         'Вся прелесть бескаркасной мебели заключается в отсутствии каркаса, что позволяет пуфикам, бинбэгам и '
         'кресло-мешкам подстроится под форму Вашего тела. При перевозке мы плотно упаковываем кресло-мешки для '
         'экономии пространства и исключения попадания пыли/влаги на материал, поэтому при распаковке товар может '
         'отличаться от изображений.'),
        ('Как почистить или постирать кресло-мешок?',
         'Мы используем только качественные материалы, благодаря чему любые загрязнения легко очистить. Достаточно '
         'простой мыльной воды с губкой и даже самые трудные пятна бесследно исчезнут. А если возникнет '
         'необходимость постирать полностью чехол, то с помощью молнии Вы можете открыть пуфик, бинбэг или '
         'кресло-мешок и достать второе дно с наполнителем, который необходимо будет пересыпать в любую емкость и '
         'можно смело помещать чехол в стиральную машину.'),
    ]),
    ('delivery', 'Доставка', 'img/truck_125px.png', [
        ('Сколько дней занимает доставка?',
         'Изготовление некоторых товаров требует 2-3 дней. Обычная доставка осуществляется в течение 3-8 дней, '
         'а быстрая доставка - в течение 1-2 дней. Доставка по городам Казахстана занимает от 1 до 8 дней.'),
        ('В какие города осуществляется доставка?',
         'Мы осуществляем доставку заказов в Алматы, Нур-Султан (Астана), Актау, Актобе, Атырау, Аксай, Акколь, '
         'Балхаш, Жезказган, Караганда, Кокшетау, Костанай, Кызылорда, Талдыкорган, Тараз, Темиртау, Уральск, '
         'Усть-Каменогорск, Павлодар, Петропавловск, Семей, Шымкент, Щучинск, Экибастуз и другие регионы.'),
    ]),
    ('payment', 'Оплата', 'img/money_125px.png', [
        ('Какие способы оплаты доступны?',
         'Вы можете оплатить покупку наличными, а также банковской картой через интернет.'),
        ('Как обеспечивается безопасность оплаты банковской картой?',
         'Оплата происходит через вебсайт банка АО ДБ "Альфа Банк", который обеспечивает полную '
         'безопасность оплаты банковской картой через интернет.'),
    ]),
    ('return', 'Возврат или замена', 'img/refresh_125px.png', [
        ('Как заменить продукцию?',
         'Если Вам не понравился цвет или Ваш товар оказался бракованным, то в течение 14-ти дней со дня получения '
         'заказа Вы можете написать нам письмо через интернет или обратиться к нам по указанному на сайте телефону.'),
        ('Как вернуть продукцию?',
         'Если Вы решили вернуть товар обратно, то в течение 14-ти дней со дня получения '
         'заказа Вы можете написать нам письмо через интернет или обратиться к нам по указанному на сайте телефону.'),
    ]),
]


def support_view(request):
    context = dict()
    context['sections'] = SECTIONS
    context['meta_description'] = ' '.join(
        [question[0] for section in SECTIONS for question in section[3]] + [HOME_META_DESCRIPTION]
    )

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
    context['meta_description'] = '{} {} {}'.format(question[0], question[1], HOME_META_DESCRIPTION)

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
