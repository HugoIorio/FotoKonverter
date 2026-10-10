import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox
import compressor
import threading

ctk.set_appearance_mode("Dark")

class Aplicativo(ctk.CTk):

    def escolher_dir_entrada(self):
        pasta = ctk.filedialog.askdirectory(title="Selecionar Diretório de Entrada")
        if pasta:
            self.dir_entrada.set(pasta)

    def escolher_dir_saida(self):
        pasta = ctk.filedialog.askdirectory(title="Selecionar Diretório de Saída")
        if pasta:
            self.dir_saida.set(pasta)

    def atualizar_label_qualidade(self, valor):
        self.txt_qualidade.configure(text=f"Qualidade ({int(valor)}%)")

    def atualizar_label_threshold(self, valor):
        if self.slide_threshold.get() > 1024:
            self.txt_threshold.configure(text=f"Ignorar compressão abaixo de {valor/1024:.2f} MB")
        else:
            self.txt_threshold.configure(text=f"Ignorar compressão abaixo de {int(valor)} KB")

    def executar_compressao(self):
        entrada = self.dir_entrada.get()
        saida = self.dir_saida.get()

        if entrada == "Não Selecionado" or saida == "Não Selecionado": # verificar se diretórios de entrada/saída foram selecionados
            messagebox.showerror(
                "Diretórios Não Selecionados",
                "Você deve selecionar um diretório de entrada e de saída para converter as imagens."
            )
            return

        if entrada == saida: # erro caso o usuário selecione o mesmo diretório como entrada e saída
            messagebox.showerror(
                "Diretórios Iguais",
                "O diretório de saída deve ser um diretório diferente do diretório de entrada. \n\nPor favor, selecione outro diretório de saída."
            )
            return

        if self.sw_redimensionar.get() == 1: # verificar se quer redimensionar imagens
            quer_redimensionar = True
            try:
                limite_maior_lado = int(self.entry_maior_lado.get())
            except ValueError:
                messagebox.showerror(
                    "Valor Não Informado",
                    "Se quiser redimensionar as imagens, você deve informar o tamanho do maior lado apenas com números. Exemplo: 1080"
                )
                return
        else:
            quer_redimensionar = False
            limite_maior_lado = 2147483647 # maior valor que um int 32 bits armazena

        copiar_outros = self.chk_copiar_arq.get() == "on"
        salvar_exif = self.chk_preservar_meta.get() == "on"
        qualidade = int(self.slide_qualidade.get())
        limite_tamanho = self.slide_threshold.get()

        def tarefa_conversao():
            # desligar o botão quando começar
            self.botao_converter.configure(state="disabled")

            compressor.comprimir(
                entrada,
                saida,
                quer_redimensionar=quer_redimensionar,
                limite_maior_lado=limite_maior_lado,
                salvar_exif=salvar_exif,
                copiar_outros=copiar_outros,
                qualidade=qualidade,
                limite_tamanho=limite_tamanho,
                status_compressao=self.txtbox_status,
                formato_alvo=self.cmb_formato_alvo.get()
            )
            # reativa o botão quando a conversão terminar
            self.botao_converter.configure(state="normal")
            self.txtbox_status.configure(state="normal")
            self.txtbox_status.insert("end","\nConversão Finalizada!")  # exibe na interface a mensagem ao usuário
            self.txtbox_status.see("end")  # rolar textbox para baixo
            self.txtbox_status.configure(state="disabled")
            self.txtbox_status.update_idletasks()

        thread = threading.Thread(target=tarefa_conversao, daemon=True)
        thread.start()

    def __init__(self):
        super().__init__()

        ######### TELA PRINCIPAL (FUNDO) #########

        self.title("FotoKonverter")
        self.geometry("900x625")

        try:
            self.iconbitmap("FotoKonverter.ico")
        except Exception:
            pass

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        #construir tela principal (fundo)
        self.construir_tela()


        self.titulo_tela = ctk.CTkLabel( #título
            self,
            text="FotoKonverter",
            font=("Arial", 40, "bold")
        )
        self.titulo_tela.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(10, 10),
            sticky="we"
        )

        self.painel_config = ctk.CTkFrame( #painel de configurações (esquerda)
            self,
            width=350,
            height= 50,
            corner_radius=25,
            fg_color="#1F1F1F"
        )
        self.painel_config.grid(
            row = 1,
            column = 0,
            padx = (10, 5),
            pady = (10, 5),
            sticky="nsew"
        )

        self.painel_status = ctk.CTkFrame( #painel de status (direita)
            self,
            width=900,
            height=350,
            corner_radius=25,
            fg_color="#111111"
        )
        self.painel_status.grid(
            row=1,
            column=1,
            padx=(5, 10),
            pady=(10, 5),
            sticky="nsew"
        )

        self.painel_inferior = ctk.CTkFrame( #painel inferior (diretórios e botão principal)
            self,
            width=900,
            height=150,
            corner_radius=25,
            fg_color="#1F1F1F"
        )
        self.painel_inferior.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=(10, 10),
            pady=(5, 10),
            sticky="nsew"
        )

        ######### PARTES DO PAINEL DE CONFIGURAÇÃO (PAINEL ESQUERDO) #########

        self.painel_config.grid_columnconfigure(0, weight=1)
        self.painel_config.grid_columnconfigure(1, weight=1)
        self.painel_config.grid_columnconfigure(2, weight=1)
        self.painel_config.grid_rowconfigure(0, weight=0)

        self.titulo_painel_config = ctk.CTkLabel(
            self.painel_config,
            text="Configurações de Conversão",
            font=("Arial", 20)
        )
        self.titulo_painel_config.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=(10, 5)
        )

        self.txt_redimensionar = ctk.CTkLabel(
            self.painel_config,
            text="Redimensionar Imagem",
            font=("Arial", 16)
        )
        self.txt_redimensionar.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(10, 5),
            sticky="w"
        )

        switch_var = ctk.StringVar(value="on")

        self.sw_redimensionar = ctk.CTkSwitch(
            self.painel_config,
            fg_color="#111111",
            progress_color="#2270E6",
            text="",
            #command=
        )
        self.sw_redimensionar.grid(
            row=1,
            column=1,
            padx=(70, 10),
            pady=(10, 5),
            sticky="e"
        )
        self.sw_redimensionar.select()

        self.txt_maior_lado = ctk.CTkLabel(
            self.painel_config,
            text="Maior Lado (Px)",
            font=("Arial", 16)
        )
        self.txt_maior_lado.grid(
            row=2,
            column=0,
            padx=(20,10),
            pady=(10,5),
            sticky="w"
        )

        self.entry_maior_lado = ctk.CTkEntry(
            master=self.painel_config,
            width=200,
            height=40,
            font=("Arial", 16),
            fg_color="#111111",
            border_color="#383838",
            border_width=1
        )
        self.entry_maior_lado.grid(
            row=3,
            column=0,
            padx=(20,10),
            pady=(0,5),
            sticky = "w"
        )

        self.txt_formato_alvo = ctk.CTkLabel(
            self.painel_config,
            text="Formato Alvo",
            font=("Arial", 16)
        )
        self.txt_formato_alvo.grid(
            row=2,
            column=1,
            padx=(20, 10),
            pady=(10, 5),
            sticky="w"
        )

        self.cmb_formato_alvo = ctk.CTkComboBox(
            self.painel_config,
            height=40,
            font=("Arial", 14),
            fg_color="#111111",
            button_color="#383838",
            dropdown_fg_color="#111111",
            border_width=1,
            border_color="#383838",
            values=[".jpeg", ".webp", ".avif"]
        )
        self.cmb_formato_alvo.grid(
            row=3,
            column=1,
            padx=(20, 20),
            pady=(0, 5),
            sticky="w"
        )

        self.txt_qualidade = ctk.CTkLabel(
            self.painel_config,
            text="Qualidade ()",
            font=("Arial", 16)
        )
        self.txt_qualidade.grid(
            row=4,
            column=0,
            padx=(20, 10),
            pady=(10, 5),
            sticky="w"
        )

        self.slide_qualidade = ctk.CTkSlider(
            master=self.painel_config,
            height=18,
            from_=0,
            to=100,
            button_color="#FFFFFF",
            fg_color="#111111",
            button_hover_color="#AAAAAA",
            progress_color="#2270E6",
            command=self.atualizar_label_qualidade
        )
        self.slide_qualidade.grid(
            row=5,
            column=0,
            columnspan=3,
            padx=(20, 20),
            pady=(0, 3),
            sticky="we"
        )
        self.slide_qualidade.set(85)
        self.atualizar_label_qualidade(85)

        self.txt_threshold = ctk.CTkLabel(
            self.painel_config,
            text="Ignorar compressão abaixo de 0 KB",
            font=("Arial", 16)
        )
        self.txt_threshold.grid(
            row=6,
            column=0,
            columnspan=3,
            padx=(20, 0),
            pady=(10, 5),
            sticky="w"
        )

        self.slide_threshold = ctk.CTkSlider(
            master=self.painel_config,
            height=18,
            from_=0,
            to=8192,
            button_color="#FFFFFF",
            fg_color="#111111",
            button_hover_color="#AAAAAA",
            progress_color="#2270E6",
            number_of_steps=512,
            command=self.atualizar_label_threshold
        )
        self.slide_threshold.grid(row=7, column=0, columnspan=3, padx=(20, 20), pady=(0, 10), sticky="we")
        self.slide_threshold.set(0)

        self.chk_copiar_arq = ctk.CTkCheckBox(
            master=self.painel_config,
            fg_color="#2270E6",
            hover_color="#1A488D",
            text=" Copiar arquivos não convertidos para diretório de saída.",
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=5,
            border_width=2,
            font=("Arial", 13),
            onvalue="on",
            offvalue="off"
        )
        self.chk_copiar_arq.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=(20, 0),
            pady=(5, 10),
            sticky="w"
        )
        self.chk_copiar_arq.select()

        self.chk_preservar_meta = ctk.CTkCheckBox(
            master=self.painel_config,
            fg_color="#2270E6",
            hover_color="#1A488D",
            text=" Preservar metadados (exif) nas imagens convertidas.",
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=5,
            border_width=2,
            font=("Arial", 13),
            onvalue="on",
            offvalue="off"
        )
        self.chk_preservar_meta.grid(
            row=9,
            column=0,
            padx=(20, 0),
            columnspan=2,
            pady=(0, 5),
            sticky="w"
        )
        self.chk_preservar_meta.select()


        ######### PARTES DO PAINEL DE STATUS (PAINEL DIREITO) #########

        self.painel_status.grid_columnconfigure(0, weight=1)
        self.painel_status.grid_rowconfigure(0, weight=0)


        self.titulo_painel_status = ctk.CTkLabel(
            self.painel_status,
            text="Status de Conversão",
            font=("Arial", 20)
        )
        self.titulo_painel_status.grid(
            row=0,
            column=0,
            pady=(10, 10)
        )

        self.txtbox_status = ctk.CTkTextbox(
            master=self.painel_status,
            state="disabled",
            fg_color="#111111",
            height=320,
            scrollbar_button_color="#FFFFFF",

        )
        self.txtbox_status.grid(
            row=1,
            column=0,
            sticky="sew"
        )

        ######### PARTES DO PAINEL INFERIOR (SELECIONAR DIRETORIOS E COMPRIMIR) #########

        self.painel_inferior.grid_columnconfigure(1, weight=1)


        self.btn_selecionar_entrada = ctk.CTkButton(
            self.painel_inferior,
            text="Selecionar",
                font = ("Arial", 18, "bold"),
            border_spacing=8,
            corner_radius=5,
            fg_color = "#2270E6",
            hover_color="#1A488D",
            command=self.escolher_dir_entrada
        )
        self.btn_selecionar_entrada.grid(
            row=0,
            rowspan=2,
            column=0,
            padx=(20, 10),
            pady=(20, 10)
        )

        self.tooltip_entrada = CTkToolTip(
            self.btn_selecionar_entrada,
            message="Selecionar a pasta com as imagens \nque devem ser processadas."
        )

        self.txt_diretorio_entrada = ctk.CTkLabel(
            self.painel_inferior,
            text="Diretório de Entrada:",
            font=("Arial", 14)
        )
        self.txt_diretorio_entrada.grid(
            row=0,
            column=1,
            padx=(10, 0),
            pady=(10, 0),
            sticky = "sw"
        )

        self.dir_entrada = ctk.StringVar(value="Não Selecionado")
        self.txt_entrada_caminho = ctk.CTkLabel(
            self.painel_inferior,
            textvariable=self.dir_entrada,
            font=("Arial", 12)
        )
        self.txt_entrada_caminho.grid(
            row=1,
            column=1,
            padx=(10, 0),
            pady=(0, 0),
            sticky = "nw"
        )


        self.btn_selecionar_saida = ctk.CTkButton(
            self.painel_inferior,
            text="Selecionar",
            font = ("Arial", 18, "bold"),
            border_spacing=8,
            corner_radius=5,
            fg_color="#2270E6",
            hover_color="#1A488D",
            command=self.escolher_dir_saida
        )
        self.btn_selecionar_saida.grid(
            row=2,
            column=0,
            rowspan=2,
            padx=(20, 10),
            pady=(10, 20)
        )
        self.tooltip_saida = CTkToolTip(
            self.btn_selecionar_saida,
            message="Selecionar a pasta para onde as\n imagens processadas devem ir."
        )

        self.txt_diretorio_saida = ctk.CTkLabel(
            self.painel_inferior,
            text="Diretório de Saída:",
            font=("Arial", 14)
        )
        self.txt_diretorio_saida.grid(
            row=2,
            column=1,
            padx=(10, 0),
            pady=(0, 0),
            sticky="sw"
        )

        self.dir_saida = ctk.StringVar(value="Não Selecionado")
        self.txt_saida_caminho = ctk.CTkLabel(
            self.painel_inferior,
            textvariable=self.dir_saida,
            font=("Arial", 12)
        )
        self.txt_saida_caminho.grid(
            row=3,
            column=1,
            padx=(10, 0),
            pady=(0, 10),
            sticky="nw"
        )


        self.botao_converter = ctk.CTkButton(
            self.painel_inferior,
            text="Converter",
            font = ("Arial", 18, "bold"),
            border_spacing=16,
            corner_radius=5,
            fg_color="#009E6E",
            hover_color="#005B3F",
            command=self.executar_compressao
        )
        self.botao_converter.grid(
            row=1,
            rowspan=2,
            column=2,
            padx=(10, 40),
            sticky="e"
        )
        self.tooltip_converter = CTkToolTip(
            self.botao_converter,
            message="Iniciar conversão das imagens."
        )

    def construir_tela(self):
        pass
