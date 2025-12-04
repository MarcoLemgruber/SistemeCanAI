import sqlite3
from datetime import datetime

DB_PATH = 'instance/event_log.db'

# Cria tabela se não existir
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    valor INTEGER,
    timestamp TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    objeto TEXT,
    score REAL,
    timestamp TEXT
)''')
conn.commit()
conn.close()

def log_event(tipo, valor):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO eventos (tipo, valor, timestamp) VALUES (?, ?, ?)',
              (tipo, valor, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_alert(objeto, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO alertas (objeto, score, timestamp) VALUES (?, ?, ?)',
              (objeto, score, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Entradas
    c.execute('SELECT COUNT(*) FROM eventos WHERE tipo = "entrada"')
    entradas = c.fetchone()[0]
    # Saidas
    c.execute('SELECT COUNT(*) FROM eventos WHERE tipo = "saida"')
    saidas = c.fetchone()[0]
    # Max pessoas
    c.execute('SELECT MAX(valor) FROM eventos WHERE tipo = "dentro"')
    max_pessoas = c.fetchone()[0] or 0
    # Alertas
    c.execute('SELECT COUNT(*) FROM alertas')
    alertas = c.fetchone()[0]
    conn.close()
    return {
        'entradas': entradas,
        'saidas': saidas,
        'max_pessoas': max_pessoas,
        'alertas': alertas
    }

def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT objeto, score, timestamp FROM alertas ORDER BY timestamp DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    return rows
