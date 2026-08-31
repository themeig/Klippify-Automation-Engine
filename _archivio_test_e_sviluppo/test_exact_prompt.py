import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, r"c:\Users\HP\Desktop\contenuti klippify")

import gemini_bot

EXACT_PROMPT = """Vertical 9:16 cinematic video, 25 seconds. Strong emotional contrast hook in the first 2 seconds: a relatable creator looking overwhelmed at a gray corporate desk under cold office lights, rubbing her temples. A quick cinematic match-cut transition flips to a bright, sunlit morning room: the same creator relaxed in cozy aesthetic knitwear, enjoying her coffee while reviewing digital projects on a tablet with complete peace of mind. Followed by serene golden hour b-roll walking in nature, symbolizing independence. Soft natural tones, cinematic anamorphic bokeh, authentic storytelling tone. Ends with an empowering warm smile toward the camera. Brand rule: Rispetta le linee guida Klippify."""

print("="*60)
print("AVVIO TEST GEMINI BOT CON PROMPT ESATTO:")
print(EXACT_PROMPT)
print("="*60)

gemini_bot.run(prompt_to_send=EXACT_PROMPT, is_auto=True)
