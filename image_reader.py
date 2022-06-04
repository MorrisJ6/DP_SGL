import rasterio, os

def main():
    imagedir = ".../IMG_DATA" # cesta ke slozce
    dirr10m = str(imagedir + "/R10m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 10m
    dirr20m = str(imagedir + "/R20m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    #dirr60m = str(imagedir + "/R60m/")
    
    f = os.path.exists(dirr10m)
    if f == True:    
        directR10m = os.listdir(dirr10m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR10m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B02_10m.jp2"):
                b2 = r
                b2path = str(dirr10m + b2) # cesta ke snimku modreho pasma
                b2raster = rasterio.open(b2path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
            elif r.endswith("_B03_10m.jp2"):
                b3 = r
                b3path = str(dirr10m + b3) # cesta ke snimku zelenho pasma
                b3raster = rasterio.open(b3path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
            elif r.endswith("_B04_10m.jp2"):
                b4 = r
                b4path = str(dirr10m + b4) # cesta ke snimku cerveneho pasma
                b4raster = rasterio.open(b4path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
            elif r.endswith("_B08_10m.jp2"):
                b8 = r
                b8path = str(dirr10m + b8) # cesta ke snimku blizkeho infracerveneho pasma
                b8raster = rasterio.open(b8path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
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
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rasterio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rasterio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rasterio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
            elif r.endswith("_B11_20m.jp2"):
                b11 = r
                b11path = str(dirr20m + b11) # cesta ke snimku cerveneho pasma
                b11raster = rasterio.open(b11path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
            elif r.endswith("_B12_20m.jp2"):
                b12 = r
                b12path = str(dirr20m + b12) # cesta ke snimku blizkeho infracerveneho pasma
                b12raster = rasterio.open(b12path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
            else:
                continue
    else:
        print("Slozka obsahujici rastry s rozlisenim 20m neexistuje!")
        return

if __name__ == "__main__":
    main()