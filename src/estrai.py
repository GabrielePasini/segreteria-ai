import sys
import datetime
GIORNI = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]

# sys.argv contiene il nome dello script più il percorso dell'email, quindi devono essere esattamente 2 elementi.
if len(sys.argv) != 2:
    print("Uso: python src/estrai.py <percorso_email>")
    sys.exit(1)
    
percorso_email = sys.argv[1]

# lettura dell'email dal file passato come argomento
with open(percorso_email, "r", encoding="utf-8") as file:
   testo_email = file.read()

# lettura del file estrazione.txt contenente il modello del prompt da integrare con le informazioni mancanti
with open("prompts/estrazione.txt", "r", encoding="utf-8") as file:
    modello_prompt = file.read()

# python da il nome del giorno in inglese, la lista in italiano e la posizione corrisponde a .weekday()  
oggi = datetime.date.today()
data_per_prompt = f"{GIORNI[oggi.weekday()]} {oggi.isoformat()}"
    
# rimpiazzo prima la data di oggi nel modello del prompt in modo che il messaggio 
# del cliente nella mail non possa essere minimamente modificato
prompt = modello_prompt.replace("[DATA_OGGI]", data_per_prompt)

prompt_finale = prompt.replace("[TESTO_EMAIL]", testo_email)
print(prompt_finale)