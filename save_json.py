import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = [
  {
    "campaign_id": "6a76d24b5ade3cb2f77429aa",
    "campaign_name": "Brunch e Cocktail a Peschiera del Garda",
    "section": "Nuove",
    "feasibility_score": 1039.0,
    "feasibility_rating": "ALTA",
    "feasibility_reasoning": "High payout potential and very high feasibility score relative to others.",
    "payout_per_1k": 1.0,
    "budget_remaining": 450.0,
    "video_prompt_gemini": "Genera un video in formato verticale 9:16 per TikTok di 15-30 secondi. Nei primi 2 secondi (hook), mostra un cocktail colorato e fumante su un tavolo al sole con lo sfondo del Lago di Garda a Peschiera, con un movimento di camera dinamico. Successivamente (3-15s) stacchi cinematici su pancake golosi, uova alla benedict e brindisi tra amici. Atmosfera vivace ed estetica luminosa. Chiudi con un cartello accattivante: Guarda il video completo su Klippify!",
    "tiktok_caption": "Brunch vista lago e cocktail spaziali? 🥞🍹 Tagga chi ti deve portare al @9dayscafbrunchcocktailsmore a Peschiera del Garda! 😍 👉 Guarda il video completo su Klippify! #brunchecocktailapeschieradelgarda #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-2s", "description": "Primo piano di un cocktail scenografico con ghiaccio secco fumante.", "text_overlay": "Il brunch perfetto esiste?"},
      {"scene": 2, "duration": "3-8s", "description": "Tagli rapidi su piatti deliziosi (pancake, uova).", "text_overlay": "Siamo a Peschiera del Garda!"},
      {"scene": 3, "duration": "9-15s", "description": "Amici che brindano, atmosfera felice e solare.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A vibrant vertical thumbnail showing a delicious brunch plate with pancakes and a colourful cocktail in the foreground, Lake Garda in the background, cinematic lighting"
  },
  {
    "campaign_id": "6a7239b2245627c6899bedf7",
    "campaign_name": "Il gusto francese sul Lago Maggiore",
    "section": "Nuove",
    "feasibility_score": 289.0,
    "feasibility_rating": "ALTA",
    "feasibility_reasoning": "High score and appealing food content.",
    "payout_per_1k": 1.0,
    "budget_remaining": 450.0,
    "video_prompt_gemini": "Genera un video in formato verticale 9:16 di 15-30 secondi per TikTok. Hook (0-2s): Un croissant perfetto e friabile che viene spezzato a metà, mostrando un interno soffice. 3-15s: Carrellata cinematografica su macaron colorati, caffè espresso fumante ed eleganti dolci stile francese. Sfondo sfocato che richiama il Lago Maggiore. Chiudi con la CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Un angolo di Parigi sul Lago Maggiore! 🥐✨ Non hai mai provato un croissant così. Vieni a scoprire @lapasticceria. Guarda il video completo su Klippify! #ilgustofrancesesullagomaggiore #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Croissant che viene spezzato a metà con suono croccante (ASMR).", "text_overlay": "Pov: Il miglior croissant fuori Parigi"},
      {"scene": 2, "duration": "3-10s", "description": "Macaron perfetti e pouring di un caffè fumante.", "text_overlay": "Tutto questo sul Lago Maggiore"},
      {"scene": 3, "duration": "11-15s", "description": "Estetica elegante del banco dolci.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A perfectly baked, flaky French croissant being torn apart, revealing buttery layers, vibrant colors, photorealistic, vertical layout"
  },
  {
    "campaign_id": "6a6dc4b494bf29a44b05d822",
    "campaign_name": "Scontly - UGC Campaign",
    "section": "Nuove",
    "feasibility_score": 219.9,
    "feasibility_rating": "ALTA",
    "feasibility_reasoning": "High payout ($4) and relatable problem (hotel prices dropping).",
    "payout_per_1k": 4.0,
    "budget_remaining": 450.0,
    "video_prompt_gemini": "Genera un video verticale 9:16 di 15-30 secondi. Hook (0-2s): Una persona guarda il telefono scioccata, tenendosi la testa. 3-15s: Schermate in grafica 3D che mostrano il prezzo di un hotel che scende. La persona sorride sollevata. Stile UGC, molto dinamico e luminoso. CTA finale: Guarda il video completo su Klippify!",
    "tiktok_caption": "Quando prenoti l'hotel e il giorno dopo costa la metà... 😭 Ma poi scopri @scontly! Ti rimborsano la differenza! 💸 Guarda il video completo su Klippify! #scontlyugccampaign #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Ragazzo disperato guardando lo smartphone.", "text_overlay": "Hai prenotato e il prezzo è sceso?"},
      {"scene": 2, "duration": "4-10s", "description": "Transizione felice, grafica con soldi che tornano nel portafoglio.", "text_overlay": "Scontly ti fa riavere i soldi!"},
      {"scene": 3, "duration": "11-15s", "description": "Persona che festeggia.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A shocked person looking at their smartphone screen which displays a dramatic price drop graph for a hotel room, high contrast, youtube thumbnail style"
  },
  {
    "campaign_id": "699ededd3f5febcf2f3acae9",
    "campaign_name": "WoodCrafts DIY",
    "section": "Iscritte",
    "feasibility_score": 187.0,
    "feasibility_rating": "ALTA",
    "feasibility_reasoning": "Extremely high payout ($6) and satisfying DIY niche.",
    "payout_per_1k": 6.0,
    "budget_remaining": 314.0,
    "video_prompt_gemini": "Generate a vertical 9:16 video, 15-30 seconds. Hook (0-2s): Fast-paced cinematic shot of a circular saw cutting wood with sawdust flying in slow motion. 3-15s: Montage of a beautiful, modern wooden furniture piece being assembled quickly by a hobbyist in a home garage. High quality, satisfying aesthetics. End with CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Build stunning furniture with zero experience! 🪚✨ Get the best plans from @woodcraftsdiy and start crafting! Guarda il video completo su Klippify! #woodcraftsdiy #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Sawdust flying as a piece of wood is perfectly cut.", "text_overlay": "No workshop? No problem."},
      {"scene": 2, "duration": "4-10s", "description": "Satisfying time-lapse of building a modern coffee table.", "text_overlay": "Build it yourself with WoodCrafts DIY"},
      {"scene": 3, "duration": "11-15s", "description": "The finished piece of furniture in a beautiful living room.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A highly aesthetic, satisfying close-up of a perfectly smooth wooden joint being assembled, warm lighting, woodworking vibe"
  },
  {
    "campaign_id": "6a22ff48e3244ca026570f72",
    "campaign_name": "FundedPoly",
    "section": "Nuove",
    "feasibility_score": 176.4,
    "feasibility_rating": "ALTA",
    "feasibility_reasoning": "Creative freedom and great payout ($5).",
    "payout_per_1k": 5.0,
    "budget_remaining": 500.0,
    "video_prompt_gemini": "Generate a vertical 9:16 video, 15-30 seconds. Hook (0-2s): A fast, chaotic, meme-style edit of a person holding a laptop on a mountain peak, looking at a trading chart. 3-15s: Quick zoom into the laptop screen showing the FundedPoly website with a futuristic glow. High energy, absurd and funny cinematic style. End with CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Trading from the top of the world 🏔️📈 Check out @fundedpoly! Guarda il video completo su Klippify! #fundedpoly51kfilmanythingjustshowthesite #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-2s", "description": "Absurd setup: trading on a mountain.", "text_overlay": "Me trading at 10,000 ft"},
      {"scene": 2, "duration": "3-8s", "description": "Close-up of the screen clearly showing the FundedPoly logo.", "text_overlay": "FundedPoly is all you need"},
      {"scene": 3, "duration": "9-15s", "description": "Epic celebration, funny meme effects.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A funny and absurd vertical thumbnail of a trader on a snowy mountain peak holding a glowing laptop with the word FundedPoly visible"
  },
  {
    "campaign_id": "6a71c6f7245627c68999eae2",
    "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali",
    "section": "Nuove",
    "feasibility_score": 135.0,
    "feasibility_rating": "MEDIA",
    "feasibility_reasoning": "Lower payout but very targeted female audience.",
    "payout_per_1k": 0.5,
    "budget_remaining": 446.5,
    "video_prompt_gemini": "Genera un video verticale 9:16 di 15-30 secondi. Hook (0-2s): Una ragazza elegante al computer in una caffetteria luminosa, che sorride sorpresa guardando lo schermo. 3-15s: Estetica aspirazionale, lifestyle digitale, lusso discreto. Grafica in sovrimpressione moderna. Chiudi con CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Vuoi scoprire il segreto dei negozi digitali? 🤫 Inizia da qui! Segui @saradizdariacademy per la lezione gratuita. Guarda il video completo su Klippify! #saradizdariacademyscopriinegozidigitali #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Ragazza sorridente lavora dal laptop sorseggiando matcha.", "text_overlay": "Il segreto per lavorare da dove vuoi..."},
      {"scene": 2, "duration": "4-10s", "description": "Dettagli di lifestyle e lavoro digitale.", "text_overlay": "Scopri i negozi digitali con la video-lezione gratuita"},
      {"scene": 3, "duration": "11-15s", "description": "Sguardo in camera e gesto di invito.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A young woman looking surprised and happy at her laptop in an aesthetic coffee shop, bright lighting, vertical format"
  },
  {
    "campaign_id": "6a2d2ec66c09e42f05891f56",
    "campaign_name": "MedX",
    "section": "Nuove",
    "feasibility_score": 130.9,
    "feasibility_rating": "MEDIA",
    "feasibility_reasoning": "High budget but restricted target audience.",
    "payout_per_1k": 1.0,
    "budget_remaining": 500.0,
    "video_prompt_gemini": "Genera un video verticale 9:16 di 15-30 sec. Hook (0-2s): Primo piano di una pelle perfetta, luminosa e dall'aspetto naturale, stile beauty premium. 3-15s: Carrellata in una clinica estetica di lusso, dettagli di macchinari all'avanguardia e atmosfera rilassante ed elegante (bianco e oro). CTA finale: Guarda il video completo su Klippify!",
    "tiktok_caption": "Il segreto per una pelle perfetta e naturale? La medicina estetica d'eccellenza a Roma. ✨ Segui @medxclinic. Guarda il video completo su Klippify! #medx #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Primo piano di una donna con pelle impeccabile.", "text_overlay": "La tua pelle, ma perfetta."},
      {"scene": 2, "duration": "4-10s", "description": "Spazi eleganti di una clinica e strumenti di precisione.", "text_overlay": "Eccellenza della medicina estetica a Roma"},
      {"scene": 3, "duration": "11-15s", "description": "Risultato finale radioso e logo.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A premium beauty aesthetic shot of a flawless, glowing face half illuminated in a luxurious white and gold clinic environment"
  },
  {
    "campaign_id": "69b0ffca471017e7bfe49765",
    "campaign_name": "Physioterapeasy",
    "section": "In pausa",
    "feasibility_score": 97.4,
    "feasibility_rating": "MEDIA",
    "feasibility_reasoning": "Good payout, relatable student struggles.",
    "payout_per_1k": 3.0,
    "budget_remaining": 226.0,
    "video_prompt_gemini": "Genera un video verticale 9:16 (15-30s). Hook (0-2s): Uno studente disperato sommerso da enormi libri di anatomia, espressione stravolta. 3-15s: Transizione magica, lo studente ora è rilassato, tiene un iPad luminoso che mostra schemi muscolari colorati in 3D. Atmosfera da stressata a serena. CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Studiare fisioterapia = impazzire sui libri? 📚🤯 Non più! Tutto quello che ti serve è sul tuo iPad con @physioterapeasy. Guarda il video completo su Klippify! #physioterapeasy #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Studente che sbatte la testa su una pila di libri giganti.", "text_overlay": "Ancora a studiare così?"},
      {"scene": 2, "duration": "4-10s", "description": "Lo studente sorride usando la WebApp su iPad, schemi visivi chiari.", "text_overlay": "Semplifica con Physio Bundle!"},
      {"scene": 3, "duration": "11-15s", "description": "Simulazione esame superata, festeggiamento.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "Split screen: Left side a stressed student buried in heavy anatomy books, right side a happy student holding a glowing iPad with colorful charts"
  },
  {
    "campaign_id": "6a346c9ba53170de02cc90b4",
    "campaign_name": "YC Startup podcast (Lobster Talks)",
    "section": "Nuove",
    "feasibility_score": 86.5,
    "feasibility_rating": "MEDIA",
    "feasibility_reasoning": "Solid payout and strong startup niche appeal.",
    "payout_per_1k": 2.5,
    "budget_remaining": 467.5,
    "video_prompt_gemini": "Generate a vertical 9:16 video (15-30s). Hook (0-2s): A dramatic, high-contrast shot of a studio microphone and an intense speaker leaning in, making a bold statement. 3-15s: Quick cuts of tech founders nodding, futuristic startup office vibes, dark cinematic lighting with neon red accents. CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "Real founders. No fluff. 🦞🎙️ Listen to the secrets of building the future with @lobstercapital. Guarda il video completo su Klippify! #ycstartuppodcastlobstertalks #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Close-up of a microphone with a red lobster logo glowing in the background.", "text_overlay": "The truth about building startups"},
      {"scene": 2, "duration": "4-10s", "description": "Intense podcast conversation, fast paced.", "text_overlay": "Founders sharing real failures & wins"},
      {"scene": 3, "duration": "11-15s", "description": "Host pointing to the camera confidently.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A high-contrast cinematic podcast setup with a silver microphone, neon red lighting, and the silhouette of a speaker leaning in intensely"
  },
  {
    "campaign_id": "6a7a13715ade3cb2f77b30df",
    "campaign_name": "What's Next - Nello Cristianini",
    "section": "Nuove",
    "feasibility_score": 75.4,
    "feasibility_rating": "BASSA",
    "feasibility_reasoning": "Low score, but still makes the top 10.",
    "payout_per_1k": 1.25,
    "budget_remaining": 378.75,
    "video_prompt_gemini": "Genera un video verticale 9:16 (15-30s). Hook (0-2s): Animazione 3D misteriosa di reti neurali e circuiti di intelligenza artificiale che brillano nel buio. 3-15s: Stile documentario tech premium, grafiche olografiche e spezzoni di un professore illuminato da luci blu. CTA: Guarda il video completo su Klippify!",
    "tiktok_caption": "L'AI ci ruberà il lavoro? Il Prof. Nello Cristianini svela la verità. 🤖🎙️ Ospite di @raffaelegaito a What's Next. Guarda il video completo su Klippify! #whatsnextnellocristianini #klippify",
    "storyboard": [
      {"scene": 1, "duration": "0-3s", "description": "Occhio umano che guarda un ologramma di AI.", "text_overlay": "Cosa ci aspetta davvero con l'AI?"},
      {"scene": 2, "duration": "4-10s", "description": "Scena da podcast tech di alto livello con grafiche futuristiche.", "text_overlay": "Il Prof. Nello Cristianini risponde"},
      {"scene": 3, "duration": "11-15s", "description": "Dinamico zoom sul microfono.", "text_overlay": "Guarda il video completo su Klippify!"}
    ],
    "thumbnail_prompt": "A futuristic and slightly mysterious AI-themed podcast thumbnail featuring glowing neural network lines and a serious presenter in a dark tech studio"
  }
]

with open(r'c:\Users\HP\Desktop\contenuti klippify\generated_content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('JSON successfully saved!')
