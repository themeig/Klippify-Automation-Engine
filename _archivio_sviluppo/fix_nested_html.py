import os

filepath = r"C:\Users\HP\Desktop\contenuti klippify\generate_report.py"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "<!-- VIEW 4: TIKTOK MANAGER SECTION             -->" in line:
        skip = True
        # remove previous line which is "        <!-- ========================================== -->\n"
        if new_lines and "======" in new_lines[-1]:
            new_lines.pop()
        continue
    
    if skip:
        if "</div> <!-- closes container -->" in line:
            skip = False
            # Before closing the container, we need to close the view-studio-section
            new_lines.append("    </div> <!-- End Studio View -->\n")
            new_lines.append(line)
        continue
    
    new_lines.append(line)

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Removed old tiktok section inside studio section.")
