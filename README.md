# Funzionamento dell'Applicazione

Questo documento mira a spiegare il funzionamento dell’applicazione sviluppata al fine di analizzare immagini tramite l’utilizzo di modelli di intelligenza artificiale. L’obiettivo principale dell’applicativo è fornire una piattaforma intuitiva e versatile che permetta agli utenti di caricare e analizzare immagini tramite modelli di intelligenza artificiale.

## Funzionalità

- **Caricamento immagine**: l’applicazione permette il caricamento di un'immagine presente nel file system del proprio dispositivo.
- **Caricamento cartella di immagini**: l’applicazione permette il caricamento di un’intera cartella contenente immagini.
- **Analisi immagini**: è possibile eseguire l’analisi di una o più immagini caricate per estrarre informazioni rilevanti tramite il modello di intelligenza artificiale selezionato.
- **Selezione modello**: tramite un menù a tendina è possibile selezionare il modello con cui si vuole effettuare l’analisi dell’immagine per estrarre informazioni (è disponibile di default un modello per l’analisi del testo).
- **Caricamento di un nuovo modello**: è possibile caricare nuovi modelli di intelligenza artificiale direttamente dal proprio file system, in formato `.keras` o `.h5`. Sarà inoltre necessario allegare un file json contenente il nome delle classi con le quali il modello dovrà effettuare la predizione.
- **Eliminare un modello**: l’applicazione consente di eliminare un modello precedentemente caricato. Non sarà possibile rimuovere il modello di default.
- **Visualizzazione risultati**: una volta effettuata l’analisi dell’immagine i risultati appariranno a schermo mostrando le bounding boxes estratte e le relative predizioni.
- **Download risultati**: una volta ottenuti i risultati sarà possibile salvarli nel proprio dispositivo. Verrà salvata l’immagine con le bounding boxes disegnate e un file json contenenti tutte le informazioni estratte (predizione, nome del modello che ha eseguito l’analisi...).
- **Upload risultati**: l’applicazione consente di caricare nuovamente i risultati precedentemente scaricati, i quali verranno mostrati a schermo.
- **Reset interfaccia**: è possibile resettare l’interfaccia rimuovendo tutti gli elementi mostrati a schermo in quel momento.
- **Visualizzazione lista di immagini**: sul lato sinistro dell’interfaccia verrà visualizzata la lista delle immagini in quel momento importate all’interno dell’applicazione. Sarà possibile selezionare ognuna di esse per poterle visualizzare.
- **Visualizzazione immagini caricate**: una volta selezionata l’immagine che si desidera visualizzare dalla lista, essa apparirà sulla sinistra. Sarà inoltre possibile cliccarla per poter aprire una finestra dove verrà mostrata ingrandita.

## Installazione

1. Clonare il repository tramite il comando:
   ```sh
   git clone https://github.com/KevinConcettoni/ImageAnalyzer
2. Installare le dipendenze necessarie al funzionamento dell’applicazione:
   ```sh
   pip install -r requirements.txt
3. Avviare l'applicazione dalla classe Main oppure tramite il comando:
  ```sh
  python Main.py
