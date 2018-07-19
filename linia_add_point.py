import math

def linia_point(linia):
    y_list = []
    x_list = []
    z_list = []
    Xa = float(linia[10])
    Ya = float(linia[15])
    Xb = float(linia[11])
    Yb = float(linia[16])
    Fz = float(linia[3])
    #print(Xa, Ya, Xb, Yb)
    distance = math.sqrt((Xa-Xb)**2+(Ya-Yb)**2)
    #print(distance)
    if distance > 0:
        numer = int(distance/5)
        for element in range(numer):
            if Xa > Xb:
                x = (Xa - Xb) / numer * element + Xb
            elif Xa < Xb:
                x = (Xb - Xa) / numer * element + Xa
            y = ((Ya-Yb)/(Xa-Xb))*x+(Ya-((Ya-Yb)/(Xa-Xb))*Xa)
            if x > 0 and y > 0 and Fz > 0:
                x_list.append(round(x, 3))
                y_list.append(round(y, 3))
                z_list.append(round(Fz, 3))
            else:
                pass
        #print(x_list, y_list)
    else:
        pass
    return (x_list, y_list, z_list)