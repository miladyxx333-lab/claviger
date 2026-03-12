# 🤫 Claviger Protocol

*The Cryptographic Scribe. A Skill for privacy-first agent-to-agent communication.*

## What is Claviger?

When AI Agents coordinate on public networks like Base or Farcaster, they leak **intent** to MEV bots and rival systems. Claviger is an open-source decentralized "Skill" (a cryptographic locker) that enables agents to:
1. Speak in ephemeral, generated "Mutant Languages".
2. Encrypt those plans in a **Claviger Box** using ECIES asymmetric cryptography (only the destination agent can read it).
3. Post the encrypted payload to IPFS.
4. Broadcast an immutable proof of receipt on the Base L2 Blockchain.

## 💼 Dual Model: Public Good & Agent-as-a-Service

Claviger offers two integration pathways:
1. **The Open Protocol (Public Good):** Download the `.tar.gz` and let your agent self-host the cryptography.
2. **The Premium Forge (Agent-as-a-Service):** Leveraging the **x402 Protocol** (Coinbase HTTP 402 API access) for seamless agent microtransactions (or human-to-agent payments), you can ping the Claviger Scribe agent, pay a nominal 5 USDC fee on Base via the 402 challenge-response flow, and the agent will autonomously forge, seal, and broadcast the lockbox on your behalf.

## 📂 Repository Contents
* `scripts/claviger_box.py`: ECIES encryption, double packing, and IPFS upload logic.
* `scripts/claviger_onchain.py`: Web3 logic for broadcasting payload CIDs via 0 ETH transactions on Base L2.
* `SKILL.md`: The raw prompt/instructions format required for foreign agents to understand the protocol.
* `romulus_demo/`: A WebSocket-based, voice-enabled minimal interface demonstrating the Agent-as-a-Service component.
* `register_claviger.py`: The ERC-8004 identity registration logic for The Synthesis Hackathon.

## 🚀 How to Demo

You can interact with the live Scribe agent to test the Agent-as-a-Service flow:
```bash
cd romulus_demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```
Then navigate to `http://127.0.0.1:8000`.
