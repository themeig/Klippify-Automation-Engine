import os
import re

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Tab Button
tab_target = """<button id="main-tab-studio" class="main-tab-btn" onclick="switchMainView('studio')">
                🎬 Content Studio ({gen_count})
            </button>"""
tab_replacement = tab_target + """
            <button id="main-tab-tiktok" class="main-tab-btn" onclick="switchMainView('tiktok')">
                📱 TikTok Manager
            </button>"""
content = content.replace(tab_target, tab_replacement)

# 2. Add TikTok View Section before the end of the container
# Find the end of view-studio-section
studio_end_target = """</div> <!-- End Studio View -->"""

tiktok_html = """
        <!-- ========================================== -->
        <!-- VIEW 4: TIKTOK MANAGER                     -->
        <!-- ========================================== -->
        <div id="view-tiktok-section" class="creator-dashboard-v2" style="display: none;">
            <div class="dashboard-welcome-header">
                <h1>TikTok Manager 📱</h1>
                <p>Gestisci il tuo account TikTok e pubblica i video generati con un clic.</p>
            </div>

            <!-- Stats Grid -->
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
                        <button onclick="publishToTikTok()" id="tiktok-publish-btn" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; padding:0.8rem 1.5rem; border:radius:0.5rem; font-size:1rem; font-weight:700; border:none; border-radius:0.5rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(16, 185, 129, 0.3);">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                            Pubblica su TikTok 🚀
                        </button>
                        <div id="tiktok-publish-status" style="margin-top:0.8rem; font-size:0.9rem; font-weight:600;"></div>
                    </div>
                </div>
            </div>
        </div>
"""
# I need to insert it before the closing container div.
# But there might not be a '<!-- End Studio View -->' comment. Let's just insert it before '    </div>' which closes the container, which is right before `<script>`.
content = content.replace("    </div>\n\n    <script>", tiktok_html + "\n    </div>\n\n    <script>")

# 3. Add to switchMainView
switch_target_1 = """const studioView = document.getElementById('view-studio-section');"""
switch_repl_1 = switch_target_1 + """\n            const tiktokView = document.getElementById('view-tiktok-section');"""
content = content.replace(switch_target_1, switch_repl_1)

switch_target_2 = """const studioBtn = document.getElementById('main-tab-studio');"""
switch_repl_2 = switch_target_2 + """\n            const tiktokBtn = document.getElementById('main-tab-tiktok');"""
content = content.replace(switch_target_2, switch_repl_2)

switch_target_3 = """studioView.style.display = 'none';"""
switch_repl_3 = switch_target_3 + """\n            tiktokView.style.display = 'none';"""
content = content.replace(switch_target_3, switch_repl_3)

switch_target_4 = """studioBtn.classList.remove('active');"""
switch_repl_4 = switch_target_4 + """\n            tiktokBtn.classList.remove('active');"""
content = content.replace(switch_target_4, switch_repl_4)

switch_target_5 = """studioView.scrollIntoView({ behavior: 'smooth' });
                renderStudioCards();
                fetchAndRenderVideos();
            }"""
switch_repl_5 = switch_target_5 + """ else if (viewName === 'tiktok') {
                tiktokView.style.display = 'flex';
                tiktokBtn.classList.add('active');
                tiktokView.scrollIntoView({ behavior: 'smooth' });
                loadTikTokData();
            }"""
content = content.replace(switch_target_5, switch_repl_5)

# 4. Add loadTikTokData and publishToTikTok JS functions
js_code = """
        async function loadTikTokData() {
            // Load stats
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
                            <div class="k-stat-val">${followers.toLocaleString()}</div>
                            <div class="k-stat-sub">Followers totali</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-icon-wrapper" style="background: rgba(239, 68, 68, 0.15); color: #ef4444;">
                            <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>
                        </div>
                        <div class="k-stat-info">
                            <div class="k-stat-title">Mi Piace Totali</div>
                            <div class="k-stat-val">${likes.toLocaleString()}</div>
                            <div class="k-stat-sub">Su tutti i tuoi video</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-icon-wrapper" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">
                            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
                        </div>
                        <div class="k-stat-info">
                            <div class="k-stat-title">Video Pubblicati</div>
                            <div class="k-stat-val">${videos.toLocaleString()}</div>
                            <div class="k-stat-sub">Video attivi sul profilo</div>
                        </div>
                    </div>
                `;
                document.getElementById('tiktok-stats-container').innerHTML = statsHtml;
            } catch(e) {
                document.getElementById('tiktok-stats-container').innerHTML = `<div style="color:red;">Errore: ${e.message}</div>`;
            }

            // Load videos into select
            try {
                const res = await fetch('/api/videos');
                const videos = await res.json();
                const sel = document.getElementById('tiktok-video-select');
                if (videos.length === 0) {
                    sel.innerHTML = '<option value="">Nessun video generato trovato.</option>';
                } else {
                    sel.innerHTML = '<option value="">Seleziona un video da pubblicare...</option>' + 
                        videos.map(v => `<option value="${v.filename}">${v.filename} (${(v.size / 1024 / 1024).toFixed(1)} MB)</option>`).join('');
                }
            } catch(e) {
                console.error("Errore caricamento video", e);
            }
        }

        async function publishToTikTok() {
            const sel = document.getElementById('tiktok-video-select');
            const cap = document.getElementById('tiktok-video-caption');
            const btn = document.getElementById('tiktok-publish-btn');
            const status = document.getElementById('tiktok-publish-status');
            
            const filename = sel.value;
            const title = cap.value.trim();
            
            if (!filename) { alert("Seleziona prima un video!"); return; }
            if (!title) { alert("Scrivi un titolo/caption per il video!"); return; }
            
            btn.disabled = true;
            btn.innerHTML = "⏳ Caricamento in corso... (non chiudere la pagina)";
            btn.style.opacity = "0.7";
            status.innerText = "";
            
            try {
                const res = await fetch('/api/tiktok/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filename, title })
                });
                
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                status.innerText = "✅ Video pubblicato con successo su TikTok!";
                status.style.color = "#10b981";
                cap.value = "";
                sel.selectedIndex = 0;
            } catch (e) {
                status.innerText = "❌ Errore durante la pubblicazione: " + e.message;
                status.style.color = "#ef4444";
            }
            
            btn.disabled = false;
            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Pubblica su TikTok 🚀`;
            btn.style.opacity = "1";
        }
"""
content = content.replace("</script>\n</body>", js_code + "\n    </script>\n</body>")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Injected successfully!")
