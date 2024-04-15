import tkinter as tk
from tkinter import messagebox


class ContadorOvosPáscoa:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de Ovos de Páscoa")
        self.root.geometry("520x500")  # tamanho da janela

        self.contagem = self.carregar_contagem()
        # Carrega o número da última senha
        self.senha_atual = self.carregar_ultima_senha()
        self.ultima_acao = ""

        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(pady=20)

        self.label_contagem = tk.Label(
            self.frame_principal, text="Contagem: 0", font=("Helvetica", 18))
        self.label_contagem.pack(pady=10)

        self.frame_botoes = tk.Frame(self.frame_principal)
        self.frame_botoes.pack(pady=10)

        self.botao_adicionar = tk.Button(self.frame_botoes, text="Adicionar Ovo", command=self.adicionar_ovo, font=(
            "Helvetica", 12), bg="#4CAF50", fg="white")
        self.botao_adicionar.grid(row=0, column=0, padx=5)

        self.botao_subtrair = tk.Button(self.frame_botoes, text="Subtrair Ovo", command=self.subtrair_ovo, font=(
            "Helvetica", 12), bg="#F44336", fg="white")
        self.botao_subtrair.grid(row=0, column=1, padx=5)

        self.entry_quantidade = tk.Entry(
            self.frame_botoes, font=("Helvetica", 12), width=5)
        self.entry_quantidade.grid(row=0, column=2, padx=5)

        self.botao_adicionar_customizado = tk.Button(
            self.frame_botoes, text="Adicionar/Subtrair", command=self.adicionar_subtrair_customizado, font=("Helvetica", 12))
        self.botao_adicionar_customizado.grid(row=0, column=3, padx=5)

        self.label_dica = tk.Label(
            self.frame_principal, text="Dica: Digite um número positivo para adicionar ovos e um número negativo para subtrair", font=("Helvetica", 10), fg="gray")
        self.label_dica.pack(pady=5)

        self.botao_reiniciar = tk.Button(
            self.frame_principal, text="Reiniciar Contagem", command=self.reiniciar_contagem, font=("Helvetica", 12))
        self.botao_reiniciar.pack(pady=10)

        self.botao_senha = tk.Button(
            self.frame_principal, text="Pegar Senha", command=self.pegar_senha, font=("Helvetica", 12))
        self.botao_senha.pack(pady=10)
        self.botao_desfazer = tk.Button(
            self.frame_principal, text="Desfazer", command=self.desfazer, font=("Helvetica", 12))
        self.botao_desfazer.pack(pady=5)

        self.botao_sair = tk.Button(
            self.frame_principal, text="Sair", command=self.sair, font=("Helvetica", 12))
        self.botao_sair.pack(pady=5)

        self.label_aviso = tk.Label(root, text="", fg="red")
        self.label_aviso.pack(pady=5)

        self.log_text = tk.Text(
            root, height=5, width=40, font=("Helvetica", 12))
        self.log_text.pack()

        self.atualizar_label_contagem()

    def adicionar_ovo(self):
        self.contagem += 1
        self.ultima_acao = "Adicionado 1 ovo"
        self.atualizar_label_contagem()
        self.log(self.ultima_acao)

    def subtrair_ovo(self):
        if self.contagem > 0:
            self.contagem -= 1
            self.ultima_acao = "Subtraído 1 ovo"
            self.atualizar_label_contagem()
            self.log(self.ultima_acao)

    def adicionar_subtrair_customizado(self):
        try:
            quantidade = int(self.entry_quantidade.get())
            if quantidade > 0:
                self.contagem += quantidade
                self.ultima_acao = f"Adicionado {quantidade} ovos"
                self.atualizar_label_contagem()
                # Limpa o campo de entrada após a operação
                self.entry_quantidade.delete(0, tk.END)
                self.label_aviso.config(text="")
                self.log(self.ultima_acao)
            else:
                # Converte a quantidade negativa em positiva
                quantidade = abs(quantidade)
                if self.contagem >= quantidade:  # Verifica se há ovos suficientes para subtrair
                    self.contagem -= quantidade
                    self.ultima_acao = f"Subtraído {quantidade} ovos"
                    self.atualizar_label_contagem()
                    # Limpa o campo de entrada após a operação
                    self.entry_quantidade.delete(0, tk.END)
                    self.label_aviso.config(text="")
                    self.log(self.ultima_acao)
                else:
                    self.label_aviso.config(text="Quantidade inválida")
        except ValueError:
            self.label_aviso.config(text="Quantidade inválida")

    def reiniciar_contagem(self):
        self.contagem = 0
        self.ultima_acao = "Contagem reiniciada"
        self.atualizar_label_contagem()
        self.log(self.ultima_acao)

    def pegar_senha(self):
        self.senha_atual += 1
        messagebox.showinfo("Senha", f"Sua senha é: {self.senha_atual}")
        self.log(f"Senha {self.senha_atual} retirada")

    def desfazer(self):
        if self.ultima_acao:
            if "Adicionado" in self.ultima_acao:
                self.contagem -= int(self.ultima_acao.split()[1])
            elif "Subtraído" in self.ultima_acao:
                self.contagem += int(self.ultima_acao.split()[1])
            self.atualizar_label_contagem()
            self.log("Última ação desfeita")

    def atualizar_label_contagem(self):
        self.label_contagem.config(text="Contagem: " + str(self.contagem))

    def log(self, mensagem):
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)

    def sair(self):
        self.salvar_contagem()  # Salva a contagem de ovos
        self.salvar_ultima_senha()  # Salva o número da última senha
        self.root.destroy()

    def salvar_contagem(self):
        with open("contagem.txt", "w") as arquivo:
            arquivo.write(str(self.contagem))

    def salvar_ultima_senha(self):
        with open("ultima_senha.txt", "w") as arquivo:
            arquivo.write(str(self.senha_atual))

    def carregar_contagem(self):
        try:
            with open("contagem.txt", "r") as arquivo:
                return int(arquivo.read())
        except FileNotFoundError:
            return 0

    def carregar_ultima_senha(self):
        try:
            with open("ultima_senha.txt", "r") as arquivo:
                return int(arquivo.read())
        except FileNotFoundError:
            return 0


root = tk.Tk()
app = ContadorOvosPáscoa(root)
root.mainloop()
