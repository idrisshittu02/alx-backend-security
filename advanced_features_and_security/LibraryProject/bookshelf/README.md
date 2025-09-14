# Permissions and Groups Setup — Django Library App

This guide explains how custom permissions and user groups are implemented in the `bookshelf` app of the Django project.

---

## Custom Permissions

Custom permissions are defined for the `Book` model to control access to various actions.

### Defined Permissions:

- `can_view` – View books
- `can_create` – Add new books
- `can_edit` – Edit existing books
- `can_delete` – Delete books

These permissions are declared in `bookshelf/models.py`:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
Groups Setup
User groups are created and assigned permissions using a custom Django management command.

Groups:
Viewers – can_view

Editors – can_view, can_create, can_edit

Admins – all permissions (can_view, can_create, can_edit, can_delete)

Run Command:
bash
Copy code
python manage.py setup_groups
This script is defined in:

bash
Copy code
bookshelf/management/commands/setup_groups.py
After running the command, use the Django Admin panel to assign users to the appropriate groups.

View Permissions
Each view that interacts with the Book model is protected using @permission_required.

Example:
python
Copy code
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
Protected Views:
View Function	Required Permission
list_books	bookshelf.can_view
create_book	bookshelf.can_create
edit_book	bookshelf.can_edit
delete_book	bookshelf.can_delete

File Overview
File Path	Description
bookshelf/models.py	Custom permissions added to Book model
bookshelf/views.py	Views protected using permission decorators
bookshelf/forms.py	BookForm used in create/edit views
bookshelf/management/commands/setup_groups.py	Script to create user groups and assign permissions
README.md	Documentation of permission & group setup

🚀 Deployment
Once all files are updated, commit and push your changes:

bash
Copy code
git add .
git commit -m "Implement custom permissions and group-based access control"
git push


## Security Enhancements

### Django Settings (settings.py)

| Setting | Purpose |
|--------|---------|
| `DEBUG = False` | Disables debug mode in production |
| `SECURE_BROWSER_XSS_FILTER = True` | Enables XSS filter in modern browsers |
| `SECURE_CONTENT_TYPE_NOSNIFF = True` | Prevents MIME-sniffing |
| `X_FRAME_OPTIONS = 'DENY'` | Prevents clickjacking |
| `CSRF_COOKIE_SECURE = True` | Sends CSRF cookies over HTTPS only |
| `SESSION_COOKIE_SECURE = True` | Sends session cookies over HTTPS only |
| `CSP_*` | Enforces Content Security Policy via `django-csp` |

### Content Security Policy (CSP)

We used [`django-csp`](https://github.com/mozilla/django-csp) to add a Content Security Policy:

```python
INSTALLED_APPS += ['csp']
MIDDLEWARE = ['csp.middleware.CSPMiddleware', ...]
Example CSP settings:

python
Copy code
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", 'https://fonts.googleapis.com')
CSP_FONT_SRC = ("'self'", 'https://fonts.gstatic.com')
CSP_IMG_SRC = ("'self'", 'data:')
2. Manual Security Testing Checklist
Here’s how to test the protections you’ve added:

CSRF Protection
Go to a form (e.g. create/edit book)

View page source — you should see:
<input type="hidden" name="csrfmiddlewaretoken" ... >

Try submitting the form without the CSRF token → it should throw an error.

XSS Protection
Try entering a <script> tag in a form field

It should not execute when displayed — it should be escaped.

SQL Injection Protection
If you have any form input that filters/searches DB records:

Try input like: 1' OR 1=1 -- or '; DROP TABLE

Should not break the app

Django ORM automatically prevents these unless you write raw SQL

CSP Header Check
Open browser dev tools → Network tab → click on any request → go to Headers

You should see:

css
Copy code
content-security-policy: default-src 'self'; ...


# HTTPS Deployment Guide

To securely deploy the Django app in production:

## 1. SSL Certificate
Use Let's Encrypt or a commercial SSL certificate.

### For Nginx:
- Install `certbot` and generate certificate:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
Ensure Nginx config includes SSL:

nginx
Copy code
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        ...
    }
}
2. Django Settings
Ensure the following are enabled in settings.py:

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000

3. Redirect HTTP to HTTPS
Nginx configuration:

nginx
Copy code
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
yaml
Copy code

---

## Step 5: Documentation and Review

You’ll want to create a file like this:

### `SECURITY_REVIEW.md` (Sample Summary)

```markdown
# Security Review: HTTPS and Secure Configuration

## Security Features Implemented

- Enforced HTTPS with `SECURE_SSL_REDIRECT`
- HSTS enabled (1-year duration, preload, subdomains)
- Secure cookies (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`)
- Security headers:
  - `X_FRAME_OPTIONS = 'DENY'`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `SECURE_BROWSER_XSS_FILTER = True`
- Content Security Policy via `django-csp` middleware

## Deployment
- SSL certificates installed via Let's Encrypt
- Nginx config set to redirect HTTP to HTTPS
- Django settings updated for production

## Summary
These settings protect the application from:
- Data leakage over HTTP
- XSS, CSRF, clickjacking, and MIME attacks
- Man-in-the-middle attacks via SSL enforcement

## Potential Improvements
- Enable `SECURE_PROXY_SSL_HEADER` if using a proxy (like Gunicorn behind Nginx)
- Use Subresource Integrity (SRI) in templates for external assets