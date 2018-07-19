from pykrige.uk import UniversalKriging
import numpy as np
import subprocess
import os
import pykrige.kriging_tools as kt

def max_min(zestaw):
    X_max = 0
    X_min = 10000000
    Y_max = 0
    Y_min = 10000000
    licz = 0
    data = np.array(zestaw)
    data = np.transpose(data)

    # print(zestaw[1][1][0])
    for i in range(len(zestaw[0])):
        if zestaw[0][licz] > X_max:
            X_max = zestaw[0][licz]
        if zestaw[0][licz] < X_min:
            X_min = zestaw[0][licz]
        if zestaw[1][licz] > Y_max:
            Y_max = zestaw[1][licz]
        if zestaw[1][licz] < Y_min:
            Y_min = zestaw[1][licz]
        licz += 1

    return(X_min, X_max, Y_min, Y_max)

def krigingi(Dane,X_min,X_max,Y_min,Y_max,krok):
    print(X_min, X_max, Y_min, Y_max)
    data = Dane
    gridx = np.arange(X_min-100, X_max+100, krok)
    gridy = np.arange(Y_min-100, Y_max+100, krok)

    # Create the ordinary kriging object. Required inputs are the X-coordinates of
    # the data points, the Y-coordinates of the data points, and the Z-values of the
    # data points. Variogram is handled as in the ordinary kriging case.
    # drift_terms is a list of the drift terms to include; currently supported terms
    # are 'regional_linear', 'point_log', and 'external_Z'. Refer to
    # UniversalKriging.__doc__ for more information.
    UK = UniversalKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear')

    # Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
    # grid of points, on a masked rectangular grid of points, or with arbitrary points.
    # (See UniversalKriging.__doc__ for more information.)
    z, ss = UK.execute('grid', gridx, gridy)

    # Writes the kriged grid to an ASCII grid file.
    kt.write_asc_grid(gridx, gridy, z, filename="Rozklad.asc")
    cwd = os.getcwd()



    # Import gdal
    from osgeo import gdal

    # Open existing dataset
    src_ds = gdal.Open(cwd+"/"+"Rozklad.asc")

    # Open output format driver, see gdal_translate --formats for list
    format = "GTiff"
    driver = gdal.GetDriverByName(format)

    # Output to new format
    dst_ds = driver.CreateCopy("Rozklad.tif", src_ds, 0)

    # Properly close the datasets to flush to disk
    dst_ds = None
    src_ds = None

    return True