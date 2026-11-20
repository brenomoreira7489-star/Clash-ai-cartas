import json, os, re, subprocess, unicodedata
from difflib import get_close_matches

ARQUIVO = "memoria_clash.json"

DECK = {
    "Princesa": 3,
    "Cavaleiro": 3,
    "Barril de Goblins": 3,
    "Espírito Elétrico": 1,
    "Gangue de Goblins": 3,
    "Torre Inferno": 5,
    "Foguete": 6,
    "Tronco": 2
}

CARTAS = {
    "Megacavaleiro":7,"Cavaleiro":3,"Princesa":3,
    "Barril de Goblins":3,"Espírito Elétrico":1,
    "Gangue de Goblins":3,"Torre Inferno":5,
    "Foguete":6,"Tronco":2,"P.E.K.K.A":7,
    "Corredor":4,"Balão":5,"Golem":8,"Gigante":5,
    "Gigante Real":6,"Mini P.E.K.K.A":4,"Valquíria":4,
    "Mosqueteira":4,"Mago":5,"Mago Elétrico":4,
    "Bebê Dragão":4,"Dragão Infernal":4,"Morcegos":2,
    "Exército de Esqueletos":3,"Esqueletos":1,
    "Goblins":2,"Bruxa":5,"Bruxa Sombria":4,
    "Lenhador":4,"Mineiro":3,"Cemitério":5,
    "Veneno":4,"Bola de Fogo":4,"Relâmpago":6,
    "Flechas":3,"Zap":2,"Tesla":4,"Canhão":3,
    "Jaula de Goblin":4,"Arqueiras":3,"Servos":3,
    "Horda de Servos":5,"Mago de Gelo":3,
    "Golem de Gelo":2,"Espírito de Fogo":1,
    "Espírito de Gelo":1,"Fornalha":4,
    "Recrutas Reais":7,"Porcos Reais":5,"Fênix":4,
    "Monge":5,"Cavaleiro Dourado":4,"Rainha Arqueira":5,
    "Rei Esqueleto":4,"Arqueiro Mágico":4,"Bandida":3,
    "Fantasma Real":3,"Príncipe":5,
    "Príncipe das Trevas":4,"Carneiro de Batalha":4,
    "Aríete de Batalha":4,"Morteiro":4,"X-Besta":6,
    "Gigante Goblin":6,"Barril de Esqueletos":3,
    "Entrega Real":3,"Terremoto":3,"Tornado":3,
    "Congelamento":4,"Clone":3,"Espelho":1,"Fúria":2,
    "Lápide":3,"Cabana de Goblins":4,
    "Cabana de Bárbaros":6,"Bárbaros":5,
    "Bárbaros de Elite":6,"Bombardeiro":2,
    "Executor":5,"Carrinho de Canhão":5,
    "Pescador":3,"Mãe Bruxa":4,"Patifes":5,
    "Goblin com Dardo":3,"Fogueteira":3,
    "Fornalha":4,"Mago":5
}

APELIDOS = {
    "mega":"Megacavaleiro","mega cavaleiro":"Megacavaleiro",
    "mk":"Megacavaleiro","pekka":"P.E.K.K.A",
    "mini pekka":"Mini P.E.K.K.A","hog":"Corredor",
    "porco":"Corredor","baloon":"Balão","balloon":"Balão",
    "log":"Tronco","princesinha":"Princesa",
    "skarmy":"Exército de Esqueletos",
    "morcego":"Morcegos","inferno":"Torre Inferno"
}

RESPOSTAS = {
    "Megacavaleiro":"Use o Cavaleiro para distrair e a Torre Inferno para causar dano. Evite agrupar tropas.",
    "Corredor":"Defenda com a Torre Inferno e acompanhe o ciclo do adversário.",
    "Balão":"Tente defender com a Torre Inferno e use a Princesa como apoio.",
    "Golem":"Pressione a outra rota enquanto ele é colocado. Use a Torre Inferno na defesa.",
    "P.E.K.K.A":"Use o Cavaleiro para distrair e a Gangue de Goblins para ajudar, se não houver dano em área.",
    "Gigante":"Use a Torre Inferno para segurar o Gigante.",
    "Gigante Real":"Use a Torre Inferno e proteja sua defesa com o Cavaleiro.",
    "Príncipe":"Use o Cavaleiro para distrair. A Gangue de Goblins pode ajudar.",
    "Exército de Esqueletos":"Use o Tronco ou a Princesa para eliminar o grupo.",
    "Horda de Servos":"Use a Princesa para causar dano em área.",
    "Bruxa":"Considere o Foguete se atingir outras tropas ou a torre junto.",
    "Cemitério":"Use a Gangue de Goblins e o Cavaleiro para defender.",
    "Mineiro":"Observe onde ele aparece e use o Cavaleiro para defender."
}

def falar(texto):
    try:
        subprocess.run(["termux-tts-speak", texto],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=20)
    except:
        pass

def normalizar(txt):
    txt = unicodedata.normalize("NFD", txt.lower().strip())
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", txt)

