from mysqlcontroller import MysqlController

if __name__ == "__main__":

    mysql = MysqlController('SUA SENHA AQUI')
    
    # EXEMPLOS DE SELECT==================================================================
    # print('\nselect *')
    # r = mysql.select("RESERVA_ASSENTO")
    # for i in r:
    #     print(i)
    
    # print('\nselect com colunas especificas')
    # columns = ['Numero_voo', 'Numero_trecho', 'Data_reserva_assento', 'Nome_cliente']
    # r = mysql.select('RESERVA_ASSENTO', collist=columns)
    # for i in r:
    #     print(i)

    # print('\nselect com colunas e condição(es)')
    # columns = ['Numero_voo', 'Numero_trecho', 'Nome_cliente', 'Telefone_cliente']
    # conditions = ['Numero_voo=2','OR', 'Telefone_cliente=5463311212']
    # r = mysql.select('RESERVA_ASSENTO', collist=columns, condition=conditions)
    # for i in r:
    #     print(i)
    

    # EXEMPLOS DE INSERT==================================================================
    # print('\ninsert unico em todas as colunas')
    # value = ['3', '3', '2021-02-05', '40', 'Linda Silva 2', '5463311213']
    # r = mysql.insert('RESERVA_ASSENTO', values=value)
    # print(r)

    # print('\ninsert unico em algumas colunas')
    # value = ['3', '3', '2021-02-05', '41', 'Linda Silva 3']
    # col = ['Numero_voo', 'Numero_trecho', 'Data_reserva_assento', 'Numero_assento', 'Nome_cliente']
    # r = mysql.insert('RESERVA_ASSENTO', values=value, collist=col)
    # print(r)

    # print('\ninsert multiplo em todas as colunas')
    # value = [['3', '3', '2021-02-05', '42', 'Linda Silva 4', '5463311214'],
    #          ['3', '3', '2021-02-05', '43', 'Linda Silva 5', '5463311215']]
    # r = mysql.insert('RESERVA_ASSENTO', values=value)
    # print(r)

    # print('\ninsert multiplo em algumas colunas')
    # value = [['3', '3', '2021-02-05', '44', 'Linda Silva 6'],
    #          ['3', '3', '2021-02-05', '45', 'Linda Silva 7']]
    # col = ['Numero_voo', 'Numero_trecho', 'Data_reserva_assento', 'Numero_assento', 'Nome_cliente']
    # r = mysql.insert('RESERVA_ASSENTO', values=value, collist=col)
    # print(r)


    # EXEMPLOS DE UPDATE==================================================================
    # print('\nupdate com condiçao')
    # forset = ['Numero_voo=3', 'Numero_trecho=3']
    # con = ['Numero_voo=2', 'and', 'Numero_trecho=2']
    # r = mysql.update("RESERVA_ASSENTO", forset, con)
    # print(r)

    # print('\nupdate sem condiçao')
    # forset = ['Numero_voo=3', 'Numero_trecho=3']
    # r = mysql.update("RESERVA_ASSENTO", forset)
    # print(r)


    # EXEMPLOS DE DELETE==================================================================
    # print('\nexemplo de delete com condição')
    # conditions = ['Numero_voo=3', 'and', 'Nome_cliente=Linda Silva']
    # r = mysql.delete('RESERVA_ASSENTO', condition=conditions)
    # print(r)
   
    # print('\ndelete em toda a tabela')
    # r = mysql.delete('RESERVA_ASSENTO')
    # print(r)



