import redis

# Connettiti al database Redis
r = redis.Redis(
  host='redis-13715.c242.eu-west-1-2.ec2.cloud.redislabs.com',
  port=13715,
  password='jlXH1esGaf93WTtDkkrH8j0BUtHtEOU3')

def carica_proposta(username):
    # Chiedi all'utente di inserire la descrizione della proposta
    descrizione = input("Descrivi la proposta: ")
    existing_proposta_id = None
    existing_proposta_descrizioni = []

    for key in r.scan_iter("proposta:*"):
        existing_descrizione = r.hget(key, "descrizione").decode()
        if existing_descrizione == descrizione:
            existing_proposta_id = key
            break
        existing_proposta_descrizioni.append(existing_descrizione)

    if existing_proposta_id:
        print("Questa proposta è già stata inserita. Aggiungo il tuo username alla lista di proponenti.")
        proponenti = r.hget(existing_proposta_id, "proponenti").decode().split(",")
        proponenti.append(username)
        proponenti = list(set(proponenti))  # Rimuovi eventuali doppioni
        r.hset(existing_proposta_id, "proponenti", ",".join(proponenti))
        print("Aggiunto proponente alla proposta esistente.")

    else:
        # Chiedi all'utente di inserire i nomi dei proponenti separati da virgole
        solo = input("Oltre a te ci sono altri proponenti? s/n? ")
        if solo.lower() == 's':
            proponenti = input("Inserisci i loro nomi e separali da una virgola ").split(',')
            if username not in proponenti:
                proponenti.append(username)
        else:
            proponenti = [username]
        
        # Crea una nuova chiave per la proposta nel database Redis
        proposta_id = r.incr("proposta_id")
        # Aggiungi la descrizione e i proponenti alla proposta
        r.hset("proposta:" + str(proposta_id), "descrizione", descrizione)
        r.hset("proposta:" + str(proposta_id), "proponenti", ",".join(proponenti))
        r.hset("proposta:" + str(proposta_id), "voti", 0)
        print("Proposta caricata con successo.")

    
def mostra_proposte():
    # Mostra tutte le proposte attuali ordinate per numero di voti
    return


def vota_proposta():
    # Chiedi all'utente di inserire il numero della proposta da votare
    return


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
            carica_proposta(username)
        elif opzione == "v":
            mostra_proposte()
            vota_proposta()
        else:
            print("Opzione non valida")

# Avvia l'applicazione
mostra_menu()