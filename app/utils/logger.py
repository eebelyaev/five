from datetime import datetime


LOG_LEVEL = 5
IS_TSTAMP = False

def log(message: str, log_level: int = LOG_LEVEL, is_tstamp: bool = IS_TSTAMP) -> None:
    if log_level > LOG_LEVEL:
        return
    
    log_str = ""
    if is_tstamp:
        now = datetime.now()
        log_str = f"[{now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] "
    
    log_str += message
    print(log_str)

