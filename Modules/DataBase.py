import pymysql
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from .Functions import tryex

class DataBase:
    def __connect(self):
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return connection
        
        
    @tryex
    def Execute(self, execute:str, args:tuple=None, commit:bool=False):
        '''
        `args` - Агрументы для запроса. Пример: cursor.execute(запрос, `args`)\n
        `commit` - сделать коммит после выполнения запроса
        '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                if args != None: cursor.execute(execute)
                else: cursor.execute(execute, args)
                
                if commit: connection.commit()
                return True
    
    
    @tryex
    def AddUser(self, login:str, password:str):
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                cursor.execute(f'INSERT INTO users (login, password) VALUES ("{login}", "{password}")')
                connection.commit()
                
                user = self.GetUser(login, 'users', 'login')
                return user
    
    @tryex
    def DeleteUser(self, user_id:int):
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
                connection.commit()
                
                return True
    
    @tryex
    def GetUser(self, tag:str, table:str, field:str):
        '''
        `tag` - чему должно равняться поле в бд (field)\n
        `table` - таблица\n
        `field` - по какому полю будет искать юзера\n
        Пример: SELECT * FROM `table` WHERE `field` = `tag`
        '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                cursor.execute(f'SELECT * FROM {table} WHERE {field} = "{tag}"')
                
                desc = cursor.description
                data = cursor.fetchone()
                
                user = self.__dataHandler(data, desc, 'one')

                return user
    
    
    @tryex
    def HasUser(self, tag, table, field):
        '''
        `tag` - чему должно равняться поле в бд (field)\n
        `table` - таблица\n
        `field` - по какому полю будет искать юзера\n
        Пример: SELECT * FROM `table` WHERE `field` = '`tag`'
        '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {table} WHERE {field} = "{tag}"')
                return True if cursor.fetchone() != None else False
    
    
    @tryex
    def GetHash(self, tag:str, table:str, field:str):
        '''
        `tag` - чему должно равняться поле в бд (field)\n
        `table` - таблица\n
        `field` - по какому полю будет искать юзера
        '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT password FROM {table} WHERE {field} = "{tag}"')
                hash = cursor.fetchone()[0]
                
                return hash
    
    
    @tryex
    def GetData(self, get:str, table:str, where:str='', sort_by='', mode:str = 'one'):
        ''' 
        `get` - что нужно получить\n
        `table` - из какой таблицы получать данные\n
        `where` - условие для данных\n
        `sort_by` - сортировать данные по какому-то полю\n
        mode = `one` || `all` || `many`\n
        '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                query = f'SELECT {get} FROM {table}'
                
                if where: query += f' WHERE {where}'
                if sort_by: query += f' ORDER BY {sort_by}'
                
                cursor.execute(query)
                
                desc = cursor.description
                data = []
                
                match mode:
                    case 'one': data = cursor.fetchone()
                    case 'all': data = cursor.fetchall()
                    case 'many': data = cursor.fetchmany()
                
                if data: data = self.__dataHandler(data, desc, mode)
                    
                return data
    
    
    @tryex
    def __dataHandler(self, data, desc, mode):
        res = []
        match mode:
            case 'one':
                res = [dict(zip([col[0] for col in desc], row)) for row in [data]][0]
                
                for key in res:
                    if res[key] == None: res[key] = ''
                
                
            case 'all': 
                res = [dict(zip([col[0] for col in desc], row)) for row in data]
                
                for index, el in enumerate(res):
                    for key in el.keys():
                        if res[index][key] == None: res[index][key] = ''
                
                   
                        
            case 'many': 
                res = [dict(zip([col[0] for col in desc], row)) for row in data]
                
                for index, el in enumerate(res):
                    for key in el.keys():
                        if res[index][key] == None: res[index][key] = ''
            
        print(res)       
        return res
    
    
    @tryex
    def InsertEmptyRow(self, tables:list|str):
        'Вставляет в базу данных пустые таблицы'
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                
                def insert():
                    cursor.execute(f"""SELECT * FROM {table} ORDER BY id DESC LIMIT 1""")
                    desc = cursor.description
                    
                    field = ''
                    
                    for i in range(len(desc)):
                        field += 'DEFAULT,'
                        
                    field = field[:len(field)-1]
                    
                    query = f"""INSERT INTO {table} VALUES ({field})"""
                    
                    cursor.execute(query)
            
                if type(tables) == str: 
                    insert(tables)
                    
                elif type(tables) == list:
                    for table in tables:
                        insert(table)
                
                connection.commit()
    

    @tryex
    def close(self):
        self.__connect().close()
        return True