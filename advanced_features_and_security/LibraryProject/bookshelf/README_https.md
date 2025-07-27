## HTTPS & Secure Redirect Configuration

The application is configured for HTTPS-only access:

- `SECURE_SSL_REDIRECT`: All HTTP requests are redirected to HTTPS.
- `SECURE_HSTS_SECONDS`: Enforces HTTPS for 1 year.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`: Includes subdomains in HSTS policy.
- `SESSION_COOKIE_SECURE` & `CSRF_COOKIE_SECURE`: Ensures cookies are only sent over HTTPS.
- `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`: Defend against clickjacking and XSS attacks.

For production deployment, HTTPS must be enforced using an SSL certificate via Nginx or Apache.
