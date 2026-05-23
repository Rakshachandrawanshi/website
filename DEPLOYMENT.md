# Deploy and Link From Existing Website

Recommended setup:

- Existing website: `https://idealtechnos.com`
- Django portal: `https://portal.idealtechnos.com`
- Existing website link: `<a href="https://portal.idealtechnos.com">Student Portal</a>`

## 1. Upload the Django project to a Django host

Use a host that supports Python/Django, such as Wasmer Edge, PythonAnywhere, Render, Railway, DigitalOcean, or a VPS.

For Wasmer Edge, use `WASMER_DEPLOYMENT.md`.

On the server:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

## 2. Set production environment variables

Use the values from `.env.example`, but replace the domain and secret key:

```env
DJANGO_DEBUG=False
SECRET_KEY=your-long-random-secret-key
DJANGO_ALLOWED_HOSTS=portal.idealtechnos.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://portal.idealtechnos.com
```

For real production data, also configure:

```env
DB_HOST=your-db-host
DB_PORT=3306
DB_NAME=your-db-name
DB_USERNAME=your-db-user
DB_PASSWORD=your-db-password
```

For uploaded photos/images in production, configure S3-compatible storage:

```env
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_REGION_NAME=your-region
MEDIA_URL=https://your-media-domain-or-bucket-url/
```

If you also want the Django app to answer on the root or `www` domain, include those too:

```env
DJANGO_ALLOWED_HOSTS=idealtechnos.com,www.idealtechnos.com,portal.idealtechnos.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://idealtechnos.com,https://www.idealtechnos.com,https://portal.idealtechnos.com
```

## 3. Add DNS record for the portal URL

In your domain provider DNS panel, add one of these depending on your host:

```text
CNAME  portal  your-host-provided-target
```

or:

```text
A      portal  server-ip-address
```

Your Django host will tell you which one to use.

## 4. Add link on existing website

Add this to the existing website menu, button, or page:

```html
<a href="https://portal.idealtechnos.com">Student Portal</a>
```

## 5. Production reminders

- Keep `DEBUG=False`.
- Use HTTPS on the Django portal.
- Do not upload your local `db.sqlite3` publicly if it contains private student data.
- Use server/static hosting for static and media files.
- Make admin passwords strong.
