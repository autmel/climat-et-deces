#!/usr/bin/env python3
# Génère app/data.js à partir des deux CSV
import csv, json, os

BASE = '/mnt/ssd2/ASSO/OpenData/deces'
OUT = os.path.join(BASE, 'app', 'data.js')

# --- température quotidienne (température_jour.csv) ---
jours = []
tmoy = []
with open(os.path.join(BASE, 'CSV', 'temperature_jour.csv')) as f:
    for r in csv.DictReader(f):
        jours.append(r['date'])          # YYYYMMDD
        tmoy.append(float(r['tmoy']))

# dates continues 1970-01-01 .. dernier jour
start = jours[0]

# --- décès par jour de l'année (analyse_deces_2020-2026-FR.csv) ---
dej = {'jour': [], 'moyenne_indexee': [], 'deces_2026': []}
with open(os.path.join(BASE, 'analyse_deces_2020-2026-FR.csv')) as f:
    for r in csv.DictReader(f):
        dej['jour'].append(r['jour'])
        dej['moyenne_indexee'].append(float(r['moyenne_indexee']))
        dej['deces_2026'].append(int(r['deces_2026']))

# dernier jour 2026 avec données (dernier non nul)
last26 = 0
for j, d in zip(dej['jour'], dej['deces_2026']):
    if d > 0:
        last26 = j

data = {
    'temp': {'start': start, 'tmoy': tmoy},
    'deces': {
        'jour': dej['jour'],
        'moyenne_indexee': dej['moyenne_indexee'],
        'deces_2026': dej['deces_2026'],
        'last_jour_2026': last26,
    },
}

with open(OUT, 'w') as f:
    f.write('window.DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n')

print('OK', OUT, len(jours), 'jours temp,', len(dej['jour']), 'jours deces, dernier 2026 =', last26)