import psycopg2

# Функция установки соединения
def connect(username1,password1):
    conn = psycopg2.connect(dbname='Storage', user=username1, 
                        password=password1, host='localhost')
    print('Connection established')
    return conn
#Возращает переменную соединения conn


#Фукнция выбора поле из таблиц
def select(cur):
    '''
    :param cur: Параметр cur необходим для того что бы мы могли работать с коннектом к базе и выполнять по нему скрипты
    :cur type: psycorg2.connect.cursor()
    :return: rows - результат селекта
    :rtype: list(list())
    '''
    fields = input('Введите какие поля нужно выбрать через запятую: ')
    table = input('Введите таблицу из которой нужно выбрать: ')
    where = input('Введите условия если необходимо, если оно не нужно просто нажмите Enter: ')
    print(table)
    print(fields)
    print(where)
    if where !='': # Условие на случий если нету блока where
        cur.execute('select '+fields+' from public.'+table+' where '+where)
    if where =='': # Условия на случай если есть блок where
        cur.execute('select '+fields+' from public.'+table)
    rows = cur.fetchall() # Обработка всех записей
    print(rows) # вывод всех записей
    print('Select done')
    return rows

#Фукнция вставки данных
def insert(cur):
    '''
    :param cur: Параметр cur необходим для того что бы мы могли работать с коннектом к базе и выполнять по нему скрипты
    :cur type: psycorg2.connect.cursor()
    :return: None (Функция вставляет данные, так что результат работы не является нужным для возвращения)
    :rtype: None
    '''
    table = input('Введите таблицу в которую нужно добавить запись: ')
    cur.execute("select column_name,data_type from information_schema.columns where column_name!='id' and table_name = '"+table+"'")# Выбираем все поля которые нам нужно вставить из служебной таблицы
    columns={}
    rows = cur.fetchall()
    column_names=''
    column_values=''
    for row in rows:# проходимся по каждому полю и даём заполнить значение
        if rows[1]=='integer':# Если тип данных числовой, нужно первести ввод в число
            columns[row[0]]=int(input('Введите значения для поля '+row[0]+' :'))
        else:# если тип данных текстовый просто оставляем input()
            columns[row[0]]=input('Введите значения для поля '+row[0]+' :')
    for keys,values in columns.items():# Делаем словарь для того что бы потом сформировать строки для insert'а
        if type(values)==int:
            column_names=column_names+str(keys)+","
            column_values=column_values+str(values)+','
        else:
            column_names=column_names+""+str(keys)+","
            column_values=column_values+"'"+str(values)+"',"
    insert_Sql="Insert into public."+table+"("+column_names[:-1:]+") values("+column_values[:-1:]+")"#Формируем запрос
    print(insert_Sql)
    cur.execute(insert_Sql)
    print('Данные вставлены')
    connection.commit()#Коммитим
    return None

#Функция удаления
def delete(cur):
    '''
    :param cur: Параметр cur необходим для того что бы мы могли работать с коннектом к базе и выполнять по нему скрипты
    :cur type: psycorg2.connect.cursor()
    :return: None (Функция удаляет данные, так что результат работы не является нужным для возвращения)
    :rtype: None
    '''
    table = input('Введите таблицу в которую нужно удалить запись: ')
    where = input('Введите условие удаления, если нужно почистить всю таблицу(крайне не рекомендуется) то просто ничего не вбивайте: ')
    #Обработка условий
    if where !='':
        delete_Sql="delete from public."+table+" where "+where
    else:
        delete_Sql="delete from public."+table
    cur.execute(delete_Sql)
    print('Запись удалена')
    connection.commit()
    return None

#Функция обновления записи
def update(cur):
    '''
    :param cur: Параметр cur необходим для того что бы мы могли работать с коннектом к базе и выполнять по нему скрипты
    :cur type: psycorg2.connect.cursor()
    :return: None (Функция Обновляет данные, так что результат работы не является нужным для возвращения)
    :rtype: None
    '''
    table = input('Введите таблицу в которую нужно обновить запись: ')
    where = input('Введите условие по которому надо обновить запись, если нужно обновить записи просто нажмите enter: ')
    set = input('Введите поле, и значение обновления в формате поле = значение: ')

    #обработка условий
    if where !='':
        update_sql="update public."+table+" set "+set+" where "+where
    else:
        update_sql="update public."+table+" set "+set
    cur.execute(update_sql)
    print('Запись обновлена')
    connection.commit()
    return None

if __name__=='__main__':
    
    #Ввод данных пользавателя
    userName=input('Введите имя пользователя: ')
    passWord=input('Введите пароль: ')
    connection = connect(userName,passWord)
    #Открытия курсора для выполнения скриптов
    cur = connection.cursor()
    #Меню для работы в терминале
    x=input('''Введите действие которое хотите сделать
    1 - Select
    2 - Insert
    3 - Delete
    4 - Update
    Exit - для выхода из программы
    Выбрать действие: ''')
    while x!='Exit':#Делаем цикл с выходом Exit, для того что бы можно было выполнять много различных действий в рамках 1ой сессии
        if x == '1':
            select(cur)
            x=input('''Введите действие которое хотите сделать
    1 - Select
    2 - Insert
    3 - Delete
    4 - Update
    Exit - для выхода из программы
    Выбрать действие: ''')
        elif x == '2':
            insert(cur)
            x=input('''Введите действие которое хотите сделать
    1 - Select
    2 - Insert
    3 - Delete
    4 - Update
    Exit - для выхода из программы
    Выбрать действие: ''')
        elif x == '3':
            delete(cur)
            x=input('''Введите действие которое хотите сделать
    1 - Select
    2 - Insert
    3 - Delete
    4 - Update
    Exit - для выхода из программы
    Выбрать действие: ''')
        elif x == '4':
            update(cur)
            x=input('''Введите действие которое хотите сделать
    1 - Select
    2 - Insert
    3 - Delete
    4 - Update
    Exit - для выхода из программы
    Выбрать действие: ''')
        else:
            x=input('Введите цифры из предложенных, если хотите выйти нажмите Exit: ')
    #Закрытия соединения, для уменьшения кол-ва одновременных сессий

    cur.close()
    connection.close()
