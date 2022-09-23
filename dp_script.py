import rasterio as rio, numpy as np, os, scipy.ndimage as sp, time, pandas as pd, sklearn.metrics as metrics, sklearn.ensemble as scikit
import pandas as pd, sklearn.model_selection as model, datetime as dt

def main():

    """
    Hlavni funkce programu. Nacte cestu k souborum s daty Sentinel-2, spusti casovac a zavola funkci nacteni_dat.
    """
    print(dt.datetime.now())
    starttime = time.perf_counter() # Spusteni casovace
    image_dir = "C:/Users/START/Desktop/!!!Data/S2A_MSIL2A_20210605T151911_N0300_R068_T22WEC_20210605T194737.SAFE/GRANULE/L2A_T22WEC_A031096_20210605T151910/IMG_DATA" # Cesta ke slozce
    train_samples_file = "C:/Users/START/Desktop/!!!Data/roi_body_tecka.csv"
    nacteni_dat(image_dir, train_samples_file) # Zavolani funkce nacteni_dat
    stoptime = time.perf_counter() # Zastaveni casovace
    doba_behu = (stoptime - starttime) / 60 # Vypocet casu behu programu v minutach

    if doba_behu >= 1.0: # Kosmeticka funkce, ktera rozhodne, zda cas vypsat v sekundach nebo minutach, hodiny snad nebudou potreba :)
        doba_behu_m = format(doba_behu, '.2f') 
        print("Doba behu programu byla: {} minut.".format(doba_behu_m))
    else:
        doba_behu_s = format(doba_behu * 60, '.2f')
        print("Doba behu programu byla: {} sekund.".format(doba_behu_s))
    print("Program probehl uspesne.")
    exit(0)

