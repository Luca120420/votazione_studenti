import redis

# Connettiti al database Redis
r = redis.Redis(
  host='redis-13715.c242.eu-west-1-2.ec2.cloud.redislabs.com',
  port=13715,
  password='jlXH1esGaf93WTtDkkrH8j0BUtHtEOU3')

# r.flushall() 

def login():
    while True:
        scelta = input("Vuoi registrarti o accedere (r/a)? ")

        if scelta.lower() == 'r':
            username = input("Inserisci il tuo username: ")
            if r.hexists("users", username):
               print("L'username è già stato registrato. Scegli un altro username.")
               continue
            password = input("Inserisci la tua password: ")
            r.hset("users", username, password)
        elif scelta.lower() == 'a':
            username = input("username: ")
            password = input("password: ")

            stored_password = r.hget("users", username)
            if stored_password == None:
                print("Username o password errati!!")
            elif stored_password.decode() == password:
                print("Accesso riuscito!")
                break
            else:
                print("Username o password errati!")
        else:
            print("Scelta non valida!")
        
    return username



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
        elif solo.lower() == 'n':
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
    proposte = r.keys("proposta:*")
    proposte = sorted(proposte, key=lambda p: int(r.hget(p, "voti")), reverse=True)
    for proposta in proposte:
        descrizione = r.hget(proposta, "descrizione").decode("utf-8")
        proponenti = r.hget(proposta, "proponenti").decode("utf-8")
        voti = r.hget(proposta, "voti").decode("utf-8")
        proponenti = " ".join(proponenti.split(","))  # Replace commas with spaces
        print(f"{descrizione} ({proponenti}): {voti} voti")



def vota_proposta(nome_studente):
    # Chiedi all'utente di inserire il numero della proposta da votare
    numero_proposta = input("Che proposta voti? ")
    proposta = "proposta:" + numero_proposta
    
    # Controlla se la proposta esiste nel database
    if not r.exists(proposta):
        print("Proposta non valida")
        return

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
    username = login()
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
            vota_proposta(username)
        else:
            print("Opzione non valida")

# Avvia l'applicazione
mostra_menu()