from tkinter import *
from mysqlcontroller import MysqlController

class MysqlGui:

    def __init__(self, passw) -> None:
        self.mysql = MysqlController(passw)
        
        self.gui = Tk()
        self.gui.title("Mysql visual interface")

        self.tables = ['AEROPORTO', 'VOO', 'TRECHO_VOO', 'INSTANCIA_TRECHO', 'TARIFA', 'TIPO_AERONAVE', 'PODE_POUSAR', 'AERONAVE', 'RESERVA_ASSENTO']
    
        self.menuBar = Menu(self.gui)
        tablemenu = Menu(self.menuBar)
        for t in self.tables:
            tablemenu.add_command(label=t, command=lambda x=t: self.reloadPage(x))
        self.menuBar.add_cascade(label='TABELAS', menu=tablemenu)
        self.menuBar.add_cascade(label='ATUAL: AEROPORTO')

        self.gui.config(menu=self.menuBar)

        return
    
    def createRows(self):
        self.rowcontainer = Frame(self.gui)
        self.rowcontainer.grid(row=0, column=0, sticky='ew')

        self.keysframe = Frame(self.rowcontainer)
        self.keysframe.grid(row=0, column=0, sticky='w')
        self.createColumnTitle('AEROPORTO')

        scroll = Scrollbar(self.rowcontainer, orient='vertical')
        self.rowlistbox = Listbox(self.rowcontainer, yscrollcommand=scroll.set, width=163)
        scroll.config(command=self.rowlistbox.yview)
        self.rowlistbox.grid(row=1, column=0)
        scroll.grid(row=1, column=1, rowspan=10, sticky='ns')
        
        rows = self.mysql.select('AEROPORTO')        
        for i, r in enumerate(rows):
            r = list(map(str, r))
            self.rowlistbox.insert(i, '| ' + ' | '.join(r) + ' |')
        
        return

    def createColumnTitle(self, table, col=[]):
        tablekeys = self.mysql.getcolumns(table)

        for w in self.keysframe.winfo_children():
            w.destroy()

        if col:
            for i, t in enumerate(tablekeys):
                if t in col:
                    Label(self.keysframe, text=t, relief='ridge', bd=5).grid(row=0, column=i)
            return

        for i, t in enumerate(tablekeys):
            Label(self.keysframe, text=t, relief='ridge', bd=5).grid(row=0, column=i)
        
        return


    def createOpt(self):
        optcontainer = Frame(self.gui)
        optcontainer.grid(row=1, column=0, sticky='nswe')

        self.entrycontainer = Frame(optcontainer)
        self.entrycontainer.grid(row=0, column=0, sticky='ns')

        self.createEntry('AEROPORTO')

        buttoncontainer = Frame(optcontainer)
        buttoncontainer.grid(row=0, column=1, sticky='ns')

        selectbutton = Button(buttoncontainer, text='SELECT', command=lambda :self.selectFrom(), relief='raised')
        selectbutton.grid(row=1, column=0, padx=10, pady=30)

        insertbutton = Button(buttoncontainer, text='INSERT', command=lambda :self.insertTable(), relief='raised')
        insertbutton.grid(row=2, column=0)

        updatebutton = Button(buttoncontainer, text='UPDATE', command=lambda :self.updateTable(), relief='raised')
        updatebutton.grid(row=1, column=1)

        deletebutton = Button(buttoncontainer, text='DELETE', command=lambda :self.deleteTable(), relief='raised')
        deletebutton.grid(row=2, column=1)

        aeronavePorAeroporto = Button(buttoncontainer, text='AERONAVE\nPOR AEROPORTO', command=lambda :self.aeronavePorAeroporto(), relief='raised')
        aeronavePorAeroporto.grid(row=1, column=2, padx=10)
        
        ultimaaeronave = Button(buttoncontainer, text='ULTIMA\nAERONAVE', command=lambda :self.ultimaaeronave(), relief='raised')
        ultimaaeronave.grid(row=2, column=2)

        trechoporaeroporto = Button(buttoncontainer, text='TRECHO VOO\nPOR AEROPORTO', command=lambda :self.trechoPorAeroporto(), relief='raised')
        trechoporaeroporto.grid(row=3, column=2, pady=15)

        helpbutton = Button(buttoncontainer, text='AJUDA', command=lambda :self.help(), relief='solid')
        helpbutton.grid(row=3, column=1)

        return

    def createEntry(self, table):
        tablekeys = self.mysql.getcolumns(table)

        for w in self.entrycontainer.winfo_children():
            w.destroy()

        Label(self.entrycontainer, text='insert/update', relief='ridge', bd=5).grid(row=0, column=0)
        self.insertentrys = {k: None for k in tablekeys}
        self.insertentrys['table'] = table
        for i, t in enumerate(tablekeys):
            Label(self.entrycontainer, text=t, bd=5).grid(row=i+1, column=0, sticky='w')
            s = StringVar()
            e = Entry(self.entrycontainer, textvariable=s)
            e.grid(row=i+1, column=1)
            self.insertentrys[t] = s

        Label(self.entrycontainer, text='where/select', relief='ridge', bd=5).grid(row=0, column=2)
        self.whereentrys = {k: None for k in tablekeys}
        for i, t in enumerate(tablekeys):
            Label(self.entrycontainer, text=t, bd=5).grid(row=i+1, column=2, sticky='w')
            
            s = StringVar()
            e = Entry(self.entrycontainer, textvariable=s)
            e.grid(row=i+1, column=3)
            self.whereentrys[t] = s

        self.wherecond = {}
        quantkeys = len(tablekeys)
        for i in range(quantkeys-1):
            s = StringVar()
            andopt = Radiobutton(self.entrycontainer, text='and', variable=s, value='and')
            oropt =  Radiobutton(self.entrycontainer, text='or', variable=s, value='or')
            noneopt = Radiobutton(self.entrycontainer, text='', variable=s, value=None)          
            noneopt.grid(row=i+1, column=4)
            andopt.grid(row=i+1, column=5)
            oropt.grid(row=i+1, column=6)
            
            iv = IntVar()
            includeopt = Checkbutton(self.entrycontainer, text='incluir', variable=iv, onvalue=1, offvalue=0)
            includeopt.grid(row=i+1, column=7)
            self.wherecond[tablekeys[i]] = (s, iv)
        iv = IntVar()
        includeopt = Checkbutton(self.entrycontainer, text='incluir', variable=iv, onvalue=1, offvalue=0)
        includeopt.grid(row=quantkeys, column=7)
        self.wherecond[tablekeys[-1]] = (StringVar(),iv)

        return

    def reloadPage(self, table=None, col=[], cond=[]):
        if table == None:
            table = self.menuBar.entrycget(2, 'label')
            table = table[7:]
        
        self.menuBar.entryconfig(2, label=f'ATUAL: {table}')

        self.createColumnTitle(table, col)

        self.rowlistbox.delete(0,self.rowlistbox.size())
        rows = self.mysql.select(table, collist=col, condition=cond)
        for i, r in enumerate(rows):
            r = list(map(str, r))
            self.rowlistbox.insert(i, '| ' + ' | '.join(r) + ' |')

        self.createEntry(table)

        return

    def reloadSpecialPage(self, title, rows, columns):
        self.menuBar.entryconfig(2, label=f'ATUAL: {title}')

        for w in self.keysframe.winfo_children():
            w.destroy()

        for i, t in enumerate(columns):
            Label(self.keysframe, text=t, relief='ridge', bd=5).grid(row=0, column=i)

        self.rowlistbox.delete(0,self.rowlistbox.size())
        for i, r in enumerate(rows):
            r = list(map(str, r))
            self.rowlistbox.insert(i, '| ' + ' | '.join(r) + ' |')

        return
    
    def insertTable(self):
        val = []
        col = []
        for key, value in self.insertentrys.items():
            if key == 'table':
                table = value
                continue

            if value.get() != '':
                col.append(key)
                val.append(value.get())
            
        self.mysql.insert(table, values=val, collist=col)
        self.reloadPage(table)

        return

    def updateTable(self):
        forset = []
        cond = []
        for key, value in self.insertentrys.items():
            if key == 'table':
                table = value
                continue

            if value.get() != '':
                forset.append(f'{key}={value.get()}')
            
        for key, value in self.whereentrys.items():
            if self.wherecond[key][1].get():
                cond.append(f'{key}={value.get()}')
                if self.wherecond[key][0].get() != '':
                    cond.append(self.wherecond[key][0].get())

        self.mysql.update(table, forset, cond)
        self.reloadPage(table)

        return

    def deleteTable(self):
        cond = []
        table = self.insertentrys['table']

        for key, value in self.whereentrys.items():
            if self.wherecond[key][1].get():
                cond.append(f'{key}={value.get()}')
                if self.wherecond[key][0].get() != '':
                    cond.append(self.wherecond[key][0].get())

        self.mysql.delete(table, condition=cond)
        self.reloadPage(table)

        return

    def selectFrom(self):
        col = []
        cond = []
        table = self.insertentrys['table']

        for key, value in self.wherecond.items():
            if value[1].get():
                col.append(key)

        for key, value in self.whereentrys.items():
            if value.get() != '':
                cond.append(f'{key}={value.get()}')
                if self.wherecond[key][0].get() != '':
                    cond.append(self.wherecond[key][0].get())

        self.reloadPage(table, col=col, cond=cond)

        return

    def aeronavePorAeroporto(self):
        cod = self.insertentrys['Codigo_aeroporto'].get()
        c, r = self.mysql.aeronavePorAeroporto(cod)
        
        self.reloadSpecialPage('Aeronave por aeroporto', r, c)

        return

    def ultimaaeronave(self):
        c, r = self.mysql.ultimaaeronave()
        self.reloadSpecialPage('Ultima aeronave a voar', r, c)
        
        return

    def trechoPorAeroporto(self):
        cod = self.insertentrys['Codigo_aeroporto'].get()
        c, r = self.mysql.trechoporaeroporto(cod)

        self.reloadSpecialPage('Trecho voo por aeroporto', r, c)

        return

    def help(self):
        helpbox = Toplevel()
        Label(helpbox, 
        text="""Select:Marcar caixas 'incluir' faz um select para aquelas colunas.
        Colocar valores nos campos 'where' faz um select para linhas com aqueles valores.
        """
        ).grid(row=0,column=0)
        
        Label(helpbox,
        text="""Insert:Os campos 'insert/select' podem estar vazios, basta lidar com chaves primarias.
        """
        ).grid(row=1, column=0)
        
        Label(helpbox,
        text="""Update:Nos campos 'insert/select' deve ser colocado os valores novos e
        nos campos 'where' deve ser colocado a condição dos campos a serem alterados.
        Depois marque a condição 'and' ou 'or' nas opções a esquerda de cada e
        marque as caixas 'incluir' para aplicar essas condições.
        Caso nenhuma condição seja aplicada, o update sera feito em todas as linhas.
        """,
        ).grid(row=2, column=0)
        
        Label(helpbox,
        text="""Delete:Nos campos 'where' deve ser dito as condições das linhas a seres excluidas
        e deve ser marcado as caixas 'incluir' para aplicar essas condições.
        Caso nenhuma condição seja aplicada, será deletada toda a tabela.
        """
        ).grid(row=3, column=0)

        Label(helpbox,
        text="""Aeronave por aeroporto: Mostra as companhias que possuem aeronaves pousando
        no aeroporto informado. 
        Para informa um aeroporto basta colocar seu codigo no campo 'codigo_aeroporto'
        na tabela 'AEROPORTO'.
        """
        ).grid(row=4, column=0)

        Label(helpbox,
        text="""Ultima aeronave: Mostra a ultima aeronave salva na tabela 'INSTANCIA_TRECHO'
        """
        ).grid(row=5, column=0)

        Label(helpbox,
        text="""Trecho voo por aeroporto: Mostra todos os trechos de voo que passam pelo
        aeroporto informado, seja chegada ou saida.
        Para informar um aeroporto basta colocar seu codigo no campo 'codigo_aeroporto'
        na tabela 'AEROPORTO'
        """
        ).grid(row=6, column=0)

    def open(self):
        self.createRows()
        self.createOpt()
        self.gui.mainloop()

        return