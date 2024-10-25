from datetime import time

def parse_time(time_string: str) -> time:
    parts = time_string.split(":")

    h = int(parts[0]) % 24
    m = int(parts[1])
    s = int(parts[2])



    return time(h, m, s)
