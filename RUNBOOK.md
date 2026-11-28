# Slow Fox – manuale operativo (ogni esecuzione parte da zero: leggilo tutto)

Canale TikTok @SlowFox_Original, italiano, educazione finanziaria / mentalità. 1 video al giorno, ~55 s, 11-12 frasi,
una scena animata per ogni frase. Voce: Speko/Cartesia "Giancarlo". Utente: Alessio.

## Stato e dove vivono i file
Tutto sta nel repository GitHub albuzzialessio/slowfox-media (nessun PC necessario): `pipeline/` (codice + episodes/), `state.json`
(`next_episode`, `published`, note), `RUNBOOK.md`, `inbox/` (video temporaneo). Setup di ogni esecuzione:
1. `mcp__claude-code-remote__add_repo` {owner:"albuzzialessio",repo:"slowfox-media",access:"push"}, poi UN solo `git clone --depth 1 https://github.com/albuzzialessio/slowfox-media /home/claude/slowfox-media` (timeout 10 min).
2. `pip install --break-system-packages skia-python numpy soundfile`; ffmpeg e font Poppins (/usr/share/fonts/truetype/google-fonts) sono già presenti. Copia `pipeline/` in /home/claude/tiktok e lavora lì.
3. A fine lavoro aggiorna state.json, commit + push (con le righe Co-Authored-By richieste dal sistema).
Episodi già fatti: vedi `published` in state.json. Argomenti 4-30 (gli episodi 2 e 3 hanno già il JSON in pipeline/episodes/):
4. ABBONAMENTI (tema red)
5. ACQUISTI (tema purple)
6. PAGA TE STESSO (tema gold)
7. INFLAZIONE (tema blue)
8. REGOLA DEL 72 (tema green)
9. DISCIPLINA (tema red)
10. REGOLA DEI 2 MINUTI (tema purple)
11. CRESCITA (tema gold)
12. SOCIAL (tema blue)
13. LIFESTYLE CREEP (tema red)
14. DEBITI (tema purple)
15. DIVERSIFICARE (tema green)
16. COSTO IN ORE (tema gold)
17. ENTRATE (tema blue)
18. MINDSET (tema red)
19. ROUTINE SERALE (tema purple)
20. PRIORITÀ (tema gold)
21. IDENTITÀ (tema blue)
22. COMFORT ZONE (tema green)
23. SPESA INTELLIGENTE (tema red)
24. OBIETTIVI (tema purple)
25. ENERGIA (tema gold)
26. STUDIO (tema blue)
27. NO (tema red)
28. PIANIFICA (tema green)
29. GRATITUDINE (tema purple)
30. INIZIA OGGI (tema gold)

## Setup (sandbox nuova)
1. device_stage_files del file `SlowFox\slowfox_pipeline.zip` e di state.json → unzip in /home/claude/tiktok
2. `pip install --break-system-packages skia-python numpy soundfile` ; ffmpeg deve esistere; font Poppins in /usr/share/fonts/truetype/google-fonts
3. Test rapido: `python3 -c "import scenes"`

## 1. Scrivi l'episodio (episodes/NN.json)
Chiavi: id, tag (pillola in alto, MAIUSCOLO breve), theme (gold|blue|green|red|purple), sentences, caption, post, scenes.
- sentences: 11-12 frasi, totale ~130-150 parole (≈55 s). Elemento = "testo" oppure ["testo mostrato","testo letto"]
  (numeri/percentuali scritti per esteso nel testo letto: "il 30%" → "il trenta per cento"). Prima frase = hook forte.
  Ultima frase = invito a salvare/commentare/seguire. Solo calcoli verificabili e regole note, niente statistiche inventate,
  niente promesse di guadagno; se parli di investimenti: "esempio ipotetico, non è consulenza finanziaria".
