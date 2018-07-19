import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import codecs
from shapely.geometry import Point
import geopandas

def convert_res11(res11_lok):

    nazwa = os.path.basename(res11_lok)
    nazwa = os.path.splitext(nazwa)[0]
    if "HDAdd" not in nazwa:
        # path to the mike res11read program
        read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2011\\bin\\RES11READ.exe\""
        # creation of result directory
        lok_file = os.path.dirname(res11_lok)
        if not os.path.exists(lok_file+"\\GIS"):
            os.makedirs(lok_file+"\\GIS")

        res_lok = lok_file+"\\GIS"
    # ------------------------------------------------------------------------------------------------------------------------
        # call res11read to convert res file to xyz data of model markers M1, M2, M3
        os.system(read11res_lok + " -xyh " + res11_lok + " " + res_lok+"\\"+nazwa+".csv")
        os.system(read11res_lok + " -allres -FloodWatch " + res11_lok + " " + res_lok + "/" + nazwa + "_h.csv")

        #wywalenie majkowej inwokacji pliku
        with open(res_lok+"\\"+nazwa+".csv", 'r') as fin:
            data = fin.read().splitlines(True)

        with open(res_lok+"\\"+nazwa+".csv", 'w') as fout:
            fout.writelines(data[19:-3])

        # add new heading for the csv file
        plik = codecs.open(res_lok+"\\"+nazwa+".csv", "r", encoding = 'windows-1250')
        napis = plik.readline()
        plik2 = codecs.open(res_lok+"\\"+nazwa+"_out.csv", "w", encoding = 'utf-8')
        #"X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\n",
        title = [" X ", "Y ", "River ", "Chainage ", "Type ", "Bottom ", "LeftBank ", "RightBank ", "X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\r\n"]
        plik2.writelines(title)

        # delete redundant space sign
        while napis != '':
            licznik = 0
            napis = list(napis)
            while licznik < len(napis):
                if napis[licznik] == " ":
                    while napis[licznik + 1] == " ":
                        del napis[licznik]
                licznik += 1
            napis = "".join(napis)
            #print(napis)
            plik2.writelines(napis)
            napis = plik.readline()
        plik.close()
        plik2.close()

        with open(res_lok+"\\"+nazwa+"_h.csv") as f:
            lines = f.read().splitlines()
            TS = []
            for line in lines:
                line2 = line.split(';')
                TS.append(line2)

        with open(res_lok+"\\"+nazwa+"_out.csv") as f:
            lines = f.read().splitlines()
            srednie_L=[]
            XY = []
            for line in lines:
                line2 = line.split(' ')
                XY.append(line2[1:])
            kroki_czasowe = len(TS)-1
            df_XY = {}
            XY[0].append("H_elev")
            for i in range(len(XY)-1):
                srednia = (float(TS[kroki_czasowe][i+1])+float(TS[kroki_czasowe-1][i+1])+float(TS[kroki_czasowe-2][i+1]))/3
                last = float(TS[kroki_czasowe][i+1])
                differ = srednia - last

                XY[i+1].append(last)

                srednie_L.append(differ)


            XY2 = [[row[i] for row in XY] for i in range(len(XY[0]))]
            XY = XY2
            print(XY)

            for x in range(len(XY)):
                df_XY[XY[x][0]] = XY[x][1:]

            df = pd.DataFrame(data=df_XY)
            print(df.head())

        total_rows = df.shape[0]
        print("Ilosc wierszy: ")
        print(total_rows)
        M1 = []
        M2 = []
        M3 = []
        for i in range(total_rows):
            M1.append("M1")
            M2.append("M2")
            M3.append("M3")

        M1 = pd.Series(data=M1); M2 = pd.Series(data=M2); M3 = pd.Series(data=M3)

        koryto = df[['X', 'Y', 'H_elev', 'River', 'Chainage',]]
        koryto['M'] = M2.values

        lewy = df[['X_Marker_1', 'Y_Marker_1', 'H_elev', 'River', 'Chainage',]]
        lewy = lewy.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y'})
        lewy['M'] = M1.values

        prawy = df[['X_Marker_3', 'Y_Marker_3', 'H_elev', 'River', 'Chainage', ]]
        prawy = prawy.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y'})
        prawy['M'] = M3.values
        frames = [koryto, lewy, prawy]

        zbiorcza = pd.concat(frames)

        writer = pd.ExcelWriter(res_lok + "\\" + nazwa + '.xlsx')
        zbiorcza.to_excel(writer, 'Sheet1')
        df.to_excel(writer, 'Sheet2')
        # df_left.to_excel(writer,'LewyBrzeg')
        # df_right.to_excel(writer,'PrawyBrzeg')
        writer.save()
        writer.close()

        zbiorcza['geometry'] = zbiorcza.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        zbiorcza = geopandas.GeoDataFrame(zbiorcza, geometry='geometry')
        zbiorcza.to_file(res_lok + "\\" + nazwa + '.shp', driver='ESRI Shapefile')

    else:
        pass
    return (0)

