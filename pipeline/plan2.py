# -*- coding: utf-8 -*-
# Script lunghi (40-55 s). Ogni elemento è una frase: "testo" oppure ("testo mostrato", "testo letto").
# Solo calcoli verificabili o regole note; nessuna statistica inventata.

TAGS = "#soldi #educazionefinanziaria #risparmio #motivazione #imparacontiktok"

VIDEOS2 = [
 dict(id=1, tag="REGOLA 50/30/20", theme="gold",
  sentences=[
   "Se guadagni uno stipendio ma a fine mese non ti resta niente, questo video è per te.",
   "Il problema di solito non è quanto guadagni, è che non sai dove finiscono i soldi.",
   ("Ti insegno un metodo semplicissimo, da usare già da oggi: la regola del 50/30/20.", "Ti insegno un metodo semplicissimo, da usare già da oggi: la regola del cinquanta, trenta, venti."),
   "Prendi il tuo stipendio netto, quello che arriva davvero sul conto.",
   ("Il 50% va alle spese necessarie: affitto o mutuo, bollette, spesa e trasporti.", "Il cinquanta per cento va alle spese necessarie: affitto o mutuo, bollette, spesa e trasporti."),
   ("Il 30% è per te: uscite, hobby, vestiti, tutto quello che ti fa stare bene.", "Il trenta per cento è per te: uscite, hobby, vestiti, tutto quello che ti fa stare bene."),
   ("E il 20% va subito da parte: risparmio, fondo di emergenza, investimenti.", "E il venti per cento va subito da parte: risparmio, fondo di emergenza, investimenti."),
   ("Un esempio: con 1500 euro al mese, sono 750 per le spese fisse, 450 per te, e 300 da parte.", "Un esempio: con millecinquecento euro al mese, sono settecentocinquanta per le spese fisse, quattrocentocinquanta per te, e trecento da parte."),
   ("Se oggi non ci arrivi, parti dal 5% e aumenta ogni mese.", "Se oggi non ci arrivi, parti dal cinque per cento e aumenta ogni mese."),
   "Non è una legge, è una guida. L'importante è avere un sistema.",
   "Salva questo video, e scrivimi nei commenti: tu quanto riesci a mettere da parte?"],
  caption="La regola 50/30/20 per organizzare lo stipendio: 50% necessità, 30% desideri, 20% risparmio."),
 dict(id=2, tag="INTERESSE COMPOSTO", theme="blue",
  sentences=[
   "Con duecento euro al mese puoi arrivare a una cifra che non ti aspetti.",
   "Ma c'è una condizione, e quasi nessuno la rispetta.",
   "Si chiama interesse composto: i guadagni generano altri guadagni.",
   "Facciamo un esempio ipotetico. Metti da parte duecento euro al mese.",
   ("Immagina un rendimento medio del 7% all'anno. Attenzione: non è garantito, è solo un'ipotesi.", "Immagina un rendimento medio del sette per cento all'anno. Attenzione: non è garantito, è solo un'ipotesi."),
   ("Dopo 10 anni hai versato 24 mila euro, e ne hai circa 34 mila.", "Dopo dieci anni hai versato ventiquattro mila euro, e ne hai circa trentaquattro mila."),
   ("Dopo 20 anni, 48 mila versati, e circa 104 mila.", "Dopo venti anni, quarantotto mila versati, e circa centoquattro mila."),
   ("Dopo 30 anni, 72 mila versati, e oltre 240 mila.", "Dopo trent'anni, settantadue mila versati, e oltre duecentoquaranta mila."),
   "Vedi la differenza? Dal ventesimo al trentesimo anno la cifra più che raddoppia. Non è magia, è il tempo.",
   "Per questo la cosa più importante non è quanto metti, ma quando inizi.",
   "Questo è solo un esempio educativo, non un consiglio finanziario. Informati sempre prima di investire.",
   "Seguimi per altri video così, e salva questo per non dimenticarlo."],
  caption="Esempio ipotetico di interesse composto (7% annuo non garantito). Contenuto educativo, non consulenza."),
 dict(id=3, tag="FONDO DI EMERGENZA", theme="green",
  sentences=[
   "Se domani perdessi il lavoro, per quanti mesi riusciresti a vivere?",
   "Se la risposta è meno di tre, questo video ti serve.",
   "Prima di investire, prima di comprare qualunque cosa, serve un fondo di emergenza.",
   "Cos'è? Una somma messa da parte solo per gli imprevisti. Il lavoro che salta, la macchina che si rompe, una spesa medica.",
   "Quanto? Da tre a sei mesi delle tue spese essenziali. Non del tuo stipendio, delle tue spese.",
   ("Un esempio: se per vivere ti servono 1200 euro al mese, il tuo obiettivo è tra 3600 e 7200 euro.", "Un esempio: se per vivere ti servono milleduecento euro al mese, il tuo obiettivo è tra tremilaseicento e settemiladuecento euro."),
   "Dove tenerlo? Su un conto separato, facile da raggiungere, ma non quello che usi ogni giorno.",
   "Come costruirlo? Parti piccolo. Anche cinquanta euro a settimana, in automatico.",
   "Il primo traguardo è uno stipendio intero. Poi due. Poi tre mesi.",
   "Non serve a farti guadagnare, serve a non farti andare nel panico.",
   "Quando ce l'hai, puoi fare scelte migliori, anche sul lavoro.",
   "Condividilo con qualcuno che ne ha bisogno, e seguimi per il prossimo passo: come iniziare a investire."],
  caption="Il fondo di emergenza: da 3 a 6 mesi di spese essenziali, prima di qualsiasi investimento."),
]
def plain(s): return s[0] if isinstance(s, tuple) else s
def spoken(s): return s[1] if isinstance(s, tuple) else s