- scenes: lista lunga come sentences, ogni voce [tipo, parametri]. Una scena pertinente a ciò che dice la frase.
  Tipi (vedi episodes/01-03.json per esempi reali, copia da lì):
  bignum{from,to,suf,pre,txt,label,sub,icon,size,warn} · question{lines:[..2 righe..]} · donut{parts:[[nome,%,colore_idx]..],hl,center,csub,anim,icons:[[icona,etichetta]..]}
  bars{items:[[nome,valore,colore_idx]..],suf,title,sub,max} · pairbars{groups,reveal,la,lb} · growth{la,lb} · list{items:[[check|cross,testo]..],title}
  icons{items:[[icona,etichetta]..],title,sub} · split{l:{icon,title,value,sub,good},r:{..},foot} · calendar{marks:[[giorni,[r,g,b]]..],label,sub}
  hero{icon,coins,lines:[..]} · words{icon,lines} · cta{title,sub} (ultima scena)
  Icone disponibili: wallet coin house bolt cart car piggy shield chartup briefcase medical gamepad bag star check cross clock info warn heart bookmark chat user calendar question
  Testi brevi: max ~22 caratteri per riga grande. Alterna tipi diversi (mai due scene uguali di fila salvo donut/pairbars progressivi).
- post: caption TikTok (≤ 150 caratteri di testo + 5-6 hashtag, in italiano, con invito al commento) – es. in episodes/01.json.
- Salva anche `testo_voce_NN.txt`: il testo letto, frasi separate da spazio, per ElevenLabs.

