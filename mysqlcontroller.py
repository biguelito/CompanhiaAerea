import re
import mysql.connector

class MysqlController:

    def __init__(self, passw):
        self.passoword = passw
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=self.passoword,
        database="COMPANHIA_AEREA")

        return

    def select(self, table, collist=[], condition=[]):
        mycursor = self.mydb.cursor()
            
        query = f"SELECT * FROM {table}"
        if collist:
            cols = ', '.join(collist)  
            query = f"SELECT {cols} FROM {table}"

        wherecond = None
        if condition:
            query += ' WHERE'
            wherecond = []
            
            for i, c in enumerate(condition):
                if i%2==0:
                    x = c.split('=')
                    query += f' {x[0]} = %s'
                    wherecond.append(x[1])

                else:
                    query += ' ' + c
        query += ';'
        
        mycursor.execute(query, wherecond)

        return list(map(list, mycursor.fetchall())) 


    def insert(self, table, values, collist=[]):
        mycursor = self.mydb.cursor()

        if type(values[0]) != type(list):
            values = [values]

        s = ', '.join(['%s' for i in range(len(values[0]))])
        query = f"INSERT INTO {table} VALUES ({s});"
        if collist:
            cols = ', '.join(collist)
            query = f"INSERT INTO {table} ({cols}) VALUES ({s});"

        mycursor.executemany(query, values)
        self.mydb.commit()
        
        return f"{mycursor.rowcount} record inserted"

    def delete(self, table, condition=[]):
        mycursor = self.mydb.cursor()

        query = f"DELETE FROM {table}"

        wherecond = None
        if condition:
            query += ' WHERE'
            wherecond = []
            
            for i, c in enumerate(condition):
                if i%2==0:
                    x = c.split('=')
                    query += f' {x[0]} = %s'
                    wherecond.append(x[1])

                else:
                    query += ' ' + c
        query += ';'

        mycursor.execute(query, wherecond)
        self.mydb.commit()

        return f"{mycursor.rowcount} record deleted"

    def update(self, table, values, condition=[]):
        mycursor = self.mydb.cursor()

        query = f'UPDATE {table}'

        query += ' SET'
        newvalues = []
        for v in values:
            x = v.split('=')
            query += f' {x[0]} = %s,'
            newvalues.append(x[1])
        query = query[:-1]
        setandwhere = newvalues

        if condition:
            query += ' WHERE'
            wherecond = []
            for i, c in enumerate(condition):
                    if i%2==0:
                        x = c.split('=')
                        query += f' {x[0]} = %s'
                        wherecond.append(x[1])

                    else:
                        query += ' ' + c
            setandwhere += wherecond
        query += ';'

        mycursor.execute(query, setandwhere)
        self.mydb.commit()

        return f"{mycursor.rowcount} record updated"

    def aeronavePorAeroporto(self, codAeroporto):
        mycursor = self.mydb.cursor()
        mycursor.execute(f'SELECT Companhia from TIPO_AERONAVE natural join PODE_POUSAR natural join AEROPORTO WHERE Codigo_aeroporto={codAeroporto} GROUP BY(Companhia);')

        c = [k[0] for k in mycursor.description]
        
        return c, list(map(list, mycursor.fetchall()))

    # TODO: criar novo select
    def ultimaaeronave(self):
        mycursor = self.mydb.cursor()
        mycursor.execute('SELECT * FROM AERONAVE WHERE Codigo_aeronave IN (SELECT Codigo_aeronave FROM INSTANCIA_TRECHO WHERE Data_instancia_trecho = (SELECT max(Data_instancia_trecho) FROM INSTANCIA_TRECHO));')

        c = [k[0] for k in mycursor.description]
        r = list(map(list, mycursor.fetchall()))

        return c, r
    
    def trechoporaeroporto(self, codaero):
        mycursor = self.mydb.cursor()
        mycursor.execute(f'CALL TrechoVooPorAeroporto({codaero});')

        c = [k[0] for k in mycursor.description]
        r = list(map(list, mycursor.fetchall()))
        
        self.mydb.close()
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=self.passoword,
        database="COMPANHIA_AEREA")

        return c, r

    def getcolumns(self, table):
        mycursor = self.mydb.cursor()   

        mycursor.execute(f'SELECT * FROM {table}')
        k = [k[0] for k in mycursor.description]
        mycursor.fetchall()
        return k
    