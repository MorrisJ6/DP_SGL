import rasterio, numpy, os, scipy.ndimage, time, sklearn.ensemble, osgeo.gdal
#import sys

def main():
    print("Inicializuji")
    starttime = time.perf_counter()
#-----Opticka data-----
    imagedir = "C:/Users/START/Desktop/!!!Data/S2A_MSIL2A_20210605T151911_N0300_R068_T22WEC_20210605T194737.SAFE/GRANULE/L2A_T22WEC_A031096_20210605T151910/IMG_DATA" # cesta ke slozce
    dirr10m = str(imagedir + "/R10m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 10m
    dirr20m = str(imagedir + "/R20m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    #dirr60m = str(imagedir + "/R60m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    
# Nahrani optickych snimku
    f = os.path.exists(dirr10m)
    if f == True:    
        directR10m = os.listdir(dirr10m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR10m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B02_10m.jp2"):
                b2 = r
                b2path = str(dirr10m + b2) # cesta ke snimku modreho pasma
                b2raster = rasterio.open(b2path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
                blue = b2raster.read().astype("float32")
            elif r.endswith("_B03_10m.jp2"):
                b3 = r
                b3path = str(dirr10m + b3) # cesta ke snimku zelenho pasma
                b3raster = rasterio.open(b3path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                green = b3raster.read().astype("float32")
            elif r.endswith("_B04_10m.jp2"):
                b4 = r
                b4path = str(dirr10m + b4) # cesta ke snimku cerveneho pasma
                b4raster = rasterio.open(b4path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                red = b4raster.read().astype("float32")
            elif r.endswith("_B08_10m.jp2"):
                b8 = r
                b8path = str(dirr10m + b8) # cesta ke snimku blizkeho infracerveneho pasma
                b8raster = rasterio.open(b8path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir1 = b8raster.read().astype("float32")
            else:
                continue
    else: 
        print("Slozka obsahujici rastry s rozlisenim 10m neexistuje!")
        return

    f = os.path.exists(dirr20m)
    if f == True:     
        directR20m = os.listdir(dirr20m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR20m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B05_20m.jp2"):
                b5 = r
                b5path = str(dirr20m + b5) # cesta ke snimku modreho pasma
                b5raster = rasterio.open(b5path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
                rededge1reader = b5raster.read().astype("float32")
                rededge1 = scipy.ndimage.zoom(rededge1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rasterio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                rededge2reader = b6raster.read().astype("float32")
                rededge2 = scipy.ndimage.zoom(rededge2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rasterio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                rededge3reader = b7raster.read().astype("float32")
                rededge3 = scipy.ndimage.zoom(rededge3reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rasterio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir2reader = b8Araster.read().astype("float32")
                nir2 = scipy.ndimage.zoom(nir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B11_20m.jp2"):
                b11 = r
                b11path = str(dirr20m + b11) # cesta ke snimku cerveneho pasma
                b11raster = rasterio.open(b11path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                swir1reader = b11raster.read().astype("float32")
                swir1 = scipy.ndimage.zoom(swir1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B12_20m.jp2"):
                b12 = r
                b12path = str(dirr20m + b12) # cesta ke snimku blizkeho infracerveneho pasma
                b12raster = rasterio.open(b12path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                swir2reader = b12raster.read().astype("float32")
                swir2 = scipy.ndimage.zoom(swir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            else:
                continue
    else:
        print("Slozka obsahujici rastry s rozlisenim 20m neexistuje!")
    
    # Smazani nepotrebnych promennych
    del b2, b3, b4, b5, b6, b7, b8, b8A, b11, b12, b2path, b3path, b4path, b5path, b6path, b7path, b8path, b8Apath, b11path, b12path
    del b3raster, b4raster, b5raster, b6raster, b7raster, b8raster, b8Araster, b11raster, b12raster
    del rededge1reader, rededge2reader, rededge3reader, nir2reader, swir1reader, swir2reader, f, imagedir, imagedir, directR10m, 
    del directR20m, dirr10m, dirr20m

# Vypocet indexu TCwet, AWEIsh/nsh, NDWIice, NDSI
    
    #NDWIice blue, red
    #"--------------------------NDWIice----------------------------------------"
    NDWIice = numpy.divide((blue - red), (blue + red), out = numpy.zeros_like(blue - red), where = (blue + red) != 0)

    #NDSI green, swir1
    #"-----------------------------NDSI----------------------------------------"
    NDSI = numpy.divide((green - swir1), (green + swir1), out = numpy.zeros_like(green - swir1), where = (green + swir1) != 0)

    #TCwet blue, green, red, nir1, swir1, swir2
    #"-----------------------------TCwet---------------------------------------"
    TCwet = numpy.array(0.1509 * blue + 0.1973 * green + 0.3279 * red + 0.3406 * nir1 - 0.7112 * swir1 - 0.4572 * swir2, dtype = "float32") 

    #AWEIsh blue, green, nir1, swir1, swir2
    #"-----------------------------AWEIsh--------------------------------------"
    AWEIsh = numpy.array(blue + 2.5 * green - 1.5 * (nir1 + swir1) - 0.25 * swir2, dtype = "float32")

    #Aweinsh  green, nir1, swir1, swir2
    #"-----------------------------AWEInsh-------------------------------------"
    AWEInsh = numpy.array(4 * (green - swir1) - (0.25 * nir1 + 2.75 * swir2), dtype = "float32")

    #print(numpy.size(blue))
    #print(numpy.size(swir1))
    #print(numpy.size(NDSI))
    #print(numpy.size(AWEInsh))

    #stack = numpy.stack((blue, green, red, rededge1, rededge2, rededge3, nir1, nir2, swir1, swir2, NDWIice, NDSI, TCwet, AWEIsh, AWEInsh), axis = 0)
    #print(stack)

    #classifier = sklearn.ensemble.RandomForestClassifier(n_estimators = 15)

# Parametry pro tvorbu vystupniho rastru
    rows_source = b2raster.height
    cols_source = b2raster.width
    transform_source = b2raster.transform
    reference_system_source = b2raster.crs
    print(rows_source, cols_source, transform_source, reference_system_source) 



#-----SAR-----
# Nahrani SAR snimku
    sarreader = "C:/Users/START/Desktop/!!!Data/S1A_IW_GRDH_1SDH_20210802T095223_20210802T095248_039049_049B89_FFDF.SAFE/measurement/"
    f = os.path.exists(sarreader)
    if f == True:    
        directSAR = os.listdir(sarreader) # cteni slozky obsahujici Sentinel-1 snimky s rozlisenim 10m
        for r in directSAR: # prohledani slozky obsahujici Sentinel-1 snimky
            if r.startswith("s1a-iw-grd-hh"):
                hh = r
                hhpath = str(sarreader + hh) # cesta ke snimku s HH polarizaci
                hhraster = rasterio.open(hhpath, driver = "GTiff") # cteni snimku s HH polarizaci
            elif r.startswith("s1a-iw-grd-hv"):
                hv = r
                hvpath = str(sarreader + hv) # cesta ke snimku HV polarizaci
                hvraster = rasterio.open(hvpath, driver = "GTiff") # cteni snimku s HV polarizaci
    else:
        print("Slozka obsahujici SAR snimky neexistuje!")
        return
    
    stoptime = time.perf_counter()
    print("Doba trvani v sekundach: ", stoptime - starttime)

if __name__ == "__main__":
    main()