## 2. Voce (Speko, standard del canale: Giancarlo)
Tool mcp__Speko__audio_synthesize (caricalo con ToolSearch "speko"): body = {"text": <testo letto intero, frasi separate da spazio>,
"intent": {"language":"it","optimizeFor":"quality"}, "voice":"029c3c7a-b6d9-44f0-814b-200d849830ff",
"constraints":{"allowedProviders":{"tts":["cartesia:sonic-3.5"]}}}. Il risultato è un file .wav già salvato nella sandbox
(percorso indicato nell'output "saved to ..."): usalo come audio per make_episode.py. ~58 s per 11 frasi. Niente browser, niente ElevenLabs.
Se Speko finisce i crediti gratuiti: avvisa l'utente (PushNotification) e fermati dopo aver lasciato lo script pronto.

## 3. Render
`python3 make_episode.py episodes/NN.json voce.mp3` (≈3 min). Produce out/video_NN_ep.mp4 (qualità piena, ~20 MB),
out/video_NN_ep_upload.mp4 (<3,7 MB, per upload via estensione) e _caption.txt. Controlla un fotogramma (ffmpeg -ss 20 -frames:v 1)
con Read: testi non tagliati, sottotitoli leggibili. Poi device_commit_files in Downloads\SlowFox\video\ :
`SlowFox_NN_<tag>.mp4` e la caption `.txt`; aggiorna state.json.

## 4. Pubblicazione su TikTok (automatica: GitHub + Metricool, nessun intervento dell'utente)
1. Copia `out/video_NN_ep_upload.mp4` in `inbox/video.mp4` del repo, commit + push su main (il repo è pubblico). Verifica con
   `curl -sI https://raw.githubusercontent.com/albuzzialessio/slowfox-media/main/inbox/video.mp4` → 200.
2. Tool Metricool (ToolSearch "metricool"): `createScheduledPost` blogId 8109026, date = ora+7 min (ISO con offset, fuso Europe/Rome),
   info JSON: autoPublish true, media [URL raw], providers [{"network":"tiktok"}], publicationDate {dateTime, timezone:"Europe/Rome"},
   text = caption `post`, tiktokData {privacyOption:"PUBLIC_TO_EVERYONE", title: stessa caption, isAigc:true, disableComment:false,
   disableDuet:false, disableStitch:false, photoCoverIndex:0, autoAddMusic:false, commercialContentThirdParty:false, commercialContentOwnBrand:false}.
   Metricool copia il file nel proprio storage subito: puoi rimuovere `inbox/video.mp4` dal repo (git rm, commit, push) appena la creazione risponde ok.
3. Dopo la data programmata controlla con `getScheduledPosts` e/o https://www.tiktok.com/tiktokstudio/content (browser integrato) che il post sia pubblicato.
   Se fallisce: avvisa l'utente con PushNotification (una riga) e lascia il video in Downloads\SlowFox\video\ se il PC è collegato.
Orario: un video al giorno, programmato verso le 19:00-19:30 Europe/Rome. Non pubblicare mai due volte lo stesso episodio.
Eliminare un post: tiktokstudio/content → ⋯ → Elimina → Elimina (recuperabile 30 giorni).

## Note
- Il video 1 è già online ("REGOLA 50/30/20"). Voce standard: Speko/Cartesia Giancarlo (il video 1 pubblicato con Leo è stato eliminato e rifatto con Giancarlo).
- Mai citare nomi reali dell'utente. Profilo: @SlowFox_Original, bio "Soldi e mentalità, un passo alla volta 🦊 Nuovo video ogni giorno".

## 5. Strategia e apprendimento (il profilo lo gestisci TU, decidi tutto)
L'utente ti ha dato la gestione completa del canale: obiettivo = più visualizzazioni, retention e follower. Ogni esecuzione, PRIMA di scrivere l'episodio:
1. **Misura.** Metricool `getAnalyticsDataByMetrics` (brandId 8109026, network TikTok, connector posts) sugli ultimi 14-30 giorni con le metriche:
   TKPO03 url, TKPO02 data/ora, TKPO05 descrizione, TKPO06 durata, TKPO07 views, TKPO08 likes, TKPO09 commenti, TKPO10 condivisioni, TKPO11 reach,
   TKPO13 % video guardato per intero, TKPO15 tempo medio guardato, TKPO16 views da For You, TKPO18 da hashtag, TKPO21 da ricerca (vedi `getAnalyticsAvailableMetrics`).
   Opzionale: tiktokstudio/content nel browser integrato per sanity check.
2. **Impara.** Aggiorna `learnings.md` (tabella episodio → data/ora → hook → tema → durata → views/likes/commenti/condivisioni/% completamento) e
   scrivi 3-5 righe di conclusioni: quali temi, hook, durate, scene e orari rendono di più. Segnali forti = % completamento, tempo medio guardato, condivisioni e salvataggi, poi views.
   Con pochi dati (primi giorni) non trarre conclusioni forzate: varia apposta formati e hook e annota l'esperimento.
3. **Decidi** e applica: argomento (puoi cambiare l'ordine dell'elenco o inventare nuovi temi coerenti col canale se qualcosa funziona di più), tipo di hook
   (domanda, numero shock, errore comune, "smetti di…", confronto), lunghezza (30-60 s: se la completion cala, accorcia), caption, hashtag (mix di 1-2 ampi + 3-4 di nicchia, max 6),
   frequenza (1 video al giorno di default; se i dati mostrano un vantaggio puoi cambiare il numero e l'orario dell'attività con update_trigger, senza prompt se possibile).
4. **Orario.** `getBestTimeToPostByNetwork` (TikTok, giorno di oggi, Europe/Rome) e incrocialo con le ore dei tuoi video migliori. Dati iniziali Metricool (nov 2026, profilo generico):
   nei giorni feriali i picchi sono alle 10:00, 12:00 e 18:00; il weekend 10:00, 12:00 e 18:00-19:00. Default: programma il post tra le 18:00 e le 18:30; prova altri slot
   (12:00, 10:00, 20:00) a rotazione per qualche giorno e confronta i risultati nel learnings.md. Usa lo slot migliore mostrato dai dati reali del canale appena sono sufficienti.
5. **Contenuto.** Mantieni accuratezza (solo regole e calcoli verificabili, niente promesse di guadagno, niente consulenza finanziaria personalizzata), niente contenuti ingannevoli, etichetta IA sempre attiva.
   Primi 2 secondi = hook forte; una scena diversa per frase; sottotitoli sempre; chiudi con una domanda per i commenti. Rispondere ai commenti non è possibile via Metricool: se vedi commenti rilevanti, segnalalo nel riepilogo.
6. **Riepilogo.** Chiudi con una riga per l'utente: episodio, orario, cosa hai imparato/cambiato (es. "ep3 programmato 18:10, hook a domanda, tema X perché Y"). Notifica push solo per problemi o per un risultato davvero notevole.

## 6. Frequenza attuale (dal 28/11/2026): 2 video al giorno
Ogni run (~17:30 Europe/Rome) produce DUE episodi: uno per stasera alle 18:30 (se già passato: +7 min) e uno per domani alle 10:00. Stesso flusso per entrambi (voce → render → inbox/video.mp4 con URL raw per SHA → Metricool). Tra un upload e l'altro basta sovrascrivere inbox/video.mp4 (Metricool copia subito il file). Alla fine `git rm inbox/video.mp4`. Se ci sono pochi crediti Speko, fai almeno l'episodio di domani 10:00.
