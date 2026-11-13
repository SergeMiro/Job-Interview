"""Problème N+1 : 1 requête pour les datasets + 1 requête par dataset pour son éditeur."""
import sqlite3

# Base de démonstration en mémoire
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE publisher (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE dataset (id INTEGER PRIMARY KEY, title TEXT,
                      publisher_id INTEGER REFERENCES publisher(id));
INSERT INTO publisher VALUES (1, 'INSEE'), (2, 'Météo-France');
INSERT INTO dataset VALUES (1, 'Population', 1), (2, 'Emploi', 1), (3, 'Pluie', 2);
""")

# Compteur de requêtes, pour prouver le gain
queries = []
db.set_trace_callback(queries.append)


# --- Version d'origine : N+1 requêtes ---
def select_all_datasets():
    return db.execute("SELECT id, publisher_id FROM dataset").fetchall()

def select_publisher(publisher_id):
    return db.execute("SELECT id, name FROM publisher WHERE id = ?", (publisher_id,)).fetchone()

def get_dataset_publishers_naive():
    return [select_publisher(pid) for _, pid in select_all_datasets()]


# --- Solution : une seule requête avec JOIN ---
def get_dataset_publishers():
    # La base fait la jointure : 1 aller-retour au lieu de N+1.
    # Même résultat : un éditeur par dataset, doublons compris, dans l'ordre des datasets.
    return db.execute("""
        SELECT p.id, p.name
        FROM dataset d
        JOIN publisher p ON p.id = d.publisher_id
        ORDER BY d.id
    """).fetchall()


# Variante si on veut seulement les éditeurs distincts
def get_distinct_publishers():
    return db.execute("""
        SELECT DISTINCT p.id, p.name
        FROM publisher p
        JOIN dataset d ON d.publisher_id = p.id
    """).fetchall()


if __name__ == "__main__":
    queries.clear(); naive = get_dataset_publishers_naive(); n_naive = len(queries)
    queries.clear(); fast = get_dataset_publishers(); n_fast = len(queries)
    assert naive == fast, "les deux versions doivent renvoyer la même chose"
    assert (n_naive, n_fast) == (4, 1)  # 3 datasets : 1+3 requêtes contre 1
    assert len(get_distinct_publishers()) == 2
    print(f"OK : {n_naive} requêtes -> {n_fast}")
