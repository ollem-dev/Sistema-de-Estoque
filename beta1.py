
import graphics as gs
import csv

ARQUIVO_ESTOQUE = "estoque.csv"

def carregar_estoque():
    estoque = {}
    try:
        with open(ARQUIVO_ESTOQUE, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor) 
            for linha in leitor:
                if len(linha) == 3:
                    produto, quantidade, valor = linha
                    estoque[produto.upper()] = {
                        'quantidade': int(quantidade),
                        'valor': float(valor)
                    }
    except FileNotFoundError: 
        with open(ARQUIVO_ESTOQUE, mode="w", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Produto", "Quantidade", "Valor"])
    return estoque

def salvar_estoque(estoque): 
    with open(ARQUIVO_ESTOQUE, mode="w", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Produto", "Quantidade", "Valor"])
        for produto, dados in estoque.items():
            escritor.writerow([produto, dados["quantidade"], dados["valor"]])

def exibir_estoque(win, estoque):
    for item in win.items[:]:
        item.undraw()
    gs.Text(gs.Point(100, 50), "Produto").draw(win)
    gs.Text(gs.Point(300, 50), "Quantidade").draw(win)
    gs.Text(gs.Point(500, 50), "Valor (R$)").draw(win)

    y = 80
    for produto, dados in estoque.items():
        gs.Text(gs.Point(100, y), produto).draw(win)
        gs.Text(gs.Point(300, y), str(dados["quantidade"])).draw(win)
        gs.Text(gs.Point(500, y), f"R$ {dados['valor']:.2f}").draw(win)
        y += 20

    gs.Line(gs.Point(50, 60), gs.Point(550, 60)).draw(win)

def criar_botao(win, texto, x, y, largura, altura, cor="lightgray"):
    botao = gs.Rectangle(gs.Point(x - largura / 2, y - altura / 2),
                         gs.Point(x + largura / 2, y + altura / 2))
    botao.setFill(cor)
    botao.draw(win)

    texto_botao = gs.Text(gs.Point(x, y), texto)
    texto_botao.setTextColor("purple")
    texto_botao.setSize(12)
    texto_botao.draw(win)

    return botao

def criar_botao_voltar_x(win):
    botao_voltar = gs.Rectangle(gs.Point(10, 10), gs.Point(40, 40))
    botao_voltar.setFill("red")
    botao_voltar.draw(win)

    gs.Line(gs.Point(10, 10), gs.Point(40, 40)).draw(win)
    gs.Line(gs.Point(10, 40), gs.Point(40, 10)).draw(win)

    return botao_voltar

def criar_botao_concluir(win):
    largura = win.getWidth() * 0.3  
    altura = 50
    x = win.getWidth() / 2  
    y = win.getHeight() - 80  

    return criar_botao(win, "Concluir", x, y, largura, altura, "green")

def clicar_no_botao(botao, click_point):
    return (botao.getP1().getX() <= click_point.getX() <= botao.getP2().getX()) and (botao.getP1().getY() <= click_point.getY() <= botao.getP2().getY())

def exibir_interface_compras(win, estoque, valor_total_atual):

    for item in win.items[:]:
        item.undraw()

    gs.Text(gs.Point(100, 50), "Produto").draw(win)
    gs.Text(gs.Point(300, 50), "Valor (R$)").draw(win)
    gs.Text(gs.Point(500, 50), "Adicionar").draw(win)

    y = 80  
    botao_comprar = {}
    for produto, dados in estoque.items():
        gs.Text(gs.Point(100, y), produto).draw(win)
        gs.Text(gs.Point(300, y), f"R$ {dados['valor']:.2f}").draw(win)

        
        botao_comprar[produto] = criar_botao(win, "Comprar", 500, y + 10, 100, 30, "lightblue")
        y += 50  # Distância entre os itens

    gs.Line(gs.Point(50, 60), gs.Point(550, 60)).draw(win) #linha do cabeçalho
    gs.Text(gs.Point(100, y + 20), f"Total Atual: R$ {valor_total_atual:.2f}").draw(win)# valor total 
    botao_finalizar = criar_botao(win, "Finalizar Compra", 350, y + 60, 250, 50, "lightgreen")#finalizar a compra
    
    return botao_comprar, botao_finalizar

def processar_compra(win, estoque):
    valor_total_atual = 0  
    compras = {} 

    while True:
        if win.isClosed():
            break 
        botao_adicionar, botao_finalizar = exibir_interface_compras(win, estoque, valor_total_atual)

        if win.checkMouse():
            click_point = win.getMouse()

            for produto, botao in botao_adicionar.items(): 
                y_pos = 80 + list(estoque.keys()).index(produto) * 50 
                if clicar_no_botao(botao, click_point):
                    valor_total_atual += estoque[produto]["valor"]
            
                    if produto in compras:
                        compras[produto] += 1  
                    else:
                        compras[produto] = 1  

                    break

            if clicar_no_botao(botao_finalizar, click_point):
                for produto, quantidade in compras.items(): 
                    if produto in estoque:
                        estoque[produto]["quantidade"] -= quantidade  

                gs.Text(gs.Point(350, 650), f"Compra finalizada! Total: R$ {valor_total_atual:.2f}").draw(win)
                salvar_estoque(estoque)
 
                win.getMouse()

                valor_total_atual = 0  
                compras = {} 
                
                break

def aba_reduzir_estoque(win, estoque):
    processar_compra(win, estoque)

def sistema_estoque():
    estoque = carregar_estoque()

    win = gs.GraphWin("Karanlık Ay Store", 700, 700, 'purple')  # Janela maior
    win.setBackground("white")

    gs.Image(gs.Point(350, 80), 'logo.gif').draw(win)

    titulo = gs.Text(gs.Point(350, 200), "Karanlık Ay Store")
    titulo.setSize(30)
    titulo.setStyle("bold")
    titulo.setTextColor("purple")
    titulo.draw(win)
    sub_titulo = gs.Text(gs.Point(350, 240), "Velas Aromáticas")
    sub_titulo.setSize(20)
    sub_titulo.setStyle("italic")
    sub_titulo.draw(win)

    botao_adicionar = criar_botao(win, "Adicionar Produto", 200, 350, 250, 50, "lavender")
    botao_verificar = criar_botao(win, "Verificar Estoque", 500, 350, 250, 50, "lavender")
    botao_comprar = criar_botao(win, "Compras", 500, 450, 250, 50, "lavender")
    botao_exibir = criar_botao(win, "Exibir Estoque", 200, 450, 250, 50, "lavender")
    botao_sair = criar_botao(win, "Sair", 350, 530, 250, 50, "lavender")

    while True:
        if win.isClosed():
            break

        if win.checkMouse():
            click_point = win.getMouse()
        else:
            continue 

        if clicar_no_botao(botao_adicionar, click_point):
            win_add = gs.GraphWin("Adicionar Produto", 400, 350)

            gs.Text(gs.Point(200, 50), "Produto:").draw(win_add)
            input_produto = gs.Entry(gs.Point(200, 70), 15)
            input_produto.draw(win_add)

            gs.Text(gs.Point(200, 100), "Quantidade:").draw(win_add)
            input_quantidade = gs.Entry(gs.Point(200, 120), 15)
            input_quantidade.draw(win_add)

            gs.Text(gs.Point(200, 150), "Valor:").draw(win_add)
            input_valor = gs.Entry(gs.Point(200, 170), 15)
            input_valor.draw(win_add)

            botao_voltar = criar_botao_voltar_x(win_add)
            botao_concluir = criar_botao_concluir(win_add)

            while True:
                if win_add.isClosed():
                    break

                if win_add.checkMouse():
                    click_point = win_add.getMouse()
                else:
                    continue

                if clicar_no_botao(botao_voltar, click_point):
                    win_add.close()
                    break

                if clicar_no_botao(botao_concluir, click_point):
                    produto = input_produto.getText().upper()
                    quantidade = int(input_quantidade.getText())
                    valor = float(input_valor.getText())  
                    if produto in estoque:
                        estoque[produto]["quantidade"] += quantidade
                    else:
                        estoque[produto] = {"quantidade": quantidade, "valor": valor}

                    salvar_estoque(estoque)
                    win_add.close()
                    break

        elif clicar_no_botao(botao_verificar, click_point):
            win_verifica = gs.GraphWin("Verificar Produto", 500, 500)
            gs.Text(gs.Point(250, 50), "Produto:").draw(win_verifica)
            input_produto = gs.Entry(gs.Point(250, 70), 15)
            input_produto.draw(win_verifica)

            botao_voltar = criar_botao_voltar_x(win_verifica)
            botao_concluir = criar_botao_concluir(win_verifica)

            while True:
                if win_verifica.isClosed():
                    break

                if win_verifica.checkMouse():
                    click_point = win_verifica.getMouse()
                else:
                    continue 

                if clicar_no_botao(botao_voltar, click_point):
                    win_verifica.close()
                    break

                if clicar_no_botao(botao_concluir, click_point):
                    produto = input_produto.getText().upper()  
                    quantidade = estoque.get(produto, 0)
                    gs.Text(gs.Point(250, 100), f"Quantidade: {
                            quantidade}").draw(win_verifica)
                    win_verifica.getMouse()
                    win_verifica.close()  
                    break

        elif clicar_no_botao(botao_comprar, click_point):
            win_reduce = gs.GraphWin("Compras", 700, 700)
            aba_reduzir_estoque(win_reduce, estoque)

        elif clicar_no_botao(botao_exibir, click_point):
            exibir_estoque(win, estoque)
            
            botao_voltar = criar_botao_voltar_x(win)
            
            while not win.isClosed(): 
                if clicar_no_botao(botao_voltar, win.getMouse()):
                    break 

        elif clicar_no_botao(botao_sair, click_point):
            break

    win.close()

sistema_estoque()
