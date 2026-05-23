# PythonAnywhere Deployment for `portal.idealtechnos.com`

This is the simplest deployment path for this Django project.

## 1. Create PythonAnywhere account

Go to PythonAnywhere and create an account. A paid account is usually required for a custom domain like:

```text
portal.idealtechnos.com
```

## 2. Upload project

Upload this project folder to PythonAnywhere, or push it to GitHub and clone it there.

Recommended project path on PythonAnywhere:

```text
/home/yourusername/company
```

## 3. Create virtual environment

In a PythonAnywhere Bash console:

```bash
cd /home/yourusername/company
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If Python 3.13 is not available, use the newest Python version PythonAnywhere offers.

## 4. Run Django setup

```bash
python manage.py migrate
python manage.py collectstatic
```

When asked to continue collecting static files, type:

```text
yes
```

## 5. Create web app

In PythonAnywhere:

- Open the **Web** tab.
- Click **Add a new web app**.
- Use custom domain:

```text
portal.idealtechnos.com
```

- Choose **Manual configuration**.
- Choose the same Python version used for your virtual environment.

## 6. Configure virtualenv

In the **Web** tab, set virtualenv path:

```text
/home/yourusername/company/.venv
```

## 7. Configure WSGI file

Open the WSGI configuration file from the PythonAnywhere **Web** tab and replace its contents with:

```python
import os
import sys

path = "/home/yourusername/company"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "company.settings"
os.environ["DJANGO_DEBUG"] = "False"
os.environ["SECRET_KEY"] = "replace-with-a-long-random-secret-key"
os.environ["DJANGO_ALLOWED_HOSTS"] = "portal.idealtechnos.com"
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = "https://portal.idealtechnos.com"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace:

```text
yourusername
replace-with-a-long-random-secret-key
```

## 8. Configure static and media files

In PythonAnywhere **Web** tab, add static files mappings:

```text
URL:       /static/
Directory: /home/yourusername/company/staticfiles
```

```text
URL:       /media/
Directory: /home/yourusername/company/media
```

## 9. Add DNS record

In the DNS panel for `idealtechnos.com`, add the CNAME record PythonAnywhere gives you.

It will look similar to:

```text
Type:  CNAME
Name:  portal
Value: yourusername.pythonanywhere.com
```

Use the exact value shown in PythonAnywhere.

## 10. Reload web app

Return to PythonAnywhere **Web** tab and click:

```text
Reload
```

Then open:

```text
https://portal.idealtechnos.com
```

## 11. Link from existing website

Add this link to the existing `idealtechnos.com` website:

```html
<a href="https://portal.idealtechnos.com">Student Portal</a>
```
