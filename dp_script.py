import rasterio as rio, numpy as np, os, scipy.ndimage, time

def main():

    """
    Hlavni funkce programu. Nacte cestu k souborum s daty Sentinel-2, spusti casovac a funkci nacteni_dat_sentinel_2.
    """

    starttime = time.perf_counter()
    image_dir = "C:/Users/START/Desktop/!!!Data/S2A_MSIL2A_20210605T151911_N0300_R068_T22WEC_20210605T194737.SAFE/GRANULE/L2A_T22WEC_A031096_20210605T151910/IMG_DATA"
    nacteni_dat_sentinel_2(image_dir)
    stoptime = time.perf_counter()
    doba_behu = format(((stoptime - starttime) / 60), '.2f')
    print("Doba behu programu byla: {} minut".format(doba_behu))
    print("Program probehl uspesne.")
    exit(0)

def nacteni_dat_sentinel_2(imagedir):

    """
    Vstupem je slozka obsahujici vstupni rastry Sentinel-2.
    Vystupem jsou nactene rastry prevedene do numpy matic, ktere vstupuji do zavolene funkce vypoctu indexu. 
    """ 

    imagedir = imagedir
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
                blue_read = b2raster.read().astype("float32")
                blue = np.array(blue_read)
            elif r.endswith("_B03_10m.jp2"):
                b3 = r
                b3path = str(dirr10m + b3) # cesta ke snimku zelenho pasma
                b3raster = rio.open(b3path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                green_read = b3raster.read().astype("float32")
                green = np.array(green_read)
            elif r.endswith("_B04_10m.jp2"):
                b4 = r
                b4path = str(dirr10m + b4) # cesta ke snimku cerveneho pasma
                b4raster = rio.open(b4path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                red_read = b4raster.read().astype("float32")
                red = np.array(red_read)
            elif r.endswith("_B08_10m.jp2"):
                b8 = r
                b8path = str(dirr10m + b8) # cesta ke snimku blizkeho infracerveneho pasma
                b8raster = rio.open(b8path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir1_read = b8raster.read().astype("float32")
                nir1 = np.array(nir1_read)
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
                rededge1_zoom = scipy.ndimage.zoom(rededge1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge1 = np.array(rededge1_zoom)
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                rededge2reader = b6raster.read().astype("float32")
                rededge2_zoom = scipy.ndimage.zoom(rededge2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge2 = np.array(rededge2_zoom)
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                rededge3reader = b7raster.read().astype("float32")
                rededge3_zoom = scipy.ndimage.zoom(rededge3reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge3 = np.array(rededge3_zoom)
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir2reader = b8Araster.read().astype("float32")
                nir2_zoom = scipy.ndimage.zoom(nir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                nir2 = np.array(nir2_zoom)
            elif r.endswith("_B11_20m.jp2"):
                b11 = r
                b11path = str(dirr20m + b11) # cesta ke snimku cerveneho pasma
                b11raster = rio.open(b11path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                swir1reader = b11raster.read().astype("float32")
                swir1_zoom = scipy.ndimage.zoom(swir1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir1 = np.array(swir1_zoom)
            elif r.endswith("_B12_20m.jp2"):
                b12 = r
                b12path = str(dirr20m + b12) # cesta ke snimku blizkeho infracerveneho pasma
                b12raster = rio.open(b12path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                swir2reader = b12raster.read().astype("float32")
                swir2_zoom = scipy.ndimage.zoom(swir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir2 = np.array(swir2_zoom)
            else:
                continue
    else:
        print("Slozka obsahujici rastry s rozlisenim 20m neexistuje!")
        exit(1)

    vypocet_indexu(blue, green, red, nir1, rededge1, rededge2, rededge3, nir2, swir1, swir2)
    return

def vypocet_indexu(blue, green, red, nir1, rededge1, rededge2, rededge3, nir2, swir1, swir2):

    """
    Vstupem jsou numpy matice z predchozi funkce.
    Vystupem jsou predchozi matice doplnene nove vypocitanymi indexy opet ve forme matic.
    """

    NDWIice = np.divide((blue - red), (blue + red), out = np.zeros_like(blue - red), where = (blue + red) != 0)
    NDSI = np.divide((green - swir1), (green + swir1), out = np.zeros_like(green - swir1), where = (green + swir1) != 0)
    TCwet = np.array(0.1509 * blue + 0.1973 * green + 0.3279 * red + 0.3406 * nir1 - 0.7112 * swir1 - 0.4572 * swir2, dtype = "float32")
    AWEIsh = np.array(blue + 2.5 * green - 1.5 * (nir1 + swir1) - 0.25 * swir2, dtype = "float32")
    AWEInsh = np.array(4 * (green - swir1) - (0.25 * nir1 + 2.75 * swir2), dtype = "float32")
    
    return blue, green, red, nir1, rededge1, rededge2, rededge3, nir2, swir1, swir2, NDWIice, NDSI, TCwet, AWEIsh, AWEInsh
    




if __name__ == "__main__": #Volani programu
    main()
