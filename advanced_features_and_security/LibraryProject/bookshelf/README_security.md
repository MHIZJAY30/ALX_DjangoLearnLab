## 🔐 Django Security Setup

### ✅ Configured Settings in settings.py:
- `DEBUG = False`: Disables debug mode in production.
- `SECURE_BROWSER_XSS_FILTER = True`: Enables browser XSS protection.
- `X_FRAME_OPTIONS = 'DENY'`: Prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents MIME sniffing.
- `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True`: Only send cookies over HTTPS.

### ✅ Templates:
- All forms include `{% csrf_token %}` to prevent CSRF attacks.

### ✅ Views:
- All queries use Django ORM to prevent SQL injection.
- Inputs are validated using Django forms.

### ✅ CSP:
- Implemented using `django-csp` to restrict script/style sources and prevent XSS.
