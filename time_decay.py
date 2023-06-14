import math

# vraća koeficijent između 0.1 i 10 za opseg od 0 do 30 dana
def get_time_decay(old_date, current_date):
    return max(0.1, min(10, 5 - math.log(max(1, (current_date - old_date).total_seconds()) / 86400) * 1.4))   # exponential
    return max(0.1, min(10, 10 - (current_date - old_date).total_seconds() / 259200))                         # linear
