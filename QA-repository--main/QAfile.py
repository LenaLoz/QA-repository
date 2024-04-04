
#basic_op = lambda o, v1, v2: eval("{}{}{}".format(v1, o, v2))
#basic_op = lambda o,a,b: eval(str(a)+o+str(b))
#print(basic_op('-', 10, 3))
def find_total_pages(total_sum):
    n = 1  # Начинаем с первой страницы
    while total_sum - n >= 0:
        total_sum -= n  # Уменьшаем общую сумму на номер текущей страницы
        n += 1  # Переходим к следующей странице
    return n

# Сумма всех номеров страниц равна 1095
total_pages = find_total_pages(1095)
print("Общее количество страниц в книге:", total_pages)

