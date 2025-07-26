
# LogiRotor

## Descrizione
Il seguente repository è relativo al progetto dell'insegnamento [Sistemi Robotici](https://www.dmi.unict.it/santoro/index.php?p=21), tenuto presso il Dipartimento di Matematica e Informatica dell'Università di Catania. LogiRotor è un multirotore autonomo progettato per l'ottimizzazione della logistica pacchi all'interno di ambienti di magazzino.

## Strumenti

Per la simulazione del drone e del relativo ambiente è stato scelto di utilizzare il software [Godot Engine](https://godotengine.org/). Per quanto riguarda invece la gestione del sistema dinamico del multirotore e delle sue istruzioni di consegna, sono stati creati script python e notebook jupyter. Le [librerie del corso](https://github.com/corradosantoro/RoboticSystems/tree/main/lib), infine, sono state impiegate per poter interfacciarsi con la simulazione del drone tramite godot 


## Struttura del Progetto

- `config` contiene i file di configurazione della simulazione:
  - *coordinates.csv* : contiente le coordinate dei nodi del grafo del percorso del drone
  - *edges.txt*: contiene tutti gli archi del grafo non orientato
  - **.json*: due file contententi i settaggi delle istruzioni del multirotore


- `docs` contiene l'immagine del grafo usato per l'algoritmo di path-planning
- `godot` contiene tutti i file relativi alla scena godot, incluso il file progetto
- `graphs` contiene i grafici che mostrano posizione e velocità del drone rispetto alla traitettoria da seguire (tecnica del Virtual Robot)
- `lib` contiene le librerie del corso relative al controllo del multirotore e alla sua interfaccia con godot
- `notebooks` contiene un notebook di esempio per la simulazione e la visualizzazione dei grafici
- `src` contiene la logica di controllo e navigazione del multirotore:
  - *multirotor.py*: contiene la modellazione di un multirotore a quattro eliche con forma ad X, comprensivo delle classi rappresentanti i movimenti effettuati dal robot;
  - *path_planner.py*: contiene la classe Path_Planner che si occupa della creazione di un percorso per il robot, a partire dal grafo di navigazione;
  - *control_system.py*: contiene la classe Control System che si occupa della simulazione e comunicazione con godot;
  - *courier.py*: contiene la classe Courier che orchestra i vari componenti per la simulazione;
## Esecuzione
Per la corretta  esecuzione è necessario **Godot 4.4.1** o superiore.
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
Avviare **Godot** importando il file del progetto ed **eseguire la scena**, infine eseguire lo script `main.py`:

```bash
  python main.py
```



## Autori

- [@eddy2809](https://www.github.com/eddy2809)
- [@weiss25r](https://www.github.com/weiss25r)

