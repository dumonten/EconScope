import g4f
import re

class Gpt():
    # Configure request 
    REQUEST_TEMPLATE = "Проанализируй текст чека ниже и предоставь ответ исключительно в виде json файла (структура json должна соответствовать шаблону, запрещено \
    добавлять свои ключи. Также если значение для какого-то ключа неопределено, то допустимо испольование null в качестве значения. \
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

    # Configure gpt 
    g4f.debug.logging = False 
    g4f.debug.version_check = False 

    @staticmethod
    def ask(request, model): 
        response = g4f.ChatCompletion.create(
            model=model,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": request}],
        )
        return response
    
    @classmethod
    def receipt_ask(cls, receipt_data, is_gpt_version_4=True): 
        if is_gpt_version_4: 
            model = g4f.models.gpt_4
        else: 
            model = "gpt-3.5-turbo"
            
        request = cls.REQUEST_TEMPLATE.format(template_json=cls.template_json, categories=cls.categories, receipt_data=receipt_data)
        response = cls.ask(request, model)

        reg_res = re.search(r"```json(.*?)```", response, re.DOTALL)
        if reg_res:
            json_response = reg_res.group(1)
        else:
            json_response = ""
        
        return json_response