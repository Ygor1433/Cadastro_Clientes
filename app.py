from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import  TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do cliente')

        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'Telefone: ')
        self.c.drawString(50, 610, 'Endereço: ')

        self.c.setFont("Helvetica", 16)
        self.c.drawString(120, 700 ,'00' + self.codigoRel)
        self.c.drawString(110, 670 , self.nomeRel)
        self.c.drawString(130, 640 , self.foneRel)
        self.c.drawString(135, 610 , self.cidadeRel)

        self.c.rect(20, 580, 550, 170, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

#Back End
class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect('clientes.bd')
        self.cursor = self.conn.cursor(); print('Conectando ao Banco')
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando ao Banco')
    def montaTabelas(self):
        self.conecta_bd()
        # Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                fone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit(); print('Banco criado')
        self.desconecta_bd(); print()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, fone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, fone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, fone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, [self.codigo])
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, fone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()

#Front End
class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.botoes_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title('Cadastro de Clientes')
        self.root.configure(background='#5F9EA0')
        self.root.geometry('800x500')
        self.root.resizable(True, True)
        self.root.maxsize()
    def frames_da_tela(self):  # Criando abas na tela
        self.frame_1 = Frame(self.root, bd=4, bg='#98FB98'  # Cor da aba
                             , highlightbackground='white'  # Cor borda da aba
                             , highlightthickness=3  # Dimenção da aba
                             )
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.38)  # Criando aba na tela

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='white', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.42, relwidth=0.96, relheight=0.55)
    def botoes_frame1(self):

        #Caixa de botoes
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='#5F9EA0', highlightbackground='#2F4F4F',
            highlightthickness=3)
        self.canvas_bt.place(relx=0.115, rely=0.1, relwidth=0.24, relheight=0.2)

        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='#5F9EA0', highlightbackground='#2F4F4F',
                                highlightthickness=3)
        self.canvas_bt.place(relx=0.605, rely=0.1, relwidth=0.37, relheight=0.2)


        # Botao limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd= 0, bg='#5F9EA0', fg='white',
                                activeforeground='#5F9EA0',
                                font=('verdana', 8 , 'bold'), command=self.limpa_cliente,)
        self.bt_limpar.place(relx= 0.24, rely=0.15, relwidth=0.1, relheight= 0.1) #Posição do botão

        # Botao buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd= 0, bg='#5F9EA0',fg='white',
                                activeforeground='#5F9EA0',
                                font=('verdana', 8 , 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.13, rely=0.15, relwidth=0.1, relheight=0.1)

        # Botao novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd= 0, bg='#5F9EA0', fg='white',
                              activeforeground='#5F9EA0',
                              font=('verdana', 8 , 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.62, rely=0.15, relwidth=0.1, relheight=0.1)

        # Botao alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd= 0, bg='#5F9EA0',fg='white',
                                 activeforeground='#5F9EA0',
                                 font=('verdana', 8 , 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.74, rely=0.15, relwidth=0.1, relheight=0.1)

        # Botao Apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd= 0, bg='#5F9EA0',fg='white',
                                activeforeground='#5F9EA0',
                                font=('verdana', 8 , 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.86, rely=0.15, relwidth=0.1, relheight=0.1)

    #Criação da label e entrada do codigo

        #Codigo Label
        self.lb_codigo = Label(self.frame_1, text='Código', background='#98FB98')
        self.lb_codigo.place(relx=0.01, rely=0.01)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.01, rely=0.14, relwidth=0.1)

        #Nome Label
        self.lb_nome = Label(self.frame_1, text='Nome', background='#98FB98')
        self.lb_nome.place(relx=0.01, rely=0.3)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.01, rely=0.45, relwidth=0.64)

        #Telefone Label
        self.lb_fone = Label(self.frame_1, text='Telefone', background='#98FB98')
        self.lb_fone.place(relx=0.01, rely=0.58)

        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx=0.01, rely=0.7, relwidth=0.2)

        #Cidade Label
        self.lb_cidade = Label(self.frame_1, text='Endereço', background='#98FB98')
        self.lb_cidade.place(relx=0.25, rely=0.58)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.25, rely=0.7, relwidth=0.4)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1','col2',
                                                                      'col3','col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Codigo')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')

        self.listaCli.column('#0', width=-40)
        self.listaCli.column('#1', width=20)
        self.listaCli.column('#2', width=120)
        self.listaCli.column('#3', width=100)
        self.listaCli.column('#4', width=260)

        self.listaCli.place(relx=-0.001, rely=0.03, relwidth=0.97, relheight=0.95)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical', background='#98FB98' )
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.97, rely=0.03, relwidth=0.035, relheight=0.95)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label = "Relatorios", menu= filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu.add_command(label="Limpa Cliente", command= self.limpa_cliente)

        filemenu2.add_command(label="Ficha Cliente", command=self.geraRelatCliente)

Application()