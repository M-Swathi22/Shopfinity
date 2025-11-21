import os
import dj_database_url

# --------------------------
# DATABASE (Railway MySQL)
# --------------------------

# Railway gives: MYSQL_URL
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("MYSQL_URL"),
        conn_max_age=600,
        ssl_require=False
    )
}

# --------------------------
# STRIPE KEYS
# --------------------------

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# --------------------------
# DJANGO SECRET KEY
# --------------------------

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
MYSQL_URL = mysql://root:yCtOEzurgzaDYBvXHUrRPmKkbNufQkJr@mysql.railway.internal:3306/railway