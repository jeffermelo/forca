import random
import tkinter as tk

##-------------------------------------

palavras_por_categoria = {
    'Comida': ['banana', 'sushi', 'lasanha', 'taco', 'pizza'],
    'Animal': ['gato', 'cachorro', 'elefante', 'leao', 'tigre'],
    'Fruta': ['uva', 'manga', 'abacaxi', 'morango', 'laranja', 'fruta do conde'],
    'Profissão': ['professor', 'medico', 'engenheiro', 'advogado', 'cientista']
}

##-------------------------------------

def escolher_palavra():
    categoria = random.choice(list(palavras_por_categoria.keys()))
    palavra = random.choice(palavras_por_categoria[categoria])
    return categoria, palavra

##-------------------------------------

categoria, palavra = escolher_palavra()
letras_corretas = ['_' if letra != ' ' else ' ' for letra in palavra]
tentativas = 6
letras_erradas = []

##-------------------------------------

def validar_entrada(palpite, tentando_palavra=False):
    if tentando_palavra:
        if not all(l.isalpha() or l == ' ' for l in palpite):
            raise ValueError("Entrada inválida. Apenas letras e espaços são permitidos ao adivinhar a palavra completa.")
    else:
        if not palpite.isalpha():
            raise ValueError("Entrada inválida. Apenas letras são permitidas.")

##-------------------------------------

def verificar_palpite(event=None):
    global tentativas, letras_corretas, letras_erradas

    palpite = entrada.get().lower().strip()
    if not palpite:
        status_var.set("Por favor, insira uma letra ou tente adivinhar a palavra.")
        root.after(2000, lambda: status_var.set("Digite uma letra ou tente adivinhar a palavra."))
        return
    entrada.delete(0, tk.END)

    try:
        if len(palpite) == 1:
            validar_entrada(palpite)

            if palpite in letras_corretas or palpite in letras_erradas:
                status_var.set("Você já tentou essa letra. Tente outra.")
                return

            if palpite in palavra:
                for i, letra in enumerate(palavra):
                    if letra == palpite:
                        letras_corretas[i] = palpite
                atualizar_jogo()
                if '_' not in letras_corretas:
                    finalizar(True) ## Ganhou
            else:
                tentativas -= 1
                letras_erradas.append(palpite)
                atualizar_jogo()
                if tentativas == 0:
                    finalizar(False) ## Perdeu

        elif len(palpite) == len(palavra):
            validar_entrada(palpite, tentando_palavra=True)

            if palpite == palavra:
                finalizar(True) ## Ganhou
            else:
                tentativas = 0
                atualizar_jogo()
                finalizar(False) ## Perdeu

        else:
            tentativas = 0
            atualizar_jogo()
            finalizar(False) ## Perdeu

    except ValueError as e:
        status_var.set(str(e))

##-------------------------------------

def atualizar_jogo():
    palavra_atual.set(' '.join(letras_corretas))
    tentativas_atual.set(f"Tentativas restantes: {tentativas}")
    letras_erradas_atual.set(f"Letras erradas: {', '.join(letras_erradas)}")
    categoria_atual.set(f"Dica: {categoria}")
    atualizar_cores()

## cor dos ngcs da categoria
def definir_cores_categoria():
    cores_categoria = {
        'Comida': ('#FF5722', '#FF9800'),  
        'Animal': ('#FF4081', '#F50057'),
        'Fruta': ('#8BC34A', '#4CAF50'),  
        'Profissão': ('#03A9F4', '#0288D1')  
    }
    return cores_categoria.get(categoria, ('#FFFFFF', '#FFFFFF'))  

def atualizar_cores():
    cor_palavra, cor_dica = definir_cores_categoria()
    palavra_label.config(fg=cor_palavra)  
    dica_label.config(fg=cor_dica) 


