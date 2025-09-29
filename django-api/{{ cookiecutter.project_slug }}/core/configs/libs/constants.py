from datetime import timedelta


JWT_TIMEOUTS = {
    "development": timedelta(minutes=30),
    "production": timedelta(minutes=50),
}
