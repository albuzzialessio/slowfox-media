# -*- coding: utf-8 -*-
# Una scena per ogni frase, nello stesso ordine di plan2.VIDEOS2[*]["sentences"].
D3 = [("Necessità", 50, 0), ("Per te", 30, 1), ("Da parte", 20, 2)]
CTA = ("cta", dict(title="Ti è servito?", sub="Segui per il prossimo video"))
TAB = [(10, 24, 34), (20, 48, 104), (30, 72, 244)]

SCENES = {
 1: [
  ("bignum", dict(**{"from": 1500}, to=0, suf=" €", label="STIPENDIO CHE SPARISCE", sub="e a fine mese non resta niente", icon="wallet")),
  ("question", dict(lines=["DOVE FINISCONO", "I TUOI SOLDI?"])),
  ("donut", dict(parts=D3, center="50/30/20", csub="LA REGOLA")),
  ("bignum", dict(to=1500, suf=" €", label="STIPENDIO NETTO", sub="quello che arriva davvero sul conto", icon="coin")),
  ("donut", dict(parts=D3, hl=0, center="50%", csub="NECESSITÀ", anim=False, icons=[("house", "Affitto"), ("bolt", "Bollette"), ("cart", "Spesa"), ("car", "Trasporti")])),
  ("donut", dict(parts=D3, hl=1, center="30%", csub="PER TE", anim=False, icons=[("star", "Uscite"), ("gamepad", "Hobby"), ("bag", "Vestiti")])),
  ("donut", dict(parts=D3, hl=2, center="20%", csub="DA PARTE", anim=False, icons=[("piggy", "Risparmio"), ("shield", "Emergenza"), ("chartup", "Investimenti")])),
  ("bars", dict(items=[("Spese fisse", 750, 0), ("Per te", 450, 1), ("Da parte", 300, 2)], suf=" €", title="CON 1.500 € AL MESE", max=800)),
  ("bars", dict(items=[("Mese 1", 5, 0), ("Mese 2", 10, 1), ("Mese 3", 15, 2), ("Mese 4", 20, 3)], suf="%", title="PARTI PICCOLO E SALI", sub="percentuale da parte", max=22)),
  ("list", dict(items=[("cross", "Non è una legge"), ("check", "È una guida"), ("check", "Serve un sistema")])),
  CTA],
 2: [
  ("bignum", dict(to=200, suf=" €", label="AL MESE", sub="può diventare una cifra che non ti aspetti", icon="piggy")),
  ("question", dict(lines=["C'È UNA CONDIZIONE", "CHE NESSUNO RISPETTA"])),
  ("growth", dict(la="Versato", lb="Con interesse composto")),
  ("hero", dict(icon="piggy", coins=True, lines=["200 € AL MESE", "ESEMPIO IPOTETICO"])),
  ("bignum", dict(to=7, suf="%", label="RENDIMENTO ANNUO IPOTETICO", sub="non garantito, è solo un'ipotesi", icon="warn", warn=1)),
  ("pairbars", dict(groups=TAB, reveal=1, la="Versato", lb="Valore stimato")),
  ("pairbars", dict(groups=TAB, reveal=2, la="Versato", lb="Valore stimato")),
  ("pairbars", dict(groups=TAB, reveal=3, la="Versato", lb="Valore stimato")),
  ("bignum", dict(txt="×2,3", label="DAL 20° AL 30° ANNO", sub="da 104k a oltre 240k", icon="chartup", size=270)),
  ("split", dict(l=dict(icon="clock", title="INIZI TARDI", value="104k", sub="dopo 20 anni", good=False), r=dict(icon="chartup", title="INIZI ORA", value="244k", sub="dopo 30 anni", good=True), foot="STESSI 200 € AL MESE")),
  ("hero", dict(icon="info", lines=["SOLO UN ESEMPIO", "NON È CONSULENZA FINANZIARIA"])),
  ("cta", dict(title="Salvalo per dopo", sub="Segui per altri consigli"))],
 3: [
  ("question", dict(lines=["SE PERDESSI IL LAVORO", "QUANTI MESI RESISTI?"])),
  ("calendar", dict(marks=[(2, (255, 90, 100))], label="MENO DI 3 MESI?", sub="allora questo video ti serve")),
  ("hero", dict(icon="shield", lines=["FONDO DI EMERGENZA", "PRIMA DI TUTTO IL RESTO"])),
  ("icons", dict(items=[("briefcase", "Lavoro"), ("car", "Auto"), ("medical", "Salute")], title="PER GLI IMPREVISTI", sub="lavoro che salta, auto che si rompe, spese mediche")),
  ("calendar", dict(marks=[(6, (255, 205, 70)), (3, (90, 235, 150))], label="DA 3 A 6 MESI", sub="di spese essenziali, non di stipendio")),
  ("bars", dict(items=[("× 3 mesi", 3600, 2), ("× 6 mesi", 7200, 3)], suf=" €", title="SE SPENDI 1.200 € AL MESE", max=7400)),
  ("split", dict(l=dict(icon="wallet", title="CONTO DI OGNI GIORNO", value="NO", sub="non mischiarlo", good=False), r=dict(icon="shield", title="CONTO SEPARATO", value="SÌ", sub="facile da raggiungere", good=True))),
  ("hero", dict(icon="piggy", coins=True, lines=["50 € A SETTIMANA", "IN AUTOMATICO"])),
  ("bars", dict(items=[("1 stipendio", 1, 0), ("2 stipendi", 2, 1), ("3 mesi", 3, 2)], title="I TRAGUARDI", sub="un passo alla volta", max=3.4)),
  ("split", dict(l=dict(icon="chartup", title="NON SERVE PER", value="GUADAGNARE", sub="non è un investimento", good=False), r=dict(icon="shield", title="SERVE PER", value="STARE SERENO", sub="niente panico", good=True))),
  ("list", dict(items=[("check", "Scelte più lucide"), ("check", "Più libertà sul lavoro"), ("check", "Meno ansia")], title="QUANDO CE L'HAI")),
  ("cta", dict(title="Mandalo a chi ne ha bisogno", sub="Prossimo video: come iniziare a investire"))],
}
