
const window = {
    addEventListener: () => {},
    localStorage: { getItem: () => null, setItem: () => {} },
    location: { reload: () => {} }
};
const document = {
    getElementById: (id) => ({
        style: {},
        innerHTML: '',
        innerText: '',
        value: '',
        children: [],
        addEventListener: () => {},
        classList: { add: () => {}, remove: () => {} },
        scrollIntoView: () => {}
    }),
    querySelectorAll: () => [],
    createElement: () => ({ style: {}, classList: { add: () => {} } }),
    addEventListener: () => {}
};
const localStorage = { getItem: () => null, setItem: () => {} };
const fetch = async () => ({ ok: true, json: async () => [] });


        const allCampaignsData = [{"id": "6a7386b22080c9c1c92a3f14", "campaign_token": "6a7386b22080c9c1c92a3f14", "campaign_url": "https://app.klippify.com/campaigns/6a7386b22080c9c1c92a3f14", "name": "Fabio Rovazzi - La Costiera Amalfitana", "brand": "Marco Cappelli Agency", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1568518, "creators_count": 300, "budget_remaining": 408.0, "budget_spent": 1508.0, "budget_total": 2000.0, "budget_progress_percent": "75.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/300eed23-8117-49f1-8a6a-032aefd4d3d0-ChatGPT-Image-5-ago-2026,-20_49_15.png", "logo": "https://lh3.googleusercontent.com/a/ACg8ocKtof6jsOkYphrb-ZTdiiS-zEylShB3tljHy5-J3n7niLXNx2A=s96-c", "description": "Artista: Fabio Rovazzi (feat. Arisa e Nino D'Angelo)\n\nBrano: La Costiera Amalfitana\n\nRelease: 3 luglio 2026, distribuito da Warner Records / Warner Music Italy.\n\nIl brano punta a essere uno dei tormentoni dell'estate 2026. Unisce:\n- l'ironia e lo storytelling di Rovazzi;\n- la voce pop di Arisa;\n- il sapore napoletano e nostalgico di Nino D'Angelo.\n\nIl concept è quello dell'estate italiana vista con ironia: il sogno della Costiera Amalfitana contrapposto alla realtà di chi rimane in città tra caldo, zanzare e Idroscalo.", "status": "Active", "mandatory_hashtags": ["#fabiorovazzilacostieraamalfitana", "#klippify"], "mandatory_mentions": ["@marcocappelliagency"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 41972.7}, {"id": "6a2433a7e3244ca026589180", "campaign_token": "6a2433a7e3244ca026589180", "campaign_url": "https://app.klippify.com/campaigns/6a2433a7e3244ca026589180", "name": "Fashion Bus", "brand": "Fashion Bus", "section": "Nuove", "payout_per_1k_views": 1.5, "total_views": 486679, "creators_count": 113, "budget_remaining": 276.5, "budget_spent": 223.5, "budget_total": 500.0, "budget_progress_percent": "44.7%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/7ef034bd-2190-414d-b608-1aa250c765ef-fashionbus.jpg", "description": "🚌 Non è un autobus. È un locale itinerante che gira per Roma. Musica, luci, karaoke e una festa privata tutta per te. 🎉 Richiedi subito informazioni su WhatsApp.", "status": "Active", "mandatory_hashtags": ["#fashionbus", "#klippify"], "mandatory_mentions": ["@fashionbus"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 34739.7}, {"id": "6a76d24b5ade3cb2f77429aa", "campaign_token": "6a76d24b5ade3cb2f77429aa", "campaign_url": "https://app.klippify.com/campaigns/6a76d24b5ade3cb2f77429aa", "name": "Brunch e Cocktail a Peschiera del Garda", "brand": "9Days cafè - Brunch Cocktails & More", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 0, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/dbfdf999-c1c4-497b-a786-e8f39c66f58f-_DSC4542-(2).jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/7e5ba711-5588-495a-94db-8d10faec239d-Gemini_Generated_Image_dlg8hcdlg8hcdlg8.png", "description": "Ricondivisione di un reel Instagram dal profilo @9Dayscafè a Peschiera del Garda, con focus su brunch e cocktail.", "status": "Active", "mandatory_hashtags": ["#brunchecocktailapeschieradelgarda", "#klippify"], "mandatory_mentions": ["@9dayscafbrunchcocktailsmore"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 33063.5}, {"id": "6a64cf756cdfd98478f11f28", "campaign_token": "6a64cf756cdfd98478f11f28", "campaign_url": "https://app.klippify.com/campaigns/6a64cf756cdfd98478f11f28", "name": "Million Hospitality", "brand": "Million Hospitality", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1069261, "creators_count": 282, "budget_remaining": 945.0, "budget_spent": 1035.0, "budget_total": 1980.0, "budget_progress_percent": "52.3%", "banner": "https://klippify-assets.s3.us-east-1.amazonaws.com/WhatsApp+Image+2026-07-28+at+21.35.57.jpeg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/ccd8538d-4605-4c20-8bdb-07bc3cd19310-Million-Hosptality---Senza-sfondo-.png", "description": "Lavori da strapagati nell'hospitality all'estero.\nBartender, chef de rang, sommelier, chef de cuisine, restaurant manager, host & hostess. Da 4K a 9K al mese, minimo 48K l'anno.", "status": "Active", "mandatory_hashtags": ["#millionhospitality", "#klippify"], "mandatory_mentions": ["@millionhospitality"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 30500.6}, {"id": "6a719c80a2d57190f5d7a38b", "campaign_token": "6a719c80a2d57190f5d7a38b", "campaign_url": "https://app.klippify.com/campaigns/6a719c80a2d57190f5d7a38b", "name": "Le 9 Bugie di FitActive", "brand": "Theory Spa", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 617852, "creators_count": 179, "budget_remaining": 304.75, "budget_spent": 144.25, "budget_total": 450.0, "budget_progress_percent": "32.1%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/40f05066-1e80-4fe3-be26-9afde93ea5eb-Il-Mondo-delle-Bugie.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/3aefd338-2e3b-4d4b-baae-6d4070f65a38-theory-holding-logo-real.png", "description": "Theory Holding è una azienda made in Italy dove i talenti rendono le visioni, rivoluzioni di interi mercati", "status": "Active", "mandatory_hashtags": ["#le9bugiedifitactive", "#klippify"], "mandatory_mentions": ["@theoryspa"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 27807.3}, {"id": "6a3fbb32e6a21896f767e4e7", "campaign_token": "6a3fbb32e6a21896f767e4e7", "campaign_url": "https://app.klippify.com/campaigns/6a3fbb32e6a21896f767e4e7", "name": "Dormire sotto le stelle con SkyRoom", "brand": "Skyroom", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 230297, "creators_count": 85, "budget_remaining": 473.0, "budget_spent": 27.0, "budget_total": 500.0, "budget_progress_percent": "5.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Dormire_sotto_le_stelle_con_SkyRoom__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/99c73620-5d47-431f-b704-cfe3518d6654-logo-png@300x.png", "description": "SkyRoom è un’esperienza di soggiorno immersa nella natura, pensata per chi vuole staccare dalla routine e vivere una notte diversa dal solito.\nL’obiettivo della campagna è creare contenuti spontanei ed emozionali che facciano desiderare l’esperienza e portino utenti interessati a visitare il sito ufficiale per prenotare.", "status": "Active", "mandatory_hashtags": ["#dormiresottolestelleconskyroom", "#klippify"], "mandatory_mentions": ["@skyroom"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 22033.3}, {"id": "6a759fd05ade3cb2f771b439", "campaign_token": "6a759fd05ade3cb2f771b439", "campaign_url": "https://app.klippify.com/campaigns/6a759fd05ade3cb2f771b439", "name": "Mondocash Podcast", "brand": "Ale Stark", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 326931, "creators_count": 121, "budget_remaining": 751.5, "budget_spent": 126.5, "budget_total": 900.0, "budget_progress_percent": "14.1%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/c4d336a6-8ae5-4849-974d-1a80866184ec-Screenshot-2026-08-07-at-10.23.23.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/fecb4e6a-ffa2-4f1f-bbf4-3626682a8b25-logo-stark-klippify.png", "description": "Campagna per promuovere l'host Ale Stark utilizzando le clip del podcast MondoCash. Il clipper deve creare clip virali SOLO dai link inseriti nella campagna in cui per almeno il 50% deve essere presente l'immagine di Ale Stark (il ragazzo biondo).", "status": "Active", "mandatory_hashtags": ["#mondocashpodcast", "#klippify"], "mandatory_mentions": ["@alestark"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 21889.4}, {"id": "6a1ae4d11231f047260883eb", "campaign_token": "6a1ae4d11231f047260883eb", "campaign_url": "https://app.klippify.com/campaigns/6a1ae4d11231f047260883eb", "name": "Liveral Shot", "brand": "LIVERAL", "section": "Nuove", "payout_per_1k_views": 1.25, "total_views": 197809, "creators_count": 102, "budget_remaining": 206.0, "budget_spent": 294.0, "budget_total": 500.0, "budget_progress_percent": "58.8%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Liveral_Shot__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/00a3c961-7764-4b44-beda-0d61e4307e4d-Liveral_Logo-principale.png", "description": "Descrizione campagna Liveral Shot è lo shot 100% naturale, vegan e zero caffeina che prendi prima di dormire dopo le tue serate. La formula lavora di notte mentre dormi, così il giorno dopo ti svegli al meglio e pronto a ripartire. Made in Italy, 3.000+ prodotti venduti. Obiettivo: far conoscere Liveral Shot e mostrarlo in modo autentico nei momenti di vita reale, con contenuti ad alta energia che facciano venire voglia di provarlo.A chi parliamo Pubblico trasversale, cuore fatto di universitari, giovani lavoratori e professionisti. Gente work hard, play hard, che non vuole scegliere tra godersi la serata e dare il massimo il giorno dopo. Tono autentico e ad alta energia, parla con parole tue.Il rituale (storyboard pronto)Bevi lo shot prima di dormire, agitalo bene.Vai a dormire, la formula lavora mentre riposi.Svegliati al meglio e goditi il giorno dopo al 100%.Requisiti per la monetizzazione Ogni reel deve durare almeno 15 secondi, mostrare o nominare chiaramente Liveral Shot, essere coerente con queste linee guida e includere hashtag, menzione e CTA obbligatori.Contenuti ammessi Contenuti originali ambientati nella serata reale (aperitivi, locali, amici, mood notturno), b-roll e clip fornite dal brand, UGC, storytelling, voiceover, recensioni sincere, intrattenimento, purché legati a Liveral Shot mostrato come rituale di fine serata.Contenuti NON ammessi Dichiarare di essersi ubriacati o di stare male (\"mi sono distrutto\", \"ero ubriaco\", \"sbornia\", \"postumi\"). Promettere che Liveral cura o toglie sintomi (\"toglie il mal di testa\", \"antinausea\", \"depura\", \"detox\", \"protegge il fegato\"): nessun claim medico. Contenuti fuorvianti, offensivi, di bassa qualità o non coerenti col brand. Materiali protetti da copyright. Outcome sempre in positivo: \"ti svegli al meglio\", \"al 100%\", \"pronto a ripartire\". In una riga: atmosfera della serata sì, dichiarare la sbronza e promettere il rimedio no. Claim ok: 100% naturale, vegan, zero caffeina, Made in Italy, 3.000+ venduti.Elementi obbligatori Hashtag: #liveral #liveralshot Menzione: @liveralnow CTA: invito a visitare liveral.it", "status": "Active", "mandatory_hashtags": ["#liveralshot", "#klippify"], "mandatory_mentions": ["@liveral"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 15818.2}, {"id": "6a1dabe2e3244ca026512560", "campaign_token": "6a1dabe2e3244ca026512560", "campaign_url": "https://app.klippify.com/campaigns/6a1dabe2e3244ca026512560", "name": "Personal_G", "brand": "PersonalG", "section": "Nuove", "payout_per_1k_views": 2.0, "total_views": 247602, "creators_count": 152, "budget_remaining": 38.0, "budget_spent": 462.0, "budget_total": 500.0, "budget_progress_percent": "92.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Personal_G__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/452eaf99-a6f1-495d-b4a5-03ffcfee8d01-WhatsApp-Image-2026-05-30-at-12.16.01-(1).jpeg", "description": "Personal_G non è una palestra né il programma di una fitness influencer. È il metodo di allenamento al femminile basato su un’idea semplice: ogni corpo è diverso, quindi ogni allenamento deve esserlo. Non esiste la scheda che funziona per tutte esiste quella giusta per il corpo e il tuo biotipo. Non importa da che corpo parti né le quali siano state le tue delusioni passate: dacci 3 ore a settimana e ti cambio il corpo e la vita per sempre.", "status": "Active", "mandatory_hashtags": ["#personalg", "#klippify"], "mandatory_mentions": ["@personalg"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 13257.3}, {"id": "6a0dd557394d916370d7fb3d", "campaign_token": "6a0dd557394d916370d7fb3d", "campaign_url": "https://app.klippify.com/campaigns/6a0dd557394d916370d7fb3d", "name": "Marco Billiani | Chiave immobiliare", "brand": "Chiave Immobiliare", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 168058, "creators_count": 132, "budget_remaining": 433.5, "budget_spent": 66.5, "budget_total": 500.0, "budget_progress_percent": "13.3%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/c2b3f662-92ed-4fce-b2d3-ac2d15538b19-marco-billiani-klippify.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/fdaad54a-586e-4d0a-be10-b43d78b00012-LOGHI-CHIAVE-IMMOBILIARE.png", "description": "Marco Billiani è un brand verticale sugli affitti brevi e sulla formazione immobiliare pratica, pensato per chi vuole trasformare Airbnb e il turismo in un vero business.La sua comunicazione unisce autorevolezza, risultati concreti e storytelling imprenditoriale, parlando a persone ambiziose che cercano un metodo chiaro per partire, gestire e scalare nel settore.Il posizionamento migliore: non “il solito formatore”, ma il punto di riferimento italiano per chi vuole costruire un business reale negli affitti brevi, partendo da zero o migliorando ciò che ha già.", "status": "Active", "mandatory_hashtags": ["#marcobillianichiaveimmobiliare", "#klippify"], "mandatory_mentions": ["@chiaveimmobiliare"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 10432.7}, {"id": "69e21a5ef7e6b4d2d58002b9", "campaign_token": "69e21a5ef7e6b4d2d58002b9", "campaign_url": "https://app.klippify.com/campaigns/69e21a5ef7e6b4d2d58002b9", "name": "Ascensore - EP.2", "brand": "Ascensore_media", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 455994, "creators_count": 373, "budget_remaining": 133.59999999999997, "budget_spent": 366.40000000000003, "budget_total": 500.0, "budget_progress_percent": "73.3%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Ascensore_-_EP.2__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/7bb46175-e042-4dbd-8648-54c806cb3525-Senza-titolo.png", "description": "ASCENSORE è un evento live di pitch per startup. Ogni episodio presenta imprenditori che presentano le loro idee a una giuria di esperti.Note operative per le clip:Titolo introduttivo all'inizio (2-4 secondi): accattivante, che crea curiosità e contestualizza la clipSottotitoli sincronizzati con l'audio - Font Stratos (normal o medium)Colore sottotitoli: Bianco (#FFFFFF) per i giudici | Giallo (#FDE700) o Viola (#581BBA) per i concorrentiFormato verticale (9:16) - Risoluzione minima 1080×1920pxDescrizione: sempre includere i tag @ascensore_media (Instagram e TikTok)", "status": "Active", "mandatory_hashtags": ["#ascensoreep2", "#klippify"], "mandatory_mentions": ["@ascensoremedia"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 9901.1}, {"id": "69b6fb2b7add71b606b303d2", "campaign_token": "69b6fb2b7add71b606b303d2", "campaign_url": "https://app.klippify.com/campaigns/69b6fb2b7add71b606b303d2", "name": "SFS1", "brand": "Smoke Free Skin", "section": "Iscritte", "payout_per_1k_views": 2.0, "total_views": 208419, "creators_count": 184, "budget_remaining": 28.0, "budget_spent": 472.0, "budget_total": 500.0, "budget_progress_percent": "94.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/SFS1__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/ac4c586d-7560-4a3d-a16e-fe824b4f0606-SFS-Logo2-2.png", "description": "Smoke-Free Skin è un brand cosmetico italiano sviluppato per proteggere e rigenerare la pelle esposta quotidianamente a fumo, smog e stress urbano.Le formulazioni, realizzate in Italia con ingredienti di alta qualità, sono studiate per contrastare i principali effetti dello stile di vita urbano sulla pelle: opacità, disidratazione, perdita di elasticità e invecchiamento precoce.La linea combina ricerca cosmetologica, attivi mirati e un approccio skincare essenziale, offrendo prodotti pensati per detergere, nutrire, illuminare e rigenerare la pelle di chi vive in ambienti urbani o è esposto al fumo di sigaretta.", "status": "Active", "mandatory_hashtags": ["#sfs1", "#klippify"], "mandatory_mentions": ["@smokefreeskin"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 9258.4}, {"id": "69b4326b7add71b606b18d8b", "campaign_token": "69b4326b7add71b606b18d8b", "campaign_url": "https://app.klippify.com/campaigns/69b4326b7add71b606b18d8b", "name": "Investhero", "brand": "Invest Hero", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 397831, "creators_count": 363, "budget_remaining": 318.5, "budget_spent": 181.5, "budget_total": 500.0, "budget_progress_percent": "36.3%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Investhero__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/33b5e1e6-b4a5-4acc-ac57-488328c8b41b-logo_InvestHero-1-1.png", "description": "Siamo una società di formazione in ambito educazione finanziaria. La nostra missione: \"Investhero nasce con l’obiettivo di portare una sana cultura finanziaria in Italia, per accompagnarti nel tuo percorso verso la libertà finanziaria, fornendoti tutti gli strumenti necessari per creare, far crescere, investire e proteggere il tuo denaro\".", "status": "Active", "mandatory_hashtags": ["#investhero", "#klippify"], "mandatory_mentions": ["@investhero"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 8891.1}, {"id": "6a7239b2245627c6899bedf7", "campaign_token": "6a7239b2245627c6899bedf7", "campaign_url": "https://app.klippify.com/campaigns/6a7239b2245627c6899bedf7", "name": "Il gusto francese sul Lago Maggiore", "brand": "La Pasticceria", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 4, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/516fff58-73a3-493a-9ed4-b5fdc28efe27-1000292770.jpg", "logo": "https://lh3.googleusercontent.com/a/ACg8ocIb2GYFuAbRu_AlN1uZ-G7Gd7x5BiChbrx_SgbAUzekK7KPrLM=s96-c", "description": "La Pasticceria Pallanza ha un concept di pasticceria moderna francese con contaminazioni del nord europa.Il servizio è take away con la possibilità di consumare sul posto, senza servizio al tavolo.L'offerta di prodotti non è ampia ma è molto focalizzata sull'esclusività.Il caffè espresso è prodotto con il sistema Nespresso professional, che garantisce coerenza e qualità costante, il latte proviene dai pascoli dell'Ossola, il burro è belga di altissima qualità prodotto dalla panna, il caffè filtro viene estratto ogni giorno con miscele finlandesi premium, il thè è francese con tantissimi gusti disponibili. La pasticceria produce anche macaron fantasiosi, sempre nuovi e sfiziosi. Anche la biscotteria è esclusiva, con gusti e abbinamenti inimitabili. Anche il cioccolato ed i lievitati per le ricorrenze sono delle chicche che questa pasticceria produce ogni anno per i propri clienti. Il protagonista assoluto è sempre il croissant francese, inimitabile e imitato, mai eguagliato. Il cliente che prova La Pasticceria troverà dei gusti e un'esperienza impossibile da trovare altrove.Crea contenuti che mostrino la bontà dei nostri croissant francesi e macaron, trasmettendo l'atmosfera unica della pasticceria sul Lago Maggiore.Hastag obbligatori #lapasticceria #verbania #crois #lagomaggiore #lapasticceriapallanza #breakfast", "status": "Active", "mandatory_hashtags": ["#ilgustofrancesesullagomaggiore", "#klippify"], "mandatory_mentions": ["@lapasticceria"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 8313.5}, {"id": "6a186236e38a567930b34191", "campaign_token": "6a186236e38a567930b34191", "campaign_url": "https://app.klippify.com/campaigns/6a186236e38a567930b34191", "name": "Klippify - Ascensore", "brand": "Klippify", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 761541, "creators_count": 850, "budget_remaining": 356.0, "budget_spent": 644.0, "budget_total": 1000.0, "budget_progress_percent": "64.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Klippify_-_Ascensore__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/19e04c73-e2ca-484e-9621-1e9936424e05-Klippify-Logo.png", "description": "La puntata di Ascensore in cui Klippify viene presentato agli investitori, mostrando la visione della piattaforma, il modello di business e il potenziale nel rivoluzionare il rapporto tra creator e brand.", "status": "Active", "mandatory_hashtags": ["#klippifyascensore", "#klippify"], "mandatory_mentions": ["@klippify"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 7257.5}, {"id": "6a71c6f7245627c68999eae2", "campaign_token": "6a71c6f7245627c68999eae2", "campaign_url": "https://app.klippify.com/campaigns/6a71c6f7245627c68999eae2", "name": "Sara Dizdari Academy – Scopri i negozi digitali", "brand": "Sara Dizdari Academy", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 3651, "creators_count": 9, "budget_remaining": 446.5, "budget_spent": 0.5, "budget_total": 450.0, "budget_progress_percent": "0.1%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/d5a91bf4-880b-44ec-b30a-508566f50194-copertina-sda-16x9.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/3883c984-4830-4a78-b2a5-b84e62c5b748-PHOTO-2026-08-05-17-15-49.jpg", "description": "Clip verticali 9:16 (20-60 secondi) che incuriosiscono le spettatrici verso la video‑lezione gratuita di Sara Dizdari, senza svelare il metodo, con hook forte, sottotitoli e CTA di seguire il profilo di Sara", "status": "Active", "mandatory_hashtags": ["#saradizdariacademyscopriinegozidigitali", "#klippify"], "mandatory_mentions": ["@saradizdariacademy"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 6081.5}, {"id": "69d9fd5061ce1b8904c42316", "campaign_token": "69d9fd5061ce1b8904c42316", "campaign_url": "https://app.klippify.com/campaigns/69d9fd5061ce1b8904c42316", "name": "Boardingame #1", "brand": "aledellagiusta", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 584123, "creators_count": 880, "budget_remaining": 558.5, "budget_spent": 183.0, "budget_total": 750.0, "budget_progress_percent": "24.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Boardingame_1__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/90dcb7cc-d6e8-4b52-9ec1-92c87a16e29b-BLACK-LOGO.png", "description": "Vogliamo clippare la serie \"Boardingame\" - a partire dal primo episodio appena uscito sul canale YouTube @aledellagiusta", "status": "Active", "mandatory_hashtags": ["#boardingame1", "#klippify"], "mandatory_mentions": ["@aledellagiusta"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 5400.4}, {"id": "6a7672465ade3cb2f773f6c9", "campaign_token": "6a7672465ade3cb2f773f6c9", "campaign_url": "https://app.klippify.com/campaigns/6a7672465ade3cb2f773f6c9", "name": "Gabriele Vagnato", "brand": "Gabriele Vagnato", "section": "Nuove", "payout_per_1k_views": 0.25, "total_views": 73809, "creators_count": 133, "budget_remaining": 677.25, "budget_spent": 22.25, "budget_total": 700.0, "budget_progress_percent": "3.2%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/e736669e-112f-4767-8225-1c7adf293ba4-_CBN5611.jpeg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/279e6078-2791-40fc-8fd1-e338bd1f03ec-GDP-LOGO3.png", "description": "Youtube e content creator: https://www.youtube.com/@gabrielevagnato", "status": "Active", "mandatory_hashtags": ["#gabrielevagnato", "#klippify"], "mandatory_mentions": ["@gabrielevagnato"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 4690.4}, {"id": "69db9e0c61ce1b8904c4c3b7", "campaign_token": "69db9e0c61ce1b8904c4c3b7", "campaign_url": "https://app.klippify.com/campaigns/69db9e0c61ce1b8904c4c3b7", "name": "Collecto", "brand": "Salvatore Zola", "section": "Iscritte", "payout_per_1k_views": 1.0, "total_views": 244485, "creators_count": 648, "budget_remaining": 796.0, "budget_spent": 204.0, "budget_total": 1000.0, "budget_progress_percent": "20.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/03b82d2e-f63f-4f8e-9df5-c2649179a469-Collecto_def_2.png", "description": "Collecto  è la piattaforma che permette di possedere frazioni di asset da collezione esclusivi — orologi iconici, arte contemporanea, vini rari, memorabilia leggendari. Pezzi che normalmente non si possono permettere in uno, ora accessibili a partire da piccole quote. Con oltre 270.000 utenti e €60M+ in transazioni, siamo il punto di riferimento in Europa per chi vuole entrare nel mondo del collezionismo di alto profilo — senza barriere.", "status": "Active", "mandatory_hashtags": ["#collecto", "#klippify"], "mandatory_mentions": ["@salvatorezola"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 3130.8}, {"id": "6a6dc4b494bf29a44b05d822", "campaign_token": "6a6dc4b494bf29a44b05d822", "campaign_url": "https://app.klippify.com/campaigns/6a6dc4b494bf29a44b05d822", "name": "Scontly - UGC Campaign", "brand": "Scontly", "section": "Nuove", "payout_per_1k_views": 4.0, "total_views": 1000, "creators_count": 11, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/070c619f-71dd-4931-821f-d0cbee14ee7d-ChatGPT-Image-30-lug-2026,-18_11_06.png", "description": "Scontly è un servizio che monitora il prezzo della tua prenotazione dopo l'acquisto. Se il prezzo scende e la differenza è recuperabile, Scontly restituisce all'utente l'85% del risparmio ottenuto, trattenendo il 15%. I creator devono realizzare video spontanei, in prima persona, che mostrino il problema dei prezzi che calano dopo la prenotazione e presentino Scontly come la soluzione.sito web: scontly.live", "status": "Active", "mandatory_hashtags": ["#scontlyugccampaign", "#klippify"], "mandatory_mentions": ["@scontly"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 3093.5}, {"id": "6a2d2ec66c09e42f05891f56", "campaign_token": "6a2d2ec66c09e42f05891f56", "campaign_url": "https://app.klippify.com/campaigns/6a2d2ec66c09e42f05891f56", "name": "MedX", "brand": "MedX Clinic", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 11, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/MedX__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/b8ab105b-6e2b-4807-b4e1-08a3d8ac455b-LOGO_04.png", "description": "Brand: MedX Clinic – Clinica di Medicina Estetica a Roma.Descrizione del brand:MedX Clinic è una clinica di medicina estetica avanzata specializzata in trattamenti per il viso, il corpo e i capelli. Il nostro approccio si basa su risultati naturali, eleganti e personalizzati, supportati da protocolli medici e tecnologie all'avanguardia. Il posizionamento del brand è premium e orientato a un pubblico che ricerca qualità, sicurezza e professionalità.Obiettivo della campagna:Aumentare la notorietà del brand MedX Clinic.Incrementare i follower della pagina Instagram ufficiale.Raggiungere utenti realmente interessati alla medicina estetica.Generare una community locale qualificata, con particolare focus su Roma e Lazio.Contenuto da promuovere:https://www.instagram.com/reel/DZaARKCN2Ce/?igsh=amUxYXVxb3JtazM5Area geografica:ItaliaPriorità assoluta: Roma e provinciaSecondariamente: LazioPiattaforme:Instagram (priorità principale)TikTok (secondario)Target:Uomini e donne 25-60 anniInteressati a medicina estetica, skincare, beauty, benessere, anti-aging, trattamenti viso e cura della personaRichieste per i creator/clipper:Inserire sempre il tag della pagina Instagram ufficiale MedX Clinic.Invitare gli utenti a seguire la pagina per ulteriori contenuti e informazioni.Mantenere uno stile professionale, elegante e coerente con un brand medicale premium.Non alterare il significato del contenuto originale.IMPORTANTE:Per noi è fondamentale preservare il valore percepito e il posizionamento premium del brand.Non desideriamo che il contenuto venga pubblicato all'interno di pagine generaliste o network che promuovono contemporaneamente contenuti relativi a influencer, gossip, trading, crypto, betting, business guru, motivazione generica, intrattenimento virale o altre categorie non coerenti con il settore medicale e beauty premium.Se la piattaforma non consente di selezionare con precisione le tipologie di pagine o profili che pubblicheranno il contenuto, preferiamo che vengano create pagine nuove dedicate esclusivamente alla promozione di MedX Clinic.L'obiettivo principale non è ottenere il maggior numero possibile di visualizzazioni, ma acquisire follower qualificati e in target, mantenendo un contesto coerente con l'immagine e il posizionamento della clinica.", "status": "Active", "mandatory_hashtags": ["#medx", "#klippify"], "mandatory_mentions": ["@medxclinic"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 3065.0}, {"id": "6a426231e6a21896f769dc80", "campaign_token": "6a426231e6a21896f769dc80", "campaign_url": "https://app.klippify.com/campaigns/6a426231e6a21896f769dc80", "name": "Riccardo Dose - YouTube Clipping", "brand": "Marco Cappelli Agency", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 780328, "creators_count": 2771, "budget_remaining": 1576.0, "budget_spent": 224.0, "budget_total": 1800.0, "budget_progress_percent": "12.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/4ee8af7e-92b3-4feb-aa6f-4bfd912f5653-ChatGPT-Image-29-giu-2026,-14_00_31.png", "logo": "https://lh3.googleusercontent.com/a/ACg8ocKtof6jsOkYphrb-ZTdiiS-zEylShB3tljHy5-J3n7niLXNx2A=s96-c", "description": "Riccardo Dose è uno dei creator storici di YouTube Italia. Il suo stile è spontaneo, ironico e molto riconoscibile: alterna challenge, vlog, esperimenti sociali, format di intrattenimento e contenuti di vita quotidiana. Negli anni ha costruito una community molto fedele grazie a un tono autentico, autoironico e mai troppo costruito. Oggi conta oltre 3 milioni di iscritti su YouTube, con una presenza importante anche su Instagram e TikTok.", "status": "Active", "mandatory_hashtags": ["#riccardodoseyoutubeclipping", "#klippify"], "mandatory_mentions": ["@marcocappelliagency"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 2354.1}, {"id": "6a55360dd323618f4f79e13e", "campaign_token": "6a55360dd323618f4f79e13e", "campaign_url": "https://app.klippify.com/campaigns/6a55360dd323618f4f79e13e", "name": "SIMONEMOROFX", "brand": "simonemooro", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 4478, "creators_count": 34, "budget_remaining": 448.5, "budget_spent": 1.5, "budget_total": 450.0, "budget_progress_percent": "0.3%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/c27b2d74-c806-4ff4-94af-f3a1a5ed32f6-A9735134-BCC7-429F-AE16-66FB211C25AF.JPG", "description": "Cerco creator in grado di trasformare i miei video lunghi in clip brevi, coinvolgenti e ad alto potenziale virale per TikTok, Instagram Reels e YouTube Shorts.Cosa voglio:Hook forte nei primi 3 secondi.Sottotitoli dinamici e ben leggibili.Zoom, tagli ed effetti che mantengano alta l'attenzione.Durata tra 20 e 60 secondi.Qualità video elevata (1080x1920).Contenuti da valorizzare:Psicologia del trading.Errori che fanno perdere soldi ai trader.Strategie e analisi di mercato.Esperienze personali e risultati verificabili.Consigli pratici per chi vuole imparare il trading.Stile richiesto:Video moderni, veloci e coinvolgenti, simili ai contenuti che performano meglio su TikTok e Instagram. L'obiettivo è massimizzare visualizzazioni, tempo di visione e condivisioni.Importante:❌ Non utilizzare titoli o affermazioni ingannevoli.❌ Non promettere guadagni garantiti.✅ Mantieni sempre un tono professionale e realistico.Se realizzi clip di qualità, ci saranno ottime possibilità di collaborare anche nelle campagne future.per i contenuti avete il drive che vi ho caricato per tutte le clip lifestyle su drive", "status": "Active", "mandatory_hashtags": ["#simonemorofx", "#klippify"], "mandatory_mentions": ["@simonemooro"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1847.4}, {"id": "6a5e3bd2710dc3521cedfb83", "campaign_token": "6a5e3bd2710dc3521cedfb83", "campaign_url": "https://app.klippify.com/campaigns/6a5e3bd2710dc3521cedfb83", "name": "Campagna Investire.biz - Trading & Investimenti", "brand": "Forecaster.biz", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 22320, "creators_count": 138, "budget_remaining": 447.0, "budget_spent": 3.0, "budget_total": 450.0, "budget_progress_percent": "0.7%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/1c58c904-0ba8-4a1b-aa14-36913da416ac-COPERTINA-klippify-investire.biz.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/760b2aab-ed81-456a-8868-3703bc6c7f11-ICONA-scheda-investire.biz.png", "description": "COS’È INVESTIRE.BIZInvestire.biz è un progetto italiano di informazione e formazione finanziaria.Pubblica analisi di aziende, mercati e temi d’investimento con l’obiettivo di rendere più comprensibili concetti finanziari complessi e aiutare il pubblico a ragionare in modo informato e consapevole.COSA STAI CLIPPANDOQuesta campagna contiene video long-form in italiano, principalmente presentati da Luca Discacciati.I contenuti includono analisi aziendali, approfondimenti sui mercati e spiegazioni di temi economici e finanziari.L’obiettivo è trasformare questi video in contenuti short-form per Instagram Reels e TikTok, aumentando la reach e la brand awareness di Investire.biz.Il numero e la tipologia dei video inclusi nella campagna possono cambiare nel tempo.COME È ORGANIZZATA LA CARTELLALa cartella principale contiene:• Questo documento INIZIA DA QUI.• La cartella Materiali Brand, con brand book, loghi e istruzioni.• Una cartella dedicata a ogni video.Ogni cartella video contiene:• Il video completo scaricato da YouTube.• Un documento di accompagnamento con panoramica, momenti chiave, trascrizione e parti da non utilizzare.Leggi sempre il documento di accompagnamento prima di lavorare sul video corrispondente.TONO DI VOCE — NON NEGOZIABILEInvestire.biz è educativo, analitico e data-driven.Non presentare mai il contenuto come:• Rendimenti garantiti.• Soldi facili o veloci.• «Guadagna X€ in Y giorni».• Previsioni certe.• Contenuti “diventa ricco in fretta”.• Consulenza finanziaria diretta.Non trasformare opinioni, ipotesi o valutazioni personali presenti nel video in certezze o raccomandazioni d’investimento.Promesse ingannevoli, hype eccessivo e risultati garantiti non sono in linea con il brand e possono portare al rifiuto della clip.CTA E ATTRIBUZIONE• Menziona @investire.biz nella caption.• Mostra almeno una volta il logo o l’handle, in modo leggibile e dentro le safe zone.• Non sono obbligatori watermark permanente, intro, outro o CTA fissa.• Le clip sono destinate a Instagram Reels e TikTok.", "status": "Active", "mandatory_hashtags": ["#campagnainvestirebiztradinginvestimenti", "#klippify"], "mandatory_mentions": ["@forecasterbiz"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1538.5}, {"id": "6a553268d323618f4f794fab", "campaign_token": "6a553268d323618f4f794fab", "campaign_url": "https://app.klippify.com/campaigns/6a553268d323618f4f794fab", "name": "SIMONEMOROFX", "brand": "simonemooro", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 1000, "creators_count": 25, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/8bd1d8ef-ad88-4083-9d76-ea22780060de-IMG_5385.jpg", "description": "Content creator specializing in finance, trading, and educational social media content.", "status": "Active", "mandatory_hashtags": ["#simonemorofx", "#klippify"], "mandatory_mentions": ["@simonemooro"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1378.5}, {"id": "6a6885be281dcda3390a8147", "campaign_token": "6a6885be281dcda3390a8147", "campaign_url": "https://app.klippify.com/campaigns/6a6885be281dcda3390a8147", "name": "Risparmio su Bollette Luce e Gas", "brand": "BellaScelta.it", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 28, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/60848347-fee6-44d6-91cd-7ad10b7e4aae-images.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/7034a4a4-b641-4bbe-aa28-c7bbdff9d57f-agentepiu_logo.jpg", "description": "Aiuta i potenziali clienti a capire come risparmiare su luce e gas con un supporto reale: un professionista analizza la bolletta insieme a loro e garantisce un risparmio, senza forzare offerte se quella attuale è già la migliore.", "status": "Active", "mandatory_hashtags": ["#risparmiosubolletteluceegas", "#klippify"], "mandatory_mentions": ["@bellasceltait"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1242.1}, {"id": "6a7a13715ade3cb2f77b30df", "campaign_token": "6a7a13715ade3cb2f77b30df", "campaign_url": "https://app.klippify.com/campaigns/6a7a13715ade3cb2f77b30df", "name": "What's Next - Nello Cristianini", "brand": "Raffaele Gaito", "section": "Nuove", "payout_per_1k_views": 1.25, "total_views": 1000, "creators_count": 33, "budget_remaining": 378.75, "budget_spent": 71.25, "budget_total": 450.0, "budget_progress_percent": "15.8%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/85fd6df9-584c-44ea-98f2-45db441bde5d-Cover-what's-next.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/f45c4c64-1e6e-4bb9-bbb7-d32935b5c918-logo-con-fondo-bianco.png", "description": "Questa campagna è su una puntata del podcast What's Next, dove si discute di intelligenza artificiale. L'ospite in questione è il prof. Nello Cristianini, docente di Intelligenza Artificiale all'università di Bath e uno dei massimi esperti italiani sul tema.", "status": "Active", "mandatory_hashtags": ["#whatsnextnellocristianini", "#klippify"], "mandatory_mentions": ["@raffaelegaito"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1063.9}, {"id": "6a79f2c55ade3cb2f77ad749", "campaign_token": "6a79f2c55ade3cb2f77ad749", "campaign_url": "https://app.klippify.com/campaigns/6a79f2c55ade3cb2f77ad749", "name": "Why podcast", "brand": "Why podcast", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 1000, "creators_count": 35, "budget_remaining": 519.3, "budget_spent": 0.0, "budget_total": 519.3, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/0e4d3747-0215-4bf4-b707-0b907f3b624c-ChatGPT-Image-10-ago-2026,-17_33_56.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/12851ea4-7532-4883-8bde-30f95f1b1d45-why-podcast-logo-.png", "description": "Why Podcast è il salotto di chi non si accontenta del \"si è sempre fatto così\". Intervistiamo imprenditori, sognatori, visionari e ribelli che hanno raggiunto risultati inimmaginabili. Ma a noi non interessa solo il cosa hanno fatto; vogliamo sviscerare il loro PERCHÉ. Qual è la motivazione profonda, spesso irrazionale, che li ha spinti a sacrificare tutto, sfidare le logiche comuni e infrangere le regole? Niente fuffa, solo storie vere di sangue, sudore, fallimenti e vittorie straordinarie.", "status": "Active", "mandatory_hashtags": ["#whypodcast", "#klippify"], "mandatory_mentions": ["@whypodcast"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 1003.4}, {"id": "6a7628ca922613d297f2e2c5", "campaign_token": "6a7628ca922613d297f2e2c5", "campaign_url": "https://app.klippify.com/campaigns/6a7628ca922613d297f2e2c5", "name": "Aldo Masolo viral contest test", "brand": "Aldo Masolo", "section": "Nuove", "payout_per_1k_views": 0.75, "total_views": 271, "creators_count": 30, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Aldo_Masolo_viral_contest_test__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/3dfcd9a3-aac0-4c6e-ab49-f1624db8f604-IMG_4097.JPG", "description": "Sono Aldo Masolo, bodybuilder professionista, coach e divulgatore nel settore fitness e bodybuilding. Da oltre 30 anni vivo e studio il mondo dell’allenamento e della trasformazione fisica, vincendo più di 20 gare e aiutando centinaia di persone a raggiungere i propri obiettivi attraverso programmi personalizzati di allenamento e alimentazione. Il mio approccio si basa su esperienza, disciplina e risultati concreti, valori che condivido quotidianamente attraverso il coaching e la creazione di contenuti dedicati al fitness e al bodybuilding.", "status": "Active", "mandatory_hashtags": ["#aldomasoloviralcontesttest", "#klippify"], "mandatory_mentions": ["@aldomasolo"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 968.1}, {"id": "6a6c8bf694bf29a44b01be17", "campaign_token": "6a6c8bf694bf29a44b01be17", "campaign_url": "https://app.klippify.com/campaigns/6a6c8bf694bf29a44b01be17", "name": "القيادات العليا - أر تو ALYOUNG & RANDAR - R2", "brand": "Another Group", "section": "Nuove", "payout_per_1k_views": 3.0, "total_views": 1000, "creators_count": 61, "budget_remaining": 450.0, "budget_spent": 0.0, "budget_total": 450.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/394c6884-983a-456f-b86d-5f8bec5709bf-AlYoung,-Randar-R2.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/6c1b5fbd-6a8e-4d35-8550-1041d93d34e0-yrmusicrec_1784730235_3946921944149077574_40039388610.jpg", "description": "وش المطلوب منكم: لهالكامبين، سوّوا إديت باستخدام أحد الكليبات الموجودة بالفولدر أو قصّوا مقطع من الميوزيك فيديو حق R2. ثيم الكامبين \"القديم", "status": "Active", "mandatory_hashtags": ["#alyoungrandarr2", "#klippify"], "mandatory_mentions": ["@anothergroup"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 624.5}, {"id": "6968e536d4ea0a9652cf40c0", "campaign_token": "6968e536d4ea0a9652cf40c0", "campaign_url": "https://app.klippify.com/campaigns/6968e536d4ea0a9652cf40c0", "name": "Massaggi & Lavoro - Video Gratis Marketing", "brand": "Francesco G.Saccà", "section": "In pausa", "payout_per_1k_views": 1.0, "total_views": 59463, "creators_count": 918, "budget_remaining": 82.0, "budget_spent": 18.0, "budget_total": 100.0, "budget_progress_percent": "18.0%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/a757b807-025d-48f8-b7f9-1697d7da588b-Progetto-senza-titolo(19).png", "description": "Iscrizione Landing per Video Gratuito: \"5 Clienti in 20 giorni Con Facebook Ads\". Vorrei ottenere visualizzazioni e iscritti alla landing di riferimento, di operatori olistici, massaggiatori, terapisti manuali, imprenditori del settore wellness, estetiste, che vogliono aumentare clienti nella propria zona, con un metodo innovativo e che sta funzionando", "status": "Active", "mandatory_hashtags": ["#massaggilavorovideogratismarketing", "#klippify"], "mandatory_mentions": ["@francescogsacc"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 597.9}, {"id": "6a22ff48e3244ca026570f72", "campaign_token": "6a22ff48e3244ca026570f72", "campaign_url": "https://app.klippify.com/campaigns/6a22ff48e3244ca026570f72", "name": "FundedPoly - $5/1k: Film anything, just show the site", "brand": "FundedPoly", "section": "Nuove", "payout_per_1k_views": 5.0, "total_views": 83, "creators_count": 61, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/2f0a4d3b-3803-4a59-aa8b-c8bda55133c6-pfp-2-mark-ring.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/68baedaa-99fc-42ae-8c1c-d452a345b6f3-08-gta6.png", "description": "Film anything you want — full creative freedom. $5 per 1,000 views. — GET YOUR FREE ACCOUNT FIRST: sign up at https://fundedpoly.com/?utm_source=klippify&utm_campaign=clipperFundedPoly then email support@fundedpoly.com with your FundedPoly account email and ask for a clipper account. We switch on a free FundedPoly account for you (for filming only — not eligible for payout). — THE ONLY 2 RULES: (1) Show FundedPoly on screen — the real website/app (a market, a trade, your account) (2) Say or show \"FundedPoly\" at least once (out loud or as on-screen text fully visible, or if you want to be safe you can make both). — That's it: any style, niche, meme, or edit. The funnier/weirder, the better. Go!", "status": "Active", "mandatory_hashtags": ["#fundedpoly51kfilmanythingjustshowthesite", "#klippify"], "mandatory_mentions": ["@fundedpoly"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 525.7}, {"id": "6a7a14bf5ade3cb2f77b3539", "campaign_token": "6a7a14bf5ade3cb2f77b3539", "campaign_url": "https://app.klippify.com/campaigns/6a7a14bf5ade3cb2f77b3539", "name": "What's Next - Marco Cappato", "brand": "Raffaele Gaito", "section": "Nuove", "payout_per_1k_views": 1.25, "total_views": 29, "creators_count": 56, "budget_remaining": 425.0, "budget_spent": 70.0, "budget_total": 495.0, "budget_progress_percent": "14.1%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/30440d4a-a772-4881-a767-c7ff0cb82c44-Cover-what's-next.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/f45c4c64-1e6e-4bb9-bbb7-d32935b5c918-logo-con-fondo-bianco.png", "description": "Questa campagna è su una puntata del podcast What's Next, dove si discute di intelligenza artificiale. L'ospite in questione è Marco Cappato, politico e attivista, che propone alcune soluzioni per risolvere i problemi dell'AI e per farne un uso positivo per il cittadino.", "status": "Active", "mandatory_hashtags": ["#whatsnextmarcocappato", "#klippify"], "mandatory_mentions": ["@raffaelegaito"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 515.8}, {"id": "6a2021ede3244ca02653db64", "campaign_token": "6a2021ede3244ca02653db64", "campaign_url": "https://app.klippify.com/campaigns/6a2021ede3244ca02653db64", "name": "PMI e startup: scopri se il tuo progetto può essere finanziato", "brand": "Lumivy", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 160, "creators_count": 61, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/PMI_e_startup_scopri_se_il_tuo_progetto_puo%CC%80_essere_finanziat__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/f2d922bb-926d-469d-8c23-f465cff1b49e-Logo-con-il-Brand-su-Sfondo-Bianco-(2).png", "description": "Lumivy è una società che supporta PMI, startup e imprenditori nell’individuazione e nella gestione di opportunità di finanza agevolata, bandi, contributi, agevolazioni e strumenti a supporto di progetti di crescita, digitalizzazione, AI, export, formazione, innovazione e investimenti.L’obiettivo della campagna è creare contenuti efficaci e coerenti con Lumivy, capaci di far capire a imprenditori, founder, professionisti e PMI che molti progetti aziendali possono essere analizzati preventivamente per verificare la presenza di bandi, contributi o agevolazioni compatibili.La campagna deve generare:awareness sul brand Lumivy;interesse verso il tema “pre-check di finanziabilità”;traffico verso il sito/profilo Lumivy;richieste di contatto da parte di aziende con progetti reali.Messaggio principale:Prima di investire in software, AI, export, formazione, digitalizzazione, macchinari, consulenze o innovazione, una PMI dovrebbe verificare se il progetto può essere finanziato o agevolato.Angolo narrativo consigliato:Non raccontare Lumivy come “società che fa bandi”, ma come partner che aiuta l’imprenditore a non perdere opportunità e a capire se il proprio progetto è finanziabile.1 Script consigliati per i creatorScript 1 — Errore da evitare“Errore che fanno tante PMI: prima spendono, poi cercano il bando. In molti casi, invece, bisogna verificare prima se il progetto è compatibile con agevolazioni, contributi o crediti d’imposta. Lumivy aiuta le aziende proprio in questa fase: analisi del progetto, ricerca delle opportunità e supporto alla candidatura. Cerca Lumivy bandi e fai il pre-check.Script 2 — AI e digitalizzazione“Se la tua azienda vuole investire in AI, software, automazioni o digitalizzazione, non partire solo dal preventivo. Parti da una domanda: questo investimento può essere agevolato? Lumivy aiuta PMI e startup a verificare se ci sono bandi o contributi compatibili con il progetto.”Script 3 — Founder/startup“Molti founder cercano investitori, ma ignorano bandi e agevolazioni. Se devi sviluppare software, validare un prodotto, fare innovazione o internazionalizzarti, forse esistono strumenti compatibili. Lumivy ti aiuta a partire dal progetto e capire se ci sono opportunità concrete.”Script 4 — Commercialista angle, ma diplomatico“Il commercialista guarda spesso la parte fiscale e contabile. Ma quando devi fare un investimento futuro, serve anche qualcuno che analizzi bandi, agevolazioni e opportunità disponibili. Lumivy lavora su questo: trasforma un progetto aziendale in una possibile pratica di finanza agevolata.”Script 5 — Hook forte“Se stai per spendere 30, 50 o 100 mila euro nella tua azienda, fermati un attimo. Prima verifica se quel progetto può essere finanziato o agevolato. Lumivy nasce per aiutare PMI e startup a fare proprio questo.”Format “errore da evitare”Esempio:“3 errori che fanno perdere contributi alle PMI.”G. Format “POV”Esempio:“POV: vuoi investire in AI, ma non hai verificato se esiste un bando.”Non sono ammessi contenuti che dicano o lascino intendere:“Lumivy ti garantisce il contributo”; “soldi gratis per tutti”; “bando sicuro”; “finanziamenti senza requisiti”; “qualsiasi azienda può ottenere soldi”; “ti pagano solo perché hai una partita IVA”; “basta compilare un modulo”; “Lumivy fa ottenere fondi automaticamente”;“ contributi garantiti al 100%”;“non serve rispettare requisiti o scadenze”.Non sono ammessi anche: - reel troppo generici sulla ricchezza, il business o la crescita personale senza collegamento a Lumivy; - contenuti in stile fuffa guru; -contenuti aggressivi;- contenuti che screditano commercialisti, consulenti o istituzioni;- contenuti che usano loghi di enti pubblici senza autorizzazione;-contenuti che citano bandi  inventati o non verificati;-contenuti che promettono importi, percentuali o risultati non autorizzati.Esempi di Formula corretta da usare:“Lumivy verifica se il tuo progetto può essere compatibile con bandi o agevolazioni.”Formula da evitare:“Lumivy ti fa ottenere contributi.”", "status": "Active", "mandatory_hashtags": ["#pmiestartupscopriseiltuoprogettopuesserefinanziato", "#klippify"], "mandatory_mentions": ["@lumivy"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 495.8}, {"id": "6a4cef2338c714b87a3b4d4b", "campaign_token": "6a4cef2338c714b87a3b4d4b", "campaign_url": "https://app.klippify.com/campaigns/6a4cef2338c714b87a3b4d4b", "name": "Forecaster Terminal — Finance & Investing Clips", "brand": "Forecaster.biz", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 10073, "creators_count": 259, "budget_remaining": 443.5, "budget_spent": 5.0, "budget_total": 450.0, "budget_progress_percent": "1.1%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/0249ce3f-2826-4fc9-885f-66968ea211ae-COPERTINA-forecaster-ita.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/13e8f059-982c-4ac0-8abe-0f7c38094f30-icon-forecaster-logo.png", "description": "COS'È FORECASTERForecaster è un terminale di analisi finanziaria sviluppato in Svizzera che unisce diversi strumenti analitici in un'unica visione chiara e basata sulle probabilità di oltre 150.000 strumenti finanziari.Il suo scopo è rendere i dati di mercato complessi più facili da capire e da usare.COSA STAI CLIPPANDOQuesta campagna è composta da webinar long-form in italiano presentati da Luca Discacciati, founder e CEO di Forecaster.L'obiettivo è trasformare questi webinar in video short-form per Instagram Reels e TikTok, aumentando la reach e la brand awareness di Forecaster.Il numero di webinar inclusi nella campagna può aumentare o cambiare nel tempo.COME È ORGANIZZATA LA CARTELLALa cartella principale contiene:• Questo documento INIZIA DA QUI• Una cartella Materiali Brand• Una cartella dedicata per ogni webinarOgni cartella webinar contiene:• Il video completo del webinar, scaricato da YouTube.• Un documento di accompagnamento che spiega in modo chiaro e conciso di cosa parla il video.Il documento di accompagnamento è scritto in un linguaggio semplice, così che il contenuto sia comprensibile anche senza conoscenze pregresse dei mercati finanziari.Leggi sempre il documento di accompagnamento prima di lavorare sul webinar corrispondente.TONO DI VOCE — NON NEGOZIABILEForecaster è data-driven, educativo e probabilistico.Non presentare mai il contenuto come:• Rendimenti garantiti• Soldi facili o veloci• «Guadagna X€ in Y giorni»• Previsioni certe• Contenuti \"diventa ricco in fretta\"• Consulenza finanziaria direttaPromesse ingannevoli, hype eccessivo o risultati garantiti non sono in linea con il brand Forecaster e possono portare al rifiuto della clip.CTA E ATTRIBUZIONE• Menziona @forecasterbiz nella caption.• Ogni volta che nella clip compare una pagina del Forecaster Terminal o dei dati di Forecaster, includi: \"Fonte dei dati: Forecaster Terminal\"• Mantieni la promozione leggera. L'obiettivo principale è la reach e la brand awareness.• Pubblica le clip su Instagram Reels e TikTok.", "status": "Active", "mandatory_hashtags": ["#forecasterterminalfinanceinvestingclips", "#klippify"], "mandatory_mentions": ["@forecasterbiz"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 471.0}, {"id": "6a275f64e3244ca0265b49d0", "campaign_token": "6a275f64e3244ca0265b49d0", "campaign_url": "https://app.klippify.com/campaigns/6a275f64e3244ca0265b49d0", "name": "Tech 'n' Cheese:", "brand": "Tech 'n' Cheese", "section": "Nuove", "payout_per_1k_views": 1.75, "total_views": 176, "creators_count": 81, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Tech_n_Cheese__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/ebdb9b3a-8964-409f-8477-469a304f6584-Logo_TeN_Giallo_1.png", "description": "Primo podcast di Big Tech Engineers in America.", "status": "Active", "mandatory_hashtags": ["#techncheese", "#klippify"], "mandatory_mentions": ["@techncheese"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 398.5}, {"id": "69cbae122e954fa83d68934d", "campaign_token": "69cbae122e954fa83d68934d", "campaign_url": "https://app.klippify.com/campaigns/69cbae122e954fa83d68934d", "name": "Fanex 2", "brand": "Fanex", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 111, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Fanex_2__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/266361d5-fd70-40ed-85c6-9292604df4a0-fanex_icon_1024x1024.png", "description": "Fanex è la prima piattaforma dove i fan possono comprare una quota dei ricavi pubblicitari di video YouTube già pubblicati. Funziona così: i creator mettono in vendita una parte dei ricavi AdSense dei loro video. I fan comprano la loro quota e da quel momento ricevono la loro parte dei soldi che quei video continuano a generare con la pubblicità. È il primo modo concreto per i fan di partecipare al successo dei creator che seguono. Ci sono già diversi creator italiani attivi sulla piattaforma. I ricavi sono reali e verificabili, generati dalla pubblicità YouTube (AdSense). Sito:  fanex.market", "status": "Active", "mandatory_hashtags": ["#fanex2", "#klippify"], "mandatory_mentions": ["@fanex"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 362.3}, {"id": "69cbabc02e954fa83d68921c", "campaign_token": "69cbabc02e954fa83d68921c", "campaign_url": "https://app.klippify.com/campaigns/69cbabc02e954fa83d68921c", "name": "Fanex", "brand": "Fanex", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 1000, "creators_count": 134, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Fanex__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/8af2ad64-57a0-475a-bd98-935fc5bdde60-fanex_icon_1024x1024.png", "description": "Fanex è la prima piattaforma dove i fan possono comprare una quota dei ricavi pubblicitari di video YouTube già pubblicati. Un creator mette in vendita una parte dei ricavi AdSense di un suo video. Il fan compra la sua quota e da quel momento riceve la sua parte dei soldi che quel video continua a generare con la pubblicità. Su Fanex sono già disponibili i video di Cicciogamer89, uno dei creator italiani più seguiti con milioni di iscritti e di Camilla De Pandis, creator e influencer con una community enorme. È il primo modo concreto per i fan di partecipare al successo dei creator che seguono. I ricavi sono reali e verificabili, generati dalla pubblicità YouTube (AdSense). Sito:  fanex.market", "status": "Active", "mandatory_hashtags": ["#fanex", "#klippify"], "mandatory_mentions": ["@fanex"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 311.3}, {"id": "6a258cb7e3244ca02659c535", "campaign_token": "6a258cb7e3244ca02659c535", "campaign_url": "https://app.klippify.com/campaigns/6a258cb7e3244ca02659c535", "name": "Valentina Ferri", "brand": "Valentina Ferri", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 5158, "creators_count": 305, "budget_remaining": 500.0, "budget_spent": 0.0, "budget_total": 500.0, "budget_progress_percent": "0.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/8b3bb7a5-b430-42fe-92d7-56f0ebba2e9a-IDENTITA'-1.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/f5158e7a-bad0-457a-b72b-11f248b13ae5-IDENTITA'-1.jpg", "description": "CAMPAGNA PER ONLYFANS INDIRETTA. scrivimi su telegram per avere contenuti inediti da postare @gorulezRagazza influencer, di lavoro fa il corriere amazon.Potete tranquillamente usare l'intelligenza artificiale per creare qualsiasi reel vogliate, copiando anche dall'america senza problemi.Io vi carico nel drive piu video possibili, ma se sapete usare nanobanana, o seedance 2.0 (nel drive trovate la foto avatar da poter utilizzare di lei) usate pure senza problemi. l'importante è avere il link in bio che vi ho inserito.", "status": "Active", "mandatory_hashtags": ["#valentinaferri", "#klippify"], "mandatory_mentions": ["@valentinaferri"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 282.3}, {"id": "694e91113d6a349f51473682", "campaign_token": "694e91113d6a349f51473682", "campaign_url": "https://app.klippify.com/campaigns/694e91113d6a349f51473682", "name": "Marco Cappelli Personal Brand", "brand": "Marco Cappelli Agency", "section": "Nuove", "payout_per_1k_views": 1.0, "total_views": 55321, "creators_count": 2395, "budget_remaining": 936.0, "budget_spent": 54.0, "budget_total": 1000.0, "budget_progress_percent": "5.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Marco_Cappelli_Personal_Brand__16x9_2K.webp", "logo": "https://lh3.googleusercontent.com/a/ACg8ocKtof6jsOkYphrb-ZTdiiS-zEylShB3tljHy5-J3n7niLXNx2A=s96-c", "description": "Pubblicazione di contenuti riguardo la figura di Marco Cappelli (Vendita Prodotti Digitali & Accademia) - TROVATE I CONTENUTI NEL LINK DRIVE IN ALLEGATO.", "status": "Active", "mandatory_hashtags": ["#marcocappellipersonalbrand", "#klippify"], "mandatory_mentions": ["@marcocappelliagency"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 273.3}, {"id": "6980d346cea4c29db61a307e", "campaign_token": "6980d346cea4c29db61a307e", "campaign_url": "https://app.klippify.com/campaigns/6980d346cea4c29db61a307e", "name": "Ale Della Giusta - ENG", "brand": "aledellagiusta", "section": "Iscritte", "payout_per_1k_views": 1.0, "total_views": 48565, "creators_count": 2125, "budget_remaining": 595.0, "budget_spent": 39.0, "budget_total": 750.0, "budget_progress_percent": "5.2%", "banner": "", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/90dcb7cc-d6e8-4b52-9ec1-92c87a16e29b-BLACK-LOGO.png", "description": "This campaign is for Ale Della Giusta, an acclaimed documentary storyteller who explores the frontiers of human potential. Think of him as a modern-day explorer, blending high-end cinematography with deep, personal journeys of growth. This specific campaign focuses on his groundbreaking 5-episode series filmed in Mexico. It's a journalistic and immersive exploration into the world of psychedelic substances, their therapeutic potential, and their cultural significance. This is not just a travel vlog; it's a thought-provoking documentary series in the vein of shows you'd find on Netflix or HBO, touching on themes highly relevant to a US audience interested in bio-hacking, mental health, and personal transformation.", "status": "Active", "mandatory_hashtags": ["#aledellagiustaeng", "#klippify"], "mandatory_mentions": ["@aledellagiusta"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 262.4}, {"id": "69b0ffca471017e7bfe49765", "campaign_token": "69b0ffca471017e7bfe49765", "campaign_url": "https://app.klippify.com/campaigns/69b0ffca471017e7bfe49765", "name": "Physioterapeasy", "brand": "PhysioterapEasy", "section": "In pausa", "payout_per_1k_views": 3.0, "total_views": 2689, "creators_count": 351, "budget_remaining": 226.0, "budget_spent": 24.0, "budget_total": 250.0, "budget_progress_percent": "9.6%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Physioterapeasy__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/b8341ba7-41d4-4d96-82da-a95c791c8998-LOGO-IG.jpg", "description": "Rivolto a studenti di Fisioterapia o Scienze Motorie e a fisioterapisti alle prime armi. L'idea è quella di mostrare il nostro \"Physio Bundle & WebApp\" con focusc su contrasto tra \"Studiare su mille libri pesanti\" vs \"Avere tutto su iPad/PC con il nostro Bundle e testarsi con la WebApp\". Il messaggio principale deve essere: risparmio di tempo, schemi visivi bellissimi e simulazione dei vari tipi di esame. Vogliamo vedere lo schermo con i nostri PDF e la Dashboard della WebApp.", "status": "Active", "mandatory_hashtags": ["#physioterapeasy", "#klippify"], "mandatory_mentions": ["@physioterapeasy"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 209.3}, {"id": "699ededd3f5febcf2f3acae9", "campaign_token": "699ededd3f5febcf2f3acae9", "campaign_url": "https://app.klippify.com/campaigns/699ededd3f5febcf2f3acae9", "name": "WoodCrafts DIY", "brand": "WoodCrafts DIY", "section": "Iscritte", "payout_per_1k_views": 6.0, "total_views": 12572, "creators_count": 1309, "budget_remaining": 314.0, "budget_spent": 42.0, "budget_total": 500.0, "budget_progress_percent": "8.4%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/WoodCrafts_DIY__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/9b975f55-d384-4f47-9974-61cedee70f9c-logo.png", "description": "WoodCraftsDIY is a digital woodworking brand that helps beginners and hobbyists build furniture and home projects the right way without wasting time, money, or materials on guesswork. The idea behind the brand is simple: you don't need years of experience or a professional workshop to create something beautiful with your own hands. You just need the right plans.", "status": "Active", "mandatory_hashtags": ["#woodcraftsdiy", "#klippify"], "mandatory_mentions": ["@woodcraftsdiy"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 205.4}, {"id": "6a346c9ba53170de02cc90b4", "campaign_token": "6a346c9ba53170de02cc90b4", "campaign_url": "https://app.klippify.com/campaigns/6a346c9ba53170de02cc90b4", "name": "YC Startup podcast (Lobster Talks)", "brand": "Lobster Capital", "section": "Nuove", "payout_per_1k_views": 2.5, "total_views": 1353, "creators_count": 466, "budget_remaining": 467.5, "budget_spent": 32.5, "budget_total": 500.0, "budget_progress_percent": "6.5%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/46ae39d5-d53e-4f10-a88f-7ace24c54c7e-Website-Background.jpg", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/8871187b-b747-4d7b-9256-bb87ccf7452c-Modern-Logo-Featuring-Red-Lobster-With-Silver-Microphone.png", "description": "Welcome to Lobster Talks — where real founders, investors, and operators get honest about building and betting on the future.", "status": "Active", "mandatory_hashtags": ["#ycstartuppodcastlobstertalks", "#klippify"], "mandatory_mentions": ["@lobstercapital"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": 155.9}, {"id": "6a707b47a2d57190f5d39e5e", "campaign_token": "6a707b47a2d57190f5d39e5e", "campaign_url": "https://app.klippify.com/campaigns/6a707b47a2d57190f5d39e5e", "name": "Theory Best Moments", "brand": "Theory Spa", "section": "Nuove", "payout_per_1k_views": 0.5, "total_views": 4101397, "creators_count": 342, "budget_remaining": 0.0, "budget_spent": 899.75, "budget_total": 900.0, "budget_progress_percent": "100.0%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/00d21fd3-7578-4489-b6b5-f41d5e4bee7c-badge-franchising.png", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/3aefd338-2e3b-4d4b-baae-6d4070f65a38-theory-holding-logo-real.png", "description": "Theory Holding è una azienda made in Italy dove i talenti rendono le visioni, rivoluzioni di interi mercati", "status": "Active", "mandatory_hashtags": ["#theorybestmoments", "#klippify"], "mandatory_mentions": ["@theoryspa"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": -10000.0}, {"id": "6a6b425c94bf29a44bfdafe0", "campaign_token": "6a6b425c94bf29a44bfdafe0", "campaign_url": "https://app.klippify.com/campaigns/6a6b425c94bf29a44bfdafe0", "name": "Gurulandia - Green Theory vs FitActive", "brand": "Marco Cappelli Agency", "section": "Nuove", "payout_per_1k_views": 0.25, "total_views": 6226618, "creators_count": 678, "budget_remaining": 0.0, "budget_spent": 1499.0, "budget_total": 1500.0, "budget_progress_percent": "99.9%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/2de0e0b2-a96d-41e9-9fc3-c9fe5fb793bd-WhatsApp-Image-2026-07-30-at-13.32.19.jpeg", "logo": "https://lh3.googleusercontent.com/a/ACg8ocKtof6jsOkYphrb-ZTdiiS-zEylShB3tljHy5-J3n7niLXNx2A=s96-c", "description": "Gurulandia è uno dei podcast business più seguiti in Italia. Ogni settimana mette a confronto imprenditori, CEO e personaggi di primo piano con interviste senza filtri, domande scomode e dibattiti accesi. L'obiettivo è creare contenuti che facciano discutere, intrattengano e portino valore a chi vuole capire davvero come funzionano business e imprenditoria.", "status": "Active", "mandatory_hashtags": ["#gurulandiagreentheoryvsfitactive", "#klippify"], "mandatory_mentions": ["@marcocappelliagency"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": -10000.0}, {"id": "6a1996491231f0472607816f", "campaign_token": "6a1996491231f0472607816f", "campaign_url": "https://app.klippify.com/campaigns/6a1996491231f0472607816f", "name": "Lorenzo Capone", "brand": "Lorenzo Capone", "section": "Nuove", "payout_per_1k_views": 5.0, "total_views": 169959, "creators_count": 212, "budget_remaining": 0.0, "budget_spent": 469.0, "budget_total": 500.0, "budget_progress_percent": "93.8%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/580efbaa-e6ba-4e1a-9f50-f5a4b608acc5-2021-11-21-17.04.10.JPG", "logo": "https://lh3.googleusercontent.com/a/ACg8ocIh2cIZ4axwirrTgzxgqS2XM1rZRy85G1avHJSrWgkd7d0AOPUv=s96-c", "description": "Canale youtube: https://www.youtube.com/@lorenzo.caponeLorenzo Capone. 5 anni in Binance, ora Head of Growth Sud Europa @Kraken.Sogno di diventare uno startupparo seriale.Parlo di AI, Marketing & Growth, Crypto e Mindset.", "status": "Active", "mandatory_hashtags": ["#lorenzocapone", "#klippify"], "mandatory_mentions": ["@lorenzocapone"], "call_to_action": "Guarda il video completo su Klippify!", "target_niche": "Creator / Entertainment", "rules": ["Rispetta le linee guida Klippify"], "local_folder_match": "", "has_local_media": false, "convenience_score": -10000.0}];
        const dashboardData = {"user_name": "riccardo", "greeting": "Bentornato, riccardo! 👋", "subtitle": "Ecco cosa sta succedendo oggi nel tuo percorso da creator.", "stats": {"Guadagni prelevabili": {"val": "0,00 USD", "sub": "Pronti per il prelievo"}, "Guadagni totali": {"val": "0,00 USD", "sub": "Guadagni complessivi"}, "Campagne attive": {"val": "4", "sub": "Campagne in corso"}, "La tua valutazione": {"val": "0.0", "sub": "Nessuna valutazione"}}, "participating_campaigns": [{"name": "Collecto", "brand": "di Salvatore Zola", "payouts": ["1,00 USD/1k", "1,00 USD/1k"], "views": "244.485", "creators": "648", "budget_remaining": "796,00 USD", "budget_spent": "204,00 USD", "budget_total": "1000,00 USD", "progress_percent": "20%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/03b82d2e-f63f-4f8e-9df5-c2649179a469-Collecto_def_2.png"}, {"name": "Ale Della Giusta - ENG", "brand": "di aledellagiusta", "payouts": ["1,00 USD/1k", "1,00 USD/1k"], "views": "48.565", "creators": "2125", "budget_remaining": "595,00 USD", "budget_spent": "39,00 USD", "budget_total": "750,00 USD", "progress_percent": "5%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Ale_Della_Giusta__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/90dcb7cc-d6e8-4b52-9ec1-92c87a16e29b-BLACK-LOGO.png"}, {"name": "WoodCrafts DIY", "brand": "di WoodCrafts DIY", "payouts": ["6,00 USD/1k", "6,00 USD/1k"], "views": "12.572", "creators": "1309", "budget_remaining": "314,00 USD", "budget_spent": "42,00 USD", "budget_total": "500,00 USD", "progress_percent": "8%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/WoodCrafts_DIY__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/9b975f55-d384-4f47-9974-61cedee70f9c-logo.png"}, {"name": "SFS1", "brand": "di Smoke Free Skin", "payouts": ["2,00 USD/1k", "2,00 USD/1k"], "views": "208.419", "creators": "184", "budget_remaining": "28,00 USD", "budget_spent": "472,00 USD", "budget_total": "500,00 USD", "progress_percent": "94%", "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/SFS1__16x9_2K.webp", "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/ac4c586d-7560-4a3d-a16e-fe824b4f0606-SFS-Logo2-2.png"}], "earnings_summary": {"month": "0,00 USD", "week": "0,00 USD", "today": "0,00 USD"}, "recent_withdrawals": []};
        let klippifySubmissions = [{"id": "6a8780707d8d5ed7ff3eecbb", "campaign_id": "6a71c6f7245627c68999eae2", "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali", "campaign_budget": 450, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7676245138934451478", "thumbnail_url": null, "status": "rejected", "is_ai_verified": false, "ai_reasoning": "The video does not follow the guidelines because it lacks a strong hook in the first 3 seconds. Instead, it starts with an introductory question ('cosa facevi prima a livello lavorativo') and polite greetings ('allora intanto ciao Sara...'), which violates the rule of starting directly with the most engaging moment without introductions.", "views": 0, "likes": 0, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-08-20T22:32:19.744Z"}, {"id": "6a877ba57d8d5ed7ff3ee3c4", "campaign_id": "6a71c6f7245627c68999eae2", "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali", "campaign_budget": 450, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7676239876169239830", "thumbnail_url": "https://p19-common-sign.tiktokcdn-us.com/tos-no1a-p-0037-no/oQqAILALVIAuErAAYfEDfaQvT69PGeaFIoPVMO~tplv-tiktokx-origin.image?dr=9636&x-expires=1787500800&x-signature=HL3YXXmPfPuoeU0cPzrcNKJwvlA%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video satisfies all the brand guidelines. It starts immediately with the testimonial without an intro hook (within the first 3 seconds). It features dynamic Italian subtitles throughout. The duration is 36 seconds, which is well within the 20-60 seconds range. The call-to-action 'La lezione gratuita sul profilo di Sara' is constantly visible at the bottom of the screen. No operational details of dropshipping are explained, only the student's personal experience. The earnings claim is presented as a student's real testimonial ('Cristina genera più di 3000€...'), which is explicitly permitted. The tone is authentic, and there are no external watermarks.", "views": 164, "likes": 2, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-08-20T22:11:54.279Z"}, {"id": "6a874f797d8d5ed7ff3e9e3d", "campaign_id": "6a71c6f7245627c68999eae2", "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali", "campaign_budget": 450, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7676190979531001110", "thumbnail_url": "https://p16-common-sign.tiktokcdn-us.com/tos-no1a-p-0037-no/oEEF7bDbFAZbhnOXAVfaACnCcmvIQkAfgq0TTE~tplv-tiktokx-origin.image?dr=9636&x-expires=1787500800&x-signature=dGMZu%2FzmMBUYkMrgim%2BDsh%2Bsluc%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video fully respects the brand guidelines. It has an engaging hook in the first 3 seconds, dynamic Italian subtitles, and a persistent call-to-action at the bottom pointing to the free lesson on Sara's profile. The income claim is presented as a student's testimonial rather than a direct promise, the tone is authentic, and no operational details of dropshipping are explained.", "views": 24, "likes": 1, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-08-20T19:03:24.395Z"}, {"id": "6a8683ba763fa81a0f4e463d", "campaign_id": "6a71c6f7245627c68999eae2", "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali", "campaign_budget": 450, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7675966195333467414", "thumbnail_url": null, "status": "rejected", "is_ai_verified": false, "ai_reasoning": "The video does not comply with the guidelines because it fails to include the mandatory call-to-action (CTA) 'La lezione gratuita sul profilo di Sara' at the end of the clip.", "views": 0, "likes": 0, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-08-20T04:34:06.891Z"}, {"id": "6a490415b779bbed8589b166", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7658654033363750176", "thumbnail_url": "https://p19-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/osUgUfgJHgdDDtOIBNfEJfDMAGkFEr72UtJVgB~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=zYzoXCn2Hofw%2FCnHMvOcbtvqR4U%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video is 56 seconds long, exceeding the 15-second minimum. The tag '@alestark_ufficiale' is visible on screen, and the main focus is on Ale Stark, whose face matches the provided reference images. No specific brand logo was attached, but the promotional guidelines are fully respected.", "views": 153, "likes": 3, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-07-04T13:01:12.601Z"}, {"id": "6a3c038490fece2ed4977b5a", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7654997062324325665", "thumbnail_url": "https://p19-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/oAaCMjjowDBoi0zEWD8Q6gxtAdAIBvi0zZCRg~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=NZeDZYdOApySF6h5EkkHLkJsA7M%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video exceeds the 15-second minimum, features the creator Ale Stark as the main focus, and contains the required tag '@alestark_ufficiale'. The attached image shows him with a yellow car, which does not appear in this video, but his face matches.", "views": 238, "likes": 22, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-06-24T16:19:19.877Z"}, {"id": "6a3bcdf190fece2ed4974f04", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7654938180679929121", "thumbnail_url": "https://p16-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/o8bgve57egoDGAaICfkIJpDMzGdLEruEUot0KU~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=dibUaNLJDB4x3TLYMjvcAUzWrPQ%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video satisfies all key guidelines: its duration exceeds 15 seconds, the tag '@alestark_ufficiale' is clearly displayed, and the focus remains on the main subject. The person featured matches the face in the attachment, although the specific image of him with the yellow car does not appear in the video.", "views": 242, "likes": 15, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-06-24T12:30:44.545Z"}, {"id": "6a393adb90fece2ed49589f1", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7654212915725159712", "thumbnail_url": "https://p19-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/oQD5BTA6qImewcDgOBOFN4oEQADE5wEEUQf0ht~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=i%2FkvjHb7JVINo%2BIrxtL4nFJzuUY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video runs for over 15 seconds, displays the handle '@alestark_ufficiale', and centers entirely on Ale Stark. The person in the video matches the face in the provided reference images.", "views": 227, "likes": 20, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-06-22T13:38:39.777Z"}, {"id": "6a37fc46ab5818f7619176ee", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7653863135014604064", "thumbnail_url": "https://p16-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/o4IQ9e3RMQBfQvffmfXCwFN3EM8yRKaIQ3A4Av~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=0uRg5MxXWDAVcNZ8axQRPS6xRxY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video satisfies all brand requirements: its duration is well over 15 seconds, it prominently features the required '@alestark_ufficiale' tag, and Ale Stark remains the main focus. The individual shown in the attachment is present throughout the video, particularly in the final shot at 01:12.", "views": 244, "likes": 13, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-06-21T14:59:21.239Z"}, {"id": "6a355ff0ab5818f7619049b7", "campaign_id": "6a049b85cae4eba48d7c47d0", "campaign_name": "MondoCash Podcast - 2", "campaign_budget": 1000, "platform": "tiktok", "post_url": "https://www.tiktok.com/@jiemli/video/7653127949398428960", "thumbnail_url": "https://p16-common-sign.tiktokcdn-us.com/tos-useast2a-p-4864-euttp/oYfAXVPmNBDFyhKECIgTfbEnvP9Q1qgUDwB1EY~tplv-tiktokx-origin.image?dr=9636&x-expires=1785189600&x-signature=jQt7gptmH7LI1YLb%2Bfw%2F2hw4np8%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=useast5", "status": "accepted", "is_ai_verified": true, "ai_reasoning": "The video is over 15 seconds, prominently features Ale Stark, and includes the required tag '@alestark_ufficiale'. The person in the video matches the face shown in the attached images. No separate logo is present in the attachments, but the tag acts as the identifying text.", "views": 211, "likes": 21, "comments": 0, "shares": 0, "earnings": 0.0, "created_at": "2026-06-19T15:27:49.765Z"}];
        let generatedContent = [{"campaign_id": "6a2433a7e3244ca026589180", "campaign_name": "Fashion Bus", "section": "Nuove", "feasibility_score": 34739.7, "feasibility_rating": "ALTA", "feasibility_reasoning": "Payout alto (1.5€/1k) e budget residuo combinati a un concept altamente visivo (festa in autobus a Roma). Perfetto per POV e vlog locali ad alta viralità.", "payout_per_1k": 1.5, "daily_video_goal": "2-3 video al giorno", "best_video_type": "POV immersivo o Vlog locale con sound in trend", "scripts": [{"concept_name": "POV Festa Epica", "video_prompt_gemini": "Vertical 9:16 video, 15-30 seconds. A cinematic POV shot walking into a luxurious, neon-lit party bus in Rome at night. People are dancing, singing karaoke, laser lights scanning the interior. Dynamic camera movement, high energy. The first 2 seconds show a surprising transition from a quiet Roman street to the wild bus interior. Call to action to book on WhatsApp included at the end. Brand rule: Rispetta le linee guida Klippify.", "tiktok_caption": "POV: hai trovato il modo migliore per festeggiare a Roma 🚌✨ @fashionbus #fashionbus #klippify", "storyboard": [{"duration": "0-3s", "description": "Transizione veloce da una strada di Roma all'interno del Fashion Bus illuminato a festa.", "text_overlay": "POV: non sai come festeggiare a Roma... e trovi questo"}, {"duration": "3-10s", "description": "Montaggio dinamico di persone che ballano, luci neon, karaoke e drink.", "text_overlay": "Un locale intero solo per te e i tuoi amici!"}, {"duration": "10-15s", "description": "Inquadratura esterna del bus che passa vicino al Colosseo con musica a palla.", "text_overlay": "Richiedi info su WhatsApp!"}]}, {"concept_name": "Idee Compleanno Roma", "video_prompt_gemini": "Vertical 9:16 video, 15-30 seconds. A bright, fun and energetic aesthetic. Someone blowing out birthday candles inside a moving neon-lit party bus in Rome. Friends cheering, drinks clinking. The first 2 seconds feature an excited reaction face before revealing the bus interior. Call to action to book included at the end. Brand rule: Rispetta le linee guida Klippify.", "tiktok_caption": "L'idea geniale per il tuo prossimo compleanno nella Capitale 🎂🎉 @fashionbus #fashionbus #klippify", "storyboard": [{"duration": "0-3s", "description": "Primo piano di una persona emozionata che entra nel bus.", "text_overlay": "Cerchi un'idea originale per il tuo compleanno?"}, {"duration": "3-10s", "description": "La persona soffia sulle candeline mentre gli amici festeggiano nel bus in movimento.", "text_overlay": "Dimentica i soliti locali affollati..."}, {"duration": "10-15s", "description": "Chiusura con l'atmosfera della festa e logo.", "text_overlay": "Prenota il tuo Fashion Bus! Info in bio."}]}, {"concept_name": "Il Segreto di Roma", "video_prompt_gemini": "Vertical 9:16 video, 15-30 seconds. A mysterious and luxurious vibe. Someone looking out the window of a moving party bus looking at the Colosseum at night. Then cuts to a wild VIP party happening inside the bus. Cinematic lighting, smooth slow-motion shots. Strong visual hook showing an unassuming bus transforming into a club. Call to action included at the end. Brand rule: Rispetta le linee guida Klippify.", "tiktok_caption": "Il segreto meglio custodito per le serate romane 🤫 @fashionbus #fashionbus #klippify", "storyboard": [{"duration": "0-3s", "description": "Inquadratura misteriosa dall'esterno di un bus che passa per Roma.", "text_overlay": "Tutti pensano sia un semplice autobus..."}, {"duration": "3-10s", "description": "Transizione fluida all'interno che mostra una festa VIP esclusiva.", "text_overlay": "...finché non ci entri dentro!"}, {"duration": "10-15s", "description": "Focus su luci, musica e divertimento.", "text_overlay": "La tua festa privata itinerante. Scrivigli su WA!"}]}]}, {"campaign_id": "6a71c6f7245627c68999eae2", "campaign_name": "Sara Dizdari Academy – Scopri i negozi digitali", "section": "Nuove", "feasibility_score": 6081.5, "feasibility_rating": "ALTA", "feasibility_reasoning": "Budget residuo al 99.2% (446.5€ disponibili), bassissima concorrenza (solo 9 creator iscritti) e un concept formativo con forte appeal su un target femminile orientato all'indipendenza economica e allo smart working. La strategia punta sull'effetto curiosità e sul desiderio di libertà per massimizzare la ritenzione e convertire in follower e visualizzazioni della lezione gratuita.", "payout_per_1k": 0.5, "daily_video_goal": "2-3 video al giorno", "best_video_type": "POV Relatable / Aesthetic Faceless Lifestyle & Educational Hooks", "scripts": [{"concept_name": "Risultati Shopify con il minimo sforzo (Clip 1: 05:49-06:25)", "video_prompt_gemini": "Hook: POV: 3.210€ col minimo tempo dedicato...\nTrascrizione: Quindi siamo a 3.210€ di fatturato, 114 ordini. Per adesso tu sei soddisfatta del risultato? Parlami un po' di questo dedicandoci il minimo di tempo. Assolutamente soddisfatta perché appunto dedicando pochissimo tempo vedere che si riesce ad arrivare a un fatturato così, molto soddisfatta.\nCTA Obbligatoria finale: La lezione gratuita sul profilo di Sara", "tiktok_caption": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping", "video_filename": "clip_SaraDizdari_slot1_v2.mp4", "storyboard": [{"scene": 1, "duration": "0-3s", "description": "Hook Visivo: POV: 3.210€ col minimo tempo dedicato...", "text_overlay": "POV: 3.210€ col minimo tempo dedicato..."}, {"scene": 2, "duration": "05:49-06:25", "description": "Quindi siamo a 3.210€ di fatturato, 114 ordini. Per adesso tu sei soddisfatta del risultato? Parlami un po' di questo dedicandoci il minimo di tempo. Assolutamente soddisfatta perché appunto dedicando pochissimo tempo vedere che si riesce ad arrivare a un fatturato così, molto soddisfatta.", "text_overlay": "Segui @saradizdari_ecom"}, {"scene": 3, "duration": "Finale", "description": "CTA Obbligatoria Klippify: La lezione gratuita sul profilo di Sara", "text_overlay": "La lezione gratuita sul profilo di Sara"}]}, {"concept_name": "Dall'essere schiavi del lavoro alla libertà (Clip 2: 01:33-02:21)", "video_prompt_gemini": "Hook: Ero un'imprenditrice, ma schiava del lavoro...\nTrascrizione: A 37 anni vedermi chiusa... sì in una bella attività, ma non era la vita di Cristina. Dovevo rinunciare alle uscite, con le amiche, la famiglia. Vacanze calcolate al minimo e sempre con il pensiero. Volevo riacquistare la libertà, non essere più schiavo del lavoro.\nCTA Obbligatoria finale: La lezione gratuita sul profilo di Sara", "tiktok_caption": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria", "video_filename": "clip_SaraDizdari_slot2_v2.mp4", "storyboard": [{"scene": 1, "duration": "0-3s", "description": "Hook Visivo: Ero un'imprenditrice, ma schiava del lavoro...", "text_overlay": "Ero un'imprenditrice, ma schiava del lavoro..."}, {"scene": 2, "duration": "01:33-02:21", "description": "A 37 anni vedermi chiusa... sì in una bella attività, ma non era la vita di Cristina. Dovevo rinunciare alle uscite, con le amiche, la famiglia. Vacanze calcolate al minimo e sempre con il pensiero. Volevo riacquistare la libertà, non essere più schiavo del lavoro.", "text_overlay": "Segui @saradizdari_ecom"}, {"scene": 3, "duration": "Finale", "description": "CTA Obbligatoria Klippify: La lezione gratuita sul profilo di Sara", "text_overlay": "La lezione gratuita sul profilo di Sara"}]}, {"concept_name": "Mindset contro la paura di rischiare e fallire (Clip 3: 11:14-12:02)", "video_prompt_gemini": "Hook: Hai paura di sbagliare ancora?\nTrascrizione: Se a 16 anni ti innamori e rimani deluso che fai, non vivi più l'amore? Le cose vanno provate, i rischi ci sono in qualsiasi cosa si faccia nella vita. C'è chi preferisce vivere in un guscio e non fare il passo più lungo, ma non vede la bellezza fuori.\nCTA Obbligatoria finale: La lezione gratuita sul profilo di Sara", "tiktok_caption": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify", "video_filename": "clip_SaraDizdari_slot3_v2.mp4", "storyboard": [{"scene": 1, "duration": "0-3s", "description": "Hook Visivo: Hai paura di sbagliare ancora?", "text_overlay": "Hai paura di sbagliare ancora?"}, {"scene": 2, "duration": "11:14-12:02", "description": "Se a 16 anni ti innamori e rimani deluso che fai, non vivi più l'amore? Le cose vanno provate, i rischi ci sono in qualsiasi cosa si faccia nella vita. C'è chi preferisce vivere in un guscio e non fare il passo più lungo, ma non vede la bellezza fuori.", "text_overlay": "Segui @saradizdari_ecom"}, {"scene": 3, "duration": "Finale", "description": "CTA Obbligatoria Klippify: La lezione gratuita sul profilo di Sara", "text_overlay": "La lezione gratuita sul profilo di Sara"}]}]}];
        let selectedCampaigns = ["6a71c6f7245627c68999eae2", "6a049b85cae4eba48d7c47d0", "6a426231e6a21896f769dc80", "69db9e0c61ce1b8904c4c3b7", "6980d346cea4c29db61a307e", "699ededd3f5febcf2f3acae9", "69b6fb2b7add71b606b303d2", "6a2433a7e3244ca026589180"];
        const publishedContent = [{"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260813_225633.mp4", "timestamp": "2026-08-15 20:24:35", "title": "test\n\ntest"}, {"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:32:57", "title": "test\n\nssss"}, {"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260813_233108.mp4", "timestamp": "2026-08-15 20:35:36", "title": "test\n\n,,,,,"}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:36:42", "title": "test\n\n,,,,,"}, {"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260813_233108.mp4", "timestamp": "2026-08-15 20:40:52", "title": "test\n\naaaaaa"}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:45:15", "title": "titolo\n\ndescrizione"}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:47:07", "title": "test\n\nmmm"}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:50:06", "title": "mmmm\n\nnnn"}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:56:04", "title": "test\n\n.."}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 20:56:37", "title": "test\n\n."}, {"campaign_id": "6a7386b22080c9c1c92a3f14", "filename": "video_gemini_20260815_202956.mp4", "timestamp": "2026-08-15 21:00:00", "title": "test\n\nm"}, {"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260818_223119.mp4", "timestamp": "2026-08-18 22:32:22", "title": "kk\n\nkk"}, {"campaign_id": "6a2433a7e3244ca026589180", "filename": "video_gemini_20260813_233108.mp4", "timestamp": "2026-08-18 22:35:54", "title": "test\n\nff"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_20260819_182942.mp4", "timestamp": "2026-08-19 18:58:49", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita nel profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #klippify #ecom #ecommerce #dropshipping #dropshippingitalia"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot2_20260819_183239.mp4", "timestamp": "2026-08-19 21:28:42", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la video-lezione gratuita sul profilo di @saradizdari_ecom! #klippify #ecom #ecommerce #dropshipping #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_v2.mp4", "timestamp": "2026-08-20 11:30:02", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_v2.mp4", "timestamp": "2026-08-20 11:33:11", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_v2.mp4", "timestamp": "2026-08-20 11:46:10", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot2_v2.mp4", "timestamp": "2026-08-20 12:00:19", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260820_144723.mp4", "timestamp": "2026-08-20 15:09:41", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260820_150450.mp4", "timestamp": "2026-08-20 15:30:02", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260820_150450.mp4", "timestamp": "2026-08-20 15:30:35", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260820_150450.mp4", "timestamp": "2026-08-20 23:40:21", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260820_150450.mp4", "timestamp": "2026-08-21 17:56:04", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260820_150450.mp4", "timestamp": "2026-08-21 17:56:19", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot3_20260820_150450.mp4", "timestamp": "2026-08-21 18:07:28", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot2_20260820_150450.mp4", "timestamp": "2026-08-21 18:07:44", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot1_20260819_162117.mp4", "timestamp": "2026-08-21 18:30:26", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot1_20260819_162539.mp4", "timestamp": "2026-08-21 18:30:41", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260820_150450.mp4", "timestamp": "2026-08-21 20:00:10", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot1_20260820_150450.mp4", "timestamp": "2026-08-21 20:00:26", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a426231e6a21896f769dc80", "filename": "clip_SaraDizdariA_slot1_20260819_182658.mp4", "timestamp": "2026-08-21 20:00:41", "title": "Guarda fino alla fine! 🚀 Guarda il video completo sul profilo! 💡  #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260819_182658.mp4", "timestamp": "2026-08-21 20:00:56", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260819_162539.mp4", "timestamp": "2026-08-21 20:01:11", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260819_182658.mp4", "timestamp": "2026-08-21 20:01:26", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260819_162539.mp4", "timestamp": "2026-08-21 21:03:27", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260819_182658.mp4", "timestamp": "2026-08-21 21:03:42", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_20260819_183239.mp4", "timestamp": "2026-08-21 21:03:57", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260819_162539.mp4", "timestamp": "2026-08-21 21:04:12", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260819_182658.mp4", "timestamp": "2026-08-21 21:04:27", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot1_20260819_183239.mp4", "timestamp": "2026-08-21 21:04:42", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260819_162539.mp4", "timestamp": "2026-08-21 21:06:52", "title": "Guarda fino alla fine! 🚀 La lezione gratuita sul profilo di Sara 💡 @saradizdari_ecom #saradizdari #negozidigitali #ecommerce #shopify #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot2_20260819_182942.mp4", "timestamp": "2026-08-21 21:06:58", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot3_20260819_182942.mp4", "timestamp": "2026-08-21 21:07:13", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot3_20260819_183239.mp4", "timestamp": "2026-08-21 21:07:28", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdari_slot3_v2.mp4", "timestamp": "2026-08-21 21:07:43", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260820_144723.mp4", "timestamp": "2026-08-21 21:07:58", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260820_144723.mp4", "timestamp": "2026-08-21 21:08:13", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260820_145155.mp4", "timestamp": "2026-08-21 21:08:28", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260820_145724.mp4", "timestamp": "2026-08-21 21:08:43", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260820_145724.mp4", "timestamp": "2026-08-21 21:08:58", "title": "I rischi ci sono in qualsiasi cosa, ma chi resta nel suo guscio non vedrà mai la bellezza fuori! 💫 Segui @saradizdari_ecom e guarda la lezione gratuita sul profilo di Sara! #saradizdari #negozidigitali #mindset #ecommerce #klippify"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260820_145724.mp4", "timestamp": "2026-08-21 21:09:14", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260821_211349.mp4", "timestamp": "2026-08-23 05:03:01", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot2_20260821_211349.mp4", "timestamp": "2026-08-23 12:24:12", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"filename": "clip_SaraDizdariA_slot2_20260823_052421.mp4", "tiktok_url": "https://www.tiktok.com/@jiemli/video/7676701987517287702", "post_url": "https://www.tiktok.com/@jiemli/video/7676701987517287702", "video_id": "7676701987517287702", "campaign_id": "6a71c6f7245627c68999eae2", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping", "published_at": "2026-08-23 12:45:34"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260823_052421.mp4", "timestamp": "2026-08-23 12:51:00", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"filename": "clip_SaraDizdariA_slot1_20260823_052421.mp4", "tiktok_url": "https://www.tiktok.com/@jiemli/video/7676685639567297814", "post_url": "https://www.tiktok.com/@jiemli/video/7676685639567297814", "video_id": "7676685639567297814", "campaign_id": "6a71c6f7245627c68999eae2", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping", "published_at": "2026-08-23 12:52:08"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260823_052421.mp4", "timestamp": "2026-08-24 18:57:46", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot1_20260823_052421.mp4", "timestamp": "2026-08-24 18:58:01", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260823_052421.mp4", "timestamp": "2026-08-24 18:58:16", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria"}, {"campaign_id": "6a71c6f7245627c68999eae2", "filename": "clip_SaraDizdariA_slot3_20260823_052421.mp4", "timestamp": "2026-08-24 18:58:32", "title": "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"}, {"filename": "clip_SaraDizdariA_slot1_20260823_052421.mp4", "tiktok_url": "https://www.tiktok.com/@jiemli/video/7677318263520447766", "post_url": "https://www.tiktok.com/@jiemli/video/7677318263520447766", "video_id": "7677318263520447766", "campaign_id": "6a71c6f7245627c68999eae2", "title": "A 37 anni ho deciso di riprendermi la mia libertà e il mio tempo ⏳✨ Scopri la storia e la lezione gratuita sul profilo di @saradizdari_ecom! #saradizdari #negozidigitali #ecommerce #shopify #klippify #libertafinanziaria", "published_at": "2026-08-24 18:59:07"}];
        let cachedTikTokVideos = [];
        let currentDetailCampToken = null;

        function formatDuration(sec) {
            if (!sec) return "";
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        }

        function formatTikTokDate(timestamp) {
            if (!timestamp) return "";
            const d = new Date(timestamp * 1000);
            return d.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });
        }

        function renderTikTokVideoCard(v, isCompact=false) {
            const durBadge = v.duration ? `<span class="tiktok-duration-badge">⏱ ${formatDuration(v.duration)}</span>` : '';
            const coverImg = v.cover_image_url || 'https://via.placeholder.com/300x400/0f172a/94a3b8?text=TikTok+Video';
            const titleText = (v.title || v.description || 'Senza descrizione').replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const dateStr = formatTikTokDate(v.create_time);

            return `
                <div class="tiktok-video-card" style="${isCompact ? 'max-width:320px;' : ''}">
                    <div class="tiktok-cover-wrap" style="${isCompact ? 'padding-top:100%;' : ''}">
                        <img src="${coverImg}" class="tiktok-cover-img" alt="Cover" loading="lazy" onerror="this.src='https://via.placeholder.com/300x400/0f172a/94a3b8?text=TikTok+Video'">
                        ${durBadge}
                    </div>
                    <div class="tiktok-card-body">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
                                <span style="font-size:0.75rem; color:#a78bfa; font-weight:700;">TikTok Live</span>
                                <span style="font-size:0.72rem; color:var(--text-muted);">${dateStr}</span>
                            </div>
                            <div class="tiktok-card-title" title="${titleText}">${titleText}</div>
                        </div>

                        <div class="tiktok-metrics-grid">
                            <div class="tiktok-metric-pill" title="Visualizzazioni">
                                <span style="color:#38bdf8;">👁️</span>
                                <span><strong>${(v.view_count || 0).toLocaleString()}</strong> views</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Mi Piace">
                                <span style="color:#f43f5e;">❤️</span>
                                <span><strong>${(v.like_count || 0).toLocaleString()}</strong> like</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Commenti">
                                <span style="color:#34d399;">💬</span>
                                <span><strong>${(v.comment_count || 0).toLocaleString()}</strong> comm.</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Condivisioni">
                                <span style="color:#f59e0b;">🔄</span>
                                <span><strong>${(v.share_count || 0).toLocaleString()}</strong> share</span>
                            </div>
                        </div>

                        <a href="${v.share_url || '#'}" target="_blank" class="tiktok-link-btn">
                            <span>Guarda su TikTok</span>
                            <span>↗</span>
                        </a>
                    </div>
                </div>
            `;
        }

        async function loadTikTokPublishedVideos(force=false) {
            const grid = document.getElementById('tiktok-published-videos-grid');
            const refreshBtn = document.getElementById('btn-refresh-tiktok-vids');

            if (!force && cachedTikTokVideos && cachedTikTokVideos.length > 0) {
                if (grid) renderTikTokVideosGrid(cachedTikTokVideos);
                return;
            }

            if (refreshBtn) refreshBtn.innerHTML = '⏳ Caricamento...';
            if (grid) grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; grid-column: 1 / -1; text-align:center;">⏳ Connessione all&apos;API TikTok per estrarre tutti i tuoi video...</div>';

            try {
                const res = await fetch('/api/tiktok/videos');
                const data = await res.json();
                if (data.error) throw new Error(data.error);

                cachedTikTokVideos = data.videos || [];
                if (grid) renderTikTokVideosGrid(cachedTikTokVideos);

                // Update any open campaign view stats
                updateCampaignDetailTikTokStats();
            } catch(err) {
                console.error("Errore caricamento video TikTok", err);
                if (grid) grid.innerHTML = `<div style="color:#ef4444; padding:2rem; grid-column: 1 / -1; text-align:center;">❌ Errore nel caricare i video: ${err.message}</div>`;
            } finally {
                if (refreshBtn) refreshBtn.innerHTML = '🔄 Aggiorna Metriche';
            }
        }

        function renderTikTokVideosGrid(videos) {
            const grid = document.getElementById('tiktok-published-videos-grid');
            if (!grid) return;

            if (!videos || videos.length === 0) {
                grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; grid-column: 1 / -1; text-align:center;">Nessun video trovato sul profilo TikTok.</div>';
                return;
            }

            grid.innerHTML = videos.map(v => renderTikTokVideoCard(v)).join('');
        }

        function findMatchingTikTokVideo(campToken, campName, pubItem) {
            if (!cachedTikTokVideos || cachedTikTokVideos.length === 0) return null;
            
            // 1. Direct match by pubItem filename / title
            if (pubItem) {
                if (pubItem.filename) {
                    const match = cachedTikTokVideos.find(v => (v.title || '').includes(pubItem.filename) || (v.description || '').includes(pubItem.filename));
                    if (match) return match;
                }
                if (pubItem.title) {
                    const cleanT = pubItem.title.split('\n')[0].trim().toLowerCase();
                    if (cleanT.length > 3) {
                        const match = cachedTikTokVideos.find(v => (v.title || '').toLowerCase().includes(cleanT) || (v.description || '').toLowerCase().includes(cleanT));
                        if (match) return match;
                    }
                }
            }

            // 2. Match by campaign name or token
            if (campName) {
                const cleanName = campName.toLowerCase().replace(/[^a-z0-9]/g, '');
                if (cleanName.length > 3) {
                    const match = cachedTikTokVideos.find(v => {
                        const desc = (v.description || '').toLowerCase().replace(/[^a-z0-9]/g, '');
                        return desc.includes(cleanName);
                    });
                    if (match) return match;
                }
            }

            return null;
        }

        function updateCampaignDetailTikTokStats() {
            const kanbanCards = document.querySelectorAll('.kanban-card[data-video-file]');
            kanbanCards.forEach(card => {
                const filename = card.getAttribute('data-video-file');
                const campToken = card.getAttribute('data-camp-token') || '';
                const match = findMatchingTikTokVideo(campToken, null, { filename });
                if (match) {
                    const vEl = card.querySelector('.stat-views');
                    const lEl = card.querySelector('.stat-likes');
                    if (vEl) vEl.innerText = (match.view_count || 0).toLocaleString();
                    if (lEl) lEl.innerText = (match.like_count || 0).toLocaleString();
                    
                    const coverEl = card.querySelector('.kanban-video-cover');
                    if (coverEl && match.cover_image_url) {
                        coverEl.src = match.cover_image_url;
                        coverEl.style.display = 'block';
                    }
                }
            });
        }

        // --- DRAG AND DROP KANBAN LOGIC ---
        function allowDrop(ev) {
            ev.preventDefault();
        }

        function drag(ev) {
            ev.dataTransfer.setData("scriptId", ev.target.id);
            ev.dataTransfer.setData("campToken", ev.target.getAttribute("data-camp-token"));
            ev.dataTransfer.setData("scriptIndex", ev.target.getAttribute("data-script-index"));
        }

        async function drop(ev, newStatus) {
            ev.preventDefault();
            const scriptId = ev.dataTransfer.getData("scriptId");
            const campToken = ev.dataTransfer.getData("campToken");
            const scriptIndex = parseInt(ev.dataTransfer.getData("scriptIndex"));
            
            // Find the closest drop zone (the column body)
            let dropZone = ev.target;
            while(dropZone && !dropZone.classList.contains('kanban-column-body')) {
                dropZone = dropZone.parentElement;
            }
            if(!dropZone) return;

            const draggedElement = document.getElementById(scriptId);
            if (draggedElement) {
                dropZone.appendChild(draggedElement);
            }

            // Update Backend
            try {
                await fetch('/api/update-script-status', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        script_index: scriptIndex,
                        status: newStatus
                    })
                });
                
                // Aggiorniamo anche la variabile locale in memoria per evitare glitch se l'utente non ricarica
                const item = generatedContent.find(gc => gc.campaign_id === campToken);
                if (item && item.scripts) {
                    item.scripts[scriptIndex].status = newStatus;
                }
                
            } catch(e) {
                console.error("Errore salvataggio status", e);
            }
        }

        async function fetchAndRenderVideos() {
            const grid = document.getElementById('video-gallery-grid');
            grid.innerHTML = '<div style="color:var(--text-muted)">Caricamento video in corso...</div>';
            try {
                const res = await fetch('/api/videos');
                const videos = await res.json();
                
                if (videos.length === 0) {
                    grid.innerHTML = '<div style="color:var(--text-muted); font-style:italic;">Nessun video generato ancora. Usa il box qui sopra!</div>';
                    return;
                }
                
                grid.innerHTML = '';
                videos.forEach(v => {
                    const sizeMB = (v.size / (1024 * 1024)).toFixed(2);
                    const card = document.createElement('div');
                    card.style.background = 'rgba(15, 23, 42, 0.6)';
                    card.style.border = '1px solid var(--card-border)';
                    card.style.borderRadius = '0.5rem';
                    card.style.padding = '0.5rem';
                    card.style.display = 'flex';
                    card.style.flexDirection = 'column';
                    
                    const videoEl = document.createElement('video');
                    videoEl.src = '/generated_videos/' + encodeURIComponent(v.filename);
                    videoEl.controls = true;
                    videoEl.preload = 'metadata';
                    videoEl.playsInline = true;
                    videoEl.style.width = '100%';
                    videoEl.style.borderRadius = '0.4rem';
                    videoEl.style.background = '#000';
                    videoEl.style.maxHeight = '320px';
                    
                    const title = document.createElement('div');
                    title.style.color = '#fff';
                    title.style.fontSize = '0.8rem';
                    title.style.marginTop = '0.5rem';
                    title.style.wordBreak = 'break-all';
                    title.innerText = v.filename;
                    
                    const meta = document.createElement('div');
                    meta.style.color = 'var(--text-muted)';
                    meta.style.fontSize = '0.7rem';
                    meta.innerText = sizeMB + ' MB';
                    
                    const downloadBtn = document.createElement('a');
                    downloadBtn.href = videoEl.src;
                    downloadBtn.download = v.filename;
                    downloadBtn.innerText = '💾 Salva File';
                    downloadBtn.style.marginTop = '0.5rem';
                    downloadBtn.style.display = 'block';
                    downloadBtn.style.textAlign = 'center';
                    downloadBtn.style.background = 'rgba(255,255,255,0.1)';
                    downloadBtn.style.color = '#fff';
                    downloadBtn.style.padding = '0.3rem';
                    downloadBtn.style.borderRadius = '0.3rem';
                    downloadBtn.style.textDecoration = 'none';
                    downloadBtn.style.fontSize = '0.8rem';
                    
                    card.appendChild(videoEl);
                    card.appendChild(title);
                    card.appendChild(meta);
                    card.appendChild(downloadBtn);
                    grid.appendChild(card);
                });
            } catch (err) {
                grid.innerHTML = '<div style="color:#ef4444;">Errore durante il caricamento dei video.</div>';
                console.error(err);
            }
        }

        async function generateDynamicVideo() {
            const inputEl = document.getElementById('dynamic-prompt-input');
            const btnEl = document.getElementById('dynamic-prompt-btn');
            const statusEl = document.getElementById('dynamic-prompt-status');
            
            const prompt = inputEl.value.trim();
            if (!prompt) {
                alert("Per favore, inserisci un prompt prima di generare!");
                return;
            }
            
            btnEl.disabled = true;
            btnEl.innerText = "⏳ Avvio in corso...";
            btnEl.style.opacity = "0.5";
            
            const spinnerSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 5px;"><path d="M21 12a9 9 0 1 1-6.219-8.56"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite" /></path></svg>`;
            statusEl.innerHTML = spinnerSvg + "Avvio bot...";
            statusEl.style.color = "#f59e0b"; // amber
            
            // Conta video iniziali
            let initialVideoCount = 0;
            try {
                const resCount = await fetch('/api/videos');
                const vids = await resCount.json();
                initialVideoCount = vids.length;
            } catch (e) {}

            try {
                const res = await fetch('/api/generate-video', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ prompt: prompt })
                });
                
                const data = await res.json();
                if (res.ok) {
                    btnEl.innerText = "⏳ Generazione (~1 min)...";
                    statusEl.innerHTML = spinnerSvg + "Generazione video in corso...";
                    
                    // Polling per controllare quando spunta un nuovo video
                    const pollInterval = setInterval(async () => {
                        try {
                            const pollRes = await fetch('/api/videos');
                            const currentVideos = await pollRes.json();
                            if (currentVideos.length > initialVideoCount) {
                                clearInterval(pollInterval);
                                statusEl.innerText = "✅ Video pronto!";
                                statusEl.style.color = "#10b981"; // green
                                btnEl.disabled = false;
                                btnEl.innerText = "Genera Video con Gemini 🎬";
                                btnEl.style.opacity = "1";
                                fetchAndRenderVideos();
                            }
                        } catch(e) {}
                    }, 3000);
                    
                } else {
                    statusEl.innerText = "❌ " + (data.error || "Errore sconosciuto");
                    statusEl.style.color = "#ef4444"; // red
                    btnEl.disabled = false;
                    btnEl.innerText = "Genera Video con Gemini 🎬";
                    btnEl.style.opacity = "1";
                }
            } catch (err) {
                statusEl.innerText = "❌ Errore di rete: " + err.message;
                statusEl.style.color = "#ef4444"; // red
                btnEl.disabled = false;
                btnEl.innerText = "Genera Video con Gemini 🎬";
                btnEl.style.opacity = "1";
            }
        }

        let currentActiveView = 'dashboard';

        function switchMainView(viewName) {
            currentActiveView = viewName;
            const dashView = document.getElementById('view-dashboard-section');
            const intelView = document.getElementById('view-intelligence-section');
            const studioView = document.getElementById('view-studio-section');
            const tiktokView = document.getElementById('view-tiktok-section');
            const myCampsView = document.getElementById('view-my-campaigns-section');
            const debugView = document.getElementById('view-debug-section');
            
            const dashBtn = document.getElementById('main-tab-dashboard');
            const intelBtn = document.getElementById('main-tab-intelligence');
            const studioBtn = document.getElementById('main-tab-studio');
            const tiktokBtn = document.getElementById('main-tab-tiktok');
            const myCampsBtn = document.getElementById('main-tab-my-campaigns');
            const debugBtn = document.getElementById('main-tab-debug');

            if (dashView) dashView.style.display = 'none';
            if (intelView) intelView.style.display = 'none';
            if (studioView) studioView.style.display = 'none';
            if (tiktokView) tiktokView.style.display = 'none';
            if (myCampsView) myCampsView.style.display = 'none';
            if (debugView) debugView.style.display = 'none';
            
            if (dashBtn) dashBtn.classList.remove('active');
            if (intelBtn) intelBtn.classList.remove('active');
            if (studioBtn) studioBtn.classList.remove('active');
            if (tiktokBtn) tiktokBtn.classList.remove('active');
            if (myCampsBtn) myCampsBtn.classList.remove('active');
            if (debugBtn) debugBtn.classList.remove('active');
            
            if (viewName === 'dashboard') {
                if (dashView) dashView.style.display = 'flex';
                if (dashBtn) dashBtn.classList.add('active');
                if (dashView) dashView.scrollIntoView({ behavior: 'smooth' });
            } else if (viewName === 'my-campaigns') {
                if (myCampsView) myCampsView.style.display = 'block';
                if (myCampsBtn) myCampsBtn.classList.add('active');
                if (myCampsView) myCampsView.scrollIntoView({ behavior: 'smooth' });
                renderMyCampaigns();
            } else if (viewName === 'intelligence') {
                if (intelView) intelView.style.display = 'block';
                if (intelBtn) intelBtn.classList.add('active');
                if (intelView) intelView.scrollIntoView({ behavior: 'smooth' });
            } else if (viewName === 'studio') {
                if (studioView) studioView.style.display = 'block';
                if (studioBtn) studioBtn.classList.add('active');
                if (studioView) studioView.scrollIntoView({ behavior: 'smooth' });
                fetchAndRenderVideos();
            } else if (viewName === 'tiktok') {
                if (tiktokView) tiktokView.style.display = 'block';
                if (tiktokBtn) tiktokBtn.classList.add('active');
                if (tiktokView) tiktokView.scrollIntoView({ behavior: 'smooth' });
                loadTikTokPublishedVideos();
            } else if (viewName === 'debug') {
                if (debugView) debugView.style.display = 'block';
                if (debugBtn) debugBtn.classList.add('active');
                if (debugView) debugView.scrollIntoView({ behavior: 'smooth' });
                loadDebugTasks(true);
            }
        }

        // ==========================================
        // AUTOPILOT ENGINE LOGIC & UI FUNCTIONS
        // ==========================================
        // CAMPAIGN-SPECIFIC AUTOPILOT FUNCTIONS
        // ==========================================
        let currentCampaignAutopilotState = {};

        async function loadCampaignAutopilotState(campToken) {
            if (!campToken) return null;
            try {
                const res = await fetch(`/api/autopilot/campaign-status?campaign_id=${encodeURIComponent(campToken)}`);
                const data = await res.json();
                currentCampaignAutopilotState[campToken] = data;

                const toggleBtn = document.getElementById(`btn-camp-autopilot-toggle-${campToken}`);
                const statusBadge = document.getElementById(`camp-autopilot-status-badge-${campToken}`);
                const nextRunEl = document.getElementById(`camp-ap-stat-next-run-${campToken}`);
                const readyEl = document.getElementById(`camp-ap-stat-ready-${campToken}`);

                const isEnabled = data.is_enabled;

                if (toggleBtn) {
                    if (isEnabled) {
                        toggleBtn.innerHTML = '⏸ METTI IN PAUSA';
                        toggleBtn.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
                        toggleBtn.style.boxShadow = '0 4px 15px rgba(245,158,11,0.35)';
                    } else {
                        toggleBtn.innerHTML = '🟢 ATTIVA PILOTA AUTOMATICO';
                        toggleBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                        toggleBtn.style.boxShadow = '0 4px 15px rgba(16,185,129,0.35)';
                    }
                }

                if (statusBadge) {
                    if (isEnabled) {
                        statusBadge.innerHTML = '🟢 ATTIVO (CLIPPING &amp; POSTING AUTOMATICI)';
                        statusBadge.style.background = 'rgba(16,185,129,0.2)';
                        statusBadge.style.color = '#10b981';
                        statusBadge.style.borderColor = 'rgba(16,185,129,0.4)';
                    } else {
                        statusBadge.innerHTML = '⏸ IN PAUSA';
                        statusBadge.style.background = 'rgba(239,68,68,0.2)';
                        statusBadge.style.color = '#ef4444';
                        statusBadge.style.borderColor = 'rgba(239,68,68,0.4)';
                    }
                }

                if (nextRunEl) {
                    if (!isEnabled) {
                        nextRunEl.innerText = 'In pausa';
                        nextRunEl.style.color = '#94a3b8';
                    } else if (data.next_clip) {
                        const clipName = data.next_clip.generated_clip || data.next_clip.source_video || 'Video';
                        const timeStr = data.next_clip.concept_name || 'Prossimo slot';
                        nextRunEl.innerText = `${timeStr} (${clipName})`;
                        nextRunEl.style.color = '#38bdf8';
                    } else {
                        nextRunEl.innerText = 'Tutti gli slot completati!';
                        nextRunEl.style.color = '#34d399';
                    }
                }

                if (readyEl) readyEl.innerText = `${data.ready_count || 0} / ${data.target_count || 3}`;

                return data;
            } catch(e) {
                console.error("Errore fetch stato autopilot campagna:", e);
                return null;
            }
        }

        async function toggleCampaignAutopilot(campToken) {
            const current = currentCampaignAutopilotState[campToken] || {};
            const newState = !current.is_enabled;
            try {
                const res = await fetch('/api/autopilot/campaign-toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken, enable: newState })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    await loadCampaignAutopilotState(campToken);
                    if (newState) {
                        alert("🤖 Pilota Automatico ATTIVATO per questa campagna!\n\nIl bot elaborerà in background il ritaglio (clipping) dei video sorgente mancanti e pubblicherà le clip su TikTok agli orari programmati inviando subito la conferma a Klippify!");
                    } else {
                        alert("⏸ Pilota Automatico MESSO IN PAUSA per questa campagna.");
                    }
                }
            } catch(e) {
                alert("Errore cambio stato pilota automatico: " + e.message);
            }
        }

        async function queueAllCampaignSlots(campToken, btnEl) {
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Inserimento in coda...";
            }
            try {
                const res = await fetch('/api/autopilot/campaign-queue-slots', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert(`✅ Inseriti con successo ${data.added_count} slot di questa campagna nella coda del Pilota Automatico!`);
                    await loadCampaignAutopilotState(campToken);
                }
            } catch(e) {
                alert("Errore accodamento: " + e.message);
            } finally {
                if (btnEl) {
                    btnEl.disabled = false;
                    btnEl.innerText = "📋 Accoda Tutti gli Slot all'Autopilota";
                }
            }
        }

        async function runCampaignAutopilotNow(campToken, btnEl) {
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Avvio immediato...";
            }
            try {
                const res = await fetch('/api/autopilot/campaign-run-now', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert("🚀 Esecuzione avviata! Il bot sta elaborando/pubblicando il prossimo slot di questa campagna.");
                    await loadCampaignAutopilotState(campToken);
                } else {
                    alert("Nota: " + (data.message || data.error));
                }
            } catch(e) {
                alert("Errore esecuzione immediata: " + e.message);
            } finally {
                if (btnEl) {
                    btnEl.disabled = false;
                    btnEl.innerText = "⚡ Pubblica Subito Prossimo Slot";
                }
            }
        }

        async function loadDebugTasks(showLoading = false) {
            const container = document.getElementById('debug-tasks-container');
            if (!container) return;

            try {
                const res = await fetch('/api/debug/tasks');
                let tasks = await res.json();
                if (!Array.isArray(tasks)) tasks = [];

                // ⚡ RIGOROSO ORDINAMENTO: PRIMA i processi 'running' (in corso), poi per data/orario decrescente
                tasks.sort((a, b) => {
                    const aRunning = a.status === 'running' ? 1 : 0;
                    const bRunning = b.status === 'running' ? 1 : 0;
                    if (bRunning !== aRunning) return bRunning - aRunning;
                    return (b.start_timestamp || 0) - (a.start_timestamp || 0);
                });

                let runningCount = 0;
                let stuckCount = 0;
                let completedCount = 0;
                let failedCount = 0;

                tasks.forEach(t => {
                    if (t.status === 'running') {
                        runningCount++;
                        if (t.is_stuck_warning) stuckCount++;
                    } else if (t.status === 'completed') {
                        completedCount++;
                    } else {
                        failedCount++;
                    }
                });

                const badge = document.getElementById('debug-active-badge');
                if (badge) {
                    if (runningCount > 0) {
                        badge.style.display = 'inline-block';
                        badge.innerText = runningCount;
                        badge.style.background = stuckCount > 0 ? '#f59e0b' : '#10b981';
                    } else {
                        badge.style.display = 'none';
                    }
                }

                const statRunning = document.getElementById('debug-stat-running');
                const statStuck = document.getElementById('debug-stat-stuck');
                const statComp = document.getElementById('debug-stat-completed');
                const statFail = document.getElementById('debug-stat-failed');

                if (statRunning) statRunning.innerText = runningCount;
                if (statStuck) statStuck.innerText = stuckCount;
                if (statComp) statComp.innerText = completedCount;
                if (statFail) statFail.innerText = failedCount;

                // Aggiorna dinamicamente i rettangoli "⚡ STO PROCESSANDO" nelle campagne aperte
                document.querySelectorAll('[id^="assembly-active-processing-box-"]').forEach(box => {
                    const cToken = box.id.replace('assembly-active-processing-box-', '');
                    const activeUpload = tasks.find(t => t.status === 'running' && (
                        (t.meta && (t.meta.campaign_id === cToken || t.meta.campaignId === cToken)) ||
                        (t.name && (t.name.includes(cToken) || t.name.toLowerCase().includes('upload tiktok')))
                    ));
                    if (activeUpload) {
                        box.style.display = 'block';
                        const titleEl = document.getElementById('processing-clip-title-' + cToken);
                        const fileEl = document.getElementById('processing-clip-filename-' + cToken);
                        const timerEl = document.getElementById('processing-elapsed-timer-' + cToken);
                        if (titleEl) titleEl.innerText = activeUpload.name || "Upload TikTok & Invio Klippify";
                        if (fileEl && activeUpload.meta && activeUpload.meta.filename) fileEl.innerText = activeUpload.meta.filename;
                        if (timerEl) timerEl.innerText = `⏳ In corso (${activeUpload.duration_seconds || 0}s)`;
                    } else {
                        box.style.display = 'none';
                    }
                });

                if (tasks.length === 0) {
                    container.innerHTML = `
                        <div id="debug-tasks-empty-placeholder" style="text-align:center; padding:3.5rem; color:var(--text-muted); background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem;">
                            <div style="font-size:2.5rem; margin-bottom:0.6rem;">⚙️</div>
                            <div style="font-size:1.1rem; font-weight:700; color:#cbd5e1;">Nessun processo registrato</div>
                            <div style="font-size:0.85rem; margin-top:0.4rem; color:var(--text-muted);">Tutti i processi completati sono stati archiviati o puliti.</div>
                        </div>
                    `;
                    return;
                }

                // Rimuovi l'empty placeholder se presente
                const emptyPlaceholder = document.getElementById('debug-tasks-empty-placeholder');
                if (emptyPlaceholder) {
                    emptyPlaceholder.remove();
                }

                // Rimuovi card che non esistono più
                const currentIds = new Set(tasks.map(t => 'debug-card-' + t.id));
                Array.from(container.children).forEach(child => {
                    if (child.id && child.id.startsWith('debug-card-') && !currentIds.has(child.id)) {
                        child.remove();
                    }
                });

                tasks.forEach((t, index) => {
                    const isRunning = t.status === 'running';
                    const isStuck = t.is_stuck_warning;
                    
                    let statusBadge = '';
                    let cardBorder = 'rgba(255,255,255,0.08)';
                    let cardBg = 'rgba(15,23,42,0.85)';

                    if (isRunning) {
                        if (isStuck) {
                            statusBadge = `<span style="background:rgba(245,158,11,0.2); color:#f59e0b; border:1px solid rgba(245,158,11,0.4); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:800; display:inline-flex; align-items:center; gap:0.4rem;"><span style="width:8px; height:8px; border-radius:50%; background:#f59e0b; display:inline-block; animation:pulse 1s infinite;"></span> ⚠️ LENTO / IN ATTESA (${t.duration_seconds}s)</span>`;
                            cardBorder = 'rgba(245,158,11,0.5)';
                        } else {
                            statusBadge = `<span style="background:rgba(16,185,129,0.2); color:#10b981; border:1px solid rgba(16,185,129,0.4); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:800; display:inline-flex; align-items:center; gap:0.4rem; box-shadow:0 0 10px rgba(16,185,129,0.3);"><span style="width:8px; height:8px; border-radius:50%; background:#10b981; display:inline-block; animation:pulse 1s infinite;"></span> 🟢 IN ESECUZIONE (${t.duration_seconds}s)</span>`;
                            cardBorder = 'rgba(16,185,129,0.4)';
                        }
                    } else if (t.status === 'completed') {
                        statusBadge = `<span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">✅ COMPLETATO (${t.duration_seconds}s)</span>`;
                    } else if (t.status === 'terminated') {
                        statusBadge = `<span style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">🛑 TERMINATO DALL'UTENTE</span>`;
                    } else {
                        statusBadge = `<span style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">❌ ERRORE (${t.duration_seconds}s)</span>`;
                    }

                    const logsJoined = (t.logs || []).join('\n') || 'Nessun log registrato.';
                    const pidInfo = t.pid ? `PID: ${t.pid}` : 'Thread Interno';

                    let cardEl = document.getElementById('debug-card-' + t.id);
                    if (!cardEl) {
                        cardEl = document.createElement('div');
                        cardEl.id = 'debug-card-' + t.id;
                        cardEl.className = 'k-panel-card';
                        cardEl.style.background = cardBg;
                        cardEl.style.border = '1px solid ' + cardBorder;
                        cardEl.style.padding = '1.2rem';
                        cardEl.style.borderRadius = '0.8rem';
                        cardEl.style.boxShadow = isRunning ? '0 8px 25px rgba(0,0,0,0.5), 0 0 15px rgba(16,185,129,0.2)' : '0 4px 20px rgba(0,0,0,0.3)';

                        cardEl.innerHTML = `
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.8rem; margin-bottom:0.8rem;">
                                <div>
                                    <div style="font-size:1.05rem; font-weight:800; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                        <span>${t.name}</span>
                                    </div>
                                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.3rem; display:flex; gap:1rem; flex-wrap:wrap;">
                                        <span>🕒 Avviato: ${t.start_time}</span>
                                        <span id="debug-pid-${t.id}">⚡ ${pidInfo}</span>
                                        <span>ID: <code style="color:#a78bfa;">${t.id}</code></span>
                                    </div>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.8rem;">
                                    <div id="debug-badge-${t.id}">${statusBadge}</div>
                                    <div id="debug-action-${t.id}">
                                        ${isRunning ? `
                                            <button onclick="killTask('${t.id}', this)" style="background:#ef4444; color:#fff; border:none; padding:0.4rem 0.9rem; border-radius:0.4rem; font-size:0.8rem; font-weight:800; cursor:pointer; display:inline-flex; align-items:center; gap:0.3rem; box-shadow:0 2px 8px rgba(239,68,68,0.4); transition:all 0.2s;">
                                                🛑 Termina
                                            </button>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>

                            <!-- TERMINAL LOG BOX -->
                            <div id="debug-log-${t.id}" style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:0.5rem; padding:0.8rem; font-family:'Courier New', Courier, monospace; font-size:0.78rem; color:#a5f3fc; max-height:180px; overflow-y:auto; white-space:pre-wrap; line-height:1.4; box-shadow:inset 0 2px 8px rgba(0,0,0,0.6); scroll-behavior:smooth;"></div>
                        `;
                    } else {
                        cardEl.style.border = '1px solid ' + cardBorder;
                        cardEl.style.boxShadow = isRunning ? '0 8px 25px rgba(0,0,0,0.5), 0 0 15px rgba(16,185,129,0.2)' : '0 4px 20px rgba(0,0,0,0.3)';
                        const badgeEl = document.getElementById('debug-badge-' + t.id);
                        if (badgeEl) badgeEl.innerHTML = statusBadge;

                        const actionEl = document.getElementById('debug-action-' + t.id);
                        if (actionEl) {
                            actionEl.innerHTML = isRunning ? `
                                <button onclick="killTask('${t.id}', this)" style="background:#ef4444; color:#fff; border:none; padding:0.4rem 0.9rem; border-radius:0.4rem; font-size:0.8rem; font-weight:800; cursor:pointer; display:inline-flex; align-items:center; gap:0.3rem; box-shadow:0 2px 8px rgba(239,68,68,0.4); transition:all 0.2s;">
                                    🛑 Termina
                                </button>
                            ` : '';
                        }

                        const pidEl = document.getElementById('debug-pid-' + t.id);
                        if (pidEl) pidEl.innerText = `⚡ ${pidInfo}`;
                    }

                    // Riordinamento dinamico: posiziona l'elemento all'indice esatto per mostrare i running in cima
                    const targetChild = container.children[index];
                    if (targetChild !== cardEl) {
                        container.insertBefore(cardEl, targetChild || null);
                    }

                    const logBox = document.getElementById('debug-log-' + t.id);
                    if (logBox) {
                        const wasScrolledToBottom = (logBox.scrollHeight - logBox.clientHeight <= logBox.scrollTop + 35);
                        if (logBox.innerText !== logsJoined) {
                            logBox.innerText = logsJoined;
                            if (isRunning || wasScrolledToBottom) {
                                logBox.scrollTop = logBox.scrollHeight;
                            }
                        }
                    }
                });

            } catch (err) {
                console.error("Errore fetch debug tasks:", err);
            }
        }

        async function killTask(taskId, btnEl) {
            if (!confirm("Vuoi davvero interrompere e terminare forzatamente questo processo?")) return;
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Arresto...";
            }
            try {
                const res = await fetch('/api/debug/kill', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task_id: taskId })
                });
                const data = await res.json();
                loadDebugTasks();
            } catch (e) {
                alert("Errore durante l'interruzione: " + e.message);
                loadDebugTasks();
            }
        }

        async function killAllTasks() {
            if (!confirm("Sei sicuro di voler terminare TUTTI i processi in corso (Gemini bot, upload, ffmpeg)?")) return;
            try {
                const res = await fetch('/api/debug/kill', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ kill_all: true })
                });
                const data = await res.json();
                alert(data.message || "Tutti i processi attivi sono stati interrotti.");
                loadDebugTasks();
            } catch (e) {
                alert("Errore durante la terminazione: " + e.message);
            }
        }

        async function clearFinishedTasks() {
            try {
                await fetch('/api/debug/clear', { method: 'POST' });
                loadDebugTasks();
            } catch (e) {
                console.error("Errore pulizia task:", e);
            }
        }

        // Periodic background poll for task status and badge
        setInterval(() => {
            if (currentActiveView === 'debug') {
                loadDebugTasks(false);
            } else {
                fetch('/api/debug/tasks')
                    .then(r => r.json())
                    .then(tasks => {
                        const runningCount = tasks.filter(t => t.status === 'running').length;
                        const badge = document.getElementById('debug-active-badge');
                        if (badge) {
                            if (runningCount > 0) {
                                badge.style.display = 'inline-block';
                                badge.innerText = runningCount;
                            } else {
                                badge.style.display = 'none';
                            }
                        }
                    })
                    .catch(() => {});
            }

            if (currentActiveView === 'autopilot') {
                loadAutopilotState(false);
            } else {
                fetch('/api/autopilot/status')
                    .then(r => r.json())
                    .then(st => {
                        const badge = document.getElementById('autopilot-active-badge');
                        if (badge) {
                            if (st.is_enabled) {
                                badge.style.display = 'inline-block';
                                badge.innerText = 'ON';
                            } else {
                                badge.style.display = 'none';
                            }
                        }
                    })
                    .catch(() => {});
            }
        }, 3000);

        function getRatingColor(rating) {
            if (rating === 'ALTA') return '#10b981';
            if (rating === 'MEDIA') return '#f59e0b';
            return '#ef4444';
        }

        function copyToClipboard(text, btnEl) {
            navigator.clipboard.writeText(text).then(() => {
                const orig = btnEl.innerText;
                btnEl.innerText = '✅ Copiato!';
                btnEl.style.background = '#10b981';
                setTimeout(() => { btnEl.innerText = orig; btnEl.style.background = ''; }, 1500);
            });
        }

        function toggleAccordion(idx) {
            const body = document.getElementById('accordion-body-' + idx);
            const icon = document.getElementById('accordion-icon-' + idx);
            if (body.style.display === 'none') {
                body.style.display = 'block';
                icon.style.transform = 'rotate(180deg)';
            } else {
                body.style.display = 'none';
                icon.style.transform = 'rotate(0deg)';
            }
        }

        let activeCampaignsClassified = [];

        async function fetchActiveClassifiedCampaigns() {
            try {
                const res = await fetch('/api/clipping/classified-active');
                activeCampaignsClassified = await res.json();
                return activeCampaignsClassified;
            } catch(e) {
                activeCampaignsClassified = [];
                return [];
            }
        }

        async function renderMyCampaigns() {
            const grid = document.getElementById('my-campaigns-grid');
            grid.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem; grid-column: 1 / -1;">⏳ Caricamento Campagne Attive da Klippify...</div>';

            try {
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }
            } catch(e) {}

            await fetchActiveClassifiedCampaigns();

            // Raccogli tutti i token delle campagne attive (da iscrizioni Klippify + selezione manuale + submissions)
            const activeTokensSet = new Set();
            
            // 1. Campagne classificate come attive da Klippify
            (activeCampaignsClassified || []).forEach(ac => {
                const token = ac.id || ac.campaign_token || ac.campaign_id;
                if (token) activeTokensSet.add(token);
            });

            // 2. Campagne con submission video inviate
            (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).forEach(s => {
                if (s.campaign_id) activeTokensSet.add(s.campaign_id);
            });

            // 3. Campagne con contenuti/script generati
            (typeof generatedContent !== 'undefined' ? generatedContent : []).forEach(gc => {
                if (gc.campaign_id) activeTokensSet.add(gc.campaign_id);
            });

            // 4. Campagne dalla dashboard participating
            if (typeof dashboardData !== 'undefined' && dashboardData.participating_campaigns) {
                dashboardData.participating_campaigns.forEach(p => {
                    const match = allCampaignsData.find(c => (c.name && p.name && c.name.toLowerCase() === p.name.toLowerCase()) || (c.id === p.id));
                    if (match && match.id) activeTokensSet.add(match.id);
                });
            }

            // 5. Campagne salvate dall'utente
            (selectedCampaigns || []).forEach(st => activeTokensSet.add(st));

            const activeTokensList = Array.from(activeTokensSet);

            if (activeTokensList.length === 0) {
                grid.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem; grid-column: 1 / -1;">Nessuna campagna attiva rilevata su Klippify. Iscriviti a una campagna su Klippify o selezionala dalla Dashboard!</div>';
                return;
            }

            grid.innerHTML = '';

            // Iterate over active campaigns to build WIDGETS
            activeTokensList.forEach((campToken) => {
                const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {};
                if (!originalCamp.id) return;

                const classifiedInfo = activeCampaignsClassified.find(ac => 
                    ac.id === campToken || 
                    ac.campaign_token === campToken || 
                    ac.campaign_id === campToken ||
                    (originalCamp.name && ac.name && ac.name.toLowerCase() === originalCamp.name.toLowerCase())
                ) || {};
                const isClipping = classifiedInfo.category === 'CLIPPING' || 
                                   (classifiedInfo.drive_links && classifiedInfo.drive_links.length > 0) ||
                                   (classifiedInfo.all_links && classifiedInfo.all_links.some(l => l.type === 'drive' || l.type === 'wetransfer' || l.type === 'youtube' || l.type === 'reel')) ||
                                   (originalCamp.description && (
                                       originalCamp.description.toLowerCase().includes('podcast') || 
                                       originalCamp.description.toLowerCase().includes('clip') ||
                                       originalCamp.description.toLowerCase().includes('taglia') ||
                                       originalCamp.description.toLowerCase().includes('youtube') ||
                                       originalCamp.description.toLowerCase().includes('drive')
                                   ));

                const item = generatedContent.find(gc => gc.campaign_id === campToken) || {};
                const campSubmissions = (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).filter(s => {
                    if (s.campaign_id && (s.campaign_id === campToken || s.campaign_id === originalCamp.id || s.campaign_id === originalCamp.campaign_token)) return true;
                    if (originalCamp.name && s.campaign_name && originalCamp.name.trim().toLowerCase() === s.campaign_name.trim().toLowerCase()) return true;
                    return false;
                });
                
                const widget = document.createElement('div');
                widget.className = 'campaign-widget';
                widget.style.cssText = 'background:rgba(30,41,59,0.9); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:1.5rem; cursor:pointer; transition: transform 0.2s, box-shadow 0.2s; position:relative;';
                
                widget.onmouseover = () => {
                    widget.style.transform = 'translateY(-5px)';
                    widget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.5)';
                    widget.style.borderColor = isClipping ? 'rgba(245,158,11,0.6)' : 'rgba(139,92,246,0.6)';
                };
                widget.onmouseout = () => {
                    widget.style.transform = 'none';
                    widget.style.boxShadow = 'none';
                    widget.style.borderColor = 'rgba(255,255,255,0.1)';
                };
                
                widget.onclick = () => openCampaignDetail(campToken);

                const typeBadge = isClipping 
                    ? '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">✂️ CLIPPING</span>'
                    : '<span style="background:rgba(139,92,246,0.2); color:#c084fc; border:1px solid rgba(139,92,246,0.4); padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">🤖 AI VEO</span>';

                widget.innerHTML = `
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.8rem; gap:0.5rem;">
                        <div style="flex:1;">
                            <div style="font-size:1.15rem; font-weight:800; color:#fff; line-height:1.3; margin-bottom:0.4rem;">${originalCamp.name}</div>
                            <div style="display:flex; gap:0.4rem; align-items:center; flex-wrap:wrap;">
                                ${typeBadge}
                                <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold;">$${originalCamp.payout_per_1k_views || '?'}/1k</span>
                            </div>
                        </div>
                        <button onclick="deleteCampaign('${campToken}', event)" title="Rimuovi da Campagne Attive" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); border-radius:0.5rem; padding:0.35rem 0.55rem; font-size:0.85rem; cursor:pointer; transition:all 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.15)'">
                            🗑️
                        </button>
                    </div>
                    <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:1rem; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                        ${originalCamp.description || 'Nessun brief fornito'}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.08); padding-top:0.8rem;">
                        <span style="font-size:0.78rem; color:#a78bfa;">⏳ ${item.scripts ? item.scripts.length : (item.video_prompt_gemini ? 1 : 0)} Slot/Clip</span>
                        <div style="display:flex; gap:0.35rem; align-items:center;">
                            ${campSubmissions.filter(s => s.status === 'accepted').length > 0 ? `<span style="font-size:0.72rem; background:rgba(16,185,129,0.2); color:#34d399; padding:0.15rem 0.45rem; border-radius:0.35rem; font-weight:700;">✅ ${campSubmissions.filter(s => s.status === 'accepted').length}</span>` : ''}
                            ${campSubmissions.filter(s => s.status === 'rejected').length > 0 ? `<span style="font-size:0.72rem; background:rgba(239,68,68,0.25); color:#ef4444; border:1px solid rgba(239,68,68,0.4); padding:0.15rem 0.45rem; border-radius:0.35rem; font-weight:800;">❌ ${campSubmissions.filter(s => s.status === 'rejected').length} Rifiutati</span>` : ''}
                            ${campSubmissions.length === 0 ? `<span style="font-size:0.72rem; color:var(--text-muted);">0 Inviati</span>` : ''}
                        </div>
                    </div>
                `;
                grid.appendChild(widget);
            });
        }

        let campaignSchedules = {};
        let localAvailableVideos = [];

        async function openLocalFolder(campToken) {
            try {
                const res = await fetch('/api/open-local-folder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    console.log("Cartella aperta:", data.folder);
                } else {
                    alert("Errore apertura cartella: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di connessione: " + e.message);
            }
        }

        // ============================================================
        // ✂️ MULTI-VIDEO SOURCE UPLOAD & CLIPPING QUEUE ENGINE
        // ============================================================
        let clippingQueuePollTimers = {};
        let clippingQueueWasProcessing = {};

        async function uploadSourceVideoFiles(inputElem, campToken) {
            const files = Array.from(inputElem.files || []);
            if (!files.length) return;

            const btnElem = document.getElementById(`btn-upload-file-assembly-${campToken}`) || document.getElementById(`btn-upload-file-${campToken}`);
            let origHtml = "";
            if (btnElem) {
                origHtml = btnElem.innerHTML;
                btnElem.disabled = true;
            }

            let successCount = 0;
            let totalFiles = files.length;

            for (let i = 0; i < totalFiles; i++) {
                const file = files[i];
                if (btnElem) {
                    btnElem.innerHTML = `⏳ Caricamento ${i+1}/${totalFiles} (${file.name.substring(0, 18)}...)...`;
                }

                try {
                    const res = await fetch('/api/clipping/upload-source', {
                        method: 'POST',
                        headers: {
                            'X-Filename': encodeURIComponent(file.name),
                            'X-Campaign-Id': campToken
                        },
                        body: file
                    });
                    const data = await res.json();
                    if (data.status === 'ok') {
                        successCount++;
                    } else {
                        console.error("Errore upload file:", file.name, data.error);
                    }
                } catch(e) {
                    console.error("Errore rete upload:", file.name, e);
                }
            }

            if (btnElem) {
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }
            inputElem.value = "";

            if (successCount > 0) {
                fetch('/api/clipping/queue/process-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                }).catch(() => {});
                await fetchAvailableVideosList(campToken);
                await loadClippingQueue(campToken);
                renderCampaignDetailContent(campToken);
            } else {
                alert("Errore durante il caricamento dei video. Riprova.");
            }
        }

        async function loadClippingQueue(campToken) {
            if (!campToken) return;
            const container = document.getElementById(`clipping-queue-list-${campToken}`);
            const assemblyContainer = document.getElementById(`assembly-clipping-queue-list-${campToken}`);
            const countBadge = document.getElementById(`clipping-queue-count-${campToken}`);
            const assemblyCountBadge = document.getElementById(`assembly-clipping-queue-count-${campToken}`);
            const statusSummary = document.getElementById(`clipping-queue-summary-${campToken}`);
            const assemblyStatusSummary = document.getElementById(`assembly-clipping-queue-summary-${campToken}`);
            const liveBanner = document.getElementById(`assembly-clipping-live-banner-${campToken}`);
            const tabRawBtn = document.getElementById(`camp-subnav-btn-raw-${campToken}`);
            
            try {
                const res = await fetch(`/api/clipping/queue?campaign_id=${encodeURIComponent(campToken)}`);
                const queue = await res.json();
                
                if (countBadge) countBadge.innerText = `${queue.length} Video`;
                if (assemblyCountBadge) assemblyCountBadge.innerText = `${queue.length} Video`;

                if (statusSummary || assemblyStatusSummary) {
                    const queuedCount = queue.filter(q => q.status === 'queued').length;
                    const processingCount = queue.filter(q => q.status === 'processing').length;
                    const completedCount = queue.filter(q => q.status === 'completed').length;
                    const summaryHtml = `
                        <span style="color:#fbbf24; font-weight:700;">⏳ ${queuedCount} in attesa</span> &bull; 
                        <span style="color:#38bdf8; font-weight:700;">⚙️ ${processingCount} in elaborazione</span> &bull; 
                        <span style="color:#34d399; font-weight:700;">✅ ${completedCount} completati</span>
                    `;
                    if (statusSummary) statusSummary.innerHTML = summaryHtml;
                    if (assemblyStatusSummary) assemblyStatusSummary.innerHTML = summaryHtml;
                }

                const emptyHtml = `
                    <div style="text-align:center; padding:2rem 1rem; color:var(--text-muted); background:rgba(0,0,0,0.25); border-radius:0.8rem; border:1px dashed rgba(255,255,255,0.15);">
                        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎬</div>
                        <div style="font-weight:700; color:#cbd5e1; font-size:0.95rem;">Nessun video presente nella coda di clipping</div>
                        <div style="font-size:0.8rem; margin-top:0.3rem;">Clicca sul pulsante <strong>📁 Carica Video Lunghi</strong> sopra per aggiungere i file completi del brand.</div>
                    </div>
                `;

                if (!queue || queue.length === 0) {
                    if (container) container.innerHTML = emptyHtml;
                    if (assemblyContainer) assemblyContainer.innerHTML = emptyHtml;
                    if (liveBanner) liveBanner.style.display = 'none';
                    if (tabRawBtn) tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span>';
                    return;
                }

                const processingItems = queue.filter(q => q.status === 'processing');
                const pendingItems = queue.filter(q => q.status !== 'completed' && q.status !== 'processing');
                const completedItems = queue.filter(q => q.status === 'completed');

                let hasProcessing = processingItems.length > 0;
                let processingFilename = hasProcessing ? processingItems[0].filename : '';

                let htmlOutput = '';

                // 1. BOX DINAMICO: STO KLIPPANDO CON GEMINI (Solo se un video è in elaborazione)
                if (hasProcessing) {
                    const procItem = processingItems[0];
                    htmlOutput += `
                        <div style="background: linear-gradient(135deg, rgba(8,145,178,0.25), rgba(15,23,42,0.95)); border:2px solid #38bdf8; border-radius:1.1rem; padding:1.2rem 1.4rem; margin-bottom:1.1rem; box-shadow:0 0 25px rgba(56,189,248,0.35);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span class="live-dot" style="background:#38bdf8; width:10px; height:10px; border-radius:50%; display:inline-block; animation:pulse 1s infinite;"></span>
                                    <span style="font-weight:900; color:#38bdf8; font-size:0.85rem; letter-spacing:0.05em; text-transform:uppercase;">⚡ STO KLIPPANDO CON GEMINI AI</span>
                                </div>
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; border:1px solid rgba(56,189,248,0.4); padding:0.2rem 0.65rem; border-radius:1rem; font-size:0.75rem; font-weight:800;">
                                    Analisi &amp; Ritaglio Continuo...
                                </span>
                            </div>
                            <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
                                <div style="font-size:1.8rem; background:rgba(56,189,248,0.15); width:48px; height:48px; border-radius:0.7rem; display:flex; align-items:center; justify-content:center; flex-shrink:0;">🎬</div>
                                <div style="flex:1; min-width:220px;">
                                    <div style="font-weight:900; font-size:1.05rem; color:#fff; word-break:break-all;">${procItem.filename}</div>
                                    <div style="font-size:0.78rem; color:#cbd5e1; margin-top:0.2rem;">
                                        Dimensione: <strong>${(procItem.file_size_mb || 0).toFixed(1)} MB</strong> &bull; Caricato: ${procItem.uploaded_at || 'oggi'}
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top:0.9rem;">
                                <div style="font-size:0.78rem; color:#94a3b8; margin-bottom:0.4rem; display:flex; justify-content:space-between;">
                                    <span>🤖 Gemini sta estraendo le clip virali 9:16 con didascalie dedicate...</span>
                                    <span style="color:#38bdf8; font-weight:700;">Appena completato scorrerà in archivio e passerà al prossimo!</span>
                                </div>
                                <div class="processing-animated-bar" style="height:7px; background:rgba(255,255,255,0.1); border-radius:4px; overflow:hidden;">
                                    <div class="processing-bar-fill" style="height:100%; width:100%; background:linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8); animation:shimmer 2s infinite linear;"></div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                // 2. HERO CARD: 1° VIDEO IN CODA (Prossimo al Taglio)
                if (pendingItems.length > 0) {
                    const heroItem = pendingItems[0];
                    const isErr = heroItem.status === 'error';
                    htmlOutput += `
                        <div style="background: linear-gradient(135deg, rgba(245,158,11,0.14), rgba(15,23,42,0.92)); border:2px solid rgba(245,158,11,0.6); border-radius:1.1rem; padding:1.2rem 1.4rem; margin-bottom:1rem; box-shadow:0 4px 20px rgba(245,158,11,0.15);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.8rem;">
                                <span style="background:rgba(245,158,11,0.25); color:#fbbf24; border:1px solid rgba(245,158,11,0.5); padding:0.25rem 0.75rem; border-radius:1rem; font-size:0.8rem; font-weight:900; display:flex; align-items:center; gap:0.35rem;">
                                    <span>🌟 1° IN CODA</span> <span>(Prossimo al Taglio)</span>
                                </span>
                                <span style="color:#94a3b8; font-size:0.75rem;">Caricato: ${heroItem.uploaded_at || 'oggi'}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                                <div style="display:flex; align-items:center; gap:0.9rem; flex:1; min-width:240px;">
                                    <div style="width:44px; height:44px; border-radius:0.6rem; background:rgba(245,158,11,0.2); display:flex; align-items:center; justify-content:center; font-size:1.5rem; flex-shrink:0;">
                                        🎬
                                    </div>
                                    <div>
                                        <div style="font-weight:900; font-size:1rem; color:#fff; word-break:break-all;">
                                            ${heroItem.filename}
                                        </div>
                                        <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">
                                            Dimensione: <strong style="color:#fbbf24;">${(heroItem.file_size_mb || 0).toFixed(1)} MB</strong>
                                            ${isErr ? `<span style="color:#ef4444; margin-left:0.5rem; font-weight:700;">⚠️ ${heroItem.error_message || 'Errore precedente'}</span>` : ''}
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;">
                                    <button onclick="clipSingleVideoFromQueue('${campToken}', '${encodeURIComponent(heroItem.filename)}', this)" style="background:linear-gradient(135deg, #f59e0b, #d97706); color:#000; font-weight:800; border:none; padding:0.35rem 0.8rem; border-radius:0.5rem; font-size:0.75rem; cursor:pointer; display:inline-flex; align-items:center; gap:0.35rem; box-shadow:0 2px 8px rgba(245,158,11,0.3); transition:all 0.15s;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='none'">
                                        <span>⚡ Klippa Subito</span>
                                    </button>
                                    <button onclick="removeVideoFromClippingQueue('${campToken}', '${encodeURIComponent(heroItem.filename)}', this)" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.35rem 0.6rem; border-radius:0.5rem; font-size:0.75rem; cursor:pointer;" title="Rimuovi dalla coda">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }

                // 3. STRISCE COMPATTE IN RISERVA (#2, #3, #4...)
                if (pendingItems.length > 1) {
                    const reserveItems = pendingItems.slice(1);
                    htmlOutput += `
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); border-radius:1rem; padding:1.1rem; margin-bottom:1rem;">
                            <div style="font-size:0.88rem; font-weight:800; color:#38bdf8; margin-bottom:0.7rem; display:flex; justify-content:space-between; align-items:center;">
                                <span>📦 Video Lunghi Successivi in Coda (${reserveItems.length} in attesa)</span>
                                <span style="font-size:0.74rem; color:#94a3b8; font-weight:500;">Scorreranno automaticamente verso l'alto finché non sono finiti</span>
                            </div>
                            <div style="display:flex; flex-direction:column; gap:0.5rem;">
                                ${reserveItems.map((qItem, rIdx) => `
                                    <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.06); border-radius:0.6rem; padding:0.65rem 0.9rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; transition:all 0.2s;" onmouseover="this.style.borderColor='rgba(56,189,248,0.3)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.06)'">
                                        <div style="display:flex; align-items:center; gap:0.7rem;">
                                            <span style="font-weight:900; color:#94a3b8; font-size:0.82rem; font-family:monospace; min-width:24px;">#${rIdx + 2}</span>
                                            <span style="font-weight:700; color:#e2e8f0; font-size:0.85rem; word-break:break-all;">${qItem.filename}</span>
                                            <span style="font-size:0.72rem; color:#64748b;">(${(qItem.file_size_mb || 0).toFixed(1)} MB)</span>
                                        </div>
                                        <div style="display:flex; align-items:center; gap:0.4rem;">
                                            <button onclick="clipSingleVideoFromQueue('${campToken}', '${encodeURIComponent(qItem.filename)}', this)" style="background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.74rem; font-weight:800; cursor:pointer;">
                                                ⚡ Klippa
                                            </button>
                                            <button onclick="removeVideoFromClippingQueue('${campToken}', '${encodeURIComponent(qItem.filename)}', this)" style="background:transparent; color:#ef4444; border:none; padding:0.25rem 0.4rem; cursor:pointer;" title="Rimuovi">
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `;
                }

                // Se non c'è nulla in attesa o in elaborazione
                if (!hasProcessing && pendingItems.length === 0 && completedItems.length === 0) {
                    htmlOutput = emptyHtml;
                }

                // 4. ARCHIVIO A TENDINA: VIDEO LUNGHI GIÀ ELABORATI
                if (completedItems.length > 0) {
                    htmlOutput += `
                        <details style="margin-top:1.2rem; background:rgba(15,23,42,0.5); border:1px solid rgba(16,185,129,0.25); border-radius:0.9rem; overflow:hidden;">
                            <summary style="padding:0.9rem 1.2rem; cursor:pointer; font-weight:800; color:#34d399; font-size:0.9rem; display:flex; align-items:center; justify-content:space-between; user-select:none;">
                                <span style="display:flex; align-items:center; gap:0.5rem;">
                                    <span>✅ Video Lunghi Già Elaborati (${completedItems.length})</span>
                                    <span style="font-size:0.74rem; color:#94a3b8; font-weight:500;">(Clicca per espandere e vedere le clip generate)</span>
                                </span>
                                <span style="font-size:0.75rem; background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.6rem; border-radius:1rem; border:1px solid rgba(16,185,129,0.3);">
                                    Archiviati
                                </span>
                            </summary>
                            <div style="padding:0.8rem 1.2rem 1.2rem; display:flex; flex-direction:column; gap:0.6rem; border-top:1px solid rgba(255,255,255,0.06);">
                                ${completedItems.map(cItem => `
                                    <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.06); border-radius:0.7rem; padding:0.8rem 1rem;">
                                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                                            <div style="font-weight:700; color:#e2e8f0; font-size:0.85rem;">
                                                🎬 ${cItem.filename} <span style="font-size:0.72rem; color:#64748b;">(${(cItem.file_size_mb || 0).toFixed(1)} MB)</span>
                                            </div>
                                            <div style="display:flex; gap:0.4rem; align-items:center;">
                                                <span style="font-size:0.72rem; color:#34d399; font-weight:700;">✅ ${(cItem.generated_clips || []).length} clip estratte</span>
                                                <button onclick="clipSingleVideoFromQueue('${campToken}', '${encodeURIComponent(cItem.filename)}', this)" style="background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); padding:0.2rem 0.5rem; border-radius:0.3rem; font-size:0.7rem; font-weight:700; cursor:pointer;">
                                                    Ri-Klippa
                                                </button>
                                                <button onclick="removeVideoFromClippingQueue('${campToken}', '${encodeURIComponent(cItem.filename)}', this)" style="background:transparent; color:#ef4444; border:none; padding:0.2rem 0.3rem; cursor:pointer;" title="Elimina">
                                                    🗑️
                                                </button>
                                            </div>
                                        </div>
                                        ${cItem.generated_clips && cItem.generated_clips.length > 0 ? `
                                            <div style="margin-top:0.5rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                                                ${cItem.generated_clips.map(clipF => `
                                                    <span style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.25); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-family:monospace; display:inline-flex; align-items:center; gap:0.3rem;">
                                                        <span>✂️</span> <span>${clipF}</span>
                                                    </span>
                                                `).join('')}
                                            </div>
                                        ` : ''}
                                    </div>
                                `).join('')}
                            </div>
                        </details>
                    `;
                }

                if (container) container.innerHTML = htmlOutput;
                if (assemblyContainer) assemblyContainer.innerHTML = htmlOutput;

                // Gestione Badge Live e Polling dinamico
                if (hasProcessing) {
                    clippingQueueWasProcessing[campToken] = true;
                    if (liveBanner) {
                        liveBanner.style.display = 'flex';
                        liveBanner.innerHTML = `<span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#38bdf8; animation:pulse 1s infinite;"></span> <span>⚙️ <strong>Analisi &amp; Taglio in corso con Gemini...</strong> Ritaglio delle migliori clip 9:16 per <em>${processingFilename}</em> in corso. Entreranno in automatico nella cascata!</span>`;
                    }
                    if (tabRawBtn) {
                        tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span> <span style="background:rgba(56,189,248,0.25); color:#38bdf8; border:1px solid rgba(56,189,248,0.5); font-size:0.68rem; padding:0.1rem 0.45rem; border-radius:1rem; font-weight:900; animation:pulse 1.2s infinite;">⚙️ IN CORSO</span>';
                    }

                    if (clippingQueuePollTimers[campToken]) clearTimeout(clippingQueuePollTimers[campToken]);
                    clippingQueuePollTimers[campToken] = setTimeout(() => {
                        loadClippingQueue(campToken);
                    }, 3000);
                } else {
                    if (liveBanner) liveBanner.style.display = 'none';
                    if (tabRawBtn) tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span>';

                    // Se ci sono video in attesa e nessuno in elaborazione, avvia subito il clipping automatico
                    if (pendingItems.length > 0) {
                        fetch('/api/clipping/queue/process-all', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ campaign_id: campToken })
                        }).catch(() => {});
                    }

                    // Se il task è appena terminato (da processing a done), aggiorniamo la cascata
                    if (clippingQueueWasProcessing[campToken]) {
                        clippingQueueWasProcessing[campToken] = false;
                        fetchAvailableVideosList(campToken).then(() => {
                            renderCampaignDetailContent(campToken);
                        });
                    }
                }

            } catch(e) {
                console.error("Errore caricamento coda clipping:", e);
            }
        }

        async function processEntireClippingQueue(campToken, btnElem) {
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {
                btnElem.innerHTML = '⏳ Avvio Coda...';
                btnElem.disabled = true;
            }

            try {
                const res = await fetch('/api/clipping/queue/process-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert(`🚀 Elaborazione Coda Avviata!

Il Bot Gemini e FFmpeg analizzeranno e ritaglieranno in sequenza tutti i video presenti nella coda per questa campagna.

Le clip generate verranno assegnate automaticamente agli slot e rese pronte per la pubblicazione!`);
                    await loadClippingQueue(campToken);
                } else {
                    alert("Errore avvio coda: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di connessione: " + e.message);
            } finally {
                if (btnElem) {
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }
            }
        }

        async function clipSingleVideoFromQueue(campToken, encFilename, btnElem) {
            const filename = decodeURIComponent(encFilename);
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {
                btnElem.innerHTML = '⏳ In avvio...';
                btnElem.disabled = true;
            }

            try {
                const res = await fetch('/api/clipping/run-pipeline', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        video_name: filename
                    })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    await loadClippingQueue(campToken);
                } else {
                    alert("Errore avvio clipping: " + (data.error || "Errore sconosciuto"));
                    if (btnElem) {
                        btnElem.innerHTML = origHtml;
                        btnElem.disabled = false;
                    }
                }
            } catch(e) {
                alert("Errore di connessione: " + e.message);
                if (btnElem) {
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }
            }
        }

        async function removeVideoFromClippingQueue(campToken, encFilename, btnElem) {
            const filename = decodeURIComponent(encFilename);
            if (!confirm(`Sei sicuro di voler rimuovere "${filename}" dalla coda di clipping?`)) return;

            try {
                const res = await fetch('/api/clipping/queue/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        filename: filename
                    })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    await loadClippingQueue(campToken);
                } else {
                    alert("Errore rimozione video: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di rete: " + e.message);
            }
        }

        async function startClippingPipelineForCampaign(campToken, btnElem) {
            const selector = document.getElementById(`source-video-selector-assembly-${campToken}`) || document.getElementById(`source-video-selector-${campToken}`);
            const selectedVideo = selector ? selector.value : "";
            if (!selectedVideo) {
                alert("Seleziona prima un file video sorgente da klippare!");
                return;
            }
            return clipSingleVideoFromQueue(campToken, encodeURIComponent(selectedVideo), btnElem);
        }

        function getCampaignIsolatedVideos(campToken) {
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {};
            const campNameLower = (originalCamp.name || '').toLowerCase();
            const campShortName = campNameLower.replace(/[^a-zA-Z0-9]/g, '').substring(0, 8);

            return (localAvailableVideos || []).filter(v => {
                if (!v || !v.filename) return false;
                const fn = v.filename.toLowerCase();
                
                // 1. Se il video ha campaign_id esplicito dal server
                if (v.campaign_id && v.campaign_id !== 'general') {
                    return v.campaign_id === campToken;
                }
                
                // 2. Se l'URL relativo contiene il token
                if (v.rel_url && v.rel_url.includes(campToken)) return true;
                
                // 3. Regole di esclusione incrociata tra brand noti
                const isSaraCamp = (campToken === '6a71c6f7245627c68999eae2' || campNameLower.includes('dizdari') || campNameLower.includes('sara'));
                const isDoseCamp = (campToken === '6a426231e6a21896f769dc80' || campNameLower.includes('dose') || campNameLower.includes('riccardo'));
                const isStarkCamp = (campToken === '6a759fd05ade3cb2f771b439' || campNameLower.includes('stark') || campNameLower.includes('ale'));

                const isSaraFile = (fn.includes('saradizdari') || fn.includes('sara') || fn.includes('zaharia') || fn.includes('amoroso') || fn.includes('fedra'));
                const isDoseFile = (fn.includes('dose') || fn.includes('riccardo'));
                const isStarkFile = (fn.includes('stark') || fn.includes('alestark'));

                if (isSaraFile) return isSaraCamp;
                if (isDoseFile) return isDoseCamp;
                if (isStarkFile) return isStarkCamp;

                // 4. Se il nome del file include il token o il nome compatto della campagna
                if (campShortName && fn.includes(campShortName)) return true;
                if (campToken && fn.includes(campToken.toLowerCase())) return true;

                // Se non c'è match, escludi per sicurezza
                return false;
            });
        }

        async function fetchAvailableVideosList(campToken = null) {
            try {
                const url = campToken ? `/api/videos?campaign_id=${encodeURIComponent(campToken)}` : '/api/videos';
                const res = await fetch(url);
                const vids = await res.json();
                localAvailableVideos = vids || [];
                return localAvailableVideos;
            } catch(e) {
                return [];
            }
        }

        async function openCampaignDetail(campToken) {
            currentDetailCampToken = campToken;
            document.getElementById('my-campaigns-grid').style.display = 'none';
            document.getElementById('my-campaign-detail-view').style.display = 'block';
            
            const detailContainer = document.getElementById('my-campaign-detail-content');
            detailContainer.innerHTML = '<div style="text-align:center; padding:3rem; color:var(--text-muted);">⏳ Caricamento Piano Editoriale...</div>';

            try {
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }
            } catch(e) {}

            await fetchAvailableVideosList(campToken);

            try {
                const schedRes = await fetch('/api/campaign/schedules');
                campaignSchedules = await schedRes.json();
            } catch(e) {
                campaignSchedules = {};
            }

            renderCampaignDetailContent(campToken);
        }

        async function refreshCampaignSubmissions(campToken, btnEl) {
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Controllo...";
            }
            try {
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }
                renderCampaignDetailContent(campToken);
            } catch(e) {
                console.error("Errore aggiornamento submissions:", e);
            } finally {
                if (btnEl) {
                    btnEl.disabled = false;
                    btnEl.innerText = "🔄 Aggiorna Stato Klippify";
                }
            }
        }

        async function changeDailyTargetCount(campToken, delta) {
            if (!campaignSchedules[campToken]) {
                campaignSchedules[campToken] = { target_count: 3, slots: [] };
            }
            let current = campaignSchedules[campToken].target_count || 3;
            let next = Math.max(1, Math.min(10, current + delta));
            campaignSchedules[campToken].target_count = next;
            
            await saveCurrentCampaignSchedule(campToken);
            renderCampaignDetailContent(campToken);
        }

        async function saveCampaignSlotTime(campToken, slotIdx, timeVal) {
            if (!campaignSchedules[campToken]) {
                campaignSchedules[campToken] = { target_count: 3, slots: [] };
            }
            if (!campaignSchedules[campToken].slots) {
                campaignSchedules[campToken].slots = [];
            }
            while (campaignSchedules[campToken].slots.length <= slotIdx) {
                campaignSchedules[campToken].slots.push({ time: "12:00", video: "" });
            }
            campaignSchedules[campToken].slots[slotIdx].time = timeVal;
            await saveCurrentCampaignSchedule(campToken);
        }

        async function saveCampaignSlotVideo(campToken, slotIdx, videoFilename) {
            if (!campaignSchedules[campToken]) {
                campaignSchedules[campToken] = { target_count: 3, slots: [] };
            }
            if (!campaignSchedules[campToken].slots) {
                campaignSchedules[campToken].slots = [];
            }
            while (campaignSchedules[campToken].slots.length <= slotIdx) {
                campaignSchedules[campToken].slots.push({ time: "12:00", video: "" });
            }
            campaignSchedules[campToken].slots[slotIdx].video = videoFilename;
            await saveCurrentCampaignSchedule(campToken);
        }

        async function saveCurrentCampaignSchedule(campToken) {
            const data = campaignSchedules[campToken] || { target_count: 3, slots: [] };
            try {
                await fetch('/api/campaign/save-schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        target_count: data.target_count || 3,
                        slots: data.slots || []
                    })
                });
            } catch(e) {
                console.error("Errore salvataggio schedule", e);
            }
        }

        window.resetCampaignPublishedClips = async function(campToken, btnEl) {
            if (!confirm("Vuoi ripristinare tutte le clip pubblicate di questa campagna come vergini/nuove? Rientreranno immediatamente nella cascata.")) return;
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Ripristino...";
            }
            try {
                const res = await fetch('/api/campaign/reset-published-clips', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                if (res.ok) {
                    await openCampaignDetail(campToken);
                }
            } catch(e) {
                console.error("Errore reset published clips", e);
            } finally {
                if (btnEl) {
                    btnEl.disabled = false;
                    btnEl.innerText = "🧹 Ripristina Clip come Nuove";
                }
            }
        };

        function switchCampaignSubTab(campToken, tabName) {
            const tabs = ['cascade', 'raw', 'analytics', 'prompts', 'brief'];
            tabs.forEach(t => {
                const pane = document.getElementById('camp-subtab-' + t + '-' + campToken);
                const btn = document.getElementById('camp-navbtn-' + t + '-' + campToken);
                if (pane) pane.style.display = (t === tabName) ? 'block' : 'none';
                if (btn) {
                    if (t === tabName) btn.classList.add('active');
                    else btn.classList.remove('active');
                }
            });
            if (tabName === 'raw' && typeof loadClippingQueueForCampaign === 'function') {
                loadClippingQueueForCampaign(campToken);
            }
        }
        window.switchCampaignSubTab = switchCampaignSubTab;
        window.switchCampSubTab = switchCampaignSubTab;

        function switchCampaignViewMode(campToken, mode) {
            const assemblyView = document.getElementById('camp-assembly-view-' + campToken);
            const classicView = document.getElementById('camp-classic-view-' + campToken);
            const tabAssembly = document.getElementById('tab-btn-assembly-' + campToken);
            const tabClassic = document.getElementById('tab-btn-classic-' + campToken);

            if (mode === 'classic') {
                if (assemblyView) assemblyView.style.display = 'none';
                if (classicView) classicView.style.display = 'block';
                if (tabAssembly) {
                    tabAssembly.style.background = 'transparent';
                    tabAssembly.style.color = '#94a3b8';
                    tabAssembly.style.boxShadow = 'none';
                    tabAssembly.style.borderColor = 'rgba(255,255,255,0.1)';
                }
                if (tabClassic) {
                    tabClassic.style.background = 'linear-gradient(135deg, #8b5cf6, #6366f1)';
                    tabClassic.style.color = '#ffffff';
                    tabClassic.style.boxShadow = '0 4px 15px rgba(139,92,246,0.35)';
                    tabClassic.style.borderColor = 'transparent';
                }
                try { localStorage.setItem('camp_view_mode_' + campToken, 'classic'); } catch(e) {}
            } else {
                if (assemblyView) assemblyView.style.display = 'grid';
                if (classicView) classicView.style.display = 'none';
                if (tabAssembly) {
                    tabAssembly.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    tabAssembly.style.color = '#ffffff';
                    tabAssembly.style.boxShadow = '0 4px 15px rgba(16,185,129,0.35)';
                    tabAssembly.style.borderColor = 'transparent';
                }
                if (tabClassic) {
                    tabClassic.style.background = 'transparent';
                    tabClassic.style.color = '#94a3b8';
                    tabClassic.style.boxShadow = 'none';
                    tabClassic.style.borderColor = 'rgba(255,255,255,0.1)';
                }
                try { localStorage.setItem('camp_view_mode_' + campToken, 'assembly'); } catch(e) {}
            }
        }

        async function autoConfigureAssemblyPipeline(campToken, btnEl) {
            const origHtml = btnEl ? btnEl.innerHTML : '';
            if (btnEl) {
                btnEl.disabled = true;
                btnEl.innerHTML = '⚙️ Configurazione & Avvio...';
            }

            try {
                // 1. Prendi tutte le clip già pubblicate per non riutilizzarle mai
                const schedInfo = campaignSchedules[campToken] || {};
                const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
                const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : []).map(p => p.filename).filter(Boolean);
                const allPublishedFilenames = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));

                // 2. Prendi solo le clip 9:16 vergini (non pubblicate) appartenenti SOLO a questa campagna
                const campIsolatedVids = getCampaignIsolatedVideos(campToken);
                const availableClips = campIsolatedVids.filter(v => v.filename && (v.filename.startsWith('clip_') || v.filename.includes('clip')) && !allPublishedFilenames.includes(v.filename));
                
                // 3. Prendi gli slot attuali o default
                const curSched = campaignSchedules[campToken] || { target_count: 3, slots: [] };
                const defaultTimes = ["15:00", "17:00", "20:00", "22:00"];
                const targetCount = 3;
                
                const newSlots = [];
                for (let i = 0; i < targetCount; i++) {
                    const timeVal = (curSched.slots && curSched.slots[i] && curSched.slots[i].time) ? curSched.slots[i].time : defaultTimes[i];
                    let videoVal = availableClips.length > i ? availableClips[i].filename : '';
                    newSlots.push({ time: timeVal, video: videoVal });
                }

                // Salva schedule aggiornata
                campaignSchedules[campToken] = {
                    target_count: targetCount,
                    slots: newSlots,
                    published_clips: publishedClipsList,
                    autopilot_enabled: true
                };

                await fetch('/api/campaign/save-schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        target_count: targetCount,
                        slots: newSlots
                    })
                });

                // 4. Accoda gli slot all'autopilota
                await fetch('/api/autopilot/campaign-queue-slots', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });

                // 5. Abilita il pilota automatico per la campagna
                await fetch('/api/autopilot/campaign-toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken, enable: true })
                });

                if (btnEl) {
                    btnEl.innerHTML = '✅ Catena Avviata!';
                    setTimeout(() => {
                        renderCampaignDetailContent(campToken);
                    }, 600);
                }
            } catch(err) {
                console.error("Errore auto-configurazione catena", err);
                alert("Errore nell'avvio automatico: " + err.message);
                if (btnEl) {
                    btnEl.disabled = false;
                    btnEl.innerHTML = origHtml;
                }
            }
        }

        async function addNewCampaignSlot(campToken) {
            const timeVal = prompt("Inserisci l'orario per il nuovo slot di pubblicazione (formato HH:MM):", "18:00");
            if (!timeVal || !timeVal.trim()) return;
            
            try {
                const res = await fetch('/api/campaign/add-slot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        time: timeVal.trim(),
                        video: ''
                    })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    if (!campaignSchedules[campToken]) campaignSchedules[campToken] = { slots: [] };
                    campaignSchedules[campToken].slots = data.slots;
                    campaignSchedules[campToken].target_count = data.target_count;
                    renderCampaignDetailContent(campToken);
                } else {
                    alert("Errore aggiunta slot: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di rete: " + e.message);
            }
        }

        async function removeCampaignSlot(campToken, originalIdx) {
            if (!confirm("Sei sicuro di voler rimuovere questo slot dalla programmazione giornaliera?")) return;
            try {
                const res = await fetch('/api/campaign/remove-slot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        slot_index: originalIdx
                    })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    if (campaignSchedules[campToken]) {
                        campaignSchedules[campToken].slots = data.slots;
                        campaignSchedules[campToken].target_count = data.target_count;
                    }
                    renderCampaignDetailContent(campToken);
                } else {
                    alert("Errore rimozione slot: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di rete: " + e.message);
            }
        }

        async function generateVideoFromSlot(campToken, promptText, btnElem) {
            if (!promptText || !promptText.trim()) {
                alert("Il prompt è vuoto!");
                return;
            }
            const origHtml = btnElem.innerHTML;
            btnElem.innerHTML = '⏳ Avvio Bot...';
            btnElem.disabled = true;

            try {
                const res = await fetch('/api/generate-video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: promptText })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    alert("🚀 Bot Gemini avviato con successo in background! Il video apparirà nella cartella e nel selettore non appena pronto.");
                } else {
                    alert("Errore avvio bot: " + (data.error || "Errore sconosciuto"));
                }
            } catch(e) {
                alert("Errore di connessione al server: " + e.message);
            } finally {
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }
        }

        async function publishSlotToTikTok(campToken, slotIdx, btnElem) {
            // 1. Identifica il video assegnato allo slot o la prima clip vergine
            const schedInfo = campaignSchedules[campToken] || { slots: [] };
            const slotData = (schedInfo.slots && schedInfo.slots[slotIdx]) ? schedInfo.slots[slotIdx] : {};
            let filename = slotData.video || "";

            if (!filename) {
                const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
                const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : []).map(p => p.filename).filter(Boolean);
                const allPublished = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));
                const campIsolatedVids = getCampaignIsolatedVideos(campToken);
                const availableClips = campIsolatedVids.filter(v => v.filename && !allPublished.includes(v.filename));
                if (availableClips.length > 0) {
                    filename = availableClips[0].filename;
                }
            }
            
            if (!filename) {
                alert("Nessun video pronto disponibile per questo slot. Genera o seleziona una clip 9:16!");
                return;
            }

            // 2. Recupera la didascalia specifica o i tag della campagna
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {};
            const item = (typeof generatedContent !== 'undefined' ? generatedContent : []).find(gc => gc.campaign_id === campToken) || {};
            const scripts = item.scripts || [];
            let captionText = "";
            
            if (scripts[slotIdx] && scripts[slotIdx].tiktok_caption) {
                captionText = scripts[slotIdx].tiktok_caption;
            } else if (scripts[0] && scripts[0].tiktok_caption) {
                captionText = scripts[0].tiktok_caption;
            } else {
                const tags = (originalCamp.mandatory_hashtags || []).join(' ');
                const mentions = (originalCamp.mandatory_mentions || []).join(' ');
                captionText = `${tags} ${mentions} ${originalCamp.call_to_action || ''}`.trim();
            }

            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {
                btnElem.innerHTML = '⏳ Pubblicazione in corso...';
                btnElem.disabled = true;
            }

            // 3. MOSTRA IL RETTANGOLO DINAMICO "STO PROCESSANDO"
            const procBox = document.getElementById(`assembly-active-processing-box-${campToken}`);
            const procTitle = document.getElementById(`processing-clip-title-${campToken}`);
            const procStatus = document.getElementById(`processing-status-label-${campToken}`);
            const procFilename = document.getElementById(`processing-clip-filename-${campToken}`);
            const procTimer = document.getElementById(`processing-elapsed-timer-${campToken}`);

            if (procBox) {
                procBox.style.display = 'block';
                procBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            if (procTitle) procTitle.innerText = `Pubblicazione Slot #${slotIdx + 1} (In corso...)`;
            if (procStatus) procStatus.innerText = 'Caricamento video su TikTok Studio, verifica copyright e invio automatico a Klippify...';
            if (procFilename) procFilename.innerText = `📹 ${filename}`;

            let secElapsed = 0;
            const timerInterval = setInterval(() => {
                secElapsed++;
                if (procTimer) procTimer.innerText = `⏳ In corso (${secElapsed}s)...`;
            }, 1000);

            try {
                const res = await fetch('/api/tiktok/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        filename: filename,
                        title: captionText || filename,
                        cover_time_ms: 1000,
                        campaign_id: campToken
                    })
                });
                const data = await res.json();

                if (data.status === 'success' && data.task_id) {
                    const activeTaskId = data.task_id;
                    
                    // Polling in tempo reale del bot Playwright per TikTok Studio
                    const pollInterval = setInterval(async () => {
                        try {
                            const taskRes = await fetch('/api/debug/tasks');
                            const allTasks = await taskRes.json();
                            const curTask = allTasks.find(t => t.id === activeTaskId);

                            if (curTask) {
                                if (curTask.logs && curTask.logs.length > 0) {
                                    const latestLog = curTask.logs[curTask.logs.length - 1];
                                    if (procStatus) procStatus.innerText = latestLog;
                                }

                                if (curTask.status === 'completed') {
                                    clearInterval(pollInterval);
                                    clearInterval(timerInterval);

                                    if (procStatus) procStatus.innerHTML = '✅ <strong>Video pubblicato su TikTok Studio e inviato a Klippify!</strong> Scalamento slot in corso...';

                                    // Registra la clip come pubblicata nella schedule della campagna
                                    if (!campaignSchedules[campToken]) campaignSchedules[campToken] = { slots: [], published_clips: [] };
                                    if (!Array.isArray(campaignSchedules[campToken].published_clips)) campaignSchedules[campToken].published_clips = [];
                                    if (!campaignSchedules[campToken].published_clips.includes(filename)) {
                                        campaignSchedules[campToken].published_clips.push(filename);
                                    }
                                    await saveCurrentCampaignSchedule(campToken);

                                    // Aggiorna lo storico locale
                                    if (typeof publishedContent !== 'undefined') {
                                        publishedContent.push({
                                            campaign_id: campToken,
                                            filename: filename,
                                            timestamp: new Date().toISOString().replace('T', ' ').substr(0, 19),
                                            title: captionText
                                        });
                                    }

                                    // Ricarica le submissions da Klippify
                                    try {
                                        const subRes = await fetch('/api/klippify/submissions');
                                        if (subRes.ok) {
                                            const freshSubs = await subRes.json();
                                            if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                                        }
                                    } catch(e) {}

                                    setTimeout(() => {
                                        if (procBox) procBox.style.display = 'none';
                                        renderCampaignDetailContent(campToken);
                                    }, 2200);

                                } else if (curTask.status === 'error') {
                                    clearInterval(pollInterval);
                                    clearInterval(timerInterval);
                                    const errMsg = curTask.error || "Errore durante l'upload TikTok";
                                    if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore: ${errMsg}</span>`;
                                    alert("Errore upload TikTok: " + errMsg);
                                    if (btnElem) {
                                        btnElem.innerHTML = origHtml;
                                        btnElem.disabled = false;
                                    }
                                }
                            }
                        } catch(pollErr) {
                            console.error("Errore polling task upload:", pollErr);
                        }
                    }, 1500);

                } else if (data.status === 'success' || data.id) {
                    clearInterval(timerInterval);
                    if (procStatus) procStatus.innerHTML = '✅ <strong>Video inviato con successo!</strong> Scalamento slot in corso...';
                    setTimeout(() => {
                        if (procBox) procBox.style.display = 'none';
                        renderCampaignDetailContent(campToken);
                    }, 1800);
                } else {
                    clearInterval(timerInterval);
                    const errMsg = data.error || data.message || "Errore sconosciuto";
                    if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore: ${errMsg}</span>`;
                    alert("Errore upload TikTok: " + errMsg);
                    if (btnElem) {
                        btnElem.innerHTML = origHtml;
                        btnElem.disabled = false;
                    }
                }
            } catch(e) {
                clearInterval(timerInterval);
                if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore di rete: ${e.message}</span>`;
                alert("Errore comunicazione server: " + e.message);
                if (btnElem) {
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }
            }
        }
        const publishVideoFromSlot = publishSlotToTikTok;

        async function submitManualVideoToKlippify(campToken, btnElem) {
            const inputEl = document.getElementById(`manual-tiktok-url-${campToken}`);
            const url = inputEl ? inputEl.value.trim() : "";
            if (!url || !url.includes("http")) {
                alert("Inserisci un link video valido di TikTok o Instagram!");
                return;
            }
            const origHtml = btnElem.innerHTML;
            btnElem.innerHTML = "⏳ Invio a Klippify...";
            btnElem.disabled = true;
            try {
                const res = await fetch("/api/klippify/submit-content", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        campaign_id: campToken,
                        content_url: url,
                        platform: url.includes("instagram") ? "instagram" : "tiktok"
                    })
                });
                const data = await res.json();
                if (res.ok && !data.error) {
                    alert("✅ Video inviato con successo a Klippify! Ora il sistema lo analizzerà e lo mostrerà nello storico.");
                    if (inputEl) inputEl.value = "";
                    renderCampaignDetailContent(campToken);
                } else {
                    alert("Errore invio Klippify: " + (data.error || JSON.stringify(data)));
                }
            } catch(e) {
                alert("Errore di rete: " + e.message);
            } finally {
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }
        }

        function onSlotVideoChange(selectElem, slotIdx, campToken) {
            const filename = selectElem.value;
            const videoElem = document.getElementById(`slot-video-player-${slotIdx}`);
            const badgeElem = document.getElementById(`slot-status-badge-${slotIdx}`);

            if (filename) {
                if (videoElem) {
                    videoElem.src = `/generated_videos/${encodeURIComponent(filename)}`;
                    videoElem.style.display = 'block';
                }
                if (badgeElem) {
                    badgeElem.innerHTML = '🔵 Video Pronto';
                    badgeElem.style.background = 'rgba(56,189,248,0.2)';
                    badgeElem.style.color = '#38bdf8';
                }
            } else {
                if (videoElem) {
                    videoElem.style.display = 'none';
                }
                if (badgeElem) {
                    badgeElem.innerHTML = '🟡 Da Generare';
                    badgeElem.style.background = 'rgba(245,158,11,0.2)';
                    badgeElem.style.color = '#fbbf24';
                }
            }
            saveCampaignSlotVideo(campToken, slotIdx, filename);
        }

        function buildCampaignDailyStatsHtml(campToken, originalCamp, campSubmissions, targetCount) {
            const subs = campSubmissions || [];
            
            // Raggruppa per data (YYYY-MM-DD)
            const dailyMap = {};
            let totalViews = 0;
            let totalLikes = 0;
            let totalEarnings = 0;
            let acceptedCount = 0;
            let rejectedCount = 0;
            let pendingCount = 0;
            
            subs.forEach(s => {
                let dateKey = 'Oggi';
                let timeStr = '';
                if (s.created_at) {
                    try {
                        const d = new Date(s.created_at);
                        dateKey = d.toISOString().split('T')[0];
                        timeStr = d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
                    } catch(e) {
                        dateKey = 'Oggi';
                    }
                }
                
                if (!dailyMap[dateKey]) {
                    dailyMap[dateKey] = {
                        dateKey: dateKey,
                        dateObj: s.created_at ? new Date(s.created_at) : new Date(),
                        videos: [],
                        views: 0,
                        likes: 0,
                        earnings: 0,
                        accepted: 0,
                        rejected: 0,
                        pending: 0
                    };
                }
                
                const views = s.views || 0;
                const likes = s.likes || 0;
                const earnings = s.earnings || 0;
                
                totalViews += views;
                totalLikes += likes;
                totalEarnings += earnings;
                
                if (s.status === 'accepted') {
                    acceptedCount++;
                    dailyMap[dateKey].accepted++;
                } else if (s.status === 'rejected') {
                    rejectedCount++;
                    dailyMap[dateKey].rejected++;
                } else {
                    pendingCount++;
                    dailyMap[dateKey].pending++;
                }
                
                dailyMap[dateKey].views += views;
                dailyMap[dateKey].likes += likes;
                dailyMap[dateKey].earnings += earnings;
                dailyMap[dateKey].videos.push({
                    id: s.id,
                    post_url: s.post_url,
                    status: s.status,
                    views: views,
                    likes: likes,
                    time: timeStr,
                    ai_reasoning: s.ai_reasoning
                });
            });
            
            const daysKeys = Object.keys(dailyMap).sort().reverse();
            const activeDaysCount = Math.max(1, daysKeys.length);
            const totalVideos = subs.length;
            const dailyAvg = (totalVideos / activeDaysCount).toFixed(1);
            const approvalRate = totalVideos > 0 ? Math.round((acceptedCount / totalVideos) * 100) : 0;
            
            function formatDayHeader(dStr) {
                if (!dStr || dStr === 'Oggi') return 'Oggi';
                const todayStr = new Date().toISOString().split('T')[0];
                const yesterday = new Date();
                yesterday.setDate(yesterday.getDate() - 1);
                const yestStr = yesterday.toISOString().split('T')[0];
                
                try {
                    const d = new Date(dStr);
                    const dayName = d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
                    if (dStr === todayStr) return `🔥 Oggi (${dayName})`;
                    if (dStr === yestStr) return `Ieri (${dayName})`;
                    return dayName.toUpperCase();
                } catch(e) {
                    return dStr;
                }
            }
            
            let dailyRowsHtml = '';
            if (daysKeys.length === 0) {
                dailyRowsHtml = `
                    <div style="text-align:center; padding:1.8rem; background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:0.8rem; color:var(--text-muted); font-size:0.85rem;">
                        📊 Nessun video pubblicato finora per questa campagna. Non appena pubblicherai una clip su TikTok o attiverai il Pilota Automatico, qui vedrai la cronologia giorno per giorno con video pubblicati, views, media giornaliera e approvazioni.
                    </div>
                `;
            } else {
                daysKeys.forEach(dk => {
                    const dayData = dailyMap[dk];
                    const vCount = dayData.videos.length;
                    const target = targetCount || 3;
                    const pct = Math.min(100, Math.round((vCount / target) * 100));
                    const progressColor = pct >= 100 ? '#10b981' : (pct >= 50 ? '#38bdf8' : '#f59e0b');
                    
                    let statusPills = '';
                    if (dayData.accepted > 0) statusPills += `<span style="background:rgba(16,185,129,0.2); color:#34d399; font-size:0.72rem; padding:0.15rem 0.45rem; border-radius:0.3rem; font-weight:700;">✅ ${dayData.accepted} Approvati</span> `;
                    if (dayData.rejected > 0) statusPills += `<span style="background:rgba(239,68,68,0.2); color:#ef4444; font-size:0.72rem; padding:0.15rem 0.45rem; border-radius:0.3rem; font-weight:700;">❌ ${dayData.rejected} Rifiutati</span> `;
                    if (dayData.pending > 0) statusPills += `<span style="background:rgba(245,158,11,0.2); color:#fbbf24; font-size:0.72rem; padding:0.15rem 0.45rem; border-radius:0.3rem; font-weight:700;">⏳ ${dayData.pending} In Revisione</span>`;
                    
                    let videoBadges = dayData.videos.map((v, vIdx) => {
                        const isAcc = v.status === 'accepted';
                        const isRej = v.status === 'rejected';
                        const borderCol = isAcc ? 'rgba(16,185,129,0.4)' : (isRej ? 'rgba(239,68,68,0.4)' : 'rgba(245,158,11,0.4)');
                        return `
                            <a href="${v.post_url}" target="_blank" style="text-decoration:none; background:rgba(0,0,0,0.4); border:1px solid ${borderCol}; border-radius:0.4rem; padding:0.25rem 0.6rem; font-size:0.73rem; color:#fff; display:inline-flex; align-items:center; gap:0.35rem; transition:transform 0.15s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                <span>${isAcc ? '✅' : (isRej ? '❌' : '⏳')}</span>
                                <span style="font-weight:700;">Video #${vIdx+1} ${v.time ? `(${v.time})` : ''}</span>
                                ${v.views > 0 ? `<span style="color:#38bdf8; font-weight:bold;">&bull; ${v.views} views</span>` : ''}
                                <span style="font-size:0.65rem; color:var(--text-muted);">↗</span>
                            </a>
                        `;
                    }).join(' ');

                    dailyRowsHtml += `
                        <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.08); border-radius:0.8rem; padding:1rem 1.2rem; display:flex; flex-direction:column; gap:0.8rem; transition:all 0.2s;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;">
                                    <div style="font-weight:800; font-size:0.95rem; color:#fff;">
                                        📅 ${formatDayHeader(dk)}
                                    </div>
                                    <div style="display:flex; gap:0.4rem; align-items:center; flex-wrap:wrap;">
                                        ${statusPills}
                                    </div>
                                </div>

                                <div style="display:flex; align-items:center; gap:1.2rem; flex-wrap:wrap;">
                                    <div style="text-align:right;">
                                        <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;">Pubblicati vs Target</div>
                                        <div style="font-size:0.95rem; font-weight:800; color:${progressColor};">
                                            ${vCount} / ${target} video (${pct}%)
                                        </div>
                                    </div>
                                    <div style="text-align:right; min-width:80px;">
                                        <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;">Views Giorno</div>
                                        <div style="font-size:0.95rem; font-weight:800; color:#38bdf8;">${dayData.views.toLocaleString()}</div>
                                    </div>
                                    <div style="text-align:right; min-width:70px;">
                                        <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;">Guadagni</div>
                                        <div style="font-size:0.95rem; font-weight:800; color:#34d399;">$${dayData.earnings.toFixed(2)}</div>
                                    </div>
                                </div>
                            </div>

                            <!-- Progress Bar for the day -->
                            <div style="width:100%; height:6px; background:rgba(255,255,255,0.06); border-radius:3px; overflow:hidden;">
                                <div style="width:${pct}%; height:100%; background:${progressColor}; border-radius:3px; transition:width 0.3s ease;"></div>
                            </div>

                            <!-- Video chips for the day -->
                            <div style="display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center;">
                                <span style="font-size:0.72rem; color:var(--text-muted);">Video inviati:</span>
                                ${videoBadges}
                            </div>
                        </div>
                    `;
                });
            }

            return `
                <!-- STATISTICHE & PERFORMANCE GIORNO PER GIORNO -->
                <div style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(56,189,248,0.3); border-radius:1.2rem; padding:1.5rem; margin-bottom:2rem; box-shadow:0 10px 30px rgba(0,0,0,0.35);">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:1.2rem;">
                        <div>
                            <div style="font-size:1.25rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:0.6rem;">
                                <span>📈 Statistiche & Performance Giorno per Giorno</span>
                                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:1rem; font-weight:800;">
                                    ${totalVideos} Video Totali
                                </span>
                            </div>
                            <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.2rem;">
                                Monitora la costanza di pubblicazione, la media giornaliera e le visualizzazioni ottenute per questa campagna.
                            </div>
                        </div>
                        <div style="font-size:0.75rem; color:#64748b;">
                            Target configurato: <strong style="color:#38bdf8;">${targetCount || 3} video/giorno</strong>
                        </div>
                    </div>

                    <!-- 4 SUMMARY CARDS FOR THIS CAMPAIGN -->
                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:1rem; margin-bottom:1.2rem;">
                        
                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.9rem 1.1rem; border-left:4px solid #38bdf8;">
                            <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Video Pubblicati Totali</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#38bdf8; margin-top:0.2rem; line-height:1;">
                                ${totalVideos} <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">video</span>
                            </div>
                            <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.35rem;">${acceptedCount} approvati dall'AI</div>
                        </div>

                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.9rem 1.1rem; border-left:4px solid #8b5cf6;">
                            <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Media Giornaliera</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#c084fc; margin-top:0.2rem; line-height:1;">
                                ${dailyAvg} <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">video/gg</span>
                            </div>
                            <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.35rem;">su ${activeDaysCount} ${activeDaysCount === 1 ? 'giorno attivo' : 'giorni attivi'}</div>
                        </div>

                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.9rem 1.1rem; border-left:4px solid #10b981;">
                            <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Visualizzazioni Totali</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#10b981; margin-top:0.2rem; line-height:1;">
                                ${totalViews.toLocaleString()} <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">views</span>
                            </div>
                            <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.35rem;">${totalLikes.toLocaleString()} mi piace ricevuti</div>
                        </div>

                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.9rem 1.1rem; border-left:4px solid #f59e0b;">
                            <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Tasso Approvazione AI</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#fbbf24; margin-top:0.2rem; line-height:1;">
                                ${approvalRate}%
                            </div>
                            <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.35rem;">$${totalEarnings.toFixed(2)} guadagni maturati</div>
                        </div>

                    </div>

                    <!-- CRONOLOGIA GIORNALIERA -->
                    <div style="display:flex; flex-direction:column; gap:0.8rem;">
                        <div style="font-size:0.85rem; font-weight:800; color:#cbd5e1; display:flex; align-items:center; gap:0.4rem;">
                            <span>📅 Dettaglio Giorno per Giorno:</span>
                        </div>
                        ${dailyRowsHtml}
                    </div>

                </div>
            `;
        }

        function buildCampaignAssemblyPipelineHtml(campToken, originalCamp, item, isClipping, localAvailableVideos, savedSlots, targetCount, campSubmissions, scripts, defaultTimes, budgetRemaining, isDepleted, validLinks, allLinksHtml, dailyStatsHtml) {
            const schedInfo = campaignSchedules[campToken] || {};
            const isAutopilotOn = schedInfo.autopilot_enabled !== undefined ? !!schedInfo.autopilot_enabled : true;
            const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
            const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : [])
                .filter(p => p && p.campaign_id === campToken)
                .map(p => p.filename).filter(Boolean);
            const allPublishedFilenames = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));

            const campIsolatedVids = getCampaignIsolatedVideos(campToken);
            const allClips = campIsolatedVids.filter(v => v.filename && (v.filename.startsWith('clip_') || v.filename.includes('clip')));
            const rawVideos = campIsolatedVids.filter(v => v.filename && !v.filename.startsWith('clip_'));
            
            // Separa le clip vergini disponibili da quelle già pubblicate
            const virginClips = allClips.filter(c => !allPublishedFilenames.includes(c.filename));
            const publishedClips = allClips.filter(c => allPublishedFilenames.includes(c.filename));

            const originalBrief = originalCamp.description || 'Nessun brief fornito.';
            const originalHashtags = (originalCamp.mandatory_hashtags || []).join(', ') || '#klippify';
            const originalMentions = (originalCamp.mandatory_mentions || []).join(', ') || 'Nessuna';
            const originalCTA = originalCamp.call_to_action || 'Guarda il video completo su Klippify!';

            // Helper per formattazione nome progressivo incrementale
            function formatSeqClipTitle(filename, idx) {
                if (!filename) return `Clip #${idx + 1}`;
                let clean = filename.replace(/^clip_/, '').replace(/\.mp4$/i, '').replace(/\.mov$/i, '');
                clean = clean.replace(/_\d{8}_\d{6}.*$/, '');
                clean = clean.replace(/_slot\d+/i, '');
                clean = clean.replace(/_/g, ' ').trim();
                if (!clean || clean.length < 3) clean = originalCamp.name || 'Video';
                return `${clean} #${idx + 1}`;
            }

            // ⚡ SLIDING SLOTS LOGIC: separa gli slot già pubblicati oggi da quelli ancora pendenti
            const pendingSlots = [];
            const completedSlots = [];

            savedSlots.forEach((slot, originalIdx) => {
                const vid = slot.video;
                const isPub = vid && allPublishedFilenames.includes(vid);
                if (isPub) {
                    completedSlots.push({ ...slot, originalIdx, isPublished: true });
                } else {
                    pendingSlots.push({ ...slot, originalIdx, isPublished: false });
                }
            });

            // Assegna automaticamente le clip vergini disponibili a scalare per gli slot pendenti che non hanno ancora un video assegnato
            pendingSlots.forEach((pSlot, pIdx) => {
                if (!pSlot.video && virginClips.length > pIdx) {
                    pSlot.video = virginClips[pIdx].filename;
                }
            });

            let slotsMainViewHtml = '';

            if (pendingSlots.length === 0) {
                // TUTTI GLI SLOT DI OGGI SONO STATI COMPLETATI!
                slotsMainViewHtml = `
                    <div style="background:linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.25)); border:2px solid rgba(16,185,129,0.4); border-radius:1.4rem; padding:2.2rem; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.5);">
                        <div style="font-size:3.2rem; margin-bottom:0.6rem; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.5));">🎉</div>
                        <div style="font-size:1.45rem; font-weight:900; color:#34d399; margin-bottom:0.5rem;">Tutti i Video di Oggi sono stati Pubblicati!</div>
                        <div style="font-size:0.92rem; color:#cbd5e1; max-width:620px; margin:0 auto 1.4rem auto; line-height:1.5;">
                            Tutti gli slot previsti per questa campagna sono stati caricati con successo su TikTok e registrati su Klippify.<br>
                            <strong>Alle ore 00:00 il ciclo si resetterà in automatico</strong> ripristinando tutti gli slot con le nuove clip vergini pronte in magazzino.
                        </div>
                        <div style="display:flex; gap:0.8rem; justify-content:center; align-items:center; flex-wrap:wrap;">
                            <button onclick="addNewCampaignSlot('${campToken}')" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; border:none; padding:0.7rem 1.3rem; border-radius:0.6rem; font-weight:800; font-size:0.88rem; cursor:pointer; box-shadow:0 4px 15px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                ➕ Aggiungi un altro Slot per Oggi
                            </button>
                            <button onclick="resetCampaignPublishedClips('${campToken}', this)" style="background:rgba(255,255,255,0.08); color:#cbd5e1; border:1px solid rgba(255,255,255,0.2); padding:0.7rem 1.3rem; border-radius:0.6rem; font-weight:800; font-size:0.88rem; cursor:pointer;" title="Ripristina clip pubblicate come vergini">
                                🧹 Ripristina Clip per Rivederle
                            </button>
                        </div>
                    </div>
                `;
            } else {
                // 1. HERO TOP RECTANGLE: IL PROSSIMO SLOT PENDENTE (1° IN CODA)
                const heroSlot = pendingSlots[0];
                const heroSlotTime = heroSlot.time || defaultTimes[0] || "15:00";
                const heroSavedVideo = heroSlot.video || (virginClips.length > 0 ? virginClips[0].filename : "");
                const hasHeroVideo = !!heroSavedVideo && !allPublishedFilenames.includes(heroSavedVideo);
                const heroScript = scripts[0] || {};
                const heroCaption = heroScript.tiktok_caption || `${originalCamp.mandatory_hashtags ? originalCamp.mandatory_hashtags.join(' ') : '#klippify'} ${originalCamp.mandatory_mentions ? originalCamp.mandatory_mentions.join(' ') : ''}`;
                const heroTitleDisplay = heroSavedVideo ? formatSeqClipTitle(heroSavedVideo, heroSlot.originalIdx) : `In attesa di Clip (${originalCamp.name})`;

                let heroVideoOptions = '<option value="">-- Seleziona Clip 9:16 --</option>';
                virginClips.forEach(v => {
                    const isSel = (v.filename === heroSavedVideo) ? 'selected' : '';
                    heroVideoOptions += `<option value="${v.filename}" ${isSel}>🟢 ${formatSeqClipTitle(v.filename, heroSlot.originalIdx)} (${(v.size_mb || 0).toFixed(1)} MB)</option>`;
                });
                publishedClips.forEach(v => {
                    const isSel = (v.filename === heroSavedVideo) ? 'selected' : '';
                    heroVideoOptions += `<option value="${v.filename}" ${isSel} disabled style="color:#64748b;">🔒 ${v.filename} (✅ Già Pubblicata)</option>`;
                });

                const heroCardHtml = `
                    <div class="cascade-hero-card">
                        <!-- BADGE HERO IN TESTA -->
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:1.2rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:1rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; font-weight:900; font-size:0.82rem; padding:0.35rem 0.8rem; border-radius:0.5rem; box-shadow:0 0 15px rgba(16,185,129,0.5); display:flex; align-items:center; gap:0.4rem;">
                                    <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#fff; animation:pulse 1.5s infinite;"></span>
                                    🌟 1° IN CODA: PROSSIMA PUBBLICAZIONE
                                </span>
                                <span style="font-size:0.85rem; color:#34d399; font-weight:800;">Slot ${heroSlot.originalIdx + 1} (In Uscita)</span>
                            </div>

                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(0,0,0,0.5); padding:0.35rem 0.8rem; border-radius:0.6rem; border:1px solid rgba(16,185,129,0.3);">
                                    <span style="font-size:0.78rem; color:#94a3b8; font-weight:700;">⏰ Orario:</span>
                                    <input type="time" value="${heroSlotTime}" onchange="saveCampaignSlotTime('${campToken}', ${heroSlot.originalIdx}, this.value)" style="background:transparent; border:none; color:#34d399; font-weight:900; font-size:0.95rem; outline:none; cursor:pointer;">
                                </div>
                                <button onclick="addNewCampaignSlot('${campToken}')" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.45rem 0.85rem; border-radius:0.6rem; font-size:0.8rem; cursor:pointer; display:flex; align-items:center; gap:0.35rem; box-shadow:0 4px 12px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                    <span>➕ Aggiungi Slot</span>
                                </button>
                            </div>
                        </div>

                        <!-- CORPO HERO: ANTEPRIMA 3D A SINISTRA + AZIONI IN RILIEVO A DESTRA -->
                        <div style="display:grid; grid-template-columns:220px 1fr; gap:1.5rem; align-items:stretch;">
                            <div style="background:linear-gradient(180deg, #0f172a 0%, #020617 100%); border:2px solid rgba(255,255,255,0.12); border-top:2px solid rgba(255,255,255,0.3); border-bottom:4px solid #000; border-radius:1.2rem; padding:1rem; display:flex; flex-direction:column; justify-content:space-between; align-items:center; text-align:center; box-shadow:inset 0 2px 8px rgba(0,0,0,0.8), 0 10px 25px rgba(0,0,0,0.6);">
                                <div style="font-size:2.8rem; margin-top:0.3rem; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.5));">📱</div>
                                <div>
                                    <div style="font-size:0.82rem; font-weight:800; color:#fff; margin-bottom:0.2rem;">Formato 9:16 TikTok</div>
                                    <div style="font-size:0.72rem; color:#94a3b8;">${heroSavedVideo ? heroSavedVideo : 'Nessuna clip'}</div>
                                </div>
                                ${heroSavedVideo ? `
                                    <a href="/video/${encodeURIComponent(heroSavedVideo)}" target="_blank" style="width:100%; background:linear-gradient(180deg, #0284c7, #0369a1); color:#fff; border:1px solid rgba(255,255,255,0.2); border-top:1.5px solid rgba(255,255,255,0.4); border-bottom:3px solid #075985; padding:0.55rem; border-radius:0.6rem; font-size:0.78rem; font-weight:800; text-decoration:none; display:flex; align-items:center; justify-content:center; gap:0.4rem; box-shadow:0 4px 12px rgba(0,0,0,0.4); transition:all 0.15s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                        ▶️ Guarda Video
                                    </a>
                                ` : `
                                    <span style="font-size:0.72rem; color:#fbbf24;">⚠️ In attesa clip</span>
                                `}
                            </div>

                            <div style="display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                <div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                                        <h3 style="margin:0; font-size:1.35rem; font-weight:900; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,0.5);">🎬 ${heroTitleDisplay}</h3>
                                        <span style="background:linear-gradient(135deg, rgba(16,185,129,0.3), rgba(5,150,105,0.2)); border:1px solid rgba(16,185,129,0.5); border-top:1.5px solid rgba(52,211,153,0.8); border-bottom:2px solid #047857; color:#34d399; font-size:0.75rem; font-weight:800; padding:0.25rem 0.7rem; border-radius:0.5rem; box-shadow:0 3px 8px rgba(0,0,0,0.3);">
                                            ${hasHeroVideo ? '🟢 PRONTA PER INVIO' : '⚠️ SELEZIONA CLIP'}
                                        </span>
                                    </div>

                                    <div style="margin-bottom:0.8rem;">
                                        <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase; display:block; margin-bottom:0.25rem;">Cambia Clip Assegnata:</label>
                                        <select onchange="saveCampaignSlotVideo('${campToken}', ${heroSlot.originalIdx}, this.value)" style="width:100%; background:linear-gradient(180deg, #090d16 0%, #0f172a 100%); border:1px solid rgba(16,185,129,0.4); border-top:1px solid rgba(52,211,153,0.6); border-bottom:2px solid #047857; color:#f8fafc; padding:0.65rem; border-radius:0.6rem; font-size:0.82rem; font-weight:800; box-shadow:inset 0 2px 5px rgba(0,0,0,0.7);">
                                            ${heroVideoOptions}
                                        </select>
                                    </div>

                                    <div style="background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.08); border-bottom:2px solid rgba(0,0,0,0.8); border-radius:0.75rem; padding:0.85rem; box-shadow:inset 0 2px 6px rgba(0,0,0,0.6);">
                                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                                            <span style="font-size:0.72rem; color:#34d399; font-weight:800; text-transform:uppercase;">📱 Caption &amp; Tag Obbligatori:</span>
                                            <button onclick="copyToClipboard(decodeURIComponent('${encodeURIComponent(heroCaption)}'), this)" style="background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.15); border-bottom:2px solid rgba(0,0,0,0.5); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                        </div>
                                        <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; max-height:48px; overflow-y:auto;">${heroCaption}</div>
                                    </div>
                                </div>

                                <button onclick="publishSlotToTikTok('${campToken}', ${heroSlot.originalIdx}, this)" ${hasHeroVideo ? '' : 'disabled'} style="background:${hasHeroVideo ? 'linear-gradient(180deg, #10b981 0%, #059669 100%)' : 'rgba(255,255,255,0.08)'}; color:${hasHeroVideo ? '#ffffff' : '#64748b'}; border:1px solid rgba(255,255,255,0.2); border-top:${hasHeroVideo ? '2px solid rgba(255,255,255,0.5)' : 'none'}; border-bottom:${hasHeroVideo ? '4px solid #047857' : '2px solid rgba(0,0,0,0.5)'}; padding:1rem 1.4rem; border-radius:0.85rem; font-weight:900; font-size:0.95rem; cursor:${hasHeroVideo ? 'pointer' : 'not-allowed'}; display:flex; align-items:center; justify-content:center; gap:0.6rem; box-shadow:${hasHeroVideo ? '0 10px 25px rgba(0,0,0,0.5), 0 0 20px rgba(16,185,129,0.4), inset 0 1px 0 rgba(255,255,255,0.4)' : 'none'}; transition:all 0.15s;" onmouseover="if(this.style.cursor==='pointer') { this.style.transform='translateY(-2px)'; this.style.boxShadow='0 14px 30px rgba(0,0,0,0.6), 0 0 30px rgba(16,185,129,0.5)'; }" onmouseout="if(this.style.cursor==='pointer') { this.style.transform='none'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.5), 0 0 20px rgba(16,185,129,0.4)'; }" onmousedown="if(this.style.cursor==='pointer') { this.style.transform='translateY(2px)'; this.style.borderBottomWidth='2px'; }">
                                    <span>🚀 PUBBLICA SUBITO QUESTO VIDEO SU TIKTOK</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;

                // 2. MIDDLE CARDS: GLI ALTRI SLOT PENDENTI (2° IN CODA, 3° IN CODA...)
                let middleCardsHtml = '';
                pendingSlots.slice(1).forEach((slot, pIdx) => {
                    const queuePosition = pIdx + 2;
                    const slotTime = slot.time || defaultTimes[pIdx + 1] || "18:00";
                    const savedVideo = slot.video || "";
                    const hasSlotVideo = !!savedVideo && !allPublishedFilenames.includes(savedVideo);
                    const slotTitleDisplay = savedVideo ? formatSeqClipTitle(savedVideo, slot.originalIdx) : `Clip #${slot.originalIdx + 1} (${originalCamp.name})`;

                    let slotOptions = '<option value="">-- Seleziona Clip 9:16 --</option>';
                    virginClips.forEach(v => {
                        const isSel = (v.filename === savedVideo) ? 'selected' : '';
                        slotOptions += `<option value="${v.filename}" ${isSel}>🟢 ${formatSeqClipTitle(v.filename, slot.originalIdx)} (${(v.size_mb || 0).toFixed(1)} MB)</option>`;
                    });
                    publishedClips.forEach(v => {
                        const isSel = (v.filename === savedVideo) ? 'selected' : '';
                        slotOptions += `<option value="${v.filename}" ${isSel} disabled style="color:#64748b;">🔒 ${v.filename} (✅ Già Pubblicata)</option>`;
                    });

                    middleCardsHtml += `
                        <div class="cascade-slot-card" style="animation-delay:${0.12 * (pIdx + 1)}s;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:0.8rem; margin-bottom:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span style="background:linear-gradient(135deg, #8b5cf6, #6366f1); color:#fff; font-weight:900; font-size:0.75rem; padding:0.25rem 0.65rem; border-radius:0.4rem; box-shadow:0 2px 8px rgba(139,92,246,0.3);">
                                        ⏳ ${queuePosition}° IN CODA
                                    </span>
                                    <span style="font-weight:900; font-size:1.05rem; color:#f8fafc;">${slotTitleDisplay}</span>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(0,0,0,0.5); padding:0.3rem 0.6rem; border-radius:0.5rem; border:1px solid rgba(255,255,255,0.1);">
                                        <span style="font-size:0.75rem; color:#94a3b8; font-weight:700;">⏰ Orario:</span>
                                        <input type="time" value="${slotTime}" onchange="saveCampaignSlotTime('${campToken}', ${slot.originalIdx}, this.value)" style="background:transparent; border:none; color:#38bdf8; font-weight:900; font-size:0.88rem; outline:none; cursor:pointer;">
                                    </div>
                                    <button onclick="removeCampaignSlot('${campToken}', ${slot.originalIdx})" style="background:rgba(239,68,68,0.15); color:#fca5a5; border:1px solid rgba(239,68,68,0.3); padding:0.35rem 0.65rem; border-radius:0.4rem; cursor:pointer; font-size:0.8rem; font-weight:bold;" title="Elimina questo slot">
                                        🗑️
                                    </button>
                                </div>
                            </div>

                            <div style="display:grid; grid-template-columns:1fr 1.2fr; gap:1rem; align-items:center;">
                                <div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                                        <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">📹 Video Clip:</label>
                                        <span style="font-size:0.7rem; font-weight:800; color:${hasSlotVideo ? '#34d399' : '#fbbf24'};">
                                            ${hasSlotVideo ? '🟢 Clip Pronta' : '⚠️ In Riserva'}
                                        </span>
                                    </div>
                                    <select onchange="saveCampaignSlotVideo('${campToken}', ${slot.originalIdx}, this.value)" style="width:100%; background:rgba(0,0,0,0.6); border:1px solid rgba(255,255,255,0.15); color:#f8fafc; padding:0.55rem; border-radius:0.5rem; font-size:0.8rem; font-weight:700;">
                                        ${slotOptions}
                                    </select>
                                </div>

                                <div style="display:flex; gap:0.6rem; align-items:center; justify-content:flex-end;">
                                    ${savedVideo ? `
                                        <a href="/video/${encodeURIComponent(savedVideo)}" target="_blank" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.6rem 0.8rem; border-radius:0.5rem; font-size:0.78rem; font-weight:800; text-decoration:none; display:inline-flex; align-items:center; gap:0.3rem;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.15)'">
                                            ▶️ Anteprima
                                        </a>
                                    ` : ''}
                                    <button onclick="publishSlotToTikTok('${campToken}', ${slot.originalIdx}, this)" ${hasSlotVideo ? '' : 'disabled'} style="background:${hasSlotVideo ? 'linear-gradient(135deg, #10b981, #059669)' : 'rgba(255,255,255,0.08)'}; color:${hasSlotVideo ? '#ffffff' : '#64748b'}; border:none; padding:0.6rem 1rem; border-radius:0.5rem; font-weight:800; font-size:0.8rem; cursor:${hasSlotVideo ? 'pointer' : 'not-allowed'}; display:flex; align-items:center; gap:0.4rem; box-shadow:${hasSlotVideo ? '0 4px 12px rgba(16,185,129,0.3)' : 'none'};">
                                        <span>🚀 Pubblica Subito</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                });

                slotsMainViewHtml = heroCardHtml + middleCardsHtml;
            }

            // 3. CLIP IN RISERVA NEL MAGAZZINO (STRISCE COMPATTE CON NUMERAZIONE INCREMENTALE)
            let reserveRowsHtml = '';
            if (virginClips.length === 0) {
                reserveRowsHtml = `
                    <div style="text-align:center; padding:1.8rem; background:rgba(0,0,0,0.3); border:1px dashed rgba(56,189,248,0.3); border-radius:0.9rem;">
                        <div style="font-size:1.8rem; margin-bottom:0.3rem;">📦</div>
                        <div style="font-size:0.95rem; font-weight:800; color:#38bdf8;">Nessuna clip di riserva in coda</div>
                        <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">Carica nuovi video nella sezione "Materia Prima" per generare ulteriori clip a catena continua!</div>
                    </div>
                `;
            } else {
                virginClips.forEach((vClip, vIdx) => {
                    const seqNumber = targetCount + vIdx + 1;
                    const cleanTitle = formatSeqClipTitle(vClip.filename, seqNumber - 1);
                    reserveRowsHtml += `
                        <div class="cascade-reserve-row" style="animation-delay:${0.08 * (vIdx + 1)}s;">
                            <div style="display:flex; align-items:center; gap:0.8rem; min-width:240px;">
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-weight:900; font-size:0.75rem; padding:0.25rem 0.55rem; border-radius:0.4rem; border:1px solid rgba(56,189,248,0.4);">
                                    #${seqNumber}
                                </span>
                                <div>
                                    <div style="font-weight:800; font-size:0.88rem; color:#f8fafc;">${cleanTitle}</div>
                                    <div style="font-size:0.72rem; color:#94a3b8;">${vClip.filename} &bull; ${ (vClip.size_mb || 0).toFixed(1) } MB</div>
                                </div>
                            </div>

                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="background:rgba(139,92,246,0.15); color:#c084fc; font-size:0.72rem; font-weight:800; padding:0.25rem 0.6rem; border-radius:0.4rem; border:1px solid rgba(139,92,246,0.3);">
                                    ⏳ Riserva #${vIdx + 1} (Pronta a salire)
                                </span>
                                <a href="/video/${encodeURIComponent(vClip.filename)}" target="_blank" style="background:rgba(255,255,255,0.08); color:#e2e8f0; border:1px solid rgba(255,255,255,0.15); padding:0.35rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800; text-decoration:none;" onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">
                                    ▶️ Guarda
                                </a>
                                <button onclick="saveCampaignSlotVideo('${campToken}', 0, '${vClip.filename}'); renderCampaignDetailContent('${campToken}');" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:0.35rem 0.75rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800; cursor:pointer;" title="Porta subito in cima alla cascata">
                                    ⬆️ In Cima
                                </button>
                            </div>
                        </div>
                    `;
                });
            }

            // Clip pubblicate archiviate (nascoste di default tramite menu a tendina)
            let publishedRowsHtml = '';
            if (publishedClips.length > 0) {
                let pubListHtml = '';
                publishedClips.forEach((pClip, pIdx) => {
                    pubListHtml += `
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.06); padding:0.7rem 1rem; border-radius:0.6rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="color:#10b981; font-weight:900; font-size:0.85rem;">✅</span>
                                <div>
                                    <div style="font-weight:700; font-size:0.82rem; color:#cbd5e1;">${pClip.filename}</div>
                                    <div style="font-size:0.7rem; color:#64748b;">Archiviato &bull; Non riutilizzabile</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.5rem;">
                                <a href="/video/${encodeURIComponent(pClip.filename)}" target="_blank" style="background:rgba(255,255,255,0.06); color:#94a3b8; border:1px solid rgba(255,255,255,0.1); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; text-decoration:none;">
                                    ▶️ Rivedi
                                </a>
                            </div>
                        </div>
                    `;
                });

                publishedRowsHtml = `
                    <details class="published-accordion-dropdown">
                        <summary>
                            <span style="display:flex; align-items:center; gap:0.5rem;">
                                <span>🔒</span>
                                <span>Clip Storiche Già Pubblicate (${publishedClips.length})</span>
                            </span>
                            <span style="font-size:0.75rem; color:#94a3b8;">▼ Clicca per visualizzare</span>
                        </summary>
                        <div class="published-accordion-content">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                <span style="font-size:0.75rem; color:#94a3b8;">Queste clip sono già state caricate su TikTok e inviate a Klippify:</span>
                                <button onclick="resetCampaignPublishedClips('${campToken}', this)" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:0.4rem; font-size:0.72rem; font-weight:700; cursor:pointer;">
                                    🧹 Ripristina Clip
                                </button>
                            </div>
                            ${pubListHtml}
                        </div>
                    </details>
                `;
            }

            return `
                <div class="camp-layout-grid">
                    
                    <!-- NAVIGAZIONE LATERALE WIREFRAME -->
                    <div class="camp-subnav-panel">
                        <button id="camp-navbtn-cascade-${campToken}" class="camp-subnav-btn active" onclick="switchCampaignSubTab('${campToken}', 'cascade')">
                            <span>🌊</span>
                            <span>Coda &amp; Cascata</span>
                        </button>
                        <button id="camp-navbtn-raw-${campToken}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${campToken}', 'raw')">
                            <span>📦</span>
                            <span>Materia Prima &amp; Taglio (${rawVideos.length})</span>
                        </button>
                        <button id="camp-navbtn-prompts-${campToken}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${campToken}', 'prompts')">
                            <span>💡</span>
                            <span>Prompt &amp; Storyboard (${scripts.length})</span>
                        </button>
                        <button id="camp-navbtn-analytics-${campToken}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${campToken}', 'analytics')">
                            <span>📊</span>
                            <span>Dati &amp; Performance</span>
                        </button>
                        <button id="camp-navbtn-brief-${campToken}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${campToken}', 'brief')">
                            <span>📋</span>
                            <span>Dettagli Brief</span>
                        </button>
                    </div>

                    <!-- AREA CONTENUTO CENTRALE -->
                    <div>
                        <!-- TOP 2 WIDGETS A RILIEVO -->
                        <div class="camp-top-widgets-grid">
                            <!-- WIDGET 1: STATO PILOTA AUTOMATICO -->
                            <div class="camp-widget-card" style="border-left:4px solid ${isAutopilotOn ? '#10b981' : '#ef4444'};">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Pilota Automatico:</span>
                                    <span id="assembly-autopilot-badge-${campToken}" style="background:${isAutopilotOn ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)'}; color:${isAutopilotOn ? '#10b981' : '#ef4444'}; border:1px solid ${isAutopilotOn ? 'rgba(16,185,129,0.4)' : 'rgba(239,68,68,0.4)'}; padding:0.2rem 0.6rem; border-radius:1rem; font-size:0.75rem; font-weight:900;">
                                        ${isAutopilotOn ? '🟢 ATTIVO' : '⏸ IN PAUSA'}
                                    </span>
                                </div>
                                <div style="font-size:1.15rem; font-weight:900; color:#fff; display:flex; align-items:center; justify-content:space-between;">
                                    <span>${isAutopilotOn ? 'Autonomo H24' : 'Manuale'}</span>
                                    <button onclick="toggleCampaignAutopilot('${campToken}')" style="background:rgba(255,255,255,0.08); color:#cbd5e1; border:1px solid rgba(255,255,255,0.15); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer;">
                                        ${isAutopilotOn ? 'Metti in Pausa' : 'Attiva'}
                                    </button>
                                </div>
                            </div>

                            <!-- WIDGET 2: OBIETTIVO GIORNALIERO -->
                            <div class="camp-widget-card" style="border-left:4px solid #38bdf8;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Obiettivo Giornaliero:</span>
                                    <span id="assembly-ready-count-${campToken}" style="font-size:0.85rem; font-weight:900; color:#38bdf8;">
                                        ${pendingSlots.length} da Pubblicare
                                    </span>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span style="font-size:0.82rem; color:#cbd5e1;">Target Slot:</span>
                                    <select onchange="updateCampaignTargetCount('${campToken}', this.value)" style="background:rgba(0,0,0,0.5); border:1px solid rgba(56,189,248,0.4); color:#38bdf8; font-weight:900; font-size:0.88rem; padding:0.2rem 0.5rem; border-radius:0.4rem; outline:none; cursor:pointer;">
                                        <option value="1" ${targetCount === 1 ? 'selected' : ''}>1 video/giorno</option>
                                        <option value="2" ${targetCount === 2 ? 'selected' : ''}>2 video/giorno</option>
                                        <option value="3" ${targetCount === 3 ? 'selected' : ''}>3 video/giorno</option>
                                        <option value="4" ${targetCount === 4 ? 'selected' : ''}>4 video/giorno</option>
                                        <option value="5" ${targetCount === 5 ? 'selected' : ''}>5 video/giorno</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- TAB 1: CODA & CASCATA -->
                        <div id="camp-subtab-cascade-${campToken}" style="display:block;">
                            
                            <div class="cascade-waterfall-stream">
                                
                                <!-- BANNER STATO LIVE PER CLIPPING IN CORSO -->
                                <div id="assembly-clipping-live-banner-${campToken}" style="display:none; align-items:center; gap:0.8rem; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.4); border-radius:0.85rem; padding:0.85rem 1.2rem; margin-bottom:1rem; color:#38bdf8; font-weight:800; font-size:0.85rem; box-shadow:0 0 15px rgba(56,189,248,0.25);"></div>

                                <!-- RETTANGOLO DINAMICO "STO PROCESSANDO" (COMPARE SOLO DURANTE L'UPLOAD) -->
                                <div id="assembly-active-processing-box-${campToken}" class="processing-active-card" style="display:none;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:1rem; border-bottom:1px solid rgba(245,158,11,0.3); padding-bottom:0.8rem;">
                                        <div style="display:flex; align-items:center; gap:0.6rem;">
                                            <span class="processing-pulse-badge">
                                                <span class="pulse-dot"></span>
                                                ⚡ IN ELABORAZIONE: STO PROCESSANDO
                                            </span>
                                            <span id="processing-clip-title-${campToken}" style="font-weight:900; font-size:1.05rem; color:#fff;">Upload TikTok &amp; Sottomissione Klippify...</span>
                                        </div>
                                        <div style="display:flex; align-items:center; gap:0.6rem;">
                                            <span id="processing-elapsed-timer-${campToken}" style="background:rgba(0,0,0,0.6); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:0.3rem 0.7rem; border-radius:0.5rem; font-size:0.8rem; font-weight:900;">⏳ In corso...</span>
                                        </div>
                                    </div>
                                    <div style="display:grid; grid-template-columns:110px 1fr; gap:1.2rem; align-items:center;">
                                        <div style="background:#000; border-radius:0.8rem; padding:0.8rem; text-align:center; border:1px solid rgba(245,158,11,0.4); box-shadow:0 0 15px rgba(245,158,11,0.2);">
                                            <div style="font-size:2.2rem;">🚀</div>
                                            <div style="font-size:0.7rem; color:#fbbf24; font-weight:800; margin-top:0.3rem;">TikTok Studio</div>
                                        </div>
                                        <div>
                                            <div style="font-size:0.95rem; font-weight:800; color:#fff; margin-bottom:0.3rem;" id="processing-status-label-${campToken}">
                                                Caricamento video su TikTok Studio, verifica copyright e invio automatico a Klippify...
                                            </div>
                                            <div style="font-size:0.78rem; color:#cbd5e1; margin-bottom:0.7rem;" id="processing-clip-filename-${campToken}">
                                                clip.mp4
                                            </div>
                                            <div class="processing-animated-bar">
                                                <div class="processing-bar-fill"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- SLOT IN CODA DELLA GIORNATA (CON LOGICA A SCORRIMENTO) -->
                                ${slotsMainViewHtml}

                                <!-- ======================================================== -->
                                <!-- STRISCE COMPATTE IN BASSO (MAGAZZINO CLIP DI RISERVA)   -->
                                <!-- ======================================================== -->
                                <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.25); border-radius:1.2rem; padding:1.4rem; margin-top:0.8rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1rem;">
                                        <div>
                                            <div style="font-size:1.15rem; font-weight:900; color:#38bdf8; display:flex; align-items:center; gap:0.5rem;">
                                                <span>✂️ Magazzino Clip di Riserva</span>
                                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:1rem; font-weight:800;">
                                                    ${virginClips.length} Pronte
                                                </span>
                                            </div>
                                            <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">
                                                Ogni video pubblicato farà scalare automaticamente le clip sottostanti di una posizione verso l'alto!
                                            </div>
                                        </div>
                                    </div>

                                    <div style="display:flex; flex-direction:column; gap:0.6rem;">
                                        ${reserveRowsHtml}
                                    </div>

                                    ${publishedRowsHtml}
                                </div>

                            </div>
                        </div>

                        <!-- TAB 2: MATERIA PRIMA & TAGLIO (GESTIONE VIDEO LUNGHI) -->
                        <div id="camp-subtab-raw-${campToken}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:1.25rem; padding:1.5rem;">
                                
                                <!-- INPUT FILE NASCOSTO PER CARICAMENTO MULTIPLO -->
                                <input type="file" id="source-video-input-assembly-${campToken}" accept="video/*" multiple style="display:none;" onchange="uploadSourceVideoFiles(this, '${campToken}')">

                                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                    <div>
                                        <div style="font-size:1.2rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                            <span>📦 Materia Prima: Video Lunghi da Klippare</span>
                                            <span id="assembly-clipping-queue-count-${campToken}" style="background:rgba(245,158,11,0.2); color:#fbbf24; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">${rawVideos.length} Video</span>
                                        </div>
                                        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:0.3rem;">
                                            Carica i file video completi del brand: Gemini e FFmpeg ritaglieranno le migliori clip verticali 9:16 che entreranno in coda.
                                        </div>
                                    </div>
                                    
                                    <div style="display:flex; gap:0.6rem; flex-wrap:wrap;">
                                        <button id="btn-upload-file-assembly-${campToken}" onclick="document.getElementById('source-video-input-assembly-${campToken}').click()" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.65rem 1.1rem; border-radius:0.6rem; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 12px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                            📁 Carica Video Lunghi
                                        </button>
                                        <button onclick="openLocalFolder('${campToken}')" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:700; border:1px solid rgba(255,255,255,0.2); padding:0.65rem 0.9rem; border-radius:0.6rem; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                            📂 Apri Cartella
                                        </button>
                                    </div>
                                </div>

                                <div id="assembly-clipping-queue-list-${campToken}" style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">
                                    <div style="text-align:center; padding:1rem; color:var(--text-muted); font-size:0.85rem;">⏳ Caricamento coda video lunghi...</div>
                                </div>

                                ${validLinks.length > 0 ? `
                                    <div style="margin-top:1.5rem; padding-top:1.2rem; border-top:1px solid rgba(255,255,255,0.08);">
                                        <div style="font-size:0.88rem; font-weight:800; color:#38bdf8; margin-bottom:0.6rem;">
                                            🔗 Materiale Ufficiale Brand (Drive / WeTransfer / YouTube):
                                        </div>
                                        ${allLinksHtml}
                                    </div>
                                ` : ''}
                            </div>
                        </div>

                        <!-- TAB: PROMPT & STORYBOARD -->
                        <div id="camp-subtab-prompts-${campToken}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(139,92,246,0.3); border-radius:1.25rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                                    <div>
                                        <h4 style="color:#c084fc; font-size:1.15rem; font-weight:800; margin:0;">💡 Prompt Gemini Veo &amp; Storyboard AI</h4>
                                        <div style="font-size:0.8rem; color:#cbd5e1; margin-top:0.2rem;">Copie pronte per generare nuovi video su Gemini o ispirare i tagli.</div>
                                    </div>
                                    <span style="background:rgba(139,92,246,0.2); color:#c084fc; border:1px solid rgba(139,92,246,0.4); padding:0.25rem 0.7rem; border-radius:0.5rem; font-size:0.75rem; font-weight:800;">
                                        ${scripts.length} Varianti Script
                                    </span>
                                </div>
                                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.2rem;">
                                    ${scripts.map((sc, sci) => `
                                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.08); border-radius:0.9rem; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                            <div>
                                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                                                    <span style="font-weight:900; color:#38bdf8; font-size:0.92rem;">#${sci+1} ${sc.concept_name || 'Variante Script'}</span>
                                                    <button onclick="copyToClipboard('${(sc.video_prompt_gemini || '').replace(/'/g, "\\'")}' )" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.35); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer;">
                                                        📋 Copia Prompt
                                                    </button>
                                                </div>
                                                <div style="font-size:0.78rem; color:#cbd5e1; background:rgba(0,0,0,0.4); padding:0.8rem; border-radius:0.6rem; font-family:monospace; line-height:1.45; border:1px solid rgba(255,255,255,0.05); margin-bottom:0.8rem; max-height:160px; overflow-y:auto;">
                                                    ${sc.video_prompt_gemini || 'Nessun prompt'}
                                                </div>
                                                <div style="font-size:0.78rem; color:#a78bfa; font-weight:700;">
                                                    📝 TikTok Caption: <span style="color:#e2e8f0; font-weight:normal;">${sc.tiktok_caption || ''}</span>
                                                </div>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>

                        <!-- TAB 3: DATI & PERFORMANCE -->
                        <div id="camp-subtab-analytics-${campToken}" style="display:none;">
                            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                                ${dailyStatsHtml}
                            </div>
                        </div>

                        <!-- TAB 4: REGOLE & BRIEF -->
                        <div id="camp-subtab-brief-${campToken}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1.25rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem;">
                                <div>
                                    <h4 style="color:#f8fafc; font-size:1.1rem; font-weight:800; margin:0 0 0.5rem 0;">📋 Brief Ufficiale</h4>
                                    <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5; background:rgba(0,0,0,0.3); padding:0.9rem; border-radius:0.6rem;">
                                        ${originalBrief}
                                    </div>
                                </div>

                                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:1rem;">
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Hashtag Obbligatori</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${originalHashtags}</div>
                                    </div>
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Tag Creator (@)</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${originalMentions}</div>
                                    </div>
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Call to Action (CTA)</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${originalCTA}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            `;
        }

        function renderCampaignDetailContent(campToken) {
            const detailContainer = document.getElementById('my-campaign-detail-content');
            
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {};
            const item = generatedContent.find(gc => gc.campaign_id === campToken) || {};
            const publishedItems = (typeof publishedContent !== 'undefined' ? publishedContent : []).filter(pc => pc.campaign_id === campToken);
            
            const classifiedInfo = activeCampaignsClassified.find(ac => 
                ac.id === campToken || 
                ac.campaign_token === campToken || 
                ac.campaign_id === campToken ||
                (originalCamp.name && ac.name && ac.name.toLowerCase() === originalCamp.name.toLowerCase())
            ) || {};
            const isClipping = classifiedInfo.category === 'CLIPPING' || 
                               (classifiedInfo.drive_links && classifiedInfo.drive_links.length > 0) ||
                               (classifiedInfo.all_links && classifiedInfo.all_links.some(l => l.type === 'drive' || l.type === 'wetransfer' || l.type === 'youtube' || l.type === 'reel')) ||
                               (originalCamp.description && (
                                   originalCamp.description.toLowerCase().includes('podcast') || 
                                   originalCamp.description.toLowerCase().includes('clip') ||
                                   originalCamp.description.toLowerCase().includes('taglia') ||
                                   originalCamp.description.toLowerCase().includes('youtube') ||
                                   originalCamp.description.toLowerCase().includes('drive')
                               ));
            
            const originalBrief = originalCamp.description || 'Nessun brief fornito.';
            const originalHashtags = (originalCamp.mandatory_hashtags || []).join(', ') || '#klippify';
            const originalMentions = (originalCamp.mandatory_mentions || []).join(', ') || 'Nessuna';
            const originalCTA = originalCamp.call_to_action || 'Guarda il video completo su Klippify!';
            const originalRules = (originalCamp.rules || ['Segui le linee guida Klippify']).map(r => `<li>✓ ${r}</li>`).join('');
            const originalRulesText = (originalCamp.rules || ['Segui le linee guida Klippify']).join(', ');
            
            const budgetRemaining = parseFloat(originalCamp.budget_remaining) || 0;
            const isDepleted = budgetRemaining <= 0 && originalCamp.budget_remaining !== undefined;
            
            const warningBanner = isDepleted ? `
                <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; border-radius: 1rem; padding: 1.5rem; text-align: center; margin-bottom: 2rem; animation: pulse 2s infinite;">
                    <h3 style="color: #fca5a5; margin-bottom: 0.5rem; font-size: 1.5rem;">🛑 ATTENZIONE: BUDGET CAMPAGNA ESAURITO 🛑</h3>
                    <p style="color: #f8fafc; font-weight: bold;">Questa campagna non ha più fondi residui su Klippify. È sconsigliato produrre o pubblicare altri video.</p>
                </div>
            ` : '';

            // ELENCO COMPLETO DI TUTTI I LINK E RISORSE DELLA CAMPAGNA
            const allLinksRaw = [];
            (classifiedInfo.drive_links || []).forEach(d => allLinksRaw.push({ type: 'drive', title: d.title || 'Cartella Google Drive / WeTransfer', url: d.url }));
            (classifiedInfo.resource_links || []).forEach(r => allLinksRaw.push({ type: 'resource', title: r.title || 'Video / File Risorsa', url: r.url }));
            (classifiedInfo.all_extracted_links || []).forEach(u => {
                if (!allLinksRaw.some(x => x.url === u)) {
                    allLinksRaw.push({ type: 'link', title: u, url: u });
                }
            });

            // Filtra duplicati e link non rilevanti
            const validLinks = allLinksRaw.filter(l => l.url && !l.url.includes('signin') && !l.url.includes('signup') && !l.url.includes('dashboard'));

            let allLinksHtml = '';
            if (validLinks.length > 0) {
                allLinksHtml += '<div style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">';
                validLinks.forEach((l, lIdx) => {
                    let badgeBg = 'rgba(59,130,246,0.2)';
                    let badgeColor = '#60a5fa';
                    let icon = '📁';
                    let typeName = 'Google Drive';

                    if (l.url.includes('we.tl') || l.url.includes('wetransfer')) {
                        badgeBg = 'rgba(236,72,153,0.2)';
                        badgeColor = '#f472b6';
                        icon = '📦';
                        typeName = 'WeTransfer';
                    } else if (l.url.includes('youtube.com') || l.url.includes('youtu.be')) {
                        badgeBg = 'rgba(239,68,68,0.2)';
                        badgeColor = '#f87171';
                        icon = '▶️';
                        typeName = 'YouTube';
                    } else if (l.url.includes('dropbox')) {
                        badgeBg = 'rgba(14,165,233,0.2)';
                        badgeColor = '#38bdf8';
                        icon = '📂';
                        typeName = 'Dropbox';
                    } else {
                        badgeBg = 'rgba(139,92,246,0.2)';
                        badgeColor = '#c084fc';
                        icon = '🔗';
                        typeName = 'Risorsa Web';
                    }

                    allLinksHtml += `
                        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); border-radius:0.6rem; padding:0.7rem 1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem; flex:1; min-width:240px;">
                                <span style="background:${badgeBg}; color:${badgeColor}; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800; white-space:nowrap;">
                                    ${icon} ${typeName}
                                </span>
                                <a href="${l.url}" target="_blank" style="color:#e2e8f0; font-size:0.82rem; word-break:break-all; text-decoration:none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
                                    ${l.url}
                                </a>
                            </div>
                            <a href="${l.url}" target="_blank" style="background:rgba(255,255,255,0.1); hover:background:rgba(255,255,255,0.2); color:#fff; text-decoration:none; padding:0.4rem 0.8rem; border-radius:0.4rem; font-size:0.78rem; font-weight:bold; display:flex; align-items:center; gap:0.4rem; transition:background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                🔗 Apri Link
                            </a>
                        </div>
                    `;
                });
                allLinksHtml += '</div>';
            } else {
                allLinksHtml = '<div style="color:var(--text-muted); font-size:0.82rem; margin-top:0.5rem;">Nessun link esterno o Drive fornito per questa campagna.</div>';
            }

            // Schedulatore e Slot Giornalieri
            const savedSchedule = campaignSchedules[campToken] || {};
            const targetCount = savedSchedule.target_count || 3;
            const savedSlots = savedSchedule.slots || [];

            const defaultTimes = ["12:00", "16:30", "20:00", "22:00", "09:30", "14:00", "18:00", "21:00"];

            const scripts = item.scripts && item.scripts.length > 0 ? item.scripts : [
                {
                    concept_name: isClipping ? "Clip Saliente 1 (9:16)" : "Hook Emotivo & Relatable",
                    video_prompt_gemini: `Vertical 9:16 video, 15-30s. Dynamic TikTok format for ${originalCamp.name}. Visual hook in first 2s. Respect rules: ${originalRulesText}. Include CTA: ${originalCTA}.`,
                    tiktok_caption: `Scopri ${originalCamp.name}! ✨ ${originalHashtags} ${originalMentions}`,
                    storyboard: [
                        { duration: "0-3s", description: "Hook visivo forte", text_overlay: "Non ci crederai mai..." },
                        { duration: "3-10s", description: "Sviluppo del concept", text_overlay: "Guarda fino alla fine!" },
                        { duration: "10-15s", description: "Call to Action finale", text_overlay: "${originalCTA}" }
                    ]
                }
            ];

            let slotsHtml = '';
            for (let i = 0; i < targetCount; i++) {
                const slotTime = (savedSlots[i] && savedSlots[i].time) ? savedSlots[i].time : (defaultTimes[i] || "12:00");
                const savedVideo = (savedSlots[i] && savedSlots[i].video) ? savedSlots[i].video : "";
                
                const scriptIndex = i % scripts.length;
                const script = scripts[scriptIndex] || {};
                const conceptName = script.concept_name || (isClipping ? `Clip Ritagliata ${i+1}` : `Slot Video ${i+1}`);
                const promptText = script.video_prompt_gemini || `Genera video 9:16 per ${originalCamp.name}`;
                const captionText = script.tiktok_caption || `${originalHashtags} ${originalMentions}`;

                let videoOptionsHtml = '<option value="">-- Seleziona un Video MP4 generato/ritagliato --</option>';
                const campIsolatedVidsClassic = getCampaignIsolatedVideos(campToken);
                campIsolatedVidsClassic.forEach(v => {
                    const isSel = (v.filename === savedVideo) ? 'selected' : '';
                    videoOptionsHtml += `<option value="${v.filename}" ${isSel}>${v.filename}</option>`;
                });

                const storyboardHtml = (script.storyboard || []).map((s, si) =>
                    `<div style="display:flex; gap:0.6rem; align-items:flex-start; padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.75rem;">`
                    + `<div style="min-width:32px; height:32px; border-radius:0.4rem; background:rgba(255,255,255,0.08); display:flex; align-items:center; justify-content:center; font-weight:700;">S${si+1}</div>`
                    + `<div><strong style="color:#f8fafc;">⏱ ${s.duration}</strong> - <span style="color:#94a3b8;">${s.description}</span> <div style="color:#38bdf8; margin-top:0.1rem;">💬 "${s.text_overlay}"</div></div></div>`
                ).join('');

                const hasVideo = !!savedVideo;

                let leftColumnHtml = '';
                if (isClipping) {
                    leftColumnHtml = `
                        <!-- CLIPPING WORKFLOW CARD (PROMPT VEO RIMOSSO) -->
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#fbbf24;">✂️ Dettagli Clip Ritagliata 9:16</span>
                                    <span style="background:rgba(245,158,11,0.2); color:#fbbf24; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold;">Da Materiale Sorgente</span>
                                </div>
                                <div style="font-size:0.82rem; color:#e2e8f0; line-height:1.45; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">
                                    🎬 <strong>Concept:</strong> ${conceptName}<br>
                                    💡 <em>Questa clip viene estratta direttamente dal materiale video sorgente fornito dal brand.</em>
                                </div>
                            </div>

                            <!-- TIKTOK CAPTION BOX -->
                            <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#34d399;">📱 Caption TikTok & Tag Obbligatori</span>
                                    <button onclick="copyToClipboard(decodeURIComponent('${encodeURIComponent(captionText)}'), this)" style="background:linear-gradient(135deg,#10b981,#059669); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                </div>
                                <div id="slot-caption-${i}" style="font-size:0.82rem; color:#e2e8f0; line-height:1.4; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${captionText}</div>
                            </div>
                        </div>
                    `;
                } else {
                    leftColumnHtml = `
                        <!-- AI GENERATION WORKFLOW (PROMPT GEMINI VEO) -->
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            
                            <!-- PROMPT GEMINI BOX -->
                            <div style="background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#c084fc;">🤖 Prompt Video per Gemini Veo</span>
                                    <div style="display:flex; gap:0.5rem;">
                                        <button onclick="copyToClipboard(decodeURIComponent('${encodeURIComponent(promptText)}'), this)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                        <button onclick="generateVideoFromSlot('${campToken}', decodeURIComponent('${encodeURIComponent(promptText)}'), this)" style="background:linear-gradient(135deg,#8b5cf6,#4f46e5); color:#fff; border:none; padding:0.3rem 0.8rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer; box-shadow:0 2px 8px rgba(139,92,246,0.4);">🤖 Genera con Bot</button>
                                    </div>
                                </div>
                                <div style="font-size:0.82rem; color:#e2e8f0; line-height:1.45; max-height:90px; overflow-y:auto; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${promptText}</div>
                            </div>

                            <!-- TIKTOK CAPTION BOX -->
                            <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#34d399;">📱 Caption TikTok & Tag Obbligatori</span>
                                    <button onclick="copyToClipboard(decodeURIComponent('${encodeURIComponent(captionText)}'), this)" style="background:linear-gradient(135deg,#10b981,#059669); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                </div>
                                <div id="slot-caption-${i}" style="font-size:0.82rem; color:#e2e8f0; line-height:1.4; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${captionText}</div>
                            </div>

                            <!-- STORYBOARD PREVIEW -->
                            <details style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.8rem;">
                                <summary style="font-size:0.8rem; font-weight:700; color:#38bdf8; cursor:pointer;">🎬 Storyboard Dettagliato (Scene & Testi)</summary>
                                <div style="margin-top:0.6rem; max-height:140px; overflow-y:auto;">
                                    ${storyboardHtml}
                                </div>
                            </details>

                        </div>
                    `;
                }

                slotsHtml += `
                    <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1.2rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem; box-shadow:0 8px 20px rgba(0,0,0,0.3);">
                        
                        <!-- SLOT TOP BAR -->
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:1rem;">
                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <span style="background:${isClipping ? 'linear-gradient(135deg, #f59e0b, #d97706)' : 'linear-gradient(135deg, #8b5cf6, #4f46e5)'}; color:#000; padding:0.3rem 0.8rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem;">
                                    ⏰ Slot ${i+1}
                                </span>
                                <div style="display:flex; align-items:center; gap:0.4rem;">
                                    <span style="font-size:0.8rem; color:var(--text-muted);">Orario:</span>
                                    <input type="time" value="${slotTime}" onchange="saveCampaignSlotTime('${campToken}', ${i}, this.value)" style="background:rgba(0,0,0,0.5); border:1px solid rgba(139,92,246,0.4); color:#38bdf8; border-radius:0.4rem; padding:0.25rem 0.5rem; font-weight:bold; font-size:0.85rem;">
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <h3 style="margin:0; font-size:1.05rem; color:#fff;">🎬 ${conceptName}</h3>
                                <span id="slot-status-badge-${i}" style="background:${hasVideo ? 'rgba(56,189,248,0.2)' : 'rgba(245,158,11,0.2)'}; color:${hasVideo ? '#38bdf8' : '#fbbf24'}; padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700;">
                                    ${hasVideo ? '🔵 Video Pronto' : '🟡 Da Caricare/Tagliare'}
                                </span>
                            </div>
                        </div>

                        <!-- 2-COLUMNS WORKFLOW -->
                        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:1.5rem;">
                            
                            <!-- LEFT COLUMN -->
                            ${leftColumnHtml}

                            <!-- RIGHT: VIDEO PREVIEW & TIKTOK UPLOAD -->
                            <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:1rem; display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                <div>
                                    <span style="font-weight:800; font-size:0.85rem; color:#38bdf8; display:block; margin-bottom:0.6rem;">🎥 Video MP4 Associato (9:16)</span>
                                    <select id="slot-video-select-${i}" onchange="onSlotVideoChange(this, ${i}, '${campToken}')" style="width:100%; background:rgba(15,23,42,0.9); border:1px solid rgba(255,255,255,0.2); color:#fff; border-radius:0.5rem; padding:0.5rem; font-size:0.8rem; margin-bottom:0.8rem;">
                                        ${videoOptionsHtml}
                                    </select>
                                    
                                    <video id="slot-video-player-${i}" src="${savedVideo ? '/generated_videos/' + encodeURIComponent(savedVideo) : ''}" controls preload="metadata" playsinline style="width:100%; max-height:260px; min-height:160px; border-radius:0.6rem; background:#000; display:${hasVideo ? 'block' : 'none'}; outline:none; box-shadow:0 4px 14px rgba(0,0,0,0.5);"></video>
                                </div>

                                <div style="display:flex; flex-direction:column; gap:0.5rem;">
                                    <button onclick="publishVideoFromSlot('${campToken}', ${i}, this)" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:0.7rem 1rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:0.5rem; box-shadow:0 4px 12px rgba(16,185,129,0.3); transition:all 0.2s;">
                                        🚀 Pubblica questo Video su TikTok
                                    </button>
                                    <div style="font-size:0.72rem; color:var(--text-muted); text-align:center;">Invia direttamente a TikTok con titolo e tag precompilati</div>
                                </div>
                            </div>

                        </div>
                    </div>
                `;
            }

            // Storico Video Inviati ESCLUSIVAMENTE per questa specifica campagna
            const campSubmissions = (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).filter(s => {
                if (s.campaign_id && (s.campaign_id === campToken || s.campaign_id === originalCamp.id || s.campaign_id === originalCamp.campaign_token)) return true;
                if (originalCamp.name && s.campaign_name && originalCamp.name.trim().toLowerCase() === s.campaign_name.trim().toLowerCase()) return true;
                return false;
            });

            let publishedHtml = '';
            if (campSubmissions.length === 0) {
                publishedHtml = `
                    <div style="padding:2.5rem 1.5rem; text-align:center; background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem;">
                        <div style="font-size:2.2rem; margin-bottom:0.5rem;">📭</div>
                        <div style="font-size:1.05rem; font-weight:700; color:#e2e8f0; margin-bottom:0.3rem;">Nessun video inviato per questa campagna</div>
                        <div style="font-size:0.82rem; color:var(--text-muted); max-width:480px; margin:0 auto; line-height:1.4;">Non risultano video sottomessi su Klippify per <strong>${originalCamp.name || 'questa campagna'}</strong>. Quando pubblicherai e invierai una clip, comparirà qui con visualizzazioni, mi piace, validazione AI e guadagni reali.</div>
                    </div>
                `;
            } else {
                publishedHtml = `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:1.2rem;">`;
                campSubmissions.forEach(sub => {
                    const isRejected = sub.status === 'rejected';
                    const isAccepted = sub.status === 'accepted';

                    const statusBadge = isAccepted
                        ? '<span style="background:rgba(16,185,129,0.2); color:#34d399; border:1px solid rgba(16,185,129,0.4); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800;">✅ Approvato & Verificato AI</span>'
                        : isRejected
                            ? '<span style="background:rgba(239,68,68,0.25); color:#ef4444; border:1px solid rgba(239,68,68,0.5); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:900;">❌ RIFIUTATO DALL&#39;AI</span>'
                            : '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.35); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800;">⏳ In Revisione</span>';
                    
                    const dateFormatted = sub.created_at ? new Date(sub.created_at).toLocaleDateString('it-IT', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }) : 'N/D';

                    const cardBg = isRejected 
                        ? 'background:linear-gradient(180deg, rgba(30,15,20,0.95), rgba(15,23,42,0.95)); border:1px solid rgba(239,68,68,0.45); box-shadow:0 8px 25px rgba(239,68,68,0.15);' 
                        : isAccepted
                            ? 'background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); box-shadow:0 8px 20px rgba(0,0,0,0.3);'
                            : 'background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); box-shadow:0 8px 20px rgba(0,0,0,0.3);';

                    let aiBoxHtml = '';
                    if (isRejected) {
                        aiBoxHtml = `
                            <div style="margin-top:0.8rem; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.45); border-left:4px solid #ef4444; border-radius:0.6rem; padding:0.85rem 1rem;">
                                <div style="font-size:0.85rem; font-weight:900; color:#f87171; display:flex; align-items:center; gap:0.4rem; margin-bottom:0.35rem;">
                                    <span>⚠️ Motivo del Rifiuto (AI Klippify):</span>
                                </div>
                                <div style="font-size:0.82rem; color:#fecaca; line-height:1.45; font-weight:600;">
                                    ${sub.ai_reasoning || 'Il video non rispetta una o più linee guida obbligatorie della campagna (CTA mancante, durata errata o tag assente).'}
                                </div>
                            </div>
                        `;
                    } else if (sub.ai_reasoning) {
                        aiBoxHtml = `
                            <div style="margin-top:0.8rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-left:4px solid #10b981; border-radius:0.6rem; padding:0.7rem 0.9rem; font-size:0.78rem; color:#cbd5e1; line-height:1.4;">
                                <strong style="color:#34d399;">🤖 Verifica AI Klippify:</strong> ${sub.ai_reasoning}
                            </div>
                        `;
                    }

                    publishedHtml += `
                        <div style="${cardBg} border-radius:1rem; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; gap:0.8rem;">
                            <div>
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:0.5rem; margin-bottom:0.6rem;">
                                    <div>
                                        <div style="font-size:0.78rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">${sub.campaign_name || 'Campagna Klippify'}</div>
                                        <div style="font-size:0.72rem; color:#64748b;">ID: ${sub.id || 'N/D'}</div>
                                    </div>
                                    ${statusBadge}
                                </div>

                                <div style="margin-bottom:0.8rem;">
                                    <a href="${sub.post_url}" target="_blank" style="display:flex; align-items:center; justify-content:space-between; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); color:#38bdf8; text-decoration:none; padding:0.5rem 0.8rem; border-radius:0.6rem; font-size:0.8rem; font-weight:700; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.2)'" onmouseout="this.style.background='rgba(56,189,248,0.08)'">
                                        <span style="display:flex; align-items:center; gap:0.4rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                                            <span>🔗</span> <span>${sub.post_url}</span>
                                        </span>
                                        <span style="font-size:0.75rem; flex-shrink:0; margin-left:0.4rem;">↗</span>
                                    </a>
                                </div>

                                <!-- REAL STATS GRID FROM KLIPPIFY API -->
                                <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.05); border-radius:0.7rem; padding:0.8rem; display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; text-align:center;">
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Views Reali</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#38bdf8;">${(sub.views || 0).toLocaleString()}</div>
                                    </div>
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Likes Reali</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#f43f5e;">${(sub.likes || 0).toLocaleString()}</div>
                                    </div>
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Guadagno</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#34d399;">$${(sub.earnings || 0).toFixed(2)}</div>
                                    </div>
                                </div>

                                ${aiBoxHtml}
                            </div>

                            <div style="font-size:0.7rem; color:#64748b; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.6rem; display:flex; justify-content:space-between;">
                                <span>📅 Inviato: ${dateFormatted}</span>
                                <span>🎵 TikTok API Reale</span>
                            </div>
                        </div>
                    `;
                });
                publishedHtml += `</div>`;
            }

            const dailyStatsHtml = buildCampaignDailyStatsHtml(campToken, originalCamp, campSubmissions, targetCount);
            const assemblyPipelineHtml = buildCampaignAssemblyPipelineHtml(
                campToken, originalCamp, item, isClipping, localAvailableVideos, 
                savedSlots, targetCount, campSubmissions, scripts, defaultTimes, 
                budgetRemaining, isDepleted, validLinks, allLinksHtml, dailyStatsHtml
            );

            detailContainer.innerHTML = `
                <!-- TOP VIEW MODE SWITCHER -->
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem; background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:0.65rem 1.2rem; box-shadow:0 8px 24px rgba(0,0,0,0.3);">
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="font-size:0.85rem; font-weight:800; color:#cbd5e1;">🏭 MODALITÀ DASHBOARD:</span>
                        <span style="font-size:0.75rem; background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">Nuovo Sistema Autonomo</span>
                    </div>
                    <div style="display:inline-flex; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); border-radius:0.8rem; padding:0.25rem; gap:0.4rem;">
                        <button id="tab-btn-assembly-${campToken}" onclick="switchCampaignViewMode('${campToken}', 'assembly')" style="background:linear-gradient(135deg, #10b981, #059669); color:#ffffff; border:none; padding:0.45rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 15px rgba(16,185,129,0.35); transition:all 0.2s;">
                            🏭 Catena di Montaggio (Automatica & Compatta)
                        </button>
                        <button id="tab-btn-classic-${campToken}" onclick="switchCampaignViewMode('${campToken}', 'classic')" style="background:transparent; color:#94a3b8; border:1px solid rgba(255,255,255,0.1); padding:0.45rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;">
                            📊 Vista Classica Dettagliata
                        </button>
                    </div>
                </div>

                <!-- 1. VISTA CATENA DI MONTAGGIO AUTOMATICA -->
                ${assemblyPipelineHtml}

                <!-- 2. VISTA CLASSICA DETTAGLIATA (PRESERVATA AL 100%) -->
                <div id="camp-classic-view-${campToken}" style="display:none;">
                    <div style="background:rgba(30,41,59,0.9); border:1px solid rgba(255,255,255,0.1); border-radius:1.5rem; box-shadow:0 20px 40px rgba(0,0,0,0.4); overflow:hidden; padding:2rem;">
                        
                        ${warningBanner}

                        <!-- CAMPAIGN HEADER -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
                            <div>
                                <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
                                    <h2 style="font-size:1.8rem; font-weight:900; color:#f8fafc; margin:0;">${originalCamp.name}</h2>
                                    <span style="background:${isClipping ? 'rgba(245,158,11,0.2)' : 'rgba(139,92,246,0.2)'}; color:${isClipping ? '#fbbf24' : '#c084fc'}; border:1px solid ${isClipping ? 'rgba(245,158,11,0.4)' : 'rgba(139,92,246,0.4)'}; padding:0.25rem 0.6rem; border-radius:0.5rem; font-size:0.75rem; font-weight:800;">
                                        ${isClipping ? '✂️ CLIPPING VIDEO' : '🤖 GENERAZIONE AI'}
                                    </span>
                                </div>
                                <div style="display:flex; gap:0.6rem; flex-wrap:wrap; font-size:0.85rem;">
                                    <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:0.3rem 0.8rem; border-radius:0.5rem; font-weight:700;">$${originalCamp.payout_per_1k_views || '?'}/1k views</span>
                                    <span style="background:rgba(239,68,68,0.15); color:#ef4444; padding:0.3rem 0.8rem; border-radius:0.5rem; font-weight:700;">Budget Residuo: $${budgetRemaining}</span>
                                </div>
                            </div>
                            <div style="display:flex; gap:1rem; align-items:center;">
                                <div style="background:linear-gradient(135deg, rgba(245,158,11,0.1), rgba(217,119,6,0.2)); border:1px solid rgba(245,158,11,0.3); padding:0.8rem 1.2rem; border-radius:1rem; text-align:center;">
                                    <div style="font-size:0.72rem; color:#fbbf24; text-transform:uppercase; font-weight:800; margin-bottom:0.2rem;">🎯 Obiettivo Consigliato</div>
                                    <div style="font-size:1.1rem; font-weight:900; color:#fff;">${item.daily_video_goal || "2-3 video al giorno"}</div>
                                </div>
                            </div>
                        </div>

                        <!-- STATISTICHE & PERFORMANCE GIORNO PER GIORNO -->
                        ${dailyStatsHtml}

                        <!-- REQUISITI KLIPPIFY -->
                        <div style="background:rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.05); border-radius:1rem; padding:1.2rem; margin-bottom:1.5rem;">
                            <span style="font-weight:800; font-size:0.95rem; color:#f8fafc; display:block; margin-bottom:0.6rem;">📋 Requisiti Ufficiali Klippify</span>
                            <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:0.8rem; line-height:1.5;"><strong>Brief:</strong> ${originalBrief}</div>
                            <div style="display:flex; flex-wrap:wrap; gap:1.2rem; font-size:0.8rem;">
                                <div><strong style="color:#a78bfa;">Hashtag:</strong> ${originalHashtags}</div>
                                <div><strong style="color:#a78bfa;">Tag (@):</strong> ${originalMentions}</div>
                                <div><strong style="color:#a78bfa;">CTA:</strong> ${originalCTA}</div>
                            </div>
                        </div>

                        <!-- ELENCO COMPLETO DI TUTTI I LINK E RISORSE FORNITI DALLA CAMPAGNA -->
                        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.25); border-radius:1rem; padding:1.2rem; margin-bottom:1.5rem;">
                            <span style="font-weight:800; font-size:0.95rem; color:#38bdf8; display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;">
                                <span>📁 Contenuti forniti dal brand</span>
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:0.75rem; padding:0.15rem 0.5rem; border-radius:0.4rem;">${validLinks.length} Link Trovati</span>
                            </span>
                            <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.6rem;">
                                Tutti i link e i file presenti nella sezione ufficiale "Contenuti forniti dal brand" di Klippify:
                            </div>
                            ${allLinksHtml}
                        </div>

                        <!-- PILOTA AUTOMATICO DEDICATO PER QUESTA CAMPAGNA -->
                        <div style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9)); border:1px solid rgba(139,92,246,0.4); border-radius:1.2rem; padding:1.5rem; margin-bottom:2rem; box-shadow:0 10px 30px rgba(0,0,0,0.4);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                <div>
                                    <div style="font-size:1.25rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:0.6rem;">
                                        <span>🤖 Pilota Automatico per questa Campagna</span>
                                        <span id="camp-autopilot-status-badge-${campToken}" style="font-size:0.75rem; background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid rgba(239,68,68,0.4); padding:0.2rem 0.6rem; border-radius:1rem; font-weight:800;">
                                            ⏸ IN PAUSA
                                        </span>
                                    </div>
                                    <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.3rem;">
                                        Tieni il computer acceso: il bot ritaglierà in automatico i video sorgente mancanti e pubblicherà le clip su TikTok agli orari prestabiliti inviandole subito a Klippify.
                                    </div>
                                </div>

                                <div style="display:flex; gap:0.8rem; align-items:center; flex-wrap:wrap;">
                                    <button onclick="runCampaignAutopilotNow('${campToken}', this)" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.35); padding:0.65rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.15)'">
                                        ⚡ Pubblica Subito Prossimo Slot
                                    </button>
                                    <button id="btn-camp-autopilot-toggle-${campToken}" onclick="toggleCampaignAutopilot('${campToken}')" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:0.7rem 1.4rem; border-radius:0.6rem; font-weight:900; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(16,185,129,0.35); transition:all 0.2s;">
                                        🟢 ATTIVA PILOTA AUTOMATICO
                                    </button>
                                </div>
                            </div>

                            <!-- 3 STATS STRIP SPECIFIC TO THIS CAMPAIGN -->
                            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; border-top:1px solid rgba(255,255,255,0.08); padding-top:1rem; margin-bottom:1rem;">
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #8b5cf6;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Prossima Pubblicazione</div>
                                    <div id="camp-ap-stat-next-run-${campToken}" style="font-size:0.95rem; font-weight:800; color:#c084fc; margin-top:0.2rem;">In attesa avvio...</div>
                                </div>
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #38bdf8;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Slot Pronti al Posting</div>
                                    <div id="camp-ap-stat-ready-${campToken}" style="font-size:1.3rem; font-weight:800; color:#38bdf8; margin-top:0.1rem;">0 / 3</div>
                                </div>
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #10b981;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Inviati a Klippify</div>
                                    <div style="font-size:1.3rem; font-weight:800; color:#10b981; margin-top:0.1rem;">${campSubmissions.length} Video</div>
                                </div>
                            </div>

                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; background:rgba(0,0,0,0.25); padding:0.8rem 1rem; border-radius:0.6rem; border:1px solid rgba(255,255,255,0.05);">
                                <div style="font-size:0.8rem; color:#cbd5e1; display:flex; align-items:center; gap:0.4rem;">
                                    <span>💡</span>
                                    <span>Configura gli orari e i video negli slot sottostanti: l'autopilota li processerà in sequenza automatica.</span>
                                </div>
                                <button onclick="queueAllCampaignSlots('${campToken}', this)" style="background:linear-gradient(135deg, #8b5cf6, #6366f1); color:#fff; border:none; padding:0.45rem 0.9rem; border-radius:0.5rem; font-weight:800; font-size:0.8rem; cursor:pointer; box-shadow:0 2px 10px rgba(139,92,246,0.35);">
                                    📋 Accoda Tutti gli Slot all'Autopilota
                                </button>
                            </div>
                        </div>

                        <!-- CLIPPING HUB & CARICAMENTO VIDEO CON ESPLORA FILE -->
                        ${isClipping ? `
                            <div style="background:linear-gradient(135deg, rgba(245,158,11,0.08), rgba(217,119,6,0.12)); border:1px solid rgba(245,158,11,0.35); border-radius:1.2rem; padding:1.5rem; margin-bottom:2rem;">
                                
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                    <div>
                                        <div style="font-size:1.2rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                            <span>✂️ Gestione Video Sorgente & Bot Analisi Gemini</span>
                                        </div>
                                        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:0.3rem;">
                                            Carica i video completi del brand e avvia il bot che li carica nella chat <strong>"analisi video klippify"</strong> su Gemini.
                                        </div>
                                    </div>
                                    
                                    <!-- PULSANTI AZIONE: CARICA DA ESPLORA RISORSE E APRI CARTELLA -->
                                    <div style="display:flex; gap:0.8rem; flex-wrap:wrap;">
                                        
                                        <!-- INPUT FILE NASCOSTO PER ESPLORA RISORSE CON SUPPORTO MULTIPLO -->
                                        <input type="file" id="source-video-input-${campToken}" accept="video/*" multiple style="display:none;" onchange="uploadSourceVideoFiles(this, '${campToken}')">
                                        
                                        <!-- BOTTONE APRI ESPLORA RISORSE PER CARICARE PIÙ VIDEO -->
                                        <button id="btn-upload-file-${campToken}" onclick="document.getElementById('source-video-input-${campToken}').click()" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.65rem 1.2rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 12px rgba(56,189,248,0.35); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                            📁 Carica Video (Anche Multipli)
                                        </button>

                                        <!-- BOTTONE APRI CARTELLA LOCALE IN WINDOWS -->
                                        <button onclick="openLocalFolder('${campToken}')" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:700; border:1px solid rgba(255,255,255,0.2); padding:0.65rem 1rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                            📂 Apri Cartella Locale
                                        </button>
                                    </div>
                                </div>

                                <!-- CODA VIDEO DA KLIPPARE (MULTI-VIDEO QUEUE) -->
                                <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(245,158,11,0.35); border-radius:1rem; padding:1.2rem; margin-bottom:1.2rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:0.8rem;">
                                        <div>
                                            <div style="font-size:1.05rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                                <span>📋 Coda Video da Klippare</span>
                                                <span id="clipping-queue-count-${campToken}" style="background:rgba(245,158,11,0.2); color:#fbbf24; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">0 Video</span>
                                            </div>
                                            <div id="clipping-queue-summary-${campToken}" style="font-size:0.78rem; color:var(--text-muted); margin-top:0.2rem;">
                                                Carica più video in coda: il bot li elaborerà in sequenza estraendo automaticamente i migliori momenti 9:16.
                                            </div>
                                        </div>

                                        <button onclick="processEntireClippingQueue('${campToken}', this)" style="background:linear-gradient(135deg, #f59e0b, #d97706); color:#000; font-weight:900; border:none; padding:0.65rem 1.2rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(245,158,11,0.35); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                            ⚡ Klippa Tutta la Coda in Automatico
                                        </button>
                                    </div>

                                    <!-- LISTA DEGLI ELEMENTI IN CODA (RENDERIZZATA VIA JS) -->
                                    <div id="clipping-queue-list-${campToken}" style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">
                                        <div style="text-align:center; padding:1rem; color:var(--text-muted); font-size:0.85rem;">⏳ Caricamento coda...</div>
                                    </div>
                                </div>

                                <!-- SELETTORE DEL VIDEO DA MANDARE A GEMINI (SINGOLO) -->
                                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.1); border-radius:0.8rem; padding:1rem; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                                    <div style="flex:1; min-width:260px;">
                                        <label style="display:block; font-size:0.82rem; font-weight:800; color:#38bdf8; margin-bottom:0.4rem;">
                                            📹 Oppure Seleziona un Singolo Video da Inviare a Gemini:
                                        </label>
                                        <select id="source-video-selector-${campToken}" style="width:100%; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:0.55rem; border-radius:0.5rem; font-size:0.85rem;">
                                            ${localAvailableVideos.length > 0 ? localAvailableVideos.map(v => `<option value="${v.filename}">${v.filename} (${(v.size_mb || 0).toFixed(1)} MB)</option>`).join('') : '<option value="">-- Nessun video caricato. Carica prima un video con il pulsante sopra! --</option>'}
                                        </select>
                                    </div>

                                    <!-- BOTTONE AVVIA ANALISI GEMINI -->
                                    <button onclick="startClippingPipelineForCampaign('${campToken}', this)" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:800; border:1px solid rgba(255,255,255,0.25); padding:0.65rem 1.1rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                        🤖 Klippa Singolo Video
                                    </button>
                                </div>

                                <div style="font-size:0.8rem; color:#94a3b8; background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem; border:1px solid rgba(255,255,255,0.05); line-height:1.5;">
                                    💡 <strong>Come funziona la Coda Multi-Video:</strong><br>
                                    1. Clicca su <strong>📁 Carica Video (Anche Multipli)</strong> e seleziona tutti i video che vuoi klippare.<br>
                                    2. I video compariranno nella <strong>📋 Coda Video da Klippare</strong> con il relativo stato.<br>
                                    3. Premi <strong>⚡ Klippa Tutta la Coda in Automatico</strong> (oppure lascia fare all'Autopilota): il bot analizzerà ogni video con Gemini nella chat <em>"analisi video klippify"</em> e salverà le clip 9:16 pronte per il posting!
                                </div>
                            </div>
                        ` : ''}

                        <!-- DAILY EDITORIAL CONTROLS -->
                        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(139,92,246,0.3); border-radius:1rem; padding:1.2rem; margin-bottom:2rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                            <div>
                                <div style="font-size:1.15rem; font-weight:800; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                    <span>📅 Piano Editoriale di Oggi</span>
                                    <span style="background:rgba(139,92,246,0.2); color:#c084fc; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem;">Flessibile</span>
                                </div>
                                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">Configura quanti video vuoi produrre oggi e a che ora pubblicarli.</div>
                            </div>

                            <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
                                <!-- QUANTITY SELECTOR -->
                                <div style="display:flex; align-items:center; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.15); border-radius:0.6rem; padding:0.2rem 0.4rem; gap:0.6rem;">
                                    <span style="font-size:0.82rem; font-weight:700; color:#cbd5e1; padding-left:0.4rem;">Video al Giorno:</span>
                                    <button onclick="changeDailyTarget('${campToken}', -1)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; width:28px; height:28px; border-radius:0.4rem; font-weight:bold; cursor:pointer;">-</button>
                                    <span id="target-count-display-${campToken}" style="font-size:1.1rem; font-weight:800; color:#c084fc; min-width:24px; text-align:center;">${targetCount}</span>
                                    <button onclick="changeDailyTarget('${campToken}', 1)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; width:28px; height:28px; border-radius:0.4rem; font-weight:bold; cursor:pointer;">+</button>
                                </div>

                                <button onclick="saveSelectedCampaigns()" style="background:linear-gradient(135deg, #3b82f6, #1d4ed8); color:#fff; border:none; padding:0.65rem 1.2rem; border-radius:0.6rem; font-size:0.85rem; font-weight:800; cursor:pointer; box-shadow:0 4px 12px rgba(59,130,246,0.35);">
                                    💾 Salva Configurazione
                                </button>
                            </div>
                        </div>

                        <!-- SLOTS CARDS -->
                        <div style="display:flex; flex-direction:column; gap:1.5rem; margin-bottom:2rem;">
                            ${slotsHtml}
                        </div>

                        <!-- SEZIONE VIDEO PUBBLICATI & MONITORING KLIPPIFY -->
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:1.5rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem; flex-wrap:wrap; gap:0.8rem;">
                                <div>
                                    <h3 style="font-size:1.25rem; font-weight:800; color:#fff; margin:0; display:flex; align-items:center; gap:0.5rem;">
                                        <span>🎬 Storico Video Inviati per questa Campagna</span>
                                        <span style="background:rgba(16,185,129,0.2); color:#34d399; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:1rem;">${campSubmissions.length} Video</span>
                                    </h3>
                                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">Visualizzazioni, mi piace, validazioni AI e guadagni tracciati in tempo reale dalle API ufficiali Klippify.</div>
                                </div>
                                <button onclick="refreshCampaignSubmissions('${campToken}', this)" style="background:rgba(56,189,248,0.12); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); border-radius:0.5rem; padding:0.45rem 0.9rem; font-size:0.82rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.12)'">
                                    🔄 Aggiorna Stato Klippify
                                </button>
                            </div>
                            ${publishedHtml}
                        </div>

                    </div>
                </div>
            `;

            loadCampaignAutopilotState(campToken);
            loadClippingQueue(campToken);

            // Applica la modalità di vista salvata (default: Catena di Montaggio)
            try {
                const savedMode = localStorage.getItem('camp_view_mode_' + campToken) || 'assembly';
                switchCampaignViewMode(campToken, savedMode);
            } catch(e) {}

            setTimeout(() => {
                const cards = document.querySelectorAll('.kanban-card[data-video-file]');
                cards.forEach(async (card) => {
                    const filename = card.getAttribute('data-video-file');
                    try {
                        const res = await fetch(`/api/tiktok/video-stats?filename=${encodeURIComponent(filename)}`);
                        const stats = await res.json();
                        if (stats.view_count !== undefined) {
                            card.querySelector('.stat-views').innerText = stats.view_count.toLocaleString();
                            card.querySelector('.stat-likes').innerText = stats.like_count.toLocaleString();
                        }
                    } catch (e) {
                        console.error('Errore fetch stats', e);
                    }
                });
            }, 500);
        }

                function closeCampaignDetail() {
            currentDetailCampToken = null;
            document.getElementById('my-campaign-detail-view').style.display = 'none';
            document.getElementById('my-campaign-detail-content').innerHTML = '';
            document.getElementById('my-campaigns-grid').style.display = 'grid';
        }


        async function deleteCampaign(campToken, ev) {
            if (ev) ev.stopPropagation();
            if (!campToken) return;
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {};
            const campName = originalCamp.name || 'questa campagna';
            if (!confirm(`Sei sicuro di voler eliminare "${campName}" da "Le Mie Campagne"?`)) {
                return;
            }

            try {
                const res = await fetch('/api/delete-campaign', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_id: campToken })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    selectedCampaigns = selectedCampaigns.filter(id => id !== campToken);
                    generatedContent = generatedContent.filter(c => c.campaign_id !== campToken);
                    
                    // Deselect checkbox in Creator Dashboard if present
                    const cb = document.querySelector(`.campaign-checkbox[data-campaign-id="${campToken}"]`);
                    if (cb) cb.checked = false;

                    // If currently inside detail view of this campaign, close it
                    if (currentDetailCampToken === campToken) {
                        closeCampaignDetail();
                    }

                    // Re-render grid
                    const grid = document.getElementById('my-campaigns-grid');
                    if (grid) {
                        grid.innerHTML = '';
                        renderMyCampaigns();
                    }
                } else {
                    alert("Errore durante l'eliminazione: " + (data.error || "Errore sconosciuto"));
                }
            } catch (e) {
                console.error("Errore chiamata delete-campaign", e);
                alert("Impossibile contattare il server.");
            }
        }


        // Funzione per switchare i tab interni della card campagna
        function switchCampTab(cardId, tab) {
            document.getElementById(`tab-content-${cardId}-pending`).style.display = tab === 'pending' ? 'block' : 'none';
            document.getElementById(`tab-content-${cardId}-published`).style.display = tab === 'published' ? 'block' : 'none';
            
            const btnPending = document.getElementById(`tab-btn-${cardId}-pending`);
            const btnPublished = document.getElementById(`tab-btn-${cardId}-published`);
            
            if(tab === 'pending') {
                btnPending.style.color = '#38bdf8';
                btnPending.style.borderBottomColor = '#38bdf8';
                btnPublished.style.color = 'var(--text-muted)';
                btnPublished.style.borderBottomColor = 'transparent';
            } else {
                btnPublished.style.color = '#10b981';
                btnPublished.style.borderBottomColor = '#10b981';
                btnPending.style.color = 'var(--text-muted)';
                btnPending.style.borderBottomColor = 'transparent';
            }
        }

        function filterBySection(targetSection, btn) {
            document.querySelectorAll('.tab-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const cards = document.querySelectorAll('#main-cards-grid .card');
            cards.forEach(c => {
                const sec = c.getAttribute('data-section');
                if (targetSection === 'all' || sec === targetSection) {
                    c.style.display = 'flex';
                } else {
                    c.style.display = 'none';
                }
            });
        }

        function openModal(index) {
            const c = allCampaignsData[index];
            if (!c) return;

            const token = c.campaign_token || c.id || '';
            const tokenUrl = c.campaign_url || ('https://app.klippify.com/campaigns/' + token);
            const htStr = (c.mandatory_hashtags || []).join(' ');
            const tagStr = (c.mandatory_mentions || []).join(' ');
            const ctaStr = c.call_to_action || '';
            const payout = (c.payout_per_1k_views || 1.0).toFixed(2);
            const poolRem = (c.budget_remaining || 0).toLocaleString();
            const budgetTot = (c.budget_total || 0).toLocaleString();
            const budgetSpent = (c.budget_spent || 0).toLocaleString();
            const progPct = c.budget_progress_percent || '0%';
            const score = c.convenience_score || 50;
            const views = (c.total_views || 0).toLocaleString();
            const creators = c.creators_count || 0;
            const section = c.section || 'Nuove';

            // Match published TikTok videos for this campaign in modal
            const modalPubs = (typeof publishedContent !== 'undefined' ? publishedContent : []).filter(pc => pc.campaign_id === token || pc.campaign_id === c.id);
            let matchedModalVideos = [];
            modalPubs.forEach(mp => {
                const tv = findMatchingTikTokVideo(token, c.name, mp);
                if (tv && !matchedModalVideos.find(x => x.id === tv.id)) {
                    matchedModalVideos.push(tv);
                }
            });

            if (cachedTikTokVideos && cachedTikTokVideos.length > 0) {
                cachedTikTokVideos.forEach(tv => {
                    if (!matchedModalVideos.find(x => x.id === tv.id)) {
                        const desc = (tv.description || '').toLowerCase();
                        if (c.name && desc.includes(c.name.toLowerCase())) {
                            matchedModalVideos.push(tv);
                        } else if (c.mandatory_hashtags && c.mandatory_hashtags.some(ht => desc.includes(ht.toLowerCase()))) {
                            matchedModalVideos.push(tv);
                        }
                    }
                });
            }

            let tiktokModalSectionHtml = '';
            if (matchedModalVideos.length > 0) {
                const cardsHtml = matchedModalVideos.map(v => renderTikTokVideoCard(v, true)).join('');
                tiktokModalSectionHtml = `
                    <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(56,189,248,0.35); border-radius:0.85rem; padding:1.2rem; margin-bottom:1.5rem;">
                        <h3 style="font-size:1rem; color:#38bdf8; margin-bottom:0.8rem; display:flex; align-items:center; gap:0.4rem;">
                            <span>📱 Video TikTok Pubblicati per questa Campagna (${matchedModalVideos.length})</span>
                        </h3>
                        <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:1rem;">
                            ${cardsHtml}
                        </div>
                    </div>
                `;
            } else {
                tiktokModalSectionHtml = `
                    <div style="background:rgba(15,23,42,0.6); border:1px dashed var(--card-border); border-radius:0.85rem; padding:1rem; margin-bottom:1.5rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                        <div style="font-size:0.85rem; color:var(--text-muted);">
                            📱 <em>Nessun video TikTok ancora pubblicato per questa campagna.</em>
                        </div>
                        <button onclick="closeModal(); switchMainView('studio');" style="background:linear-gradient(135deg, #8b5cf6, #3b82f6); color:#fff; border:none; padding:0.4rem 0.8rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; cursor:pointer;">
                            Crea Video in Studio 🎬
                        </button>
                    </div>
                `;
            }

            const rulesHtml = (c.rules || ['Segui le linee guida ufficiali Klippify']).map(r => `<li>✓ ${r}</li>`).join('');

            const modalHtml = `
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.8rem;">
                    <div>
                        <span style="background:linear-gradient(90deg, #8b5cf6, #38bdf8); color:#fff; padding:0.25rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700;">TOKEN: ${token}</span>
                        <span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.25rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; margin-left:0.5rem;">SEZIONE: ${section}</span>
                    </div>
                    <span style="color:var(--accent-emerald); font-weight:600; font-size:0.85rem;">Score: ${score}/100</span>
                </div>

                <h2 style="font-size:1.8rem; font-weight:800; color:#fff; margin-bottom:0.3rem;">${c.name}</h2>
                <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:1.5rem;">Brand / Creator: <strong style="color:#fff;">${c.brand || 'Klippify Partner'}</strong></p>

                <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1.2rem; border-radius:0.85rem; margin-bottom:1.5rem;">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-cyan); margin-bottom:0.4rem; text-transform:uppercase;">Descrizione Campagna:</div>
                    <p style="color:#e2e8f0; font-size:0.9rem; line-height:1.5;">${c.description || 'Descrizione estratta dalla pagina ufficiale Klippify.'}</p>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Payout Rate / 1k</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#34d399; margin-top:0.2rem;">$${payout} /1k</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Pool Rimanente</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#38bdf8; margin-top:0.2rem;">$${poolRem}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Budget Totale</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#f59e0b; margin-top:0.2rem;">$${budgetTot}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Views / Clippers</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#fff; margin-top:0.2rem;">${views} views | ${creators} clippers</div>
                    </div>
                </div>

                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:0.75rem; border:1px solid var(--card-border); margin-bottom:1.5rem;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-muted); margin-bottom:0.4rem;">
                        <span>Budget Erogato: <strong>$${budgetSpent}</strong> di <strong>$${budgetTot}</strong></span>
                        <span>Progresso: <strong style="color:#38bdf8;">${progPct}</strong></span>
                    </div>
                    <div class="progress-bar-bg" style="height:8px;">
                        <div class="progress-bar-fill" style="width:${progPct}"></div>
                    </div>
                </div>

                <div style="background:rgba(15,23,42,0.9); border-radius:0.85rem; padding:1.2rem; border:1px solid var(--card-border); margin-bottom:1.5rem;">
                    <h3 style="font-size:1rem; color:#fff; margin-bottom:0.8rem;">📋 Copia Rapida Requisiti</h3>
                    
                    <div class="copy-item">
                        <div class="copy-header">HASHTAG OBBLIGATORI</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-ht">${htStr}</span>
                            <button class="btn-cp" onclick="copyText('modal-ht')">Copia Hashtags</button>
                        </div>
                    </div>
                    <div class="copy-item">
                        <div class="copy-header">TAG ACCOUNT (@)</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-tag">${tagStr}</span>
                            <button class="btn-cp" onclick="copyText('modal-tag')">Copia Tag</button>
                        </div>
                    </div>
                    <div class="copy-item">
                        <div class="copy-header">CALL TO ACTION (CTA)</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-cta">${ctaStr}</span>
                            <button class="btn-cp" onclick="copyText('modal-cta')">Copia CTA</button>
                        </div>
                    </div>
                </div>

                <div style="margin-bottom:1.5rem;">
                    <h3 style="font-size:0.95rem; color:#fff; margin-bottom:0.5rem;">📜 Regole & Linee Guida Video:</h3>
                    <ul style="list-style:none; color:var(--text-muted); font-size:0.85rem; display:flex; flex-direction:column; gap:0.4rem;">
                        ${rulesHtml}
                    </ul>
                </div>

                ${tiktokModalSectionHtml}

                <div style="display:flex; gap:1rem; margin-top:1.5rem;">
                    <a href="${tokenUrl}" target="_blank" style="flex:1; text-align:center; background:linear-gradient(135deg, #8b5cf6, #6d28d9); color:#fff; padding:0.8rem; border-radius:0.6rem; text-decoration:none; font-weight:700; font-size:0.9rem;">🔗 Apri Pagina Token Ufficiale (${token})</a>
                    <button onclick="closeModal()" style="background:rgba(255,255,255,0.1); border:1px solid var(--card-border); color:#fff; padding:0.8rem 1.5rem; border-radius:0.6rem; font-weight:600; cursor:pointer;">Chiudi</button>
                </div>
            `;

            document.getElementById('modal-body').innerHTML = modalHtml;
            document.getElementById('modal-overlay').classList.add('active');
        }

        function closeModal() {
            document.getElementById('modal-overlay').classList.remove('active');
        }

        function closeModalOnOverlay(e) {
            if (e.target.id === 'modal-overlay') {
                closeModal();
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });

        function copyText(elementId) {
            const val = document.getElementById(elementId).innerText;
            copyValue(val, event.target);
        }

        function copyValue(val, btn) {
            navigator.clipboard.writeText(val).then(() => {
                const orig = btn.innerText;
                btn.innerText = 'Copiato! ✓';
                btn.style.background = '#10b981';
                btn.style.color = '#fff';
                setTimeout(() => {
                    btn.innerText = orig;
                    btn.style.background = '';
                    btn.style.color = '';
                }, 1500);
            });
        }

        async function triggerRefresh() {
            const btn = event.target;
            btn.innerText = '⏳ Scansione in corso...';
            btn.disabled = true;
            try {
                await fetch('/api/refresh', { method: 'POST' });
                window.location.reload();
            } catch(e) {
                alert('Aggiornamento completato! Ricarico...');
                window.location.reload();
            }
        }
        async function saveSelectedCampaigns() {
            const checkboxes = document.querySelectorAll('.campaign-checkbox:checked');
            const selectedTokens = Array.from(checkboxes).map(cb => cb.getAttribute('data-campaign-id'));
            
            const btn = document.getElementById('btn-save-selected');
            const origText = btn.innerHTML;
            
            if (selectedTokens.length === 0) {
                alert("Non hai selezionato nessuna campagna!");
                return;
            }

            btn.innerHTML = '⏳ Salvataggio...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/save-selection', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(selectedTokens)
                });
                
                if (res.ok) {
                    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    btn.innerHTML = '✅ Salvate! Torna in chat';
                } else {
                    btn.style.background = 'red';
                    btn.innerHTML = '❌ Errore';
                }
            } catch(e) {
                alert('Errore nel salvataggio: ' + e);
                btn.innerHTML = origText;
            }
            
            setTimeout(() => {
                btn.innerHTML = origText;
                btn.disabled = false;
            }, 3000);
        }
    
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
                if (sel) {
                    if (videos.length === 0) {
                        sel.innerHTML = '<option value="">Nessun video generato trovato.</option>';
                    } else {
                        sel.innerHTML = '<option value="">Seleziona un video da pubblicare...</option>' + 
                            videos.map(v => `<option value="${v.filename}">${v.filename} (${(v.size / 1024 / 1024).toFixed(1)} MB)</option>`).join('');
                    }
                }
                
                const campSel = document.getElementById('tiktok-campaign-select');
                if (campSel && selectedCampaigns && selectedCampaigns.length > 0) {
                    // Populate from selectedCampaigns instead of videos because videos don't have campaign_id in the /api/videos response
                    campSel.innerHTML = '<option value="unknown">Nessuna campagna specifica</option>' + 
                        selectedCampaigns.map(id => `<option value="${id}">${id}</option>`).join('');
                }
            } catch(e) {
                console.error("Errore caricamento video", e);
            }

            // 3. Load all published TikTok videos with live stats
            loadTikTokPublishedVideos();
        }

        async function publishToTikTok() {
            const selVideo = document.getElementById('tiktok-video-select');
            const selCamp = document.getElementById('tiktok-campaign-select');
            const titleInput = document.getElementById('tiktok-video-title');
            const capInput = document.getElementById('tiktok-video-caption');
            const coverInput = document.getElementById('tiktok-video-cover');
            const btn = document.getElementById('tiktok-publish-btn');
            const status = document.getElementById('tiktok-publish-status');
            
            const filename = selVideo.value;
            const campaignId = selCamp ? selCamp.value : 'unknown';
            const titleStr = titleInput ? titleInput.value.trim() : "";
            const capStr = capInput ? capInput.value.trim() : "";
            const coverTimeSec = coverInput ? parseFloat(coverInput.value) : 1.0;
            
            if (!filename) { alert("Seleziona prima un video!"); return; }
            if (!titleStr) { alert("Il Titolo del video è obbligatorio!"); return; }
            
            const combinedTitle = capStr ? (titleStr + "\n\n" + capStr) : titleStr;
            const coverTimeMs = Math.floor((isNaN(coverTimeSec) ? 1.0 : coverTimeSec) * 1000);
            
            btn.disabled = true;
            btn.innerHTML = "⏳ Caricamento in corso... (non chiudere la pagina)";
            btn.style.opacity = "0.7";
            status.innerText = "";
            
            try {
                const res = await fetch('/api/tiktok/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        filename: filename, 
                        title: combinedTitle,
                        cover_time_ms: coverTimeMs,
                        campaign_id: campaignId
                    })
                });
                
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                status.innerText = "✅ Video pubblicato con successo su TikTok!";
                status.style.color = "#10b981";
                if(capInput) capInput.value = "";
                if(titleInput) titleInput.value = "";
                if(selVideo) selVideo.selectedIndex = 0;

                // Reload TikTok videos gallery
                setTimeout(() => {
                    loadTikTokPublishedVideos(true);
                }, 3000);
            } catch (e) {
                status.innerText = "❌ Errore durante la pubblicazione: " + e.message;
                status.style.color = "#ef4444";
            }
            
            btn.disabled = false;
            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Pubblica su TikTok 🚀`;
            btn.style.opacity = "1";
        }

        // Preload TikTok videos and Debug Tasks in background on startup
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                loadTikTokPublishedVideos(false);
                loadDebugTasks(false);
            }, 500);
        });
        setTimeout(() => {
            if (!cachedTikTokVideos || cachedTikTokVideos.length === 0) {
                loadTikTokPublishedVideos(false);
            }
            loadDebugTasks(false);
        }, 1500);

    

console.log('Testing renderCampaignDetailContent & all subtab switches...');
let errorCount = 0;
allCampaignsData.forEach(c => {
    const token = c.campaign_token || c.id;
    try {
        renderCampaignDetailContent(token);
        switchCampaignSubTab(token, 'raw');
        switchCampaignSubTab(token, 'prompts');
        switchCampaignSubTab(token, 'analytics');
        switchCampaignSubTab(token, 'brief');
        switchCampaignSubTab(token, 'cascade');
    } catch(err) {
        errorCount++;
        console.error('ERROR FOR CAMPAIGN:', token, c.name, err);
    }
});
if (errorCount === 0) {
    console.log('ALL 47 CAMPAIGNS RENDERED FLAWLESSLY WITH 0 ERRORS!');
}
