# নিজের খাতা · Nijer Khata (Self Ledger, mj-ahmad)

A quiet, inheritable ledger for learning, work, health, faith and reflection.
Plain files, no build step, Bangla and English.

1. Put your logo at `assets/logo.png`.
2. `./run.sh` validates the data and serves http://127.0.0.1:8000
3. Add entries: `python3 life.py log "..." --category learning --mood 4`
   or `python3 life.py add "Heading" "Description" --body-file notes.md`

Each entry has a LIFE tracking ID, a REG registry ID, and Dhaka and UTC timestamps.
To inherit the system, copy the whole folder and keep `data.json` and `registry.json` together.
