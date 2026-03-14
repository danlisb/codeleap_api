# CodeLeap Careers API

Django REST Framework backend for the CodeLeap technical test.

## Project structure

```
codeleap_api/
├── careers/
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py         # Post model
│   ├── pagination.py     # PageNumberPagination (10 per page)
│   ├── serializers.py    # PostSerializer + PostUpdateSerializer
│   ├── tests.py          # 15 test cases
│   ├── urls.py           # DRF router
│   └── views.py          # PostViewSet
├── codeleap_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- pip

## Setup & run

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python3 manage.py migrate

# 4. Start the development server
python3 manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Running tests

```bash
python3 manage.py test --verbosity=2
```

---

## API Reference

### Data shape

```json
{
  "id": 1,
  "username": "john",
  "created_datetime": "2024-01-15T10:30:00Z",
  "title": "My Post",
  "content": "Post body here"
}
```

---

### `GET /careers/`

Returns a paginated list of posts ordered by most recent first.

**Query params**

| Param       | Default | Max | Description      |
|-------------|---------|-----|------------------|
| `page`      | 1       | —   | Page number      |
| `page_size` | 10      | 100 | Results per page |

**Response `200 OK`**

```json
{
  "count": 42,
  "next": "http://localhost:8000/careers/?page=2",
  "previous": null,
  "results": [ /* array of post objects */ ]
}
```

---

### `POST /careers/`

Creates a new post.

**Request body**

```json
{
  "username": "john",
  "title": "My Post",
  "content": "Post body here"
}
```

**Response `201 Created`** — full post object including `id` and `created_datetime`.

---

### `PATCH /careers/{id}/`

Partially updates a post. Only `title` and `content` are editable.
Fields `id`, `username`, and `created_datetime` are ignored even if sent.

**Request body** (all fields optional)

```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

**Response `200 OK`** — full post object with all fields.

```json
{
  "id": 1,
  "username": "john",
  "created_datetime": "2024-01-15T10:30:00Z",
  "title": "Updated title",
  "content": "Updated content"
}
```

---

### `DELETE /careers/{id}/`

Deletes a post.

**Response `204 No Content`**

---

## Testing with curl

```bash
# List posts
curl http://127.0.0.1:8000/careers/

# Create a post
curl -X POST http://127.0.0.1:8000/careers/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "title": "My Post", "content": "Some content"}'

# Update a post (id = 1)
curl -X PATCH http://127.0.0.1:8000/careers/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "content": "Updated content"}'

# Delete a post (id = 1)
curl -X DELETE http://127.0.0.1:8000/careers/1/
```

---

## Design decisions

| Decision | Rationale |
|---|---|
| `PostViewSet` with explicit mixins | Exposes only the 4 required actions; PUT is blocked (`405`) |
| Two serializers | `PostSerializer` (read/create) and `PostUpdateSerializer` (patch) — enforces field immutability at the serializer layer, not just `read_only_fields`. PATCH returns the full object |
| `Meta.ordering` on the model | Ensures consistent ordering regardless of how the queryset is used |
| `PageNumberPagination` | Simple, frontend-friendly; supports `page` + `page_size` query params |
| SQLite (default) | Zero-config for dev/test; swap `DATABASES` for PostgreSQL in production |
| No authentication | Per spec — the `username` is a plain string from the frontend |
