import os

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update HTML Form in generate_report.py
old_html = """                        <div style="flex:2; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">2. Titolo / Caption del Video</label>
                            <input type="text" id="tiktok-video-caption" placeholder="Scrivi una descrizione per TikTok... #klippify #trend" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem;">
                        </div>"""

new_html = """                        <div style="flex:2; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">2. Titolo del Video</label>
                            <input type="text" id="tiktok-video-title" placeholder="Es. Il segreto del successo" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem; margin-bottom:1rem;">
                            
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">3. Descrizione / Caption</label>
                            <textarea id="tiktok-video-caption" rows="3" placeholder="Scrivi una descrizione lunga, inserisci gli hashtag... #klippify #trend" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem; font-family:inherit; resize:vertical;"></textarea>
                            
                            <div style="margin-top:1rem; display:flex; align-items:center; gap:1rem;">
                                <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700;">4. Copertina (secondi):</label>
                                <input type="number" id="tiktok-video-cover" value="1.0" step="0.5" min="0" style="width:80px; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.5rem; border-radius:0.5rem; font-size:0.95rem; text-align:center;">
                            </div>
                        </div>"""
content = content.replace(old_html, new_html)

# 2. Update JS function publishToTikTok
old_js = """        async function publishToTikTok() {
            const sel = document.getElementById('tiktok-video-select');
            const cap = document.getElementById('tiktok-video-caption');
            const btn = document.getElementById('tiktok-publish-btn');
            const status = document.getElementById('tiktok-publish-status');
            
            const filename = sel.value;
            const title = cap.value.trim();
            
            if (!filename) { alert("Seleziona prima un video!"); return; }
            if (!title) { alert("Scrivi un titolo per il video!"); return; }
            
            btn.disabled = true;
            btn.innerHTML = "⏳ Caricamento...";
            status.innerText = "";
            
            try {
                const res = await fetch('/api/tiktok/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filename, title })
                });"""

new_js = """        async function publishToTikTok() {
            const sel = document.getElementById('tiktok-video-select');
            const titleInput = document.getElementById('tiktok-video-title');
            const capInput = document.getElementById('tiktok-video-caption');
            const coverInput = document.getElementById('tiktok-video-cover');
            const btn = document.getElementById('tiktok-publish-btn');
            const status = document.getElementById('tiktok-publish-status');
            
            const filename = sel.value;
            const titleStr = titleInput.value.trim();
            const capStr = capInput.value.trim();
            const coverTimeSec = parseFloat(coverInput.value) || 1.0;
            
            if (!filename) { alert("Seleziona prima un video!"); return; }
            if (!titleStr) { alert("Il Titolo è obbligatorio!"); return; }
            
            // TikTok has only ONE field for text, we combine Title and Caption
            const combinedTitle = capStr ? (titleStr + "\\n\\n" + capStr) : titleStr;
            const coverTimeMs = Math.floor(coverTimeSec * 1000);
            
            btn.disabled = true;
            btn.innerHTML = "⏳ Caricamento in corso... attendi...";
            status.innerText = "";
            
            try {
                const res = await fetch('/api/tiktok/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        filename: filename, 
                        title: combinedTitle,
                        cover_time_ms: coverTimeMs
                    })
                });"""
content = content.replace(old_js, new_js)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated generate_report.py successfully.")
