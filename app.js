// --- REAL PROTOCOL LOGIC (NO MOCKS) ---
const tabs = document.querySelectorAll('.nav-item');
const contents = document.querySelectorAll('.tab-content');
const scribeChat = document.getElementById('scribeChat');
const scribeInput = document.getElementById('scribeInput');
const sendBtn = document.getElementById('sendBtn');
const forgeBtn = document.getElementById('forgeBtn');
const cipherVisualizer = document.getElementById('cipherVisualizer');
const forgeOutput = document.getElementById('forgeOutput');
const cidValue = document.getElementById('cidValue');
const protocolLog = document.getElementById('protocolLog');
const kvBody = document.getElementById('kvBody');
const pinataJwtInput = document.getElementById('pinataJwt');

// --- INITIALIZATION ---
function init() {
    refreshKv();
    setupTabs();
    setupScribe();
}

// --- TAB SYSTEM ---
function setupTabs() {
    tabs.forEach(tab => {
        tab.addEventListener('click', async () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
            
            if (tab.dataset.tab === 'cloudflare') {
                await refreshKv();
            }
        });
    });
}

// --- THE SCRIBE (REAL AI) ---
function setupScribe() {
    sendBtn.addEventListener('click', () => sendMessage());
    scribeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

async function sendMessage() {
    const text = scribeInput.value.trim();
    if (!text) return;

    appendChat('user', text);
    scribeInput.value = '';

    try {
        appendChat('system', 'Consulting the Scribe via Workers AI...');
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        
        // Remove the "Consulting..." message
        scribeChat.removeChild(scribeChat.lastChild);
        
        // Cloudflare Workers AI returns { response: "..." }
        appendChat('system', data.response || "The Scribe is silent.");
    } catch (err) {
        scribeChat.removeChild(scribeChat.lastChild);
        appendChat('system', "Connection failure. Ensure the Worker is deployed with [ai] binding.");
    }
}

function appendChat(role, text) {
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.innerHTML = `<span class="prefix">[${role.toUpperCase()}]</span> ${text}`;
    scribeChat.appendChild(div);
    scribeChat.scrollTop = scribeChat.scrollHeight;
}

// --- FORGE SEQUENCE (REAL ECIES + IPFS) ---
forgeBtn.addEventListener('click', async () => {
    const plainText = document.getElementById('plainText').value;
    const recipientPubKey = document.getElementById('pubKey').value;
    const jwt = pinataJwtInput.value;

    if (!plainText || !recipientPubKey || !jwt) {
        alert("CRITICAL: PLAIN TEXT, PUBLIC KEY, and PINATA JWT are required for a real Forge.");
        return;
    }

    try {
        forgeBtn.disabled = true;
        cipherVisualizer.classList.add('forging');
        
        // 1. REAL ECIES ENCRYPTION
        cipherVisualizer.querySelector('.stage-text').innerText = "CALCULATING ECIES...";
        logProtocol("ENCRYPTION: Initializing ECIES-AES-GCM...");
        
        const dataToEncrypt = btoa(unescape(encodeURIComponent(plainText)));
        const encrypted = ecies.encrypt(recipientPubKey, dataToEncrypt);
        const encryptedHex = Array.from(encrypted).map(b => b.toString(16).padStart(2, '0')).join('');
        
        logProtocol("ECIES: Payload sealed. Size: " + encrypted.length + " bytes");

        // 2. REAL IPFS UPLOAD (PINATA)
        await wait(1000);
        cipherVisualizer.querySelector('.stage-text').innerText = "UPLOADING TO IPFS...";
        logProtocol("IPFS: Pinning encrypted blob...");

        const formData = new FormData();
        const blob = new Blob([encrypted], { type: 'application/octet-stream' });
        formData.append('file', blob, 'claviger_box.enc');

        const pinataRes = await fetch("https://api.pinata.cloud/pinning/pinFileToIPFS", {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${jwt}` },
            body: formData
        });

        if (!pinataRes.ok) throw new Error("IPFS Upload Failed: " + await pinataRes.text());
        
        const pinataData = await pinataRes.json();
        const cid = pinataData.IpfsHash;
        logProtocol("IPFS: Success. CID=" + cid);

        // 3. REAL KV REGISTRATION (via Worker API)
        await wait(1000);
        cipherVisualizer.querySelector('.stage-text').innerText = "REGISTERING ON KV...";
        
        const kvRes = await fetch('/api/forge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cid, recipientKey: recipientPubKey })
        });

        if (!kvRes.ok) throw new Error("KV Registration Failed");
        logProtocol("KV: Secret indexed on Cloudflare.");

        // FINISH
        cipherVisualizer.classList.remove('forging');
        cipherVisualizer.querySelector('.lock-icon').innerText = "✅";
        cipherVisualizer.querySelector('.stage-text').innerText = "FORGE COMPLETED";
        
        forgeOutput.classList.remove('hidden');
        cidValue.innerText = cid;
        
        appendChat('system', `Protocol fulfilled. Secret immortalized at ipfs://${cid}`);
        
    } catch (err) {
        console.error(err);
        cipherVisualizer.classList.remove('forging');
        cipherVisualizer.querySelector('.stage-text').innerText = "FORGE FAILED";
        logProtocol("ERROR: " + err.message);
        alert(err.message);
    } finally {
        forgeBtn.disabled = false;
    }
});

function logProtocol(msg) {
    const entry = document.createElement('div');
    entry.innerText = `> ${msg}`;
    protocolLog.appendChild(entry);
    protocolLog.scrollTop = protocolLog.scrollHeight;
}

// --- CLOUDFLARE KV REAL RENDER ---
async function refreshKv() {
    try {
        const response = await fetch('/api/kv');
        const items = await response.json();
        kvBody.innerHTML = items.map(item => `
            <tr>
                <td>${item.key}</td>
                <td class="mono">${item.value}</td>
                <td>PERPETUAL</td>
                <td><button class="status-badge">${item.status}</button></td>
            </tr>
        `).join('');
    } catch (e) {
        console.error("KV Refresh failed", e);
    }
}

// --- VAULT DECRYPTION (REAL UNLOCK) ---
const unlockBtn = document.getElementById('unlockBtn');
const decryptedOutput = document.getElementById('decryptedOutput');
const decryptedJson = document.getElementById('decryptedJson');

unlockBtn.addEventListener('click', async () => {
    const cid = document.getElementById('inputCid').value.trim();
    const privateKey = document.getElementById('privateKey').value.trim();

    if (!cid || !privateKey) {
        alert("CID and Private Key required for decryption.");
        return;
    }

    try {
        unlockBtn.innerText = "UNLOCKING...";
        unlockBtn.disabled = true;

        // 1. Download from gateway
        const gwUrl = `https://ipfs.io/ipfs/${cid}`;
        const response = await fetch(gwUrl);
        if (!response.ok) throw new Error("Could not retrieve file from IPFS gateway.");
        
        const encryptedData = await response.arrayBuffer();
        
        // 2. Real ECIES Decryption
        // Note: eciesjs expects hex keys without 0x
        const cleanKey = privateKey.startsWith('0x') ? privateKey.slice(2) : privateKey;
        const decrypted = ecies.decrypt(cleanKey, new Uint8Array(encryptedData));
        
        const decoded = new TextDecoder().decode(decrypted);
        // If it's a base64 encoded string from Forge, decode it
        const finalJson = decodeURIComponent(escape(atob(decoded)));

        decryptedOutput.classList.remove('hidden');
        decryptedJson.innerText = JSON.stringify(JSON.parse(finalJson), null, 4);
        
        appendChat('system', "Vault access granted. The secret telah d-manifestasikan.");

    } catch (err) {
        console.error(err);
        alert("Decryption Failed: " + err.message);
    } finally {
        unlockBtn.innerText = "UNLOCK SECRETS";
        unlockBtn.disabled = false;
    }
});

function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

init();
