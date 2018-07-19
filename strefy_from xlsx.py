import xlrd
import gdal_merge as gm
import numpy as np
import os
import sys
import subprocess
from krieging_mike import krigingi
from krieging_mike import max_min
from clip_gdal import python_clip
from osgeo import ogr
from gdal_merge import main
from shapely.geometry import mapping, Polygon
import matplotlib.pyplot as plt
from linia_add_point import linia_point
zestaw = [[],[],[]]
book = xlrd.open_workbook(r'C:\Test_mapping\S01_Zlotna\07_S01_Zlotna_WYNIKI\GIS\S01_Zlotna_Q1.xlsx')
sheet = book.sheet_by_index(1)
zakres = range(sheet.nrows)
plik = 0
i=0
for row in range(sheet.nrows-2):
    linia1 = sheet.row_values(row + 1)
    linia2 = sheet.row_values(row + 2)
    if linia1[2] != linia2[2] and linia1[6] == linia2[6]:
        if linia1[7] != 1 and linia1[7] != 1:
            #dwa przekroje, ten sam ciek, inny KM, wykonac interpolacje
            #print(linia1[2], linia2[2])
            if round(linia1[3], 3) == round(linia2[3], 3):
                linia2[3] = linia2[3] + 0.05
            Xa_list, Ya_list, Za_list = linia_point(linia1)
            Xb_list, Yb_list, Zb_list = linia_point(linia2)
            #plt.plot(Xa_list, Ya_list, 'ro', color='r')
            #plt.plot(Xb_list, Yb_list, 'ro', color='b')
            #plt.show()
            #generate boundary shp
            poly = Polygon([(float(linia1[10]), float(linia1[15])), (float(linia1[11]), float(linia1[16])), (float(linia2[11]), float(linia2[16])), (float(linia2[10]), float(linia2[15]))])
            driver = ogr.GetDriverByName('Esri Shapefile')
            ds = driver.CreateDataSource('boundary.shp')
            layer = ds.CreateLayer('', None, ogr.wkbPolygon)
            # Add one attribute
            layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
            defn = layer.GetLayerDefn()
            ## If there are multiple geometries, put the "for" loop here
            # Create a new feature (attribute and geometry)
            feat = ogr.Feature(defn)
            feat.SetField('id', 123)
            # Make a geometry, from Shapely object
            geom = ogr.CreateGeometryFromWkb(poly.wkb)
            feat.SetGeometry(geom)
            layer.CreateFeature(feat)
            feat = geom = None  # destroy these
            # Save and close everything
            ds = layer = feat = geom = None

            #generate interpolatet tif
            line = [Xa_list, Ya_list, Za_list]
            if len(Za_list) > 0:
                zestaw[0] = Xa_list + Xb_list
                zestaw[1] = Ya_list + Yb_list
                zestaw[2] = Za_list + Zb_list
                krok = 5
                X_min, X_max, Y_min, Y_max = max_min(zestaw)
                data = np.array(zestaw)
                data = np.transpose(data)
                print(data, X_min, X_max, Y_min, Y_max, krok)
                print(data[:, 0], data[:, 1], data[:, 2])

                krigingi(data, X_min, X_max, Y_min, Y_max, krok)
                python_clip('boundary.shp', 'Rozklad.tif', plik)



                plik+=1

                #subprocess.call("gdalwarp -dstnodata -9999 -cutline boundary.shp Rozklad.tif downtown.tif")
            else:
                pass

        else:
            pass
        #line = [Xb_list, Yb_list, Zb_list]
        #zestaw.append(line)
    elif linia1[2] == linia2[2] and linia1[6] == linia2[6]:
        #ten sam km na tym samym cieku - pominac
        pass

    if (linia1[2] != linia2[2] and linia1[6] != linia2[6]) or int(row) == int(sheet.nrows-3):
        # inny km i inny ciek
        file_path = os.getcwd()
        directory = file_path + '\\wyniki'
        import glob
        files = glob.glob(directory+"\\*.tif")
        print(files)
        print(linia1[2], linia2[2], linia1[6], linia2[6])
        main(files, out_file = r'C:\Test_mapping\S01_Zlotna\07_S01_Zlotna_WYNIKI\GIS\branchname'+str(i)+'.tif')

        #sys.argv[1:] = ['-o', directory+'\\out.tif', str(files[1]).replace("[","").replace("]",""), '-n', '9999']
        #gm.main()
        i+=1
        import shutil
        #shutil.rmtree(directory)

        #zmiana cieku, wydrukowac rastry , przejsc do nowego
    print('---')
    print(row, int(sheet.nrows-3))
    print('----')


