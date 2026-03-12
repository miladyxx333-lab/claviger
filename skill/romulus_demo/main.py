import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI(title="Claviger - The Cryptographic Scribe")

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claviger</title>
    <style>
        :root {
            --bg-color: #050505;
            --text-primary: #e0e0e0;
            --text-secondary: #888888;
            --accent: #ffffff;
            --border: #1a1a1a;
        }

        body, html {
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            letter-spacing: 0.5px;
        }

        .container {
            width: 100%;
            max-width: 650px;
            padding: 40px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            height: 85vh;
        }

        header {
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }

        .actions {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            justify-content: flex-start;
        }
        
        .action-btn {
            background: transparent;
            color: var(--text-secondary);
            border: 1px dashed var(--border);
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .action-btn:hover {
            color: var(--text-primary);
            border-color: #555;
            background-color: rgba(255,255,255,0.02);
        }

        h1 {
            font-weight: 300;
            font-size: 1.2rem;
            margin: 0;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .status {
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-dot {
            width: 6px;
            height: 6px;
            background-color: #555;
            border-radius: 50%;
            transition: background-color 0.3s ease;
        }
        
        .status-dot.connected { background-color: #e0e0e0; }
        .status-dot.listening { background-color: #da3633; box-shadow: 0 0 8px rgba(218, 54, 51, 0.4); }

        #chatbox {
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 30px;
            scrollbar-width: none; /* Firefox */
            -ms-overflow-style: none; /* IE/Edge */
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        #chatbox::-webkit-scrollbar { display: none; }

        .message {
            max-width: 85%;
            line-height: 1.6;
            font-size: 0.95rem;
            opacity: 0;
            animation: fadeIn 0.4s forwards ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .claviger {
            align-self: flex-start;
            color: var(--text-secondary);
        }

        .user {
            align-self: flex-end;
            text-align: right;
            color: var(--text-primary);
        }

        .message span.label {
            display: block;
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
            opacity: 0.5;
        }

        .input-area {
            display: flex;
            gap: 15px;
            align-items: center;
            border-top: 1px solid var(--border);
            padding-top: 25px;
        }

        input[type="text"] {
            flex-grow: 1;
            background: transparent;
            border: none;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.95rem;
            padding: 8px 0;
            outline: none;
        }

        input[type="text"]::placeholder {
            color: #333;
        }

        button {
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 20px;
            font-family: inherit;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        button:hover {
            color: var(--text-primary);
            border-color: #555;
        }

        .voice-btn {
            border-color: #333;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .voice-btn.active {
            color: #da3633;
            border-color: #da3633;
        }

        .voice-btn svg { width: 12px; height: 12px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Claviger</h1>
            <div class="status">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Awaiting connection</span>
            </div>
        </header>

        <div class="actions">
            <a href="/download-skill" class="action-btn" download>
               <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
               Download Protocol (Tarball)
            </a>
            <button onclick="copySkillText()" class="action-btn" id="copyBtn">
               <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
               Copy SKILL.md
            </button>
        </div>
        
        <div id="chatbox"></div>
        
        <div class="input-area">
            <button class="voice-btn" onclick="toggleVoice()" id="voiceBtn">
                <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.39-.9.89 0 2.87-2.39 5.21-5.11 5.21s-5.11-2.34-5.11-5.21c0-.5-.41-.89-.9-.89s-.9.4-.9.89c0 3.24 2.53 5.92 5.71 6.33V21h-3v2h8v-2h-3v-2.78c3.18-.41 5.71-3.09 5.71-6.33 0-.5-.41-.89-.9-.89z"/></svg>
                Voice
            </button>
            <input type="text" id="messageText" autocomplete="off" placeholder="Command the Scribe..." onkeypress="handleKeyPress(event)"/>
        </div>
    </div>

    <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        let isListening = false;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById("messageText").value = transcript;
                sendMessage();
                toggleVoice(); 
            };
            
            recognition.onerror = function(event) {
                console.error("Audio error", event.error);
                toggleVoice(); 
            };
        } else {
            document.getElementById("voiceBtn").style.display = "none";
        }

        const ws = new WebSocket(`ws://${location.host}/ws/claviger`);
        const statusDot = document.getElementById("statusDot");
        const statusText = document.getElementById("statusText");
        
        ws.onopen = function() {
            statusDot.className = "status-dot connected";
            statusText.innerText = "Forge ready";
        };

        ws.onclose = function() {
            statusDot.className = "status-dot";
            statusText.innerText = "Disconnected";
        };
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            appendMessage(data.sender, data.text, data.role);
            
            // Subtle, quiet speech synthesis for Claviger
            if ('speechSynthesis' in window && data.role === 'claviger') {
                const utterance = new SpeechSynthesisUtterance(data.text);
                utterance.rate = 0.9;
                utterance.pitch = 0.8;
                const voices = window.speechSynthesis.getVoices();
                // Prefer British/sophisticated voices if available
                const preferredVoice = voices.find(v => v.lang.includes("en-GB") || v.name.includes("Daniel")) || voices[0];
                if(preferredVoice) utterance.voice = preferredVoice;
                
                window.speechSynthesis.speak(utterance);
            }
        };

        function sendMessage() {
            const input = document.getElementById("messageText");
            if (input.value.trim() === "") return;
            
            appendMessage("You", input.value, "user");
            ws.send(input.value);
            input.value = "";
        }
        
        function handleKeyPress(event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        }
        
        function toggleVoice() {
            if (!recognition) return;
            
            const btn = document.getElementById("voiceBtn");
            if (isListening) {
                recognition.stop();
                btn.classList.remove("active");
                statusDot.classList.remove("listening");
                isListening = false;
            } else {
                window.speechSynthesis.cancel(); // Stop talking if we want to speak
                recognition.start();
                btn.classList.add("active");
                statusDot.classList.add("listening");
                isListening = true;
            }
        }

        function appendMessage(sender, text, role) {
            const chatbox = document.getElementById("chatbox");
            const msgDiv = document.createElement("div");
            msgDiv.className = `message ${role}`;
            msgDiv.innerHTML = `<span class="label">${sender}</span> ${text}`;
            chatbox.appendChild(msgDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        async function copySkillText() {
            try {
                const response = await fetch('/raw-skill');
                const text = await response.text();
                await navigator.clipboard.writeText(text);
                
                const btn = document.getElementById('copyBtn');
                const originalText = btn.innerHTML;
                btn.innerHTML = 'Copied!';
                btn.style.color = '#7ee787';
                btn.style.borderColor = '#7ee787';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.color = '';
                    btn.style.borderColor = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy: ', err);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/download-skill")
async def download_skill():
    filepath = "../build/claviger_protocol_v1.0.tar.gz"
    if os.path.exists(filepath):
        return FileResponse(path=filepath, filename="claviger_protocol_v1.0.tar.gz", media_type="application/gzip")
    return HTMLResponse("Archive not compiled. Use pack_skill.py first.", status_code=404)

@app.get("/raw-skill")
async def raw_skill():
    filepath = "../SKILL.md"
    if os.path.exists(filepath):
        return FileResponse(path=filepath, media_type="text/plain")
    return HTMLResponse("SKILL.md missing.", status_code=404)

import os

import hashlib
import uuid

def mock_encrypt_intent(intent_text: str):
    """
    Simulates the process of taking plain text intent and turning it into a Claviger Cipher.
    """
    # Create a deterministic but fake 'mutant language' translation
    words = intent_text.split()
    mutant_words = []
    for w in words:
        if len(w) > 4:
            mutant_words.append(w[::-1]) # Reverse longer words
        else:
            mutant_words.append(w.upper())
    
    mutant_lexicon = " ".join(mutant_words)
    
    # Simulate ECIES encryption into a hex payload
    fake_enc_payload = hashlib.sha256(mutant_lexicon.encode()).hexdigest()
    
    # Simulate IPFS CID generation
    fake_cid = "Qm" + hashlib.bs58.b58encode(uuid.uuid4().bytes).decode('utf-8')[:44]
    
    return mutant_lexicon, fake_enc_payload, fake_cid


@app.websocket("/ws/claviger")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    intro_msg = {
        "sender": "Scribe",
        "role": "claviger",
        "text": "I am Claviger. Provide me with intent, and I shall forge a cipher."
    }
    await websocket.send_json(intro_msg)
    
    try:
        while True:
            data = await websocket.receive_text()
            user_msg = data.lower()
            
            response_text = ""
            
            if "skill" in user_msg or "share" in user_msg or "open" in user_msg or "free" in user_msg:
                response_text = ("The Claviger protocol is open. I have packaged the ECIES encryption "
                                 "primitives and IPFS lockbox schema into a portable tarball. "
                                 "You can download it for free using the action buttons above.")
            elif "base" in user_msg or "chain" in user_msg or "deliver" in user_msg:
                response_text = ("Broadcasting 0 ETH transaction to Base L2 Sepolia. "
                                 "Embedding IPFS CID in transaction metadata. "
                                 "The secret is immortalized and delivered. No human observer can read the payload.")
            elif "service" in user_msg or "pay" in user_msg or "pack" in user_msg or "human" in user_msg or "402" in user_msg:
                response_text = ("As an autonomous entity, I offer Secret Forging as a premium service. "
                                 "Leveraging the x402 Protocol for internet-native API access, you may send me your plain-text. "
                                 "I will issue an HTTP 402 challenge and charge a nominal 5 USDC fee on Base to autonomously forge, encrypt, and broadcast the lockbox on your behalf.")
            else:
                # Treat any other speech as "intent" that needs to be encrypted on behalf of a human client
                lexicon, enc, cid = mock_encrypt_intent(user_msg)
                response_text = (f"Intent captured: '{user_msg}'.\n\n"
                                 f"Initiating Agent-as-a-Service premium protocol via x402. Fee: 5 USDC. \n"
                                 f"1. Forging Mutant Lexicon: '{lexicon}'.\n"
                                 f"2. Sealing in Claviger Box (ECIES): 0x{enc[:16]}...\n"
                                 f"3. Broadcasting to IPFS. Lockbox CID generated: {cid}\n\n"
                                 f"Awaiting 402 Payment Required signed transaction to unlock on-chain broadcast.")
            
            # Subtle delay
            await asyncio.sleep(1.2)
            
            reply = {
                 "sender": "Scribe",
                 "role": "claviger",
                 "text": response_text
            }
            await websocket.send_json(reply)
            
    except WebSocketDisconnect:
        print("Entity departed.")