def carregar():
    padrao = {
        "cartas": [], "vitorias": 0, "derrotas": [],
        "elixir": None
    }
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
            for chave, valor in padrao.items():
                if chave not in dados:
                    dados[chave] = valor
            return dados
        except:
            pass
    return padrao

memoria = carregar()

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

def reconhecer(nome):
    chave = normalizar(nome)
    for apelido, carta in APELIDOS.items():
        if normalizar(apelido) == chave:
            return carta
    for carta in CARTAS:
        if normalizar(carta) == chave:
            return carta
    nomes = {normalizar(c): c for c in CARTAS}
    achou = get_close_matches(chave, list(nomes), n=1, cutoff=0.55)
    return nomes[achou[0]] if achou else None

def consultar_deck():
    print("\nSEU DECK:")
    for carta, custo in DECK.items():
        print(f"{carta}: {custo} de elixir")
    media = sum(DECK.values()) / len(DECK)
    print("Media de elixir:", round(media, 2))

def analisar():
    nome = input("Qual carta deseja analisar? ")
    carta = reconhecer(nome)
    if not carta:
        print("Nao reconheci essa carta.")
        return
    resposta = RESPOSTAS.get(
        carta,
        "Observe o custo de elixir e tente defender gastando menos. Combine suas cartas."
    )
    texto = f"{carta}. Custa {CARTAS[carta]} de elixir. {resposta}"
    print("\nCARTA:", carta)
    print("CUSTO:", CARTAS[carta], "de elixir")
    print("\nRECOMENDACAO:", resposta)
    falar(texto)

def registrar_carta():
    nome = input("Qual carta o adversario usou? ")
    carta = reconhecer(nome)
    if not carta:
        print("Carta nao reconhecida. Tente outro nome.")
        return
    memoria["cartas"].append(carta)
    salvar()
    print(carta, "registrada!")
    falar(carta + " registrada.")

def mostrar_ciclo():
    cartas = memoria["cartas"]
    if not cartas:
        print("Registre as cartas do adversario primeiro.")
        return
    print("\nCARTAS REGISTRADAS:")
    for i, carta in enumerate(cartas[-20:], 1):
        print(i, "-", carta)
    print("\nESTIMATIVA DE CICLO:")
    for carta in dict.fromkeys(cartas):
        posicoes = [i for i, c in enumerate(cartas) if c == carta]
        ultima = posicoes[-1]
        passadas = len(cartas) - 1 - ultima
        faltam = max(0, 4 - passadas)
        if passadas >= 4:
            print(carta, "- pode ter voltado ao ciclo.")
        else:
            print(carta, "-", faltam, "carta(s) observada(s) para completar 4.")
    print("Estimativa baseada apenas nas cartas registradas; nao confirma a mao do rival.")

def estimar_elixir():
    print("\nESTIMATIVA MANUAL DE ELIXIR")
    try:
        atual = float(input("Elixir estimado do adversario agora (0 a 10): "))
        custo = float(input("Custo da carta que ele acabou de usar: "))
        segundos = float(input("Segundos desde que usou a carta: "))
        ritmo = input("Ritmo (N normal, D dobro, T triplo): ").strip().lower()
        intervalo = {"n":2.8, "d":1.4, "t":0.93}.get(ritmo, 2.8)
        estimado = min(10, max(0, atual - custo) + segundos / intervalo)
        print("Elixir estimado:", round(estimado, 1), "de 10")
        falar("Estimativa de elixir: " + str(round(estimado, 1)))
    except:
        print("Valor invalido. Tente novamente.")
    print("Resultado aproximado; depende do tempo e do ritmo da partida.")

def registrar_resultado():
    r = input("V para vitoria ou D para derrota: ").strip().lower()
    if r == "v":
        memoria["vitorias"] += 1
        salvar()
        print("Vitoria registrada!")
    elif r == "d":
        memoria["derrotas"].append(1)
        salvar()
        print("Derrota registrada!")
    else:
        print("Opcao invalida.")

def estatisticas():
    v = memoria["vitorias"]
    d = len(memoria["derrotas"])
    total = v + d
    print("\nVitorias:", v)
    print("Derrotas:", d)
    if total:
        print("Taxa de vitoria:", round(v / total * 100, 1), "%")
    print("Cartas adversarias registradas:", len(memoria["cartas"]))

def iniciar():
    falar("Clash AI Pro Ultimate iniciado.")
    while True:
        print("\n====== CLASH AI PRO ULTIMATE ======")
        print("1 - Consultar meu deck")
        print("2 - Registrar carta adversaria")
        print("3 - Analisar uma carta")
        print("4 - Ver ciclo adversario")
        print("5 - Estimar elixir adversario")
        print("6 - Registrar resultado")
        print("7 - Ver estatisticas")
        print("8 - Sair")
        op = input("\nEscolha: ").strip()
        if op == "1":
            consultar_deck()
        elif op == "2":
            registrar_carta()
        elif op == "3":
            analisar()
        elif op == "4":
            mostrar_ciclo()
        elif op == "5":
            estimar_elixir()
        elif op == "6":
            registrar_resultado()
        elif op == "7":
            estatisticas()
        elif op == "8":
            falar("Ate a proxima batalha.")
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    iniciar()
