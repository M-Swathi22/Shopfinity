import os
import dj_database_url

# ----------------------------------
# RAILWAY MYSQL URL (STATIC BACKUP)
# ----------------------------------
MYSQL_URL = os.environ.get(
    "MYSQL_URL",
    "mysql://root:yCtOEzurgzaDYBvXHUrRPmKkbNufQkJr@caboose.proxy.rlwy.net:55554/railway"
)

# ----------------------------------
# DATABASE CONFIG
# ----------------------------------
DATABASES = {
    "default": dj_database_url.parse(
        MYSQL_URL,
        conn_max_age=600,
        ssl_require=False
    )
}

# ----------------------------------
# STRIPE KEYS
# ----------------------------------
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# ----------------------------------
# DJANGO SECRET KEY
# ----------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
