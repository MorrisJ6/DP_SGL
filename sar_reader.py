import rasterio, os

def main():
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

if __name__ == "__main__":
    main()
