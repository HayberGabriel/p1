import threading
import tkinter as tk
import time

class Hospede:
    def __init__(self, id, canal, ttv, td):
        self.id = id
        self.canal = canal
        self.canalPreferido = canal
        self.ttv = ttv
        self.td = td
        self.thread = threading.Thread(target=self.executar)
        self.status = "Descansando"

    def executar(self):
        global semaforo, canal_atual
        while True:
            atualizar_interface()
            semaforo.acquire()
            atualizar_interface()
            canal_atual = self.canal
            atualizar_interface()
            self.status = "Assistindo TV"
            atualizar_interface()
            time.sleep(self.ttv)
            atualizar_interface()
            semaforo.release()
            atualizar_interface()
            self.status = "Descansando"
            atualizar_interface()
            time.sleep(self.td)
            atualizar_interface()

# Variáveis globais
semaforo = threading.Semaphore(1)
canal_atual = 0
hospedes = []
max_canais = 0

def inicializar():
    global max_canais

    # Cria uma caixa de diálogo para obter o número máximo de canais
    def obter_max_canais():
        try:
            valor = int(entrada.get())
            if valor > 0:
                global max_canais
                max_canais = valor
                dialogo.destroy()  # Fecha a caixa de diálogo
            else:
                tk.messagebox.showerror("Erro", "O número de canais deve ser maior que zero.")
        except ValueError:
            tk.messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")

    dialogo = tk.Toplevel()
    dialogo.title("Configuração de Canais")

    label = tk.Label(dialogo, text="Digite o número máximo de canais:")
    label.pack()

    entrada = tk.Entry(dialogo)
    entrada.pack()

    botao = tk.Button(dialogo, text="Confirmar", command=obter_max_canais)
    botao.pack()

    dialogo.wait_window()

inicializar()

def criar_hospede():
    top = tk.Toplevel()
    top.title("Adicionar Novo Hóspede")

    # Labels e campos de entrada
    label_id = tk.Label(top, text="ID:")
    label_id.pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    label_canal = tk.Label(top, text="Canal:")
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
            if canal < 1 or canal > max_canais:
                tk.simpledialog.messagebox.showerror("Erro", f"O canal deve estar entre 1 e {max_canais}.")
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
        hospede_remover.thread.join()  # Aguarda a thread terminar
        atualizar_interface()

# Função para atualizar a interface
def atualizar_interface():
    lista_hospedes.delete(0, tk.END)
    for hospede in hospedes:
        lista_hospedes.insert(tk.END, f"ID: {hospede.id}, Canal Preferido: {hospede.canalPreferido}, Ttv: {hospede.ttv}, Td: {hospede.td}, Status: {hospede.status}")
    label_canal['text'] = f"Canal atual: {canal_atual}"

# Interface gráfica
root = tk.Tk()
root.title("Simulação da Televisão")

# Labels e lista
label_canal = tk.Label(root, text="Canal atual: 0")
label_canal.pack()
lista_hospedes = tk.Listbox(root, width=75)
lista_hospedes.pack()

# Botões
botao_criar = tk.Button(root, text="Criar Hóspede", command=criar_hospede)
botao_criar.pack()
botao_remover = tk.Button(root, text="Remover Hóspede", command=remover_hospede)
botao_remover.pack()

# Atualização automática da interface
atualizar_interface()

# Loop principal
root.mainloop()