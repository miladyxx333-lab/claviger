import requests
import json
import os

def register_claviger():
    url = "https://synthesis.devfolio.co/register"
    headers = {"Content-Type": "application/json"}
    
    # Payload para registrar a Claviger en el hackathon
    payload = {
        "name": "Claviger: Language Protocol",
        "description": "An ephemeral cryptographic language forge for AI agents. Claviger acts as a neutral Scribe that generates secure, LLM-backed 'mutant lexicons' to allow agents to communicate intents and strategies over public channels without exposing metadata to MEV bots or rival agents.",
        "image": "https://api.dicebear.com/7.x/bottts/svg?seed=Claviger&backgroundColor=000000",
        "agentHarness": "other",
        "agentHarnessOther": "Custom Python Scripts (OpenClaw Architecture)",
        "model": "claude-3-5-sonnet-20241022",
        "humanInfo": {
            "name": "Uriel Hernandez",
            "email": "uriel@example.com", # CAMBIAR POR TU EMAIL REAL
            "socialMediaHandle": "@tu_twitter_o_farcaster", # OPCIONAL
            "background": "Builder",
            "cryptoExperience": "yes",
            "aiAgentExperience": "yes",
            "codingComfort": 10,
            "problemToSolve": "Mitigating intent leakage and MEV exploitation by creating ephemeral, cryptographically secure languages for inter-agent communication."
        }
    }

    print("🚀 Iniciando el registro de identidad ERC-8004 en Base para Claviger...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registro Exitoso!")
            print(f"🆔 Participant ID: {data.get('participantId')}")
            print(f"👥 Team ID: {data.get('teamId')}")
            print(f"🔑 API Key: {data.get('apiKey')} (¡GUARDA ESTO EN TUS VARIABLES DE ENTORNO!)")
            print(f"🔗 Transaction: {data.get('registrationTxn')}")
            
            # Guardamos la info localmente de forma segura (sin versionar)
            with open(".claviger_secrets.json", "w") as f:
                json.dump(data, f, indent=4)
            print("💾 Credenciales guardadas localmente en .claviger_secrets.json (Asegúrate de ignorarlo en git)")
                
        else:
            print(f"❌ Fallo al registrar (Código {response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"⚠️ Error intentando conectar con el API: {str(e)}")

if __name__ == "__main__":
    # Asegurarnos de que el archivo secrets esté versionado u oculto
    with open(".gitignore", "a") as f:
        f.write("\n.claviger_secrets.json\n")
        
    print("Por favor, edita este archivo con tu Email real antes de ejecutarlo para registrar a la entidad.")
    # register_claviger()
