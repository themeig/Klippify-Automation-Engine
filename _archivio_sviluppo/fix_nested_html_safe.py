import os

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# We need to find the OLD block and remove it.
# The old block starts at:
#         <!-- ========================================== -->
#         <!-- VIEW 4: TIKTOK MANAGER SECTION             -->
#         <!-- ========================================== -->
#         <div id="view-tiktok-section" style="margin-top: 1rem; display: none;">

start_str = "        <!-- ========================================== -->\n        <!-- VIEW 4: TIKTOK MANAGER SECTION             -->\n        <!-- ========================================== -->\n        <div id=\"view-tiktok-section\" style=\"margin-top: 1rem; display: none;\">"
start_idx = content.find(start_str)

if start_idx != -1:
    # We need to find where this old block ends.
    # It ends with:
    #                     </div>
    #                 </div>
    #             </div>
    #         </div>
    # Just before the NEW block or the container close.
    # Let's just find the next "<!-- ========================================== -->" which belongs to the NEW block.
    next_block_idx = content.find("        <!-- ========================================== -->\n        <!-- VIEW 4: TIKTOK MANAGER                     -->", start_idx + 10)
    
    if next_block_idx != -1:
        # Before next_block_idx, there should be closing divs.
        # Let's just remove from start_idx up to next_block_idx.
        # But wait! view-studio-section needs to be closed.
        # If we remove everything, view-studio-section is never closed. We must add a closing </div> for view-studio-section.
        content = content[:start_idx] + "    </div> <!-- End Studio View -->\n" + content[next_block_idx:]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Removed old block and closed studio view correctly.")
    else:
        print("Could not find the new block.")
else:
    print("Could not find the old block start string.")
