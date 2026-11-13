"""Débogage N+1, étape 1 : compter et regrouper les requêtes SQL exécutées."""
from collections import Counter
from contextlib import contextmanager
import re

from solution import db, get_dataset_publishers_naive, get_dataset_publishers


@contextmanager
def count_queries(conn):
    """Enregistre toutes les requêtes exécutées dans le bloc."""
    executed = []
    conn.set_trace_callback(executed.append)
    try:
        yield executed
    finally:
        conn.set_trace_callback(None)  # on coupe la trace en sortant


def report(executed):
    # On remplace les valeurs par « ? » pour regrouper les requêtes identiques
    shapes = Counter(re.sub(r"\b\d+\b|'[^']*'", "?", q) for q in executed)
    print(f"{len(executed)} requêtes")
    for sql, n in shapes.most_common():
        flag = "  <-- N+1 suspect" if n > 1 else ""
        print(f"  x{n}  {' '.join(sql.split())}{flag}")


if __name__ == "__main__":
    for fn in (get_dataset_publishers_naive, get_dataset_publishers):
        with count_queries(db) as q:
            fn()
        print(f"\n{fn.__name__} :")
        report(q)
