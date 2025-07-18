
# LogiRotor

## Descrizione
Il seguente repository è relativo al progetto dell'insegnamento [Sistemi Robotici](https://www.dmi.unict.it/santoro/index.php?p=21), tenuto presso il Dipartimento di Matematica e Informatica dell'Università di Catania. LogiRotor è un multirotore autonomo progettato per l'ottimizzazione della logistica pacchi all'interno di ambienti di magazzino.

## Strumenti

Per la simulazione del drone e del relativo ambiente è stato scelto di utilizzare il software [Godot Engine](https://godotengine.org/). Per quanto riguarda invece la gestione del sistema dinamico del multirotore e delle sue istruzioni di consegna, sono stati creati script python e notebook jupyter. Le [librerie del corso](https://github.com/corradosantoro/RoboticSystems/tree/main/lib), infine, sono state impiegate per poter interfacciarsi con la simulazione del drone tramite godot 


## Struttura del Progetto

- `config` contiene i file di configurazione della simulazione:
  - *coordinates.csv* : contiente le coordinate dei nodi del grafo del percorso del drone
  - *edges.txt*: contiene tutti gli archi del grafo non orientato
- `graphs` contiene i grafici che mostrano posizione e velocità del drone rispetto alla traitettoria da seguire (tecnica del Virtual Robot)

- `godot` contiene tutti i file relativi alla scena godot, incluso il file progetto

- `notebooks` contiene un notebook di esempio per la simulazione e la visualizzazione dei grafici
- `lib` contiene le librerie del corso relative al controllo del multirotore e alla sua interfaccia con godot
- `src` contiene la logica di controllo e navigazione del multirotore:
  - *template*:
## Esecuzione

Assicurarsi di aver creato un ambiente virtuale dove poter installare le dipendenze necessarie, successivamente clonare il progetto



```bash
  git clone https://github.com/eddy2809/LogiRotor.git
```

spostartsi nella cartella pricipale del progetto 

```bash
  cd LogiRotor
```

Installare le dipendenze

```bash
  pip install requirements.txt
```
Avviare Godot importando il file del progetto ed eseguire la scena, infine eseguire lo script `main.py`




## Autori

- [@eddy2809](https://www.github.com/eddy2809)
- [@weiss25r](https://www.github.com/weiss25r)

