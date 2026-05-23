# Wasmer Edge Deployment for `portal.idealtechnos.com`

Wasmer Edge supports Django auto-detection when a project has `requirements.txt` and `manage.py`.

Sources checked:

- Wasmer deploy flow: `wasmer login`, then `wasmer deploy`
- Python/Django support: Wasmer detects Python from `requirements.txt` and Django from `manage.py`
- Custom domains: add the domain in the Wasmer app dashboard, then update DNS
- Secrets: set sensitive environment variables with Wasmer app secrets

## 1. Install Wasmer CLI

Install Wasmer from the official Wasmer instructions:

```text
https://docs.wasmer.io/edge/get-started/
```

After installing, check:

```bash
wasmer --version
```

## 2. Log in

```bash
wasmer login
```

## 3. Deploy from the clean deploy folder

Use the clean deployment folder so Wasmer does not upload local `media/`, `db.sqlite3`, or `node_modules/`.

On this machine the clean folder is:

```text
C:\Users\raksh\company\deploy_clean
```

Run:

```powershell
cd C:\Users\raksh\company\deploy_clean
wasmer deploy
```

Wasmer should detect this as a Django/Python app because these files exist:

```text
requirements.txt
manage.py
```

The project includes `.wasmerignore` and `.dockerignore` so local data files, uploaded media, and `node_modules/` are not shipped in the deployment archive.

When Wasmer asks for an app name, use:

```text
idealtechnos-portal
```

After deployment, Wasmer will show a temporary app URL similar to:

```text
https://idealtechnos-portal-yourname.wasmer.app
```

Open that URL first and confirm the Django app loads.

## 4. Add production secrets

In Wasmer, set these as app secrets. You can use the dashboard, or the CLI from this project folder after `app.yaml` exists.

Core Django secrets:

```bash
wasmer app secrets create DJANGO_DEBUG "False"
wasmer app secrets create SECRET_KEY "replace-with-a-long-random-secret-key"
wasmer app secrets create DJANGO_ALLOWED_HOSTS "portal.idealtechnos.com,idealtechnos-portal-yourname.wasmer.app"
wasmer app secrets create DJANGO_CSRF_TRUSTED_ORIGINS "https://portal.idealtechnos.com,https://idealtechnos-portal-yourname.wasmer.app"
```

Replace:

```text
idealtechnos-portal-yourname.wasmer.app
replace-with-a-long-random-secret-key
```

Use the real Wasmer URL shown after deployment.

## 4a. Configure real database

For real-time production data, do not use local `db.sqlite3`.

Use a Wasmer-attached MySQL database or an external MySQL database, then set these secrets:

```bash
wasmer app secrets create DB_HOST "your-db-host"
wasmer app secrets create DB_PORT "3306"
wasmer app secrets create DB_NAME "your-db-name"
wasmer app secrets create DB_USERNAME "your-db-user"
wasmer app secrets create DB_PASSWORD "your-db-password"
```

If Wasmer auto-provisions a database, inspect the database values from the Wasmer dashboard or CLI and use those values.

After database secrets are set, run migrations against the production database:

```bash
wasmer deploy
```

Wasmer's Django deployment flow may run migrations automatically. If it does not, use a Wasmer remote shell/job for:

```bash
python manage.py migrate
```

## 4b. Configure uploaded media storage

For real student photos and gallery uploads, do not rely on local `media/` storage.

Use S3-compatible object storage, then set:

```bash
wasmer app secrets create AWS_STORAGE_BUCKET_NAME "your-bucket-name"
wasmer app secrets create AWS_ACCESS_KEY_ID "your-access-key"
wasmer app secrets create AWS_SECRET_ACCESS_KEY "your-secret-key"
wasmer app secrets create AWS_S3_REGION_NAME "your-region"
wasmer app secrets create MEDIA_URL "https://your-media-domain-or-bucket-url/"
```

If your storage provider is S3-compatible but not AWS S3, also set:

```bash
wasmer app secrets create AWS_S3_ENDPOINT_URL "https://your-storage-endpoint"
```

Examples of S3-compatible media storage providers:

- AWS S3
- Cloudflare R2
- DigitalOcean Spaces
- Backblaze B2 S3-compatible buckets

If you configure email later, also create:

```bash
wasmer app secrets create EMAIL_HOST_USER "your-email"
wasmer app secrets create EMAIL_HOST_PASSWORD "your-email-app-password"
wasmer app secrets create DEFAULT_FROM_EMAIL "your-email"
wasmer app secrets create CONTACT_EMAIL "your-contact-email"
```

## 5. Redeploy after secrets and storage/database setup

```bash
wasmer deploy
```

## 6. Add custom domain in Wasmer

In the Wasmer dashboard:

```text
App -> Settings -> Domains -> Add Domain
```

Add:

```text
portal.idealtechnos.com
```

Wasmer will show the DNS record you need.

## 7. Add DNS record for `idealtechnos.com`

In your domain DNS panel, add the record Wasmer gives you.

It will usually look like:

```text
Type:  CNAME
Name:  portal
Value: your-wasmer-target
```

Use the exact target from Wasmer.

## 8. Link from existing website

On `https://idealtechnos.com`, add:

```html
<a href="https://portal.idealtechnos.com">Student Portal</a>
```

## Important note about database and media

Wasmer Edge apps are designed for stateless web workloads. This project uses SQLite and local uploaded media only when production database/media secrets are not configured.

For real student data on Wasmer:

- Configure MySQL with the `DB_*` secrets.
- Configure S3-compatible media storage with the `AWS_*` secrets.
- Do not depend on local `db.sqlite3` or local `media/` for production records.

For first testing, deploying the app and opening the public pages is fine. Before adding real student records, finish the database and media setup above.
