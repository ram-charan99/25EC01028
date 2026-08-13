import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
print("Python :", sys.version.split()[0])
print("Numpy :", np.__version__)
print("pandas :", pd.__version__)
print("matplotlib:", matplotlib.__version__)
# a one-line smoke test of the plotting back-end
plt.plot([0, 1, 2, 3], [0, 1, 4, 9], marker="o")
plt.title("If you can see this window, the setup works")
plt.xlabel("x")
plt.ylabel("x squared")
plt.grid(True)
plt.show()
print("roll no: 25EC01028 - master")
print("roll no: 25EC01028 - branch")
print("DOB:21-07-2007")