def nacteni_dat(imagedir, train_samples_file):

    """
    Funkce projde danou slozku, nacte rastry Sentinel-2 a prevede je do numpy matic. Zaroven pripravi trenovaci data pro dalsi praci a informace
    o rastru, ktery bude pozdeji vytvoren.
    Vstupem je slozka obsahujici vstupni rastry Sentinel-2 a csv soubor obsahujici trenovaci data.
    Vystupem jsou nactene rastry prevedene do numpy matic, ktere vstupuji do zavolene funkce vypoctu indexu. Spolu s nimi pak pokracuji i trenovaci data 
    a udaje o rastru.  
    """ 

    dirr10m = str(imagedir + "/R10m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 10m
    dirr20m = str(imagedir + "/R20m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m

    f = os.path.exists(dirr10m)
    if f == True:    
        directR10m = os.listdir(dirr10m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR10m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B02_10m.jp2"):
                b2 = r
                b2path = str(dirr10m + b2) # cesta ke snimku modreho pasma
                b2raster = rio.open(b2path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
                crs = b2raster.crs # souradnicovy system
                transform = b2raster.transform # transformace
                width = b2raster.width # pocet sloupcu
                height = b2raster.height # pocet radku
                blue_read = b2raster.read().astype("float32")
                blue_1D = blue_read.reshape(width * height)
                blue = np.array(blue_1D)
            elif r.endswith("_B03_10m.jp2"):
                b3 = r
                b3path = str(dirr10m + b3) # cesta ke snimku zelenho pasma
                b3raster = rio.open(b3path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                green_read = b3raster.read().astype("float32")
                green_1D = green_read.reshape(width * height)
                green = np.array(green_1D)
            elif r.endswith("_B04_10m.jp2"):
                b4 = r
                b4path = str(dirr10m + b4) # cesta ke snimku cerveneho pasma
                b4raster = rio.open(b4path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                red_read = b4raster.read().astype("float32")
                red_1D = red_read.reshape(width * height)
                red = np.array(red_1D)
            elif r.endswith("_B08_10m.jp2"):
                b8 = r
                b8path = str(dirr10m + b8) # cesta ke snimku blizkeho infracerveneho pasma
                b8raster = rio.open(b8path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir1_read = b8raster.read().astype("float32")
                nir1_1D = nir1_read.reshape(width * height)
                nir1 = np.array(nir1_1D)
            else:
                continue
    else: 
        print("Slozka obsahujici rastry s rozlisenim 10m neexistuje!")
        exit(1)

    f = os.path.exists(dirr20m)
    if f == True:     
        directR20m = os.listdir(dirr20m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR20m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B05_20m.jp2"):
                b5 = r
                b5path = str(dirr20m + b5) # cesta ke snimku modreho pasma
                b5raster = rio.open(b5path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
                rededge1reader = b5raster.read().astype("float32")
                rededge1_zoom = sp.zoom(rededge1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge1_1D = rededge1_zoom.reshape(width * height)
                rededge1 = np.array(rededge1_1D)
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                rededge2reader = b6raster.read().astype("float32")
                rededge2_zoom = sp.zoom(rededge2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge2_1D = rededge2_zoom.reshape(width * height)
                rededge2 = np.array(rededge2_1D)
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                rededge3reader = b7raster.read().astype("float32")
                rededge3_zoom = sp.zoom(rededge3reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge3_1D = rededge3_zoom.reshape(width * height)
                rededge3 = np.array(rededge3_1D)
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir2reader = b8Araster.read().astype("float32")
                nir2_zoom = sp.zoom(nir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                nir2_1D = nir2_zoom.reshape(width * height)
                nir2 = np.array(nir2_1D)
            elif r.endswith("_B11_20m.jp2"):
                b11 = r
                b11path = str(dirr20m + b11) # cesta ke snimku cerveneho pasma
                b11raster = rio.open(b11path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                swir1reader = b11raster.read().astype("float32")
                swir1_zoom = sp.zoom(swir1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir1_1D = swir1_zoom.reshape(width * height)
                swir1 = np.array(swir1_1D)
            elif r.endswith("_B12_20m.jp2"):
                b12 = r
                b12path = str(dirr20m + b12) # cesta ke snimku blizkeho infracerveneho pasma
                b12raster = rio.open(b12path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                swir2reader = b12raster.read().astype("float32")
                swir2_zoom = sp.zoom(swir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir2_1D = swir2_zoom.reshape(width * height)
                swir2 = np.array(swir2_1D)
            else:
                continue
    else:
        print("Slozka obsahujici rastry s rozlisenim 20m neexistuje!")
        exit(1)

    train_samples = pd.read_csv(train_samples_file, sep = ";") # Cteni souboru s trenovacimi daty ve formatu csv
    X = train_samples[["blue","green","red","rededge1","rededge2","rededge3","nir1","nir2","swir1","swir2","AWEInsh","AWEIsh","NDSI","NDWIICE","TCwet"]] # Sloupce obsahuji hodnoty pixelu trenovacich dat pro jednotlive pasma a indexy
    y = train_samples["typ"] # Sloupec s typem landcoveru

    vypocet_indexu(blue, green, red, nir1, rededge1, rededge2, rededge3, nir2, swir1, swir2, X, y, crs, transform, height, width) # Zavolani nasleduji funkce
    return

def vypocet_indexu(blue, green, red, nir1, rededge1, rededge2, rededge3, nir2, swir1, swir2, X, y, crs, transform, height, width):

    """
    Funkce vypocita 5 indexu z matic nactenych v predchozi funkci. Dale pak vytvori vicerozmernou matici, kterou prevede na 2D matici 
    o velikosti [pocet pasem (15), pocet sloupcu krat pocet radku (120 560 400)]. Funkce zaroven postoupi trenovaci data a informace
    o puvodnich rastrech dalsi funkci.
    Vstupem jsou numpy matice z predchozi funkce a promenne vytvorene z trenovacich dat.
    Vystupem je 2D matice tvorena vstupnimi maticemi spolu s nove vypocitanymi maticemi indexu, ktera vstupuje do funkce tvorba_rastru spolu 
    s trenovacimi daty a informace o puvodnich rastrech.
    """
    
    NDWIice = np.divide((blue - red), (blue + red), out = np.zeros_like(blue - red), where = (blue + red) != 0) # Vypocet NDWice
    NDSI = np.divide((green - swir1), (green + swir1), out = np.zeros_like(green - swir1), where = (green + swir1) != 0) # Vypocet NDSI
    TCwet = np.array(0.1509 * blue + 0.1973 * green + 0.3279 * red + 0.3406 * nir1 - 0.7112 * swir1 - 0.4572 * swir2, dtype = "float32") # Vypocet TCwet 
    AWEIsh = np.array(blue + 2.5 * green - 1.5 * (nir1 + swir1) - 0.25 * swir2, dtype = "float32") # Vypocet AWEIsh
    AWEInsh = np.array(4 * (green - swir1) - (0.25 * nir1 + 2.75 * swir2), dtype = "float32") # Vypocet AWEInsh

    
    matrix_stack = np.stack((blue, green, red, rededge1, rededge2, rededge3, nir1, nir2, swir1, swir2, AWEInsh, AWEIsh, NDSI, NDWIice, TCwet), axis = 0) # Vytvoreni vicerozmerne matice obsahujici vsech pasma a indexy
    matrix = matrix_stack.transpose() # Transpozice matice pro dalsi zpracovani
    klasifikator(matrix, X, y, height, width, crs, transform) # Zavolani nasledujici funkce
    return

def klasifikator(matrix, X, y, height, width, crs, transform):

    """
    Popis 
    Vstup
    Vystup
    """

    classifier = scikit.RandomForestClassifier(n_estimators = 50, oob_score= True) # Zavolani klasifikatoru
    classifier.fit(X, y.values) # Fitting trenovacich dat
    
    bands = ["blue","green","red", "rededge1","rededge2","rededge3","nir1","nir2","swir1","swir2","AWEInsh","AWEIsh","NDSI","NDWIICE","TCwet"]

    data_frame = pd.DataFrame(dtype = "float32")
    data_frame["ROI"] = y # 
    data_frame["Prediction"] = classifier.predict(X) # 
    print(pd.crosstab(data_frame['ROI'], data_frame['Prediction'], margins=True)) # Matice zamen

    with open("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt", "w") as f:
        print("Predpoved OOB predikce je: {} %".format(classifier.oob_score_ * 100))
        f.write("Predpoved OOB predikce je: {} %\n".format(classifier.oob_score_ * 100)) # Zapis OOB statistiky do textoveho souboru
        for band, importance in zip(bands, classifier.feature_importances_):
            print("Dulezitost pasma {} pro klasifikator je: {} %".format(band, importance * 100))
            f.write("Dulezitost pasma {} pro klasifikator je: {} %\n".format(band, importance * 100)) # Zapis dulezitosti jednotlivych parametru do textoveho souboru

    X_train, X_test, y_train, y_test = model.train_test_split(X.values, y.values, test_size = 0.25) # Rozdeleni trenovacich dat pro testovani klasifikatoru
    classifier.fit(X_train, y_train) # Fitting vetsi casti trenovacich dat pro trenovavi
    pred_test = classifier.predict(X_test) # Klasifikace testovaci casti 
    accurancy = metrics.accuracy_score(y_test, pred_test) # Presnost
    print("Presnost: {} %".format(accurancy * 100))
    kappa = metrics.cohen_kappa_score(y_test, pred_test) # Kappa koeficient
    print("Kappa koeficient: {}".format(kappa * 100))
    
    with open("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt", "a") as f:
        f.write("Presnost: {} %\n".format(accurancy * 100)) # Zapis hodnoty presnosti do textoveho souboru 
        f.write("Kappa koeficient: {}".format(kappa * 100)) # Zapis hodnoy Kappa koeficientu do textoveho souboru

    class_image = classifier.predict(matrix) # Klasifikace matice obsahujici pasma a indexy

    tvorba_binarni_rastru(class_image, height, width, crs, transform)
    #tvorba_vystupu(class_image, height, width, crs, transform)
    return

def tvorba_binarni_rastru(class_image, height, width, crs, transform):
    for pixel in range(len(class_image)):
        if class_image[pixel] == 1:
            continue
        elif class_image[pixel] != 1:
            class_image[pixel] = 0
    #print(l)
    #class_list = np.array(l)
    #print((np.min(class_image)), np.max(class_image))
    tvorba_vystupu(class_image, height, width, crs, transform)
    return


def tvorba_vystupu(class_image, height, width, crs, transform):

    """
    Popis
    Vstup
    Vystup
    """


    class_image_reshape = class_image.reshape(width, height)

    with rio.open("C:/Users/START/Desktop/!!!Data/class_image_testing_binary.tif",
                    mode = "w",
                    driver = "GTiff",
                    height = height,
                    width = width,
                    count = 1,
                    dtype = "float32",
                    crs = crs,
                    transform = transform
                    ) as dataset:
                    dataset.write(class_image_reshape, 1)
    return

if __name__ == "__main__": 
    main() # Zavolani programu
