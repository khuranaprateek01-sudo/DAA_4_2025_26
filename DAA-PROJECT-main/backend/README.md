# Django Backend for Algorithm Visualizer

This backend serves the visualizer UI and provides JSON API endpoints for algorithm execution.

## Run

1. Open terminal in `backend/`
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start server:

```bash
python manage.py runserver
```

5. Open:

- UI: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/health/`

## API Endpoints

All API endpoints accept `POST` with `Content-Type: application/json` unless noted.

### Sorting

- `POST /api/sort/bubble/`
- `POST /api/sort/selection/`
- `POST /api/sort/insertion/`
- `POST /api/sort/merge/`
- `POST /api/sort/quick/`

Request:

```json
{
  "array": [5, 1, 4, 2]
}
```

Response:

```json
{
  "algorithm": "quick",
  "input": [5, 1, 4, 2],
  "sorted": [1, 2, 4, 5]
}
```

### Graph

- `POST /api/graph/bfs/`
- `POST /api/graph/dfs/`
- `POST /api/graph/dijkstra/`

Request:

```json
{
  "node_count": 5,
  "start": 0,
  "edges": [
    [0, 1],
    [1, 2],
    [2, 3, 4],
    [0, 4, 1]
  ]
}
```

### Dynamic Programming

- `POST /api/dp/knapsack/`
- `POST /api/dp/lcs/`

Knapsack request:

```json
{
  "weights": [2, 3, 4, 5],
  "values": [3, 4, 5, 6],
  "capacity": 5
}
```

LCS request:

```json
{
  "s1": "ABCBDAB",
  "s2": "BDCAB"
}
```
