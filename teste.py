import tkinter as tk
import ttkbootstrap as ttkb
import json
import time
import webbrowser
from PIL import Image
from graphviz import Digraph
from tkinter import messagebox, Scrollbar, scrolledtext, ttk



class MainWindow:
    def __init__(self):
        self.JanelaPrincipal = ttkb.Window(themename='superhero')
        self.JanelaPrincipal.title('Data Structure Algorithm')
        self.JanelaPrincipal.resizable(False, False)
        # teste
        vLarguraTela = self.JanelaPrincipal.winfo_screenwidth()
        vAlturaTela = self.JanelaPrincipal.winfo_screenheight()
        vX = (vLarguraTela/2) - (780/2)
        vY = (vAlturaTela/2) - (350/2)
        self.JanelaPrincipal.geometry('%dx%d+%d+%d' % (780, 350, vX, vY))
        
        # fim teste
        self.TituloJanelaPrincipal = ttkb.Label(self.JanelaPrincipal, text="Organizador de Dados", font=('Gothic',30), style="info")
        self.TituloJanelaPrincipal.place(x=140, y=10)

        # Reinicializa o vetor a cada execução
        self.vetor_principal = []
        
        # Declara lista_vetor no escopo global
        self.lista_vetor = None

        # Carrega os valores do vetor a partir do arquivo JSON, se existir
        self.carregar_vetor()
        
        
        self.CampoTextoVariavel = ttkb.Entry(self.JanelaPrincipal, font=('Gothic',12), style='success',state='norma')
        self.CampoTextoVariavel.place(x=35, y=140, width=200)

        # FrameVetor será utilizado em várias partes, então é definido como atributo da classe
        self.FrameVetor = ttkb.Frame(self.JanelaPrincipal, style='warning', width=450, height=300)

        # Carrega botões e outros elementos gráficos
        self.configurar_elementos_gui()

    def carregar_vetor(self):
        try:
            with open('vetor.json', 'r') as arquivo:
                self.vetor_principal = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def salvar_vetor(self):
        with open('vetor.json', 'w') as arquivo:
            json.dump(self.vetor_principal, arquivo)

    def fecha_app(self):
        self.JanelaPrincipal.destroy()

    def configurar_elementos_gui(self):

        # Campo de inserção de valores dentro do vetor
        self.InsereVariavelVetor = ttkb.Label(self.JanelaPrincipal, text='Valor a ser inserido no vetor', font=('Gothic',14), style="info")
        self.InsereVariavelVetor.place(x=30, y=100)

        self.BotaoInsereVariavel = ttkb.Button(self.JanelaPrincipal, text='Inserir', style='success-outline', width=12, command=self.inserir_valor)
        self.BotaoInsereVariavel.place(x=250, y=140)

        self.BotaoObservarVetor = ttkb.Button(self.JanelaPrincipal, text='Olhar Vetor', style='warning-outline', width=15, command=self.abre_janela_observar_vetor)
        self.BotaoObservarVetor.place(x=450, y=140)

        self.BotaoRecriarVetor = ttkb.Button(self.JanelaPrincipal, text='Redefinir Vetor', style='danger-outline', width=15, command=self.redefinir_vetor)
        self.BotaoRecriarVetor.place(x=610, y=140)


        # Elementos gráficos

        # Botões adicionais para outros métodos de ordenação
        self.TelaFundoOrdenacao = ttkb.LabelFrame(self.JanelaPrincipal,text='Métodos de Ordenação', style='success', width=625,height=70)
        self.TelaFundoOrdenacao.place(x=30,y=270)
        
        self.OrdenacaoDeDados = ttkb.Button(self.JanelaPrincipal, text='Quick - Merge', style='warning',width=20, command=self.janela_quick_merge)
        self.OrdenacaoDeDados.place(x=40,y=295)
        
        self.OrdenacaoHash = ttkb.Button(self.JanelaPrincipal, text='Hash Table', style='success',width=20)
        self.OrdenacaoHash.place(x=250, y=295)
        
        self.OrdenacaoGrafo = ttkb.Button(self.JanelaPrincipal, text='Grafos', style='info', width=20, state='pressed')
        self.OrdenacaoGrafo.place(x=460,y=295)
        
        
        # ----------- FECHA APP
        self.FechaApp = ttkb.Button(self.JanelaPrincipal, text='Sair', style='danger-outline',width=10, command=self.fecha_app)
        self.FechaApp.place(x=665,y=305)
        #-----------------


    def abre_janela_observar_vetor(self):
        JanelaVetor = ttkb.Toplevel()
        JanelaVetor.title('Vetor')
        # JanelaVetor.geometry('550x300')
        JanelaVetor.resizable(False, False)
        vLarguraTela = JanelaVetor.winfo_screenwidth()
        vAlturaTela = JanelaVetor.winfo_screenheight()
        vX = (vLarguraTela/2) - (550/2)
        vY = (vAlturaTela/2) - (350/2)
        JanelaVetor.geometry('%dx%d+%d+%d' % (550, 350, vX, vY))

        def fecha_janela():
            JanelaVetor.destroy()
                

        TextoVetor = ttkb.Label(JanelaVetor,text='Vetor atual',style='warning',font=('Garamond',14))
        TextoVetor.place(x=20,y=10)

        LB_vetor = tk.Listbox(JanelaVetor, selectmode=tk.SINGLE, font=("Arial",12), exportselection=False,height=10, width=30)
        LB_vetor.place(x=20, y=40)
        
        # Adiciona os valores do vetor ao frame
        for i, valor in enumerate(self.vetor_principal):        
            LB_vetor.insert(tk.END, f" INDEX[{i}] = {valor}")
            
        # Adiciona uma barra de rolagem vertical
        scrollbar = ttkb.Scrollbar(JanelaVetor, orient="vertical", command=LB_vetor.yview,style='primary')
        scrollbar.place(x=350, y=40, height=245)

        LB_vetor.configure(yscrollcommand=scrollbar.set)            
        
        
        BotaoExcluir = ttkb.Button(JanelaVetor, text='Excluir', style='danger-outline', width=10,command= lambda: self.excluir_selecionado(LB_vetor))
        BotaoExcluir.place(x=420, y=40)

        BotaoVoltar = ttkb.Button(JanelaVetor, text='Voltar', style='primary-outline', width=10, command=fecha_janela)
        BotaoVoltar.place(x=420, y=250)
        
    def excluir_selecionado(self, listbox_vetor):
            # Obtém o índice do item selecionado na Listbox
        selected_index = listbox_vetor.curselection()

        if selected_index:
            # Converte a tupla para int
            selected_index = int(selected_index[0])

            # Remove o item do vetor
            del self.vetor_principal[selected_index]

            # Atualiza a Listbox
            listbox_vetor.delete(0, tk.END)
            for i, valor in enumerate(self.vetor_principal):
                listbox_vetor.insert(tk.END, f" INDEX[{i}] = {valor}")

            # Salva as alterações no vetor
            self.salvar_vetor()
        else:
            messagebox.showinfo("Seleção", "Selecione um item para excluir.")


    def redefinir_vetor(self):
        self.vetor_principal = []
        self.salvar_vetor()  # Salva a redefinição do vetor
        self.atualizar_frame_vetor()
        messagebox.showinfo("Sucesso!","Vetor redefinido com sucesso!!")

    def inserir_valor(self):
        valor = self.CampoTextoVariavel.get()
        try:
            valor = int(valor)
            self.vetor_principal.append(valor)
            self.salvar_vetor()  # Salva o vetor após cada inserção
            self.atualizar_frame_vetor()
            self.CampoTextoVariavel.delete(0, ttkb.END)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")

    def atualizar_frame_vetor(self):
        # Limpa o frame
        for widget in self.FrameVetor.winfo_children():
            widget.destroy()

        # Adiciona os valores do vetor ao frame
        for i, valor in enumerate(self.vetor_principal):
            ttkb.Label(self.FrameVetor, text=f"Vetor[{i}] = {valor}").pack()
        
    # Métodos de ordenação
    def janela_quick_merge(self):
        Janela_ordenacao_quick_merge = ttkb.Toplevel()
        Janela_ordenacao_quick_merge.title('Ordenação Quick-Merge')
        # Janela_ordenacao_quick_merge.geometry('550x200')
        Janela_ordenacao_quick_merge.resizable(False, False)
        
        vLarguraTela = Janela_ordenacao_quick_merge.winfo_screenwidth()
        vAlturaTela = Janela_ordenacao_quick_merge.winfo_screenheight()
        vX = (vLarguraTela/2) - (550/2)
        vY = (vAlturaTela/2) - (200/2)
        Janela_ordenacao_quick_merge.geometry('%dx%d+%d+%d' % (550, 200, vX, vY))
        
        
        # --------- Funções
        def fecha_janela():
            Janela_ordenacao_quick_merge.destroy()
        
                
        
        def janela_metodo_quick_sort():
            Janela_quick_sort = ttkb.Toplevel()
            Janela_quick_sort.title('Método Quick Sort')
            # Janela_quick_sort.geometry('600x600')
            Janela_quick_sort.resizable(False,False)
            
            vLarguraTela = Janela_quick_sort.winfo_screenwidth()
            vAlturaTela = Janela_quick_sort.winfo_screenheight()
            vX = (vLarguraTela/2) - (600/2)
            vY = (vAlturaTela/2) - (600/2)
            Janela_quick_sort.geometry('%dx%d+%d+%d' % (600, 600, vX, vY))

            def abre_vetor_inicial():
                self.abre_janela_observar_vetor()
            
            def fecha_janela_quick_sort():
                Janela_quick_sort.destroy()
                
            def atualizar_vetor_quick_sort(vetor):
                lista_vetor.delete(0, tk.END)
                for i, valor in enumerate(vetor):
                    lista_vetor.insert(tk.END, f" INDEX[{i}] = {valor}")
                
            def ordenar_quick_sort():
                copia_vetor = app.vetor_principal[:]  # Cria uma cópia do vetor original
                quick_sort(copia_vetor, 0, len(copia_vetor) - 1)  # Ordena a cópia
                atualizar_vetor_quick_sort(copia_vetor)  # Exibe a cópia ordenada

            def quick_sort(vetor, low, high):
                if low < high:
                    pi = particiona(vetor, low, high)
                    quick_sort(vetor, low, pi - 1)
                    quick_sort(vetor, pi + 1, high)


            def particiona(vetor, low, high):
                i = (low - 1)
                pivot = vetor[high]

                for j in range(low, high):
                    if vetor[j] <= pivot:
                        i = i + 1
                        vetor[i], vetor[j] = vetor[j], vetor[i]

                vetor[i + 1], vetor[high] = vetor[high], vetor[i + 1]
                return i + 1



            TextoOrdenacaoQuickSort = ttkb.Label(Janela_quick_sort, text="Método de Ordenação Quick Sort", style='info',
                                                font=('Garamond', 16))
            TextoOrdenacaoQuickSort.place(x=30, y=10)

            TextoEscolherMetodoOrdenacao = ttkb.Label(Janela_quick_sort,
                                                        text="Clique no botão para iniciar a ordenação utilizando Quick Sort.",
                                                        style="info", font=('Garamond', 12))
            TextoEscolherMetodoOrdenacao.place(x=20, y=60)

            BotaoIniciarOrdenacao = ttkb.Button(Janela_quick_sort, text='Iniciar Ordenação', style='success-outline', width=20,
                                                command=lambda: ordenar_quick_sort())
            BotaoIniciarOrdenacao.place(x=20, y=150)

            lista_vetor = tk.Listbox(Janela_quick_sort, selectmode=tk.SINGLE, font=("Arial", 12), exportselection=False, height=15,
                                    width=30)
            lista_vetor.place(x=20, y=200)

            BotaoVetorAtual = ttkb.Button(Janela_quick_sort, text='Vetor inicial', style='primary-outline',command=abre_vetor_inicial)
            BotaoVetorAtual.place(x=480,y=150)

            BotaoVoltar = ttkb.Button(Janela_quick_sort, text='Voltar', style='primary-outline', width=10,
                                    command=fecha_janela_quick_sort)
            BotaoVoltar.place(x=480, y=550)
            
            # Adiciona uma barra de rolagem à janela
            scrollbar = Scrollbar(Janela_quick_sort, orient="vertical")
            scrollbar.place(x=350, y=200, height=364)
            lista_vetor.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=lista_vetor.yview)
            
            
            
            
        def janela_metodo_merge_sort():
            Janela_merge_sort = ttkb.Toplevel()
            Janela_merge_sort.title('Método Merge Sort')
            # Janela_merge_sort.geometry('600x580')
            Janela_merge_sort.resizable(False,False)
            
            vLarguraTela = Janela_merge_sort.winfo_screenwidth()
            vAlturaTela = Janela_merge_sort.winfo_screenheight()
            vX = (vLarguraTela/2) - (600/2)
            vY = (vAlturaTela/2) - (580/2)
            Janela_merge_sort.geometry('%dx%d+%d+%d' % (600, 580, vX, vY))
        
            def fecha_janela_merge_sort():
                Janela_merge_sort.destroy()
            
            def merge_sort(vetor, low, high):
                if low < high:
                    mid = (low + high) // 2
                    merge_sort(vetor, low, mid)
                    merge_sort(vetor, mid + 1, high)
                    atualizar_vetor_merge_sort(vetor[low:high + 1])
                    time.sleep(1.25)
                    merge(vetor, low, mid, high)
                    atualizar_vetor_merge_sort(vetor[low:high + 1])
                    time.sleep(1.25)
                    
                    
                
            def merge(vetor, low, mid, high):
                n1 = mid - low + 1
                n2 = high - mid

                L = [0] * n1
                R = [0] * n2

                for i in range(n1):
                    L[i] = vetor[low + i]

                for j in range(n2):
                    R[j] = vetor[mid + 1 + j]

                i = j = 0
                k = low

                while i < n1 and j < n2:
                    if L[i] <= R[j]:
                        vetor[k] = L[i]
                        i += 1
                    else:
                        vetor[k] = R[j]
                        j += 1
                    k += 1

                while i < n1:
                    vetor[k] = L[i]
                    i += 1
                    k += 1

                while j < n2:
                    vetor[k] = R[j]
                    j += 1
                    k += 1

            def atualizar_vetor_merge_sort(vetor):
                lista_vetor.delete(0, tk.END)
                for i, valor in enumerate(vetor):
                    lista_vetor.insert(tk.END, f"[{i}] = {valor}")
                Janela_merge_sort.update()
            
            def gerar_e_exibir_arvore_merge_sort(vetor, low, high):
                
                # Código para gerar a árvore
                dot = Digraph(comment='Arvore Merge Sort')
                vetor_str = ', '.join(map(str, self.vetor_principal))
                dot.node('0', vetor_str)

                def construir_arvore(arr, parent_id):
                    if len(arr) == 1:
                        return

                    mid = len(arr) // 2
                    left = arr[:mid]
                    right = arr[mid:]

                    left_id = f'{parent_id}L'
                    right_id = f'{parent_id}R'
                    
                    # Formate a saída para remover os parênteses
                    left_str = ', '.join(map(str, left))
                    right_str = ', '.join(map(str, right))
                    
                    dot.node(left_id, left_str)
                    dot.node(right_id, right_str)
                    dot.edge(parent_id, left_id)
                    dot.edge(parent_id, right_id)

                    construir_arvore(left, left_id)
                    construir_arvore(right, right_id)

                construir_arvore(vetor, '0')
                
                # Após a árvore ser construída, adicione um nó representando o vetor ordenado
                
                dot.format = 'png'
                dot.render('merge_sort_arvore')
                
                messagebox.showinfo('Sucesso','O vetor foi ordenado com sucesso!!')
                abrir_arvore()
                
            def gerar_arvore_merge_sort():
                copia_vetor = self.vetor_principal.copy()
                merge_sort(copia_vetor, 0, len(copia_vetor) - 1)
                copia_vetor_arvore = self.vetor_principal.copy()
                gerar_e_exibir_arvore_merge_sort(copia_vetor_arvore, 0, len(copia_vetor_arvore) - 1)
                
            def abrir_arvore():
                # Abra a imagem da árvore diretamente
                webbrowser.open('merge_sort_arvore.png')
                           

            TextoOrdenacaoMergeSort = ttk.Label(Janela_merge_sort, text="Método de Ordenação Merge Sort", style='info',
                                                font=('Garamond', 16))
            TextoOrdenacaoMergeSort.place(x=30, y=10)

            TextoEscolherMetodoOrdenacao = ttk.Label(Janela_merge_sort,
                                                    text="Clique no botão para iniciar a divisão e conquista para o Merge Sort",
                                                    style="info", font=('Garamond', 12))
            TextoEscolherMetodoOrdenacao.place(x=20, y=60)

            BotaoIniciarOrdenacao = ttk.Button(Janela_merge_sort, text='Iniciar Ordenação', style='success-outline', width=20,
                                                command=gerar_arvore_merge_sort)
            BotaoIniciarOrdenacao.place(x=20, y=150)

            lista_vetor = tk.Listbox(Janela_merge_sort, selectmode=tk.SINGLE, font=("Arial", 12), exportselection=False, height=15,
                                    width=40)
            lista_vetor.place(x=20, y=200)

            BotaoVoltar = ttk.Button(Janela_merge_sort, text='Voltar', style='primary-outline', width=10,
                                    command=fecha_janela_merge_sort)
            BotaoVoltar.place(x=480, y=532)

            # Adicione uma barra de rolagem à janela
            scrollbar = tk.Scrollbar(Janela_merge_sort, orient="vertical")
            scrollbar.place(x=450, y=200, height=363)
            lista_vetor.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=lista_vetor.yview)
            
        
        
        
        # Botões e frames
        
        
        TituloOrdenacaoQuickMerge = ttkb.Label(Janela_ordenacao_quick_merge,text="Método de Ordenação Quick Sort - Merge Sort",style='info',font=('Garamond',16))
        TituloOrdenacaoQuickMerge.place(x=30,y=10)
        
        TextoEscolherMetodoOrdenacao = ttkb.Label(Janela_ordenacao_quick_merge,text="Abaixo, escolha um dos métodos disponíveis para realizar a \nordenação do vetor:",style="info",font=('Garamond',12))
        TextoEscolherMetodoOrdenacao.place(x=20,y=60)

        BotaoEscolherQuickSort = ttkb.Button(Janela_ordenacao_quick_merge,text='Quick-Sort',style='warning-outline',width=20,command=janela_metodo_quick_sort)
        BotaoEscolherQuickSort.place(x=20,y=150)
        
        BotaoEscolherMergeSort = ttkb.Button(Janela_ordenacao_quick_merge,text='Merge-Sort',style='warning-outline',width=20,command=janela_metodo_merge_sort)
        BotaoEscolherMergeSort.place(x=220,y=150)
    
        BotaoVoltar = ttkb.Button(Janela_ordenacao_quick_merge, text='Voltar', style='primary-outline', width=10, padding=4 , command=fecha_janela)
        BotaoVoltar.place(x=440, y=152)
        
        
    
    
    def janela_hash_table(self):
        Janela_hash = ttkb.Toplevel()
        Janela_hash.title('Método Merge Sort')
        # Janela_merge_sort.geometry('600x580')
        Janela_hash.resizable(False,False)
        
        vLarguraTela = Janela_hash.winfo_screenwidth()
        vAlturaTela = Janela_hash.winfo_screenheight()
        vX = (vLarguraTela/2) - (600/2)
        vY = (vAlturaTela/2) - (580/2)
        Janela_hash.geometry('%dx%d+%d+%d' % (600, 580, vX, vY))

    def janela_grafo(self):
        # Falta implementação
        pass
    
if __name__ == "__main__":
    app = MainWindow()
    app.JanelaPrincipal.mainloop()
