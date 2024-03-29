import rasterio, numpy, os, scipy.ndimage, time, sklearn.ensemble, sklearn.tree, sklearn.neural_network, sklearn.model_selection, sklearn.metrics, pandas, datetime
import matplotlib
from matplotlib import pyplot
from osgeo import gdal
#import sys

# ValueError: X has 120560400 features, but RandomForestClassifier is expecting 15 features as input.

def main():
    starttime = time.perf_counter()
    print("Inicializuji")
    print(datetime.datetime.now())

#---------------Smazani souboru z predchoziho spusteni------------------
    if os.path.exists("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt"):
        os.remove("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt")
    if os.path.exists("C:/Users/START/Desktop/!!!Data/class_image.tif"):
        os.remove("C:/Users/START/Desktop/!!!Data/class_image.tif")
    if os.path.exists("C:/Users/START/Desktop/!!!Data/confusion_matrix.csv"):
        os.remove("C:/Users/START/Desktop/!!!Data/confusion_matrix.csv")
    
#----------------Opticka data-----------------------------------
    imagedir = "C:/Users/START/Desktop/!!!Data/S2A_MSIL2A_20210605T151911_N0300_R068_T22WEC_20210605T194737.SAFE/GRANULE/L2A_T22WEC_A031096_20210605T151910/IMG_DATA" # cesta ke slozce
    dirr10m = str(imagedir + "/R10m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 10m
    dirr20m = str(imagedir + "/R20m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    #dirr60m = str(imagedir + "/R60m/") # cesta ke slozce obsahujici Sentinel-2 snimky s rozlisenim 20m
    #writing_dir = "C:/Users/START/Desktop/!!!Data"
    #sentinel_file = writing_dir + "sentinel_bands.tif"
    
# Nahrani optickych snimku
    f = os.path.exists(dirr10m)
    if f == True:    
        directR10m = os.listdir(dirr10m) # cteni slozky obsahujici Sentinel-2 snimky s rozlisenim 10m
        for r in directR10m: # prohledani slozky obsahujici Sentinel-2 snimky
            if r.endswith("_B02_10m.jp2"):
                b2 = r
                b2path = str(dirr10m + b2) # cesta ke snimku modreho pasma
                b2raster = rasterio.open(b2path, driver = "JP2OpenJPEG") # cteni snimku modreho pasma
                blue_read = b2raster.read().astype("float32")
                blue = numpy.array(blue_read)
            elif r.endswith("_B03_10m.jp2"):
                b3 = r
                b3path = str(dirr10m + b3) # cesta ke snimku zelenho pasma
                b3raster = rasterio.open(b3path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                green_read = b3raster.read().astype("float32")
                green = numpy.array(green_read)
            elif r.endswith("_B04_10m.jp2"):
                b4 = r
                b4path = str(dirr10m + b4) # cesta ke snimku cerveneho pasma
                b4raster = rasterio.open(b4path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                red_read = b4raster.read().astype("float32")
                red = numpy.array(red_read)
            elif r.endswith("_B08_10m.jp2"):
                b8 = r
                b8path = str(dirr10m + b8) # cesta ke snimku blizkeho infracerveneho pasma
                b8raster = rasterio.open(b8path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir1_read = b8raster.read().astype("float32")
                nir1 = numpy.array(nir1_read)
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
                rededge1_zoom = scipy.ndimage.zoom(rededge1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge1 = numpy.array(rededge1_zoom)
            elif r.endswith("_B06_20m.jp2"):
                b6 = r
                b6path = str(dirr20m + b6) # cesta ke snimku zelenho pasma
                b6raster = rasterio.open(b6path, driver = "JP2OpenJPEG") # cteni snimku zeleneho pasma
                rededge2reader = b6raster.read().astype("float32")
                rededge2_zoom = scipy.ndimage.zoom(rededge2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge2 = numpy.array(rededge2_zoom)
            elif r.endswith("_B07_20m.jp2"):
                b7 = r
                b7path = str(dirr20m + b7) # cesta ke snimku cerveneho pasma
                b7raster = rasterio.open(b7path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                rededge3reader = b7raster.read().astype("float32")
                rededge3_zoom = scipy.ndimage.zoom(rededge3reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                rededge3 = numpy.array(rededge3_zoom)
            elif r.endswith("_B8A_20m.jp2"):
                b8A = r
                b8Apath = str(dirr20m + b8A) # cesta ke snimku blizkeho infracerveneho pasma
                b8Araster = rasterio.open(b8Apath, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                nir2reader = b8Araster.read().astype("float32")
                nir2_zoom = scipy.ndimage.zoom(nir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                nir2 = numpy.array(nir2_zoom)
            elif r.endswith("_B11_20m.jp2"):
                b11 = r
                b11path = str(dirr20m + b11) # cesta ke snimku cerveneho pasma
                b11raster = rasterio.open(b11path, driver = "JP2OpenJPEG") # cteni snimku cerveneho pasma
                swir1reader = b11raster.read().astype("float32")
                swir1_zoom = scipy.ndimage.zoom(swir1reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir1 = numpy.array(swir1_zoom)
            elif r.endswith("_B12_20m.jp2"):
                b12 = r
                b12path = str(dirr20m + b12) # cesta ke snimku blizkeho infracerveneho pasma
                b12raster = rasterio.open(b12path, driver = "JP2OpenJPEG") # cteni snimku blizkeho infracerveneho pasma
                swir2reader = b12raster.read().astype("float32")
                swir2_zoom = scipy.ndimage.zoom(swir2reader, (1,2,2), order=0) #zmena velikosti pixelu z 20m na 10m
                swir2 = numpy.array(swir2_zoom)
            else:
                continue
    else:
        print("Slozka obsahujici rastry s rozlisenim 20m neexistuje!")
    
    # Smazani nepotrebnych promennych
    del b2, b3, b4, b5, b6, b7, b8, b8A, b11, b12, b3path, b4path, b5path, b6path, b7path, b8path, b8Apath, b11path, b12path
    del b3raster, b4raster, b5raster, b6raster, b7raster, b8raster, b8Araster, b11raster, b12raster
    del rededge1reader, rededge2reader, rededge3reader, nir2reader, swir1reader, swir2reader, f, r, imagedir, directR10m, 
    del directR20m, dirr10m, dirr20m

    #print(b2raster.crs)

# Vypocet indexu TCwet, AWEIsh/nsh, NDWIice, NDSI

    # Parametry pro tvorbu vystupniho rastru
    rows_source = b2raster.height
    cols_source = b2raster.width
    #print(rows_source, cols_source)
    b2raster_source = gdal.Open(b2path, gdal.GA_ReadOnly)
    transform_source = b2raster_source.GetGeoTransform()
    #print(transform_source)
    reference_system_source = b2raster_source.GetProjectionRef()
    #print(reference_system_source)


    #print(rows_source, cols_source, transform_source, reference_system_source) 
    
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

    #"---------------------------Trenovaci data--------------------------------"
    

    train_samples = pandas.read_csv("C:/Users/START/Desktop/!!!Data/roi_body_tecka.csv", sep = ";")
    X = train_samples[["blue","green","red","rededge1","rededge2","rededge3","nir1","nir2","swir1","swir2","AWEInsh","AWEIsh","NDSI","NDWIICE","TCwet"]]
    #print(X)
    y = train_samples["typ"]
    #print(y)

    stack_pre = numpy.stack((blue, green, red, rededge1, rededge2, rededge3, nir1, nir2, swir1, swir2, AWEInsh, AWEIsh, NDSI, NDWIice, TCwet), axis = 0)
    #print(stack_pre[3,(1000,1000)])
    stack_np = numpy.reshape(stack_pre, [cols_source * rows_source, 15])
    #print(stack_np[3,10000000])
    #print(stack_np[0])
    stack = pandas.DataFrame(stack_np, dtype = "float32")
    #print(stack.shape)

    #"------------Presnost predpovedi dat na zaklade trenovacich dat------------"
    classifier = sklearn.ensemble.RandomForestClassifier(n_estimators = 50, oob_score= True) 
    #classifier = sklearn.tree.DecisionTreeClassifier() 
    #classifier = sklearn.neural_network.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    
    classifier.fit(X, y.values)
    
    bands = ["blue","green","red", "rededge1","rededge2","rededge3","nir1","nir2","swir1","swir2","AWEInsh","AWEIsh","NDSI","NDWIICE","TCwet"]

    data_frame = pandas.DataFrame(dtype = "float32")
    data_frame["ROI"] = y
    data_frame["Prediction"] = classifier.predict(X)
    print("---------------------------CROSS TABULKA-----------------------------")
    print(pandas.crosstab(data_frame['ROI'], data_frame['Prediction'], margins=True))
    #with open("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt", "w") as f:
    #    f.write(pandas.crosstab(data_frame['ROI'], data_frame['Prediction'], margins=True)+"\n")
    print("----------------------------OOB---------------------------------------")

    with open("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt", "w") as f:
        print("Predpoved OOB predikce je: {} %".format(classifier.oob_score_ * 100))
        f.write("Predpoved OOB predikce je: {} %\n".format(classifier.oob_score_ * 100))
        print("-------------------------Dulezitost pasem-------------------------------")
        for band, importance in zip(bands, classifier.feature_importances_):
            print("Dulezitost pasma {} pro klasifikator je: {} %".format(band, importance * 100))
            f.write("Dulezitost pasma {} pro klasifikator je: {} %\n".format(band, importance * 100))


    print("-------------------------Presnost--------------------------------")
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X.values, y.values, test_size = 0.25)
    classifier.fit(X_train, y_train)
    pred_test = classifier.predict(X_test)
    accurancy = sklearn.metrics.accuracy_score(y_test, pred_test)
    print("Presnost: {} %".format(accurancy * 100))
    kappa = sklearn.metrics.cohen_kappa_score(y_test, pred_test)
    print("Kappa koeficient: {}".format(kappa * 100))
    
    with open("C:/Users/START/Desktop/!!!Data/Accuracy_and_parameters.txt", "a") as f:
        f.write("Presnost: {} %\n".format(accurancy * 100))
        f.write("Kappa koeficient: {}".format(kappa * 100))

    #"-------------------------Klasifikace snimku-------------------------------"
    classifier.fit(X.values, y.values)
    prediction = classifier.predict(stack)
    print(prediction.shape)
    
    #lst = []
    #for pixel in prediction:
    #    lst.append(pixel)
    #arr = numpy.array(lst)
    #print(numpy.amax(arr))
    
    class_image = numpy.reshape(prediction, (b2raster.height, b2raster.width))
    print(class_image.shape)

    driver = gdal.GetDriverByName('GTiff')
    rows = class_image.shape[0]
    cols = class_image.shape[1]
    raster_out = driver.Create("C:/Users/START/Desktop/!!!Data/class_image.tif", cols, rows, 1, gdal.GDT_Int32)
    raster_out.SetGeoTransform(transform_source)
    raster_out.SetProjection(reference_system_source)
    band = raster_out.GetRasterBand(1)
    band.WriteArray(class_image)

    
    #"-----------------------Vizualizace-----------------------------------"
    classes = {
        1 : ("Vodni plocha", "#070447"),
        2 : ("Snih", "#e4e4ed"),
        3 : ("Led", "#3c4d52"),
        4 : ("Bare rock", "#361e0a")
    }

    classes_colors = []
    classes_labels = []

    for key in classes:
        values = classes.get(key)
        label = values[0]
        color = values[1]

        classes_labels.append(label)
        classes_colors.append(color)

    fig = pyplot.figure(figsize=(18,12))
    cmap = pyplot.matplotlib.colors.ListedColormap(classes_colors, N = 4) #colormap
    ax = fig.add_subplot(121) 
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(class_image,cmap=cmap)
    ax.title.set_text("Klasifikace")
    pyplot.show()

    stoptime = time.perf_counter()
    print("Doba trvani v minutach: ", (stoptime - starttime) / 60)
    return

    #with rasterio.open("C:/Users/START/Desktop/!!!Data/class_imagetttt.tif",
    #                mode = "w",
    #                driver = "GTiff",
    #                height = np_array.shape[1],
    #                width = np_array.shape[2],
    #                count = 1,
    #                dtype = np_array.dtype
    #                ) as dataset:
    #                dataset.write(np_array)



    #with rasterio.open(new_raster, "w", driver = "GTiff", height = rows_source, width = cols_source, count = 1, crs = reference_system_source, transform = transform_source, dtype = "float32") as w:
    #    w.write(class_image)


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
                continue
    else:
        print("Slozka obsahujici SAR snimky neexistuje!")
        return

    return 0 
    #print(hhraster.shape)
    #print(hhraster.crs)
    #hr = hhraster.read().astype("float32")
    #print(hr)

    
    #stoptime = time.perf_counter()
    #print("Doba trvani v sekundach: ", stoptime - starttime)

if __name__ == "__main__":
    main()

    #with fiona.open("C:/Users/START/Desktop/!!!Data", "r") as shp :
    #    clip = [feature["geometry"] for feature in shp]
    #print(clip)
    #print(numpy.size(blue))
    #print(numpy.size(swir1))
    #print(numpy.size(NDSI))
    #print(numpy.size(AWEInsh))
