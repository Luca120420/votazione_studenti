import redis

# Connettiti al database Redis
r = redis.Redis(
  host='redis-13715.c242.eu-west-1-2.ec2.cloud.redislabs.com',
  port=13715,
  password='jlXH1esGaf93WTtDkkrH8j0BUtHtEOU3')

def carica_proposta():
    # Chiedi all'utente di inserire la descrizione della proposta e la carico su Redis
    return
    
    
def mostra_proposte():
    # Mostra tutte le proposte attuali ordinate per numero di voti
    return


def vota_proposta():
    # Chiedi all'utente di inserire il numero della proposta da votare
    numero_proposta = input("Che proposta voti? ")
    proposta = "proposta:" + numero_proposta
    
    # Controlla se la proposta esiste nel database
    if not r.exists(proposta):
        print("Proposta non valida")
        return

    # Chiedi all'utente di inserire il proprio nome
    nome_studente = input("Chi sei? ")

    # Controlla se lo studente ha già votato la proposta
    if r.sismember("voti:" + nome_studente, proposta):
        print("Hai già votato questa proposta")
        return

    # Incrementa il numero di voti della proposta e aggiungi il voto dello studente
    r.hincrby(proposta, "voti", amount=1)
    r.sadd("voti:" + nome_studente, proposta)
    print("Voto registrato con successo")



def mostra_menu():
    #richiama le altre funzioni
    while True:
        print("\nProposte attuali:")
        mostra_proposte()
        print("\nScegli un'opzione:")
        print("n. Nuova proposta")
        print("v. Vota una proposta")

        opzione = input()
        if opzione == "n":
            carica_proposta()
        elif opzione == "v":
            mostra_proposte()
            vota_proposta()
        else:
            print("Opzione non valida")

# Avvia l'applicazione
mostra_menu()