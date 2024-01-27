import g4f
import re

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
print(g4f.Provider.Bing.params)  # Print supported args for Bing

# Using automatic a provider for the given model
# Streamed completion

template_json = '{ \
  "Товары": [ \
  { \
      "Наименование": "", \
      "Количество": float, \
      "Цена за единицу": float, \
      "Общая стоимость": float, \
      "Категория": "" ,\
      "Подкатегория": "" \
    }, \
  ], \
  "Наименование места покупки": "", \
  "Адрес места покупки": "", \
  "Время покупки": "", \
  "Имя кассира": "", \
  "Информация об оплате": { \
    "Всего без скидки": float, \
    "Общая скидка": float, \
    "Итого к оплате": float, \
    "Валюта": "", \
    "Способ оплаты": { \
        "Наличный расчет": { \
            "Получено": float, \
            "Сдача": float \
        }, \
        "Безналичный расчет": { \
            "Номер карты": "", \
            "Номер терминала": "" \
        } \
    } \
}'

categories = "\
1.Молочные продукты: Молоко и продукты из молока; Кисломолочные продукты; Сырные продукты \
2.Мясные продукты: Мясо и продукты из мяса; Птица и продукты из мяса птицы \
3.Рыбные продукты: Рыба и продукты из рыбы; Морепродукты \
4.Яйцо \
5.Масложировая продукция \
6.Хлебобулочные изделия \
7.Кондитерские изделия: Сахарные кондитерские изделия; Мучные кондитерские изделия \
8.Продукты пчеловодства \
9.Бакалейные товары: Мука и полуфабрикаты мучных изделий; Крупяные и бобовые изделия; Макаронные изделия; Вкусовые товары; Прочие бакалейные товары \
10.Безалкогольные напитки \
11.Алкогольные напитки: Крепкие алкогольные напитки; Слабоалкогольные напитки \
12.Табачные изделия \
13.Плодоовощная продукция: Овощи; Фрукты; Орехоплодовые; Грибы и грибная продукция \
14.Прочие продовольственные товары \
15.Текстильные товары \
16.Одежда \
17.Головные уборы \
18.Чулочно-носочные изделия \
19.Обувные товары \
20.Галантерейные товары \
21.Ювелирные изделия \
22.Биотовары: Цветы, растения; Семена; Домашние животные, птицы, рыбы; Корма для животных, птиц, рыб \
23.Нефтепродукты: Топливо; Масла и смазочные материалы \
24.Прочие непродовольственные товары \
25.Лекарственные средства \
26.Средства медицинского назначения  \
27.Медицинская техника и приборы \
28.Обозно-шорные изделия  \
29.Инструменты \
30.Электротовары \
31.Мебель \
32.Строительные материалы  \
33.Товары бытовой химии  \
34.Сельскохозяйственный и садово -огородный инструмент, средства малой механизации  \
35.Хозяйственные товары  \
36.Художественные товары  \
37.Средства связи  \
38.Фотокинотовары  \
39.Пиротехнические изделия бытового назначения развлекательного характера \
40.Игрушки \
41.Музыкальные товары  \
42.Товары для физической культуры, спорта и туризма (кроме спортивной одежды и обуви)  \
43.Автомобили, детали и принадлежности для  автомобилей \
44.Мотовелотовары \
45.Печатные издания  \
46.Школьно-письменные и канцелярские принадлежности, канцелярские машины \
47.Парфюмерно-косметические товары \
"

receipt_data = "'ПРИНОСИМ РАДОСТЬ' ОО \
УЛ. ГАГАРИНА, 62 \
Г. БОРИСОВ \
T. +37529765236 \
УНП: 193067319 \
ТЕРМИНАЛ: \
16747639 \
КАРТ-ЧЕК № \
0050 \
ОПЛАТА \
31.12.23 \
13:23:27 \
ТЕРМИНАЛ: \
16747639 \
КАРТОЧКА \
VISA \
**** **** **** 3942 \
25/03 \
СРОК ДЕЙСТВИЯ A0000000031010 \
AID \
СУММА (ИНТ) \
6. 30 \
ОДОБРЕНО \
КОД ОТВЕТА \
00 \
КОД АВТОРИЗАЦИИ: \
599522 \
RRN: \
336588695893 \
МЕТОД ВВОДА \
ОПЕРАЦИЯ БЕЗ ПИН-КОДА \
Подпись КЛиеНта нЕ требуеТся"

request = f"Проанализируй текст чека ниже и предоставь ответ исключительно в виде json файла (структура json должна соответствовать шаблону, запрещено \
добавлять свои ключи. Также если значение для какого-то ключа неопределено, то допустимо испольование null в качестве значения. \
Шаблон json: {template_json}). Категории товаров должны браться из существующего списка, если нет подходящей категории, то ставится null. \
Также есть подкатегории, но не у всех категорий. Они расположены за именем категории после знака ':' (двоеточие) в списке категорий. Если есть подкатегория, ее также можно указать \
в json-файле в отдельным ключом 'Подкатегория' у товаров. \
Список категорий: {categories}. \
Для обозначения валюты используй код валюты. Если в чеке нет информации о валюте, \
то верни  null. Текст чека: {receipt_data}"


# g4f.Provider.Bing / g4f.Provider.FakeGpt
# У BING вообще не вижу разницы между 3.5 и 4. У FakeGPT однозначно лучше 4. 

response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    # model=g4f.models.gpt_4, 
    provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": request}],
)

print(response)
print('-------------------------------------- JSON:')

result = re.search(r"```json(.*?)```", response, re.DOTALL)
if result:
    extracted_string = result.group(1)
    print(extracted_string)
else:
    print("No match found")
