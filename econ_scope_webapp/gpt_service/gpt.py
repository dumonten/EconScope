import g4f
import re

# configure gpt
g4f.debug.logging = False
g4f.debug.version_check = False

# configure request
REQUEST_TEMPLATE = "Проанализируй текст чека ниже и предоставь ответ исключительно в виде json файла (структура json должна соответствовать шаблону, запрещено \
добавлять свои ключи. Также если значение для какого-то ключа неопределено, то допустимо испольование null в качестве значения. \
Если товары повторяются, объединяй их в один и увеличивай количество. \
Шаблон json: {template_json}). Категории товаров должны браться из существующего списка, если нет подходящей категории, то ставится null. \
Также есть подкатегории, но не у всех категорий. Они расположены за именем категории после знака ':' (двоеточие) в списке категорий. Если есть подкатегория, ее также можно указать \
в json-файле в отдельным ключом 'Подкатегория' у товаров. \
Список категорий: {categories}. Текст чека: {receipt_data}"

CATEGORIES_FILE_PATH = "./categories.txt"

TEMPLATE_JSON_FILE_PATH = "./template_json.txt"

with open(TEMPLATE_JSON_FILE_PATH, 'r') as file:
    template_json = file.read()

with open(CATEGORIES_FILE_PATH, 'r') as file:
    categories = file.readlines()

categories = list(map(lambda x: x.rstrip('\n'), categories))

# functions
def ask(receipt_data):
    request = REQUEST_TEMPLATE.format(template_json=template_json, categories=categories, receipt_data=receipt_data)
    print(request)
    response = g4f.ChatCompletion.create(
        #model=g4f.models.gpt_4,
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": request}],
    )
    reg_res = re.search(r"```json(.*?)```", response, re.DOTALL)
    if reg_res:
        json_response = reg_res.group(1)
    else:
        json_response = response
    return json_response

receipt_data = '000 "ЕВРОТОРІ \
ДОБРО ПОЖАЛОВАТЬ!!! \
Код чнП: 10116873 \
документ №00792134 \
ПЛАТЕЖНЫЙ ДОКУМЕНТ \
Чек продажи 149/1225 \
#. ООО "ЕВРОТОРГ", Магазин "ГРОшык" \
# \
г. минск, ул. Сурганова, \
57A \
.Режим работы с 09.00 до 22.00 \
# \
# \
＿ \
# \
1846950 Яйца куриные "OMEGGA" (C-1,карт \
341 \
17355 Сахар-песок (фасов) Слуцк 1 кг 2,46 \
469664 Пельмени "МЯСНЫЕ ПОДУШЕЧКИ" (боя \
3,39 \
469663 Пельмени "МЯСНЫЕ ПОДУШЕЧКИ" (гри \
3,35 \
983433 Хлеб тостовый "ЗЕРНОВОЙ"XXL 500г \
2,29 \
983433 Хлеб тостовый "ЗЕРНОВОЙ"XXL 500г \
2,29 \
1289377 Пакет-майка "ГРОШЫК" (40/10х65, \
0,39 \
568000 Молоко пит. у/паст. бут. 2,8% Мо \
1 85 \
727006 Сыр плавл, "ЛАСКОВОЕ ЛЕТО"(слив)4 \
3,39 \
#6519-4-721284======== \
# \
ООО ЕВРОТОРГ \
магазин\=Грошык= \
# \
# \
# \
Минск , ул., Сурганова, 57А \
# \
Терминал: SHJ31225 \
# \
КАРТ-ЧЕК: 270171 \
# \
*ДЛЯ КЛИЕНТА* \
# \
ОПЛАТА \
#16.10.2023 \
#КАРТА: **** **** **** 5775 \
#Mastercard PayPass \
#A0000000041010 \
#Сунма операции: \
22,82 BY \
#КОД АВТ.: 244570 RRN: 328912254727 \
#Чек 721284/UN=481837 \
КОД:О00 \
ОДОбрено \
12 \
:42 \
4: 44# \
# \
# \
# \
# \
итога к оплате \
Оплачено (БАНК КАРТА) \
Кассир Василькова Ольг \
В СККО/3Н СКНО: 110139623/300034420 \
3H 11608083 \
22,82 \
22.32 \
16-10-2023 12:43×20 \
Of37adef3bbf0db411e70,74 \
СПАСИБО ЗА Покупку \
'

ans = ask(receipt_data)

file_path = "./file.txt"
with open(file_path, "w") as file:
    file.write(ans)
