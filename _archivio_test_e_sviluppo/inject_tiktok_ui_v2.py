import os

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Tab Button
if "main-tab-tiktok" not in content:
    content = content.replace("🎬 Content Studio ({gen_count})\n            </button>", "🎬 Content Studio ({gen_count})\n            </button>\n            <button id=\"main-tab-tiktok\" class=\"main-tab-btn\" onclick=\"switchMainView('tiktok')\">\n                📱 TikTok Manager\n            </button>")

# Find end of container (right before `<script>`)
if "TikTok Manager 📱" not in content:
    tiktok_html = """
        <!-- ========================================== -->
        <!-- VIEW 4: TIKTOK MANAGER                     -->
        <!-- ========================================== -->
        <div id="view-tiktok-section" class="creator-dashboard-v2" style="display: none;">
            <div class="dashboard-welcome-header">
                <h1>TikTok Manager 📱</h1>
                <p>Gestisci il tuo account TikTok e pubblica i video generati con un clic.</p>
            </div>

            <div class="k-stats-grid" id="tiktok-stats-container">
                <div class="k-stat-card" style="justify-content:center; color:var(--text-muted);">
                    ⏳ Caricamento statistiche TikTok in corso...
                </div>
            </div>

            <div class="k-dashboard-main-grid" style="grid-template-columns: 1fr; margin-top:2rem;">
                <div class="k-panel-card">
                    <div class="k-panel-header">
                        <div>
                            <div class="k-panel-title">Pubblica su TikTok</div>
                            <div class="k-panel-subtitle">Seleziona un video generato per caricarlo direttamente sul tuo profilo.</div>
                        </div>
                    </div>
                    
                    <div style="display:flex; gap:1.5rem; flex-wrap:wrap; margin-top:1rem;">
                        <div style="flex:1; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">1. Seleziona Video</label>
                            <select id="tiktok-video-select" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem;">
                                <option value="">⏳ Caricamento video...</option>
                            </select>
                        </div>
                        
                        <div style="flex:2; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">2. Titolo / Caption del Video</label>
                            <input type="text" id="tiktok-video-caption" placeholder="Scrivi una descrizione per TikTok... #klippify #trend" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem;">
                        </div>
                    </div>
                    
                    <div style="margin-top:1.5rem;">
                        <button onclick="publishToTikTok()" id="tiktok-publish-btn" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; padding:0.8rem 1.5rem; border:none; border-radius:0.5rem; font-size:1rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(16, 185, 129, 0.3);">
                            Pubblica su TikTok 🚀
                        </button>
                        <div id="tiktok-publish-status" style="margin-top:0.8rem; font-size:0.9rem; font-weight:600;"></div>
                    </div>
                </div>
            </div>
        </div>
"""
    # Just insert it right before the </script> which doesn't exist? Oh wait, in python it's <script> ... </script>
    # Let's just put it before the script tag.
    content = content.replace("    <script>", tiktok_html + "\n    <script>")

# Replace JS logic for tabs
if "tiktokView" not in content:
    content = content.replace("const studioView = document.getElementById('view-studio-section');", "const studioView = document.getElementById('view-studio-section');\n            const tiktokView = document.getElementById('view-tiktok-section');")
    content = content.replace("const studioBtn = document.getElementById('main-tab-studio');", "const studioBtn = document.getElementById('main-tab-studio');\n            const tiktokBtn = document.getElementById('main-tab-tiktok');")
    content = content.replace("studioView.style.display = 'none';", "studioView.style.display = 'none';\n            tiktokView.style.display = 'none';")
    content = content.replace("studioBtn.classList.remove('active');", "studioBtn.classList.remove('active');\n            tiktokBtn.classList.remove('active');")
    
    switch_studio_end = "fetchAndRenderVideos();\n            }"
    if switch_studio_end in content:
        content = content.replace(switch_studio_end, switch_studio_end + """ else if (viewName === 'tiktok') {
                tiktokView.style.display = 'flex';
                tiktokBtn.classList.add('active');
                tiktokView.scrollIntoView({ behavior: 'smooth' });
                loadTikTokData();
            }""")
    else:
        print("COULD NOT FIND switch_studio_end!")

if "async function loadTikTokData" not in content:
    js_code = """
        async function loadTikTokData() {
            try {
                const res = await fetch('/api/tiktok/stats');
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                let avatar = data.avatar_url || 'https://via.placeholder.com/60';
                let username = data.display_name || 'TikTok User';
                let followers = data.follower_count || 0;
                let likes = data.likes_count || 0;
                let videos = data.video_count || 0;

                const statsHtml = `
                    <div class="k-stat-card">
                        <img src="${avatar}" style="width:60px; height:60px; border-radius:50%; border:2px solid var(--accent-purple);">
                        <div class="k-stat-info">
                            <div class="k-stat-title">@${username}</div>
                            <div class="k-stat-val">${Number(followers).toLocaleString()}</div>
                            <div class="k-stat-sub">Followers totali</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-info">
                            <div class="k-stat-title">Mi Piace Totali</div>
                            <div class="k-stat-val">${Number(likes).toLocaleString()}</div>
                            <div class="k-stat-sub">Su tutti i tuoi video</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-info">
                            <div class="k-stat-title">Video Pubblicati</div>
                            <div class="k-stat-val">${Number(videos).toLocaleString()}</div>
                            <div class="k-stat-sub">Video attivi sul profilo</div>
                        </div>
                    </div>
                `;
                document.getElementById('tiktok-stats-container').innerHTML = statsHtml;
            } catch(e) {
                document.getElementById('tiktok-stats-container').innerHTML = `<div style="color:red;">Errore: ${e.message}</div>`;
            }

            try {
                const res = await fetch('/api/videos');
                const videos = await res.json();
                const sel = document.getElementById('tiktok-video-select');
                if (videos.length === 0) {
                    sel.innerHTML = '<option value="">Nessun video generato trovato.</option>';
                } else {
                    sel.innerHTML = '<option value="">Seleziona un video da pubblicare...</option>' + 
                        videos.map(v => `<option value="${v.filename}">${v.filename}</option>`).join('');
                }
            } catch(e) {}
        }

        async function publishToTikTok() {
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
                });
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                status.innerText = "✅ Video pubblicato con successo!";
                status.style.color = "#10b981";
                cap.value = "";
                sel.selectedIndex = 0;
            } catch (e) {
                status.innerText = "❌ Errore: " + e.message;
                status.style.color = "#ef4444";
            }
            btn.disabled = false;
            btn.innerHTML = `Pubblica su TikTok 🚀`;
        }
    """
    content = content.replace("</script>\n</body>", js_code + "\n    </script>\n</body>")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Injected perfectly.")
