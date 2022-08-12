from datetime import datetime, timedelta


def get_date_at_midnight(pdate):

    # try:
        return pdate.replace(hour=0, minute=0, second=0, microsecond=0)


def get_now_minus_days_at_mn(days):
        return get_date_at_midnight(datetime.now()) - timedelta(days=days)


"""
    except Exception as e: # unicode is a default on python 3
        print(f"strip_accents ça fait prout : {e}")
        return e
"""
