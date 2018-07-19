import os

# function creates list of model simulation files and dictionary of result files defined in them
def m21_index_unite(path):
    #puste listy i liczniki na pliki typu mike
    m21_L = []; res_dfs = []
    m21res_d = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".m21"):

                # add model simulation file to list
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                m21_L.append(element)
                # read path to res11 file from model simulation file
                with open(element) as f:
                    lines = f.readlines()
                    index = lines.index("         [OUTPUT_AREA_1]\n")
                    sciezka = element.split("\\")

                    try:
                        hd_res = lines[index + 11].split("|")[1]
                        hd_res = hd_res.split("\\")
                        kropki = len(hd_res[0])
                        sciezka = sciezka[:-kropki]
                        hd_res = hd_res[1:]
                        sciezka = sciezka + hd_res
                    except:
                        hd_res = lines[index + 11].split("'")[1]
                        sciezka = sciezka[:-1]
                        hd_res = [hd_res]
                        sciezka = sciezka+hd_res
                    # add elements to result list and model - result dictionary
                    hd_res = "\\".join(sciezka)
                    m21res_d[element] = hd_res
                    res_dfs.append(hd_res)
                    #print(m21res_d)

    return (m21_L, m21res_d, res_dfs)

# function list files in directory with specified ending
def file_index(path, rozsz):
    lista = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("."+rozsz):
                element = str(os.path.join(root, file))
                element = element.replace("/", "\\")
                lista.append(element)

    return (lista)