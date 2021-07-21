import os

def map_range_from_to(val, in_min, in_max, out_min, out_max):
   return ((val - in_min) / (in_max - in_min) * (out_max - out_min) + out_min )

def get_terminal_size():
    try:
        return os.get_terminal_size()[0]
    # output is most likely redirected to an IDE
    except OSError as e:
        return 100