import sys
import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

# python da il nome del giorno in inglese, la lista in italiano e la posizione corrisponde a .weekday()
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MODELLO = "claude-haiku-4-5-20251001"

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

lista_giorni = []
oggi = datetime.date.today()

# "oggi" e "domani" sono parole che il paziente scrive: servono righe dedicate.
# Oggi NON compare come "giovedì", altrimenti ci sarebbero due giovedì (08 e 15)
lista_giorni.append(f"oggi → {oggi.isoformat()}")
lista_giorni.append(f"domani → {oggi + datetime.timedelta(days=1)}")

for i in range(1, 8):
    nuova_data = oggi + datetime.timedelta(days=i)
    # Il nome va preso da nuova_data, non da oggi, altrimenti sarebbero tutti "giovedì"
    lista_giorni.append(f"{GIORNI[nuova_data.weekday()]} → {nuova_data.isoformat()}")
    
calendario = "\n".join(lista_giorni)

data_per_prompt = f"{GIORNI[oggi.weekday()]} {oggi.isoformat()}"
 
# rimpiazzo tutto il resto per prima cosa e infine il messaggio 
# del cliente in modo che non possa essere minimamente modificato
prompt = modello_prompt.replace("[CALENDARIO]", calendario)   
prompt = prompt.replace("[DATA_OGGI]", data_per_prompt)
prompt = prompt.replace("[TESTO_EMAIL]", testo_email)

load_dotenv()
client = Anthropic()

# chiamata al client Anthropic, max_tokens=300 lascia spazio al JSON completo: con 100 rischierebbe di essere tagliato
risposta = client.messages.create(
    model=MODELLO,
    max_tokens=300,
    messages=[{"role": "user", "content": prompt}]
)

testo = risposta.content[0].text
print(f"Risposta: {testo}")
print(f"Stop_reason: {risposta.stop_reason}")