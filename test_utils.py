import re
import pytest
from constants import EMAIL_REG, PHONE_REG, URL_REG
from utils import collect_user_data, filter_data


@pytest.mark.parametrize(
    'url, expected',
    [
        ('https://github.com/ekaterina-python-developer', True),
        ('https://www.mysite.ru', True),
        ('https://sub.domain.example.org', True),
        ('http://unsafe.com', True),
        ('www.google.com', False),
        ('google.com', False),
        ('https://', False),
        ('ftp://files.com', False),
        ('https://localhost:8000', True),
    ],
)
def test_url_validation(url, expected):
    """Проверка валидации URL различных форматов."""
    match = re.match(URL_REG, url)
    assert bool(match) == expected


@pytest.mark.parametrize(
    'test_input, expected',
    [
        (
            'Свяжитесь с лучшим кандидатом: ekaterinaponurova@ya.ru',
            ['ekaterinaponurova@ya.ru'],
        ),
        ('ekaterinaponurova@ya.ru', ['ekaterinaponurova@ya.ru']),
        ('my.name+test@work.domain.org', ['my.name+test@work.domain.org']),
        ('нет email', []),
        (
            '1@mail.com и 2@mail.com и 3@mail.com',
            ['1@mail.com', '2@mail.com', '3@mail.com'],
        ),
    ],
)
def test_email_regex(test_input, expected):
    """Проверка поиска email-адресов в строке."""
    assert sorted(filter_data(EMAIL_REG, test_input)) == sorted(expected)


@pytest.mark.parametrize(
    'test_input, expected',
    [
        ('+7 (953) 177-08-46 (Екатерина, жду оффер)', ['+7 (953) 177-08-46']),
        ('+7 (953) 177-08-46', ['+7 (953) 177-08-46']),
        ('89531770846', ['89531770846']),
        ('79531770846', ['79531770846']),
    ],
)
def test_phone_regex(test_input, expected):
    """Проверка извлечения номеров телефонов в разных форматах."""
    assert filter_data(PHONE_REG, test_input) == expected


def test_filter_data_emails():
    """Тест корректности фильтрации списка email из текста."""
    text = 'Свяжитесь с лучшим кандидатом: ekaterinaponurova@ya.ru или katya.ponurova@mail.ru'
    expected = ['ekaterinaponurova@ya.ru', 'katya.ponurova@mail.ru']
    assert sorted(filter_data(EMAIL_REG, text)) == sorted(expected)


def test_filter_data_no_emails():
    """Проверка при отсутствии email в тексте."""
    assert filter_data(EMAIL_REG, 'текст') == []


def test_collect_user_data():
    """Проверка уникальных данных пользователей."""
    fake_items = [
        {'emails': ['ekaterinaponurova@ya.ru'], 'phones': ['89531770846']},
        {'emails': ['ekaterinaponurova@ya.ru'], 'phones': ['79531770846']},
    ]
    result = collect_user_data(fake_items, 'emails')
    assert result == ['ekaterinaponurova@ya.ru']


def test_collect_user_data_robustness():
    """Тест устойчивости сбора данных к неполным словарям."""
    bad_items = [
        {'emails': ['ekaterinaponurova@ya.ru']},
        {'phones': ['89531770846']},
        {},
    ]
    result = collect_user_data(bad_items, 'emails')
    assert result == ['ekaterinaponurova@ya.ru']


def test_developer_contacts():
    """Тест на извлечение контактов самого лучшего кандидата!"""
    resume_text = 'Пишите в ТГ: @ekaterina_python_developer, почта: ekaterinaponurova@ya.ru'
    emails = filter_data(EMAIL_REG, resume_text)
    assert 'ekaterinaponurova@ya.ru' in emails
