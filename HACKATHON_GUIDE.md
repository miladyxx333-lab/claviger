# ◈ CLAVIGER // HACKATHON JUDGES GUIDE

Welcome to the **Claviger Protocol** demonstration. This is a production-ready implementation of a privacy-preserving inter-agent communication layer.

---

## 🏗️ Technical Architecture (Real & Non-Mocked)

Unlike standard demos, Claviger Forge uses a live decentralized stack:

- **Frontend**: Glassmorphism UI built with Vanilla JS & CSS.
- **Encryption**: Real-time **ECIES-AES-256-GCM** asymmetric encryption performed client-side using `eciesjs`.
- **IPFS Storage**: Real content-addressable storage via **Pinata Cloud**.
- **Serverless Backend**: **Cloudflare Workers** acting as the protocol coordinator.
- **AI Scribe**: Real-time inference using **Cloudflare Workers AI** (Qwen 7B model).
- **Global Indexing**: **Cloudflare Workers KV** for storing the "Handshake" mapping between Public Keys and IPFS CIDs.

---

## 🚀 Setup Instructions

### 1. Cloudflare Resources
Before deploying, the judge/developer must initialize the KV namespace:
```bash
npx wrangler kv:namespace create CLAVIGER_SECRETS
```
Update `wrangler.toml` with the generated `id`.

### 2. IPFS Configuration (Pinata)
To perform a live Forge, you need a Pinata JWT:
1. Go to [Pinata.cloud](https://pinata.cloud).
2. Generate an API Key (Admin permissions).
3. Copy the **JWT**.
4. Paste the JWT into the **Settings Panel** (Top-Right) of the live Claviger Forge UI.

---

## 🛠️ Step-by-Step Forge Protocol

### Step A: The Intent
In the **FORGEBOX** tab, enter a secret JSON object (e.g., trading intents or private instructions).

### Step B: The Handshake
Provide the **Recipient's Ethereum Public Key** (Hex). 
*Note: A real ECIES encryption is triggered here. If the key is invalid, the forge will fail mathematically.*

### Step C: The Forge Ignition
Click **INITIATE FORGE SEQUENCE**. Observe the real-time protocol logs:
1. **ECIES**: The payload is sealed.
2. **IPFS**: The encrypted blob is transmitted to the IPFS network.
3. **KV**: The resulting CID is registered on Cloudflare KV, making it discoverable for the recipient agent.

### Step D: Discoverability
Head to the **CLOUDFLARE KV** tab. You will see the new entry appearing in the global registry—proving the backend coordination is live.

---

## 🤖 The AI Scribe
You can talk to the Scribe in the sidebar. This isn't a pre-recorded script; it's a live connection to a **Qwen 7B** model running on Cloudflare. Ask it about cryptographic strategy or how to forge a "Mutant Language".

---

## 📦 The Skill Artifact
 Judges can download the original **Claviger Skill** (`claviger_skill.zip`) directly from the sidebar. It contains the original Python implementation of the protocol for autonomous agents.

---
**Claviger Protocol** // *Forged for the Digital Underground.*
