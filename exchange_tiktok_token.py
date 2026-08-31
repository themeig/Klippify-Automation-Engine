import urllib.request
import urllib.parse
import json
import sys

client_key = "sbawkrz4lc399y38a3"
code = "37p8ugqVMyuzvhWdB1YnuP9d-xPH7OyE8MX4oIw7WnnRU0BUNTDlP7dKnKmjRIfYJ4mstN25Utm5vW8h43nf1tkVYpFhNhqfE86bHcqMTldRjQefYLh6ziPbt7h0DYqLLevOApVN3umd_6-pMs97I-mCFshcb8_pjVKyNtvvseoDfLBF828J4Bc5ZtsGoTqQDQ1cj4YnvlTqvrdtudI_T-tDo-JdSTgFBbylj8uFHZL-ltPXQtuFFb-ZKWE*v!4930.e1"
redirect_uri = "https://klippify-test-999.surge.sh/callback"
code_verifier = "test_verifier_klippify_12345678901234567890"

print("="*50)
client_secret = input("Inserisci il tuo Client Secret da TikTok: ").strip()

url = "https://open.tiktokapis.com/v2/oauth/token/"
data = {
    "client_key": client_key,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code_verifier": code_verifier
}

encoded_data = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request(url, data=encoded_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n✅ SUCCESSO! Ecco i tuoi token:")
        print(json.dumps(result, indent=2))
        
        with open("tiktok_tokens.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\nI token sono stati salvati in 'tiktok_tokens.json'.")
except urllib.error.HTTPError as e:
    print("\n❌ ERRORE DA TIKTOK:")
    print("Codice Errore:", e.code)
    print("Risposta:", e.read().decode('utf-8'))
    print("\n⚠️ ATTENZIONE: Il 'code' scade dopo pochi minuti. Se ricevi errore, genera un nuovo link e riprova.")
