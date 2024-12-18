import threading
import tkinter as tk
import time
import datetime

class Hospede:
    def __init__(self, id, canal, ttv, td):
        self.id = id
        self.canal = canal
        self.canalPreferido = canal
        self.ttv = ttv
        self.td = td
        self.thread = threading.Thread(target=self.executar)
        self.status = "Descansando"
        self.log = []
        self.parar = False

    def executar(self):
        global semaforo, canal_atual
        while not self.parar:
            self.status = "Bloqueado"
            self.log.append((time.time(), "Bloqueado"))
            atualizar_interface()
            semaforo.acquire()
            canal_atual = self.canal
            atualizar_interface()
            self.status = "Assistindo TV"
            self.log.append((time.time(), "Assistindo TV"))
            atualizar_interface()
            time.sleep(self.ttv)
            semaforo.release()
            self.status = "Descansando"
            self.log.append((time.time(), "Descansando"))
            atualizar_interface()
            time.sleep(self.td)
            atualizar_interface()

# Variáveis globais
semaforo = threading.Semaphore(1)
canal_atual = 0
hospedes = []
max_canais = 0
# Interface gráfica
root = tk.Tk()
root.title("Simulação da Televisão")


def inicializar():
    global max_canais

    # Cria uma caixa de diálogo para obter o número máximo de canais
    def obter_max_canais():
        try:
            valor = int(entrada.get())
            if valor > 0:
                global max_canais
                max_canais = valor
                root.destroy()  # Fecha a caixa de diálogo
            else:
                tk.messagebox.showerror("Erro", "O número de canais deve ser maior que zero.")
        except ValueError:
            tk.messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")

  
    root.title("Configuração de Canais")

    label = tk.Label(root, text="Digite o número máximo de canais:")
    label.pack()

    entrada = tk.Entry(root)
    entrada.pack()
    botao = tk.Button(root, text="Confirmar", command=obter_max_canais)
    botao.pack()

    root.wait_window()

inicializar()

def criar_hospede():
    top = tk.Toplevel()
    top.title("Adicionar Novo Hóspede")

    # Labels e campos de entrada
    label_id = tk.Label(top, text="ID:")
    label_id.pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    label_canal = tk.Label(top, text=f"O canal deve estar entre 1 e {max_canais}:")
    label_canal.pack()
    entry_canal = tk.Entry(top)
    entry_canal.pack()

    label_ttv = tk.Label(top, text="Tempo na TV:")
    label_ttv.pack()
    entry_ttv = tk.Entry(top)
    entry_ttv.pack()

    label_td = tk.Label(top, text="Tempo de descanso:")
    label_td.pack()
    entry_td = tk.Entry(top)
    entry_td.pack()

    # Botão para confirmar
    def confirmar_hospede():
        try:
            id = int(entry_id.get())
            canal = int(entry_canal.get())
            ttv = int(entry_ttv.get())
            td = int(entry_td.get())
            novo_hospede = Hospede(id, canal, ttv, td)
            hospedes.append(novo_hospede)
            novo_hospede.thread.start()
            atualizar_interface()
            top.destroy()
        except ValueError:
            tk.simpledialog.messagebox.showerror("Erro", "Por favor, insira apenas números inteiros.")

    botao_confirmar = tk.Button(top, text="Confirmar", command=confirmar_hospede)
    botao_confirmar.pack()

def remover_hospede():
    index = lista_hospedes.curselection()
    if index:
        hospede_remover = hospedes[index[0]]
        hospedes.remove(hospede_remover)
        hospede_remover.parar = True

        # Tentativa de interromper a thread de forma limpa
        try:
            hospede_remover.thread.join(timeout=1)  # Aguarda no máximo 1 segundo
        except TimeoutError:
            print(f"Thread do hóspede {hospede_remover.id} não pôde ser interrompida imediatamente.")

        # Atualiza a interface de forma assíncrona
        atualizar_interface_assincrona()

def atualizar_interface_assincrona():
    root.after(100, atualizar_interface)

def exibir_log(hospede):
    for evento in hospede.log:
        timestamp, status = evento
        data_hora = datetime.datetime.fromtimestamp(timestamp)
        print(f"{data_hora:%Y-%m-%d %H:%M:%S} - {status}")

# Botão para exibir log na interface
def exibir_log_interface():
    index = lista_hospedes.curselection()
    if index:
        hospede_selecionado = hospedes[index[0]]
        exibir_log(hospede_selecionado)

# Função para atualizar a interface
def atualizar_interface():
    lista_hospedes.delete(0, tk.END)
    for hospede in hospedes:
        lista_hospedes.insert(tk.END, f"ID: {hospede.id}, Canal Preferido: {hospede.canalPreferido}, Ttv: {hospede.ttv}, Td: {hospede.td}, Status: {hospede.status}")
    label_canal['text'] = f"Canal atual: {canal_atual}"

def exibir_log_interface():
    index = lista_hospedes.curselection()
    if index:
        hospede_selecionado = hospedes[index[0]]

        # Cria uma nova janela para o log
        janela_log = tk.Toplevel(root)
        janela_log.title(f"Log do Hóspede {hospede_selecionado.id}")

        # Lista para exibir o log
        lista_log = tk.Listbox(janela_log, width = 50)
        lista_log.pack()

        # Preenche a lista com os dados do log
        for evento in hospede_selecionado.log:
            timestamp, status = evento
            data_hora = datetime.datetime.fromtimestamp(timestamp)
            lista_log.insert(tk.END, f"{data_hora:%Y-%m-%d %H:%M:%S} - {status}")

# Interface gráfica
root = tk.Tk()
root.title("Simulação da Televisão")

# Labels e lista
label_canal = tk.Label(root, text="Canal atual: 0", width=70)
label_canal.pack()
lista_hospedes = tk.Listbox(root, width=75)
lista_hospedes.pack()

# Botões
frame1 = tk.Frame(root, padx=15, pady=5) 
botao_criar = tk.Button(frame1, text="Criar Hóspede", command=criar_hospede, width="15")
frame1.pack()
botao_criar.pack()

botao_remover = tk.Button(root, text="Remover Hóspede", command=remover_hospede, width="15")
botao_remover.pack()

frame2= tk.Frame(root, padx=15, pady=5)
botao_log = tk.Button(frame2, text="Ver Log", command=exibir_log_interface, width="15")
frame2.pack()
botao_log.pack()

# Atualização automática da interface
atualizar_interface()

# Loop principal
root.mainloop()