import requests
from bs4 import BeautifulSoup


def test(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.status_code)
        # Получаем содержимое страницы
        page_content = response.content

        # Создаем объект BeautifulSoup для парсинга страницы
        soup = BeautifulSoup(page_content, 'lxml')
        print(response.text)
        # Находим элементы с заданным классом
        elements = soup.find_all(class_='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x1cy8zhl xyamay9')
        print(len(elements))
        # Выводим найденные данные
        for element in elements:
            print(element.text)
    else:
        print('Ошибка при получении страницы:', response.status_code)

# test('https://www.facebook.com/anastasia.yakovenko.31')
        
# x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq  ссылка на человека после нажатия глянуть все лайки
# x1rg5ohu класс для ссылки с href