# Django Blog API

Pure Django JSON API built without Django REST Framework, serializers, or templates. Every endpoint returns JSON via `JsonResponse`.

## About

A blog platform API with full CRUD operations for posts, categories, and comments. Session-based authentication, search, filtering, and pagination included. Built intentionally without DRF to work directly with Django's core tools and reinforce how things work under the hood before adding abstraction layers.

## Tech Stack

- Python 3.11+
- Django 4.2
- SQLite
- Session-based authentication

No third-party packages. No DRF, no JWT, no Pillow.

## Setup

```
git clone https://github.com/USERNAME/django-blog-api.git
cd django-blog-api
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

### Authentication

```
POST   /api/auth/register/     Register a new user
POST   /api/auth/login/        Login, creates session
POST   /api/auth/logout/       Logout, destroys session
GET    /api/auth/me/           Current user profile (requires login)
```

### Categories

```
GET    /api/categories/            List all categories
GET    /api/categories/<slug>/     Single category detail
POST   /api/categories/            Create category (admin only)
PUT    /api/categories/<slug>/     Update category (admin only)
DELETE /api/categories/<slug>/     Delete category (admin only)
```

### Posts

```
GET    /api/posts/                 List published posts
GET    /api/posts/<slug>/          Single post with comments
POST   /api/posts/                 Create post (requires login)
PUT    /api/posts/<slug>/          Update post (owner only)
DELETE /api/posts/<slug>/          Delete post (owner only)
GET    /api/posts/my/              Current user's posts (requires login)
```

### Comments

```
GET    /api/posts/<slug>/comments/     List comments for a post
POST   /api/posts/<slug>/comments/     Add comment (requires login)
DELETE /api/comments/<id>/             Delete comment (owner only)
```

### Query Parameters (GET /api/posts/)

```
?q=django              Search in title and content
?category=technology   Filter by category slug
?author=john           Filter by author username
?ordering=-created_at  Sort results
?limit=10&offset=0     Pagination
```

## Models

**Category** -- name, slug, description, is_active, created_at

**Post** -- title, slug, author, category, content, excerpt, status (draft/published), views_count, created_at, updated_at

**Comment** -- post, author, content, is_approved, created_at

## Authentication

Session-based. Login creates a session cookie, which is sent with subsequent requests. Protected endpoints return 401 if no valid session exists.

## Error Handling

All errors follow a consistent format:

```json
{
    "success": false,
    "error": {
        "code": "NOT_FOUND",
        "message": "Post not found"
    }
}
```

Standard error codes: VALIDATION_ERROR (400), UNAUTHORIZED (401), FORBIDDEN (403), NOT_FOUND (404).

## Testing

Tested with curl and Postman. Use session cookies for authenticated requests:

```
curl -c cookies.txt -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

curl -b cookies.txt http://127.0.0.1:8000/api/auth/me/
```
