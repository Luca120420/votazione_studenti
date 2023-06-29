# Programma di creazione e votazione proposte

## Questo programma consente agli utenti di creare e votare proposte utilizzando un database Redis. Gli utenti possono registrarsi o accedere al sistema, caricare nuove proposte, visualizzare le proposte attuali e votarle.

# Prerequisiti
- Python 3.x
- Libreria Redis

# Installazione e configurazione
- Assicurarsi di avere Python 3.x installato sul proprio sistema.
- Installare la libreria Redis eseguendo il seguente comando: pip install redis

# Utilizzo
- Eseguire il file proposta.py con Python: python proposta.py
- All'avvio, verrà richiesto di registrarsi o accedere. Se si sceglie di registrarsi, verrà richiesto di inserire un username e una password. Se si sceglie di accedere, verrà richiesto di inserire l'username e la password corrispondenti.
- Una volta effettuato l'accesso, verrà visualizzato un menu con le seguenti opzioni: "n" per caricare una nuova proposta e "v" per votare una proposta esistente.
- Se si sceglie di caricare una nuova proposta, verrà richiesto di inserire una descrizione per la proposta. Se la proposta esiste già, verrà chiesto se si desidera aggiungere il proprio username alla lista dei proponenti. In caso contrario, verrà chiesto se ci sono altri proponenti oltre all'utente corrente.
- Se si sceglie di votare una proposta, verrà visualizzato l'elenco delle proposte attuali con il numero di voti corrispondenti. Verrà quindi richiesto di inserire il numero della proposta da votare. Se la proposta non esiste o se l'utente ha già votato quella proposta, verrà mostrato un messaggio di errore.
- È possibile visualizzare l'elenco delle proposte attuali selezionando l'opzione corrispondente dal menu principale.
- Per uscire dal programma, premere Ctrl + C.


