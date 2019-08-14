import h5py
import numpy as np

x = np.linspace(0,1,100)
density = np.linspace(1,2,100)
T = np.linspace(9,10,100)
f = h5py.File("mytestfile1.hdf5", "w")
f.create_dataset("x", data=x)
f.create_dataset("density", data=density)
f.create_dataset("temperature", data=T)
f.close()

x = np.linspace(0,1,100)
density = np.linspace(2,3,100)
T = np.linspace(90,100,100)
f = h5py.File("mytestfile2.hdf5", "w")
f.create_dataset("x", data=x)
f.create_dataset("density", data=density)
f.create_dataset("temperature", data=T)
f.close()


f = h5py.File("mytestfile1.hdf5", "r")
print(f.keys())
