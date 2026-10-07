from dotenv import load_dotenv
from anthropic import Anthropic

PREZZO_INPUT_PER_MILIONE = 1
PREZZO_OUTPUT_PER_MILIONE = 5

# legge il file .env e carica le sue variabili nell'mabiente del programma
load_dotenv()

# client legge da solo ANTHROPIC_API_KEY dall'ambiente, non serve passargliela
client = Anthropic()

# manda il messaggio a Claude; max_tokens limita la lunghezza della risposta
risposta = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=[{"role": "user", "content": "Ciao, rispondimi con una frase"}]
)

# content è una lista di blocchi: il testo sta nel primo
testo = risposta.content[0].text

# token utilizzati sia in input che in output
token_input = risposta.usage.input_tokens
token_output = risposta.usage.output_tokens

# prezzi di Claude Haiku 4.5, in dollari per milione di token
costo_input = (token_input * PREZZO_INPUT_PER_MILIONE) / 1000000
costo_output = (token_output * PREZZO_OUTPUT_PER_MILIONE) / 1000000
costo_totale = costo_input + costo_output

print(f"Risposta: {testo}")
print(f"Token Input: {token_input}") 
print(f"Token Output: {token_output}")
print(f"Costo: {costo_totale:.6f} $")