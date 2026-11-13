# N+1 queries

**Problème.** `get_dataset_publishers()` fait 1 requête pour la liste des datasets, puis 1 requête par dataset : N+1 allers-retours vers la base. Avec 10 000 datasets, ça fait 10 001 requêtes.

**Solution.** Une seule requête avec `JOIN` (voir `solution.py`). Si l'accès passe par un ORM : `select_related` / `joinedload`, ou bien `WHERE id IN (...)` sur les `publisher_id` distincts (2 requêtes au total).

**À clarifier avec l'interlocuteur.** Faut-il garder les doublons (un éditeur par dataset) ou seulement les éditeurs distincts ? Que faire d'un dataset sans éditeur (`LEFT JOIN`) ? Faut-il paginer une grosse liste ?

Lancer : `python3 solution.py`
