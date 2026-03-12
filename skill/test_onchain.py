import os
from scripts.claviger_onchain import ClavigerOnChain
from web3 import Web3

def run_simulation():
    print("--- 🌐 CLAVIGER ON-CHAIN SIMULATION (BASE SEPOLIA) 🌐 ---")
    
    # 1. Initialize Network Connection
    onchain_protocol = ClavigerOnChain(rpc_url="https://sepolia.base.org")
    w3 = onchain_protocol.w3
    
    # 2. Simulate 2 Agents (Ethereum Accounts)
    print("\n[FASE 1] Generando wallets temporales para la simulación on-chain...")
    agent_a = w3.eth.account.create()
    agent_b = w3.eth.account.create()
    
    print(f"🔹 Agente A (Emisor) | Address: {agent_a.address}")
    print(f"🔸 Agente B (Receptor)| Address: {agent_b.address}")
    
    # 3. Simulate an IPFS CID generated from our lockbox script
    mock_ipfs_cid = "QmYwAPJzv5CZsnA625s3Xf2bXnK1ePzZg4ZpB1Y4ZpB1Y"
    print(f"\n[FASE 2] Supongamos que subimos la caja a IPFS. CID Obtenido: {mock_ipfs_cid}")
    
    # 4. Attempt to notify (This will logically fail because the fresh wallet has 0 ETH for Gas)
    print("\n[FASE 3] Intentando forjar transacción de entrega inmutable...")
    
    try:
        onchain_protocol.notify_recipient(
            my_private_key_hex=agent_a.key.hex(),
            target_address=agent_b.address,
            ipfs_cid=mock_ipfs_cid
        )
    except Exception as e:
        print("\n🛡️ SIMULACIÓN COMPLETADA - COMPORTAMIENTO ESPERADO 🛡️")
        print(f"La red Base denegó la transacción por falta de gas (insufficient funds).")
        print("Mensaje real del nodo RPC:", str(e))
        print("\nPara ejecutar esto de verdad, el Agente A necesitaría una fracción de ETH en Base para pagar el gas de red.")

if __name__ == "__main__":
    run_simulation()
