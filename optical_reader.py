import rasterio, os, scipy.ndimage, time

def main():
    print("Inicializuji")
#-----Opticka data-----
    imagedir = "C:/Users/START/Desktop/!!!Data/S2A_MSIL2A_20210605T151911_N0300_R068_T22WEC_20210605T194737.SAFE/GRANULE/L2A_T22WEC_A031096_20210605T151910/IMG_DATA" # cesta ke slozce
    dirr10m = str(imagedir + "/R10m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 10m
    dirr20m = str(imagedir + "/R20m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    #dirr60m?
    
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
                nir4 = b8raster.read().astype("float32")
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
                nir1reader = b5raster.read().astype("float32")
                nir1 = scipy.ndimage.zoom(nir1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rasterio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                nir2reader = b6raster.read().astype("float32")
                nir2 = scipy.ndimage.zoom(nir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rasterio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                nir3reader = b7raster.read().astype("float32")
                nir3 = scipy.ndimage.zoom(nir3reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rasterio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir5reader = b8Araster.read().astype("float32")
                nir5 = scipy.ndimage.zoom(nir5reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
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
    print("Hotovo!")

if __name__ == "__main__":
    main()