def mostrar_resultado(mensagem):
    resultado_frame = tk.Frame(root, bg="#333", padx=20, pady=20)
    resultado_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

    tk.Label(resultado_frame, text=mensagem, font=("Helvetica", 24), fg="#FFF", bg="#333").pack(pady=20)

    sim_button.config(bg="#4CAF50", fg="#FFF", font=("Helvetica", 16))
    nao_button.config(bg="#F44336", fg="#FFF", font=("Helvetica", 16)) 
    sim_button.place(relx=0.3, rely=0.75, anchor="center")
    nao_button.place(relx=0.7, rely=0.75, anchor="center")

    root.bind('<s>', lambda event: (resultado_frame.destroy(), reiniciar_jogo()))
    root.bind('<n>', lambda event: root.quit())

def finalizar(resultado):
    for i, letra in enumerate(palavra):
        if letra != ' ':
            letras_corretas[i] = letra
    atualizar_jogo()
    entrada.grid_forget()
    botao.grid_forget()
    if resultado:
        mostrar_resultado(f"Parabéns! Você venceu! A palavra era '{palavra}'.")
    else:
        mostrar_resultado(f"Você perdeu! A palavra era '{palavra}'.")

def reiniciar_jogo(event=None):
    global categoria, palavra, letras_corretas, tentativas, letras_erradas
    categoria, palavra = escolher_palavra()
    letras_corretas = ['_' if letra != ' ' else ' ' for letra in palavra]
    tentativas = 6
    letras_erradas = []
    atualizar_jogo()
    entrada.grid(row=5, column=1, padx=5, pady=50, sticky='nsew')
    botao.grid(row=6, column=1, padx=5, pady=10, sticky='nsew')

    def habilitar_componentes():
        entrada.config(state='normal') 
        botao.config(state='normal')     

    root.after(500, habilitar_componentes)

    status_var.set("Digite uma letra ou tente adivinhar a palavra.")
    sim_button.place_forget()
    nao_button.place_forget()
    root.unbind('<s>')
    root.unbind('<n>')

## Parte gráfica
root = tk.Tk()
root.title("Forca da Fiec")

##----------------------------------------------
root.attributes('-fullscreen', True)

def sair_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root.bind('<Escape>', sair_fullscreen)


root.geometry('800x900')


palavra_atual = tk.StringVar()
tentativas_atual = tk.StringVar()
letras_erradas_atual = tk.StringVar()
categoria_atual = tk.StringVar()
status_var = tk.StringVar(value="Digite uma letra ou tente adivinhar a palavra.")


font_palavra = ("Helvetica", 30, 'bold')
font_info = ("Helvetica", 16)
font_status = ("Helvetica", 18)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

tk.Label(root, text="Palavra:", font=font_info).grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
palavra_label = tk.Label(root, textvariable=palavra_atual, font=font_palavra)
palavra_label.grid(row=1, column=1, padx=5, pady=50, sticky='nsew')

tk.Label(root, textvariable=tentativas_atual, font=font_info).grid(row=2, column=1, padx=5, pady=15, sticky='nsew')
tk.Label(root, textvariable=letras_erradas_atual, font=font_info).grid(row=3, column=1, padx=5, pady=15, sticky='nsew')

dica_label = tk.Label(root, textvariable=categoria_atual, font=font_info)
dica_label.grid(row=4, column=1, padx=5, pady=15, sticky='nsew')

entrada = tk.Entry(root, font=font_info, width=25)
entrada.grid(row=5, column=1, padx=5, pady=50, sticky='nsew')
entrada.bind('<Return>', verificar_palpite)

botao = tk.Button(root, text="Verificar", font=font_info, command=verificar_palpite, width=10, bg='#00BCD4', fg='#FFF')
botao.grid(row=6, column=1, padx=5, pady=10, sticky='nsew')

status_label = tk.Label(root, textvariable=status_var, font=font_status, fg="#D32F2F")
status_label.grid(row=7, column=1, padx=10, pady=20, sticky='nsew')

sim_button = tk.Button(root, text="Sim", command=reiniciar_jogo)
nao_button = tk.Button(root, text="Não", command=root.quit)

atualizar_jogo()
root.mainloop()
