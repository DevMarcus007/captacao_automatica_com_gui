import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, time, timedelta
from PIL import Image, ImageTk
from config import *




class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("GCCAP/CTE Benfica")
        self.master.geometry("500x400")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        

    def create_widgets(self):

          # Carrega a imagem da logo
        image = Image.open("logo.webp").convert("RGBA")
        image = image.resize((300, 100), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(image)

        # Cria um label para exibir a imagem da logo
        self.logo_label = tk.Label(self, image=self.logo, highlightthickness=0)
        self.logo_label.grid(row=0, column=2, columnspan=5)


        # Cria um label Titulo
        self.title_label = tk.Label(self, justify='center')
        self.title_label["text"] = "Verificação da Postagem Automática"
        self.title_label["font"] = ("Arial", 15)
        self.title_label.grid(row=4, column=2, columnspan=6, sticky="w", pady=20 )

        # Cria um label para a entrada de data
        self.date_label = tk.Label(self, justify='left')
        self.date_label["text"] = datetime.now().strftime('%d/%m/%Y')
        self.date_label.grid(row=5, column=1, sticky="w", padx=10)

        # Cria um botão para abrir o calendário
        self.calendar_button = tk.Button(self, justify='right')
        self.calendar_button["text"] = "Alterar Data"
        self.calendar_button["command"] = self.show_calendar
        self.calendar_button.grid(row=5, column=2, sticky="w", padx=10)

        # Cria um label para a hora de início
        self.start_label = tk.Label(self)
        self.start_label["text"] = "Hora início:"
        self.start_label.grid(row=10, column=1, sticky="w")

        # # Cria um label para exibir a hora de início selecionada
        self.start_time = tk.Label(self)
        self.start_time["text"] = "15:00:00"
        # self.start_time.grid(row=3, column=2, sticky="w")

        # Cria um spinbox para permitir a seleção do horário de início
        self.start_spinbox = tk.Spinbox(self, from_=0, to=23, width=7, increment=10)
        self.start_spinbox.delete(0, "end")
        self.start_spinbox.insert(0, "15:00")
        self.start_spinbox.grid(row=10, column=2, sticky="w")

        # Cria um label para a hora de fim
        self.end_label = tk.Label(self)
        self.end_label["text"] = "Hora fim:"
        self.end_label.grid(row=14, column=1, sticky="w")

        # Cria um label para exibir a hora de fim selecionada
        self.end_time = tk.Label(self)
        self.end_time["text"] = datetime.now().strftime("%H:%M")

        self.end_spinbox = tk.Spinbox(self, from_=0, to=23, width=7)
        self.end_spinbox.delete(0, "end")
        self.end_spinbox.insert(0, self.end_time["text"])
        self.end_spinbox.grid(row=14, column=2, sticky="w")

        # Cria uma lista de seleção de rampas
        self.rampas = []
         # Cria um label Titulo
        self.title_rampas_label = tk.Label(self)
        self.title_rampas_label["text"] = "Selecione as Rampas Utilizadas"

        self.title_rampas_label.grid(row=5, column=4, columnspan=4, sticky="w" )
        for i in range(1, 6):
            for j in range(1, 3):
                var = tk.BooleanVar()
                rampa = tk.Checkbutton(self, text=i*2 + j - 2, variable=var)
                rampa.grid(row=2*i+4 , column=4+j-1, sticky="w")
                self.rampas.append((rampa, var))


        # Cria um botão para enviar os dados
        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Verificar Postagem"
        self.submit_button["command"] = self.submit
        self.submit_button.grid(row=16, column=2, columnspan = 6, pady=10)


    def show_calendar(self):
        # Cria uma janela com um calendário para seleção da data
        self.calendar_window = tk.Toplevel(self)

        # Cria um widget de calendário
        self.calendar = Calendar(self.calendar_window, selectmode="day")

        # Adiciona o widget de calendário à janela
        self.calendar.pack()

        # Cria um botão para selecionar a data
        self.date_button = tk.Button(self.calendar_window)
        self.date_button["text"] = "Selecionar"
        self.date_button["command"] = self.select_date
        self.date_button.pack()

    def submit(self):
        # Obtém os valores selecionados pelo usuário
        start_time = self.start_spinbox.get()
        end_time = self.end_spinbox.get()
        selected_ramps = [ramp[0]["text"] for ramp in self.rampas if ramp[1].get() == 1]
        rampas = []
        for item in selected_ramps:
            if item < 10:
                item = str(item)
                item = f'IP00{item}'
                rampas.append(item)
            else:
                item = str(item)
                item = f'IP0{item}'
                rampas.append(item)

        selected_date = self.date_label["text"]

        if len(start_time) != 5:
            erro("Verifique o formato da Hora Início (HH:MM)")
        if len(end_time) != 5:
            erro("Verifique o formato da Hora Fim (HH:MM)")

        data = datetime.strptime(selected_date, '%d/%m/%Y').date()
        hora_inicio = datetime.combine(data, datetime.strptime(start_time, "%H:%M").time())
        hora_fim = datetime.combine(data, datetime.strptime(end_time, "%H:%M").time())
        limite_mis = timedelta(hours=4)

        if len(rampas) < 1:
            erro("Selecione pelo menos uma rampa")

        elif hora_inicio > hora_fim:
            erro("Hora início maior que hora final")

        elif selected_date > datetime.now().strftime('%d/%m/%Y'):
            erro("Verifique a data informada")
        
        elif (hora_fim - hora_inicio) > limite_mis:
            erro("Período pesquisado maior que 4 horas")

        else:
            # Imprime os valores selecionados
            print(f"Data selecionada: {selected_date}")
            print(f"Hora de início: {hora_inicio.strftime('%H:%M:%S')}")
            print(f"Hora de término: {hora_fim.strftime('%H:%M:%S')}")
            print(f"Rampas selecionadas: {rampas}")
            cap_aut(selected_date, hora_inicio, hora_fim, rampas)
            erro("Aplicação Finalizada")
            


       

    def select_date(self):
        # Atualiza o label da data com a data selecionada no calendário
        self.date_label["text"] = f"{self.calendar.selection_get().strftime('%d/%m/%Y')}"

        # Fecha a janela do calendário
        self.calendar_window.destroy()

        # Atualiza o label de hora de fim com o horário atual
        self.end_time["text"] = datetime.now().strftime("%H:%M:%S")

def erro(texto):
    # Cria uma nova janela popup
    popup = tk.Toplevel(root)
    popup.title("Atenção")
    
    mensagem = tk.Label(popup, text=texto)
    mensagem.pack(padx=30, pady=30)
    
    # Botão para fechar a janela popup
    fechar = tk.Button(popup, text="OK", command=popup.destroy)
    fechar.pack(pady=10)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
