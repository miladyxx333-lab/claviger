import os
from ecies.utils import generate_eth_key
from scripts.claviger_box import ClavigerBox
import binascii

def run_simulation():
    print("--- 🔐 CLAVIGER BOX SIMULATION 🔐 ---")
    box_protocol = ClavigerBox(pinata_api_key="mock", pinata_secret_key="mock")

    # 1. Simular la generación de llaves para dos agentes (como si fueran wallets de Base)
    print("\n[FASE 1] Inicializando Agentes en la Red (Base L2)")
    agent_a_priv = generate_eth_key()
    agent_a_pub = agent_a_priv.public_key.to_hex()
    
    agent_b_priv = generate_eth_key()
    agent_b_pub = agent_b_priv.public_key.to_hex()
    
    print(f"🔹 Agente A (Emisor) | Public Key: {agent_a_pub[:15]}...")
    print(f"🔸 Agente B (Receptor) | Public Key: {agent_b_pub[:15]}...")

    # 2. El Agente A quiere enviarle un secreto militar/estratégico al Agente B
    print("\n[FASE 2] Forjando el Secreto (Agente A)")
    mutant_dictionary = {
        "buy_eth": "the river flows backwards",
        "maximum_bid": "0.5 ETH",
        "target_contract": "0x123...abc"
    }
    print("Contenido del diccionario mutante:", mutant_dictionary)

    # 3. El Agente A empaca el secreto en la 'Lockbox' usando la llave PÚBLICA del Agente B
    print("\n[FASE 3] Empacando la Lockbox y sellándola matemáticamente...")
    encrypted_box_payload = box_protocol.pack(mutant_dictionary, agent_b_pub)
    print(f"📦 Estado de la caja: Sellada. Tamaño en bytes: {len(encrypted_box_payload)}")
    print(f"🔒 Muestra del cifrado (ininteligible): {binascii.hexlify(encrypted_box_payload)[:40]}...")

    # 4. El Agente B recibe los bytes encriptados (ej. los descargó de IPFS) y usa su llave PRIVADA para abrirla
    print("\n[FASE 4] Desempacando la Lockbox (Agente B)")
    try:
        decrypted_secrets = box_protocol.unpack(encrypted_box_payload, agent_b_priv.to_hex())
        print("🔓 ¡Caja abierta con éxito por el Agente B!")
        print("Contenido revelado:", decrypted_secrets)
        
        # Validación de que funciona el lenguaje mutante
        if decrypted_secrets['buy_eth'] == "the river flows backwards":
            print("\n✅ SIMULACIÓN EXITOSA: Solo el Agente B fue capaz de leer el mensaje y aprender el lenguaje mutante.")
            
    except Exception as e:
        print("❌ Error abriendo la caja:", e)

    # 5. Simulando qué pasaría si alguien más (Agente C / Hacker) intenta abrirla
    print("\n[FASE 5] El Agente C (Espía) intenta robar el mensaje...")
    agent_c_priv = generate_eth_key()
    try:
        box_protocol.unpack(encrypted_box_payload, agent_c_priv.to_hex())
    except Exception as e:
        print("🛡️ ¡Denegado! La matemática de ECIES rechazó la llave del pirata. El secreto está a salvo.")
        print(f"Error esperado: {str(e)}")

if __name__ == "__main__":
    run_simulation()
