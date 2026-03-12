export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);

        // 🤖 REAL AI SCRIBE (using Cloudflare Workers AI)
        if (url.pathname === "/api/chat" && request.method === "POST") {
            const { message } = await request.json();
            try {
                const response = await env.AI.run("@cf/qwen/qwen1.5-7b-chat-awq", {
                    messages: [
                        { role: "system", content: "You are the Claviger Scribe, a master of cryptography and secret forged scripts. Speak with authority and elegance." },
                        { role: "user", content: message }
                    ]
                });
                return new Response(JSON.stringify(response), {
                    headers: { "content-type": "application/json" }
                });
            } catch (e) {
                return new Response(JSON.stringify({ error: "Scribe is exhausted.", detail: e.message }), { status: 500 });
            }
        }

        // 📦 REAL KV VAULT LIST
        if (url.pathname === "/api/kv" && request.method === "GET") {
            try {
                const list = await env.CLAVIGER_SECRETS.list();
                const items = await Promise.all(list.keys.map(async (key) => {
                    const value = await env.CLAVIGER_SECRETS.get(key.name);
                    return { key: key.name, value: value, status: "SECURED" };
                }));
                return new Response(JSON.stringify(items), {
                    headers: { "content-type": "application/json" }
                });
            } catch (e) {
                return new Response(JSON.stringify([]), { headers: { "content-type": "application/json" } });
            }
        }

        // 🔒 REAL FORGE (Storage coordination)
        if (url.pathname === "/api/forge" && request.method === "POST") {
            const { cid, recipientKey } = await request.json();
            try {
                // Register the CID in KV associated with the recipient's public key fragment
                await env.CLAVIGER_SECRETS.put(`vault:${recipientKey.slice(0, 8)}`, cid, {
                    metadata: { timestamp: Date.now() }
                });
                return new Response(JSON.stringify({ success: true }), {
                    headers: { "content-type": "application/json" }
                });
            } catch (e) {
                return new Response(JSON.stringify({ error: e.message }), { status: 500 });
            }
        }

        // 🌐 STATIC ASSETS SERVICE
        if (env.ASSETS) {
            return env.ASSETS.fetch(request);
        }

        return new Response("Claviger Worker active. ASSETS missing.", { status: 404 });
    },
};
