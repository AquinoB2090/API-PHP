from app.database import fetch_one


def health():
    return {"status": "ok"}


def db_check():
    result = fetch_one("select 'connected' as status, sysdate as checked_at from dual")
    return result or {"status": "unknown"}
