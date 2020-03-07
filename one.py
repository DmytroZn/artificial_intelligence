import re

act_minus = ['з\'їв', 'забрав', 'взяв', 'викинув']

fruits = [ 'груш', 'апельсин', 'яблук', 'ківі', 'мандарин']

fr = {
    'яблук' : ['яблуко', 'яблука', 'яблук'],
    'груш' : ['груша', 'груші', 'груш'],
    'апельсин' : ['апельсин', 'апельсини', 'апельсинів'],
    'мандарин' : ['мандарин', 'мандарини', 'мандаринів']
} 


class Begin:
    def __init__(self, orig_text):
        self.orig_text = orig_text
    
    def split_text(self):
        if len(re.split(r'[.?]', self.orig_text)) < 4:
            return 'У Вас повинно бути 3 і більше речення.'
        else:
            return First(self.orig_text).check_first()


class First:
    D_FIRST = dict()

    def __init__(self, text_first):
        self.text_first = text_first

    def check_first(self):
        t = self.text_first.split('. ')[0]
        if re.findall(r'на столі', t.lower()):
            text = t.split(' ')
            for k in fruits:
                try:
                    [self.D_FIRST.update({ k : int(text[text.index(i)-1])}) for i in text if re.search(k, i)]
                except ValueError:
                    return f'Можливо ви не поставили пробіл перед цифрою у реченні " {t}"'
            return Second(self.text_first).check_second()
        else:
            return 'Ви не уточнили де саме лежать предмети або предмети лежать не на столі.'


class Second(First):
    D_SECOND = dict()
    
    def __init__(self, text_second):
        self.text_second = text_second
    
    def check_second(self):
        t = self.text_second.split('. ')[1]
        if re.match(r'Хлопчик', t):
            t = t.split(' ')
            for i in act_minus:
                for k in t:
                    if i == k:
                        table_res = self.del_obj(t)
                        return Other(self.text_second).how_many(table_res)
        else:
            return 'Уточніть хто. Як правило це хлопчик і він повинен стояти попереду речення з великої літери.'

    def del_obj(self, t):
        D_TABLE = self.D_FIRST
        for k in fruits:
            [self.D_SECOND.update({ k :t[t.index(i)-1] }) for i in t if re.search(k, i)]
        for k1, v1 in self.D_FIRST.items():
            for k2, v2 in self.D_SECOND.items():
                if k1 == k2:
                    v3 = int(v1) - int(v2)
                    D_TABLE.update({k1:v3})
        return D_TABLE
    

class Other(Second):   
    
    def how_many(self, table_res):
        self.table_res = table_res
        t = self.text_second.split('. ')[2]
        list_ques = t.split('? ')
        return self.chec_ques(list_ques)

    def chec_ques(self, list_ques):

        for i in list_ques:
            res = re.match(r'Скільки', i)
            if res is not None:
                self.answer(i)
            else:
                return f'Скоріше за всього у вас помилка: "{i}" \n у слові "Скільки" '
        return ''

    def answer(self, get_mod):
        
        zero_answ = 'Можливо Хлопчик з\'їв більшу кількість фруктів чим можливо.'
        if re.findall(r'Скільки всього фруктів залишилось на столі', get_mod):
            sum_frut = sum([int(i) for i in self.table_res.values()])
            if sum_frut == 0:
                print(f'На столі не залишилось фруктів.')
            elif sum_frut == 1:
                print(f'На столі залишився {sum_frut} фрукт.')
            elif 2 <= sum_frut <= 4:
                print(f'На столі залишилось {sum_frut} фрукти.')
            elif sum_frut > 5:
                print(f'На столі залишилось {sum_frut} фруктів.')
            elif sum_frut < 0:
                print(zero_answ)

        for i in fruits:
            pattern = re.compile(f'Скільки залишилось {i} на столі')
            if pattern.findall(get_mod):
                if self.table_res.get(i) == 1:
                    print(f'На столі залишився {self.table_res.get(i)} {fr[i][0]}.')
                elif 2 <= self.table_res.get(i) <= 4:
                    print(f'На столі залишилось {self.table_res.get(i)} {fr[i][1]}.')
                elif self.table_res.get(i) > 5:
                    print(f'На столі залишилось {self.table_res.get(i)} {fr[i][2]}.')
                elif self.table_res.get(i) < 0:
                    print(zero_answ)

        if re.findall(r'Скільки всього фруктів з\'їв хлопчик', get_mod): 
            sum_frut = sum([int(i) for i in self.D_SECOND.values()])
            if sum_frut == 0:
                print(f'На столі не залишилось фруктів.')
            elif sum_frut == 1:
                print(f'Хлопчик з\'їв {sum_frut} фрукт.')
            elif 2 <= sum_frut <= 4:
                print(f'Хлопчик з\'їв {sum_frut} фрукти.')
            elif sum_frut > 5:
                print(f'Хлопчик з\'їв {sum_frut} фруктів.')
            elif sum_frut < 0:
                print(zero_answ)



task = str(input('Напишіть будь ласка задачу: '))
task = re.sub(r'`', '\'', task) 
b = Begin(task).split_text()
print(b)

