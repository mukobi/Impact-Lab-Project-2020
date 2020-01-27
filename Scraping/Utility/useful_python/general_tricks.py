"""general tricks"""
import time
import progressbar  # install with `pip install progressbar2`

# progressbar

# simple progressbar over iterable
for i in progressbar.progressbar(range(100)):
    time.sleep(0.02)
