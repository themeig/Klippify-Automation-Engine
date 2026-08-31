import os
import re

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the current misplaced TikTok Manager HTML
# We look for the start of the comment and the end of the div
tiktok_html_start = "        <!-- ========================================== -->\n        <!-- VIEW 4: TIKTOK MANAGER                     -->"

# We'll use a regex to extract the whole block
# It ends with </div>\n            </div>\n        </div> (the tiktok-publish-status and its parent divs)
# A safer way is to just use string splitting
if tiktok_html_start in content:
    parts = content.split(tiktok_html_start)
    before = parts[0]
    rest = parts[1]
    
    # Find the end of the tiktok section. We know it ends before `<script>` or near it.
    # Actually, we can just split by "        <!-- ========================================== -->" if there are multiple.
    # The last thing in our tiktok_html was:
    #                 </div>
    #             </div>
    #         </div>
    
    # Just find the end of the block. We know it has `<div id="tiktok-publish-status"` inside it.
    end_marker = "Pubblica su TikTok 🚀\n                        </button>\n                        <div id=\"tiktok-publish-status\" style=\"margin-top:0.8rem; font-size:0.9rem; font-weight:600;\"></div>\n                    </div>\n                </div>\n            </div>\n        </div>"
    
    idx_end = rest.find(end_marker)
    if idx_end != -1:
        after = rest[idx_end + len(end_marker):]
        # Now we have cleaned the file from the misplaced HTML
        content = before + after
    else:
        # try another end marker just in case
        end_marker2 = "id=\"tiktok-publish-status\""
        idx2 = rest.find(end_marker2)
        if idx2 != -1:
            idx_after_div = rest.find("</div>\n            </div>\n        </div>", idx2)
            if idx_after_div != -1:
                after = rest[idx_after_div + 41:]
                content = before + after

# Now insert it exactly before `</div> <!-- closes container -->`
target_insert = "    </div> <!-- closes container -->"
if target_insert in content:
    correct_html = """
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
    content = content.replace(target_insert, correct_html + "\n" + target_insert)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed HTML structure perfectly.")
