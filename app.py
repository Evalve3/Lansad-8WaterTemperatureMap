import json

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

# Открытие снимка
dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B10.TIF", gdal.GA_ReadOnly)
if dataset is None:
    exit(1)

infraredBand = dataset.GetRasterBand(1)

if infraredBand is None:
    exit(1)

# Запись изображения в массив
infraredData = infraredBand.ReadAsArray().astype(np.float64)
# Создаем маску на основе NDVI
Band5_dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B5.TIF", gdal.GA_ReadOnly)
Band4_dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B4.TIF", gdal.GA_ReadOnly)
if Band5_dataset is None or Band4_dataset is None:
    exit(1)

nir_band = Band5_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)
red_band = Band4_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)

k = 0
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Считываем метаданные, необходимые для вычисления

with open('resources/LC08_L1TP_016030_20140704_20200911_02_T1_MTL.json') as json_file:
    data = json.load(json_file)
    k1 = float(data.get('LANDSAT_METADATA_FILE', {}).get('LEVEL1_THERMAL_CONSTANTS', {}).get('K1_CONSTANT_BAND_10'))
    k2 = float(data.get('LANDSAT_METADATA_FILE', {}).get('LEVEL1_THERMAL_CONSTANTS', {}).get('K2_CONSTANT_BAND_10'))
    scale = float(
        data.get('LANDSAT_METADATA_FILE', {}).get('LEVEL1_RADIOMETRIC_RESCALING', {}).get('RADIANCE_MULT_BAND_10'))
    offset = float(
        data.get('LANDSAT_METADATA_FILE', {}).get('LEVEL1_RADIOMETRIC_RESCALING', {}).get('RADIANCE_ADD_BAND_10'))

# Считаем температуру

ln1 = len(ndvi)
ln2 = len(ndvi[0])
T_matrix = np.zeros((ln1, ln2))

valid_indices = np.logical_and(~np.isnan(ndvi), ndvi <= 0)
Li = scale * infraredData + offset
T = k2 / np.log((k1 / Li) + 1) - 273.15
T_matrix[valid_indices] = T[valid_indices]
T_matrix[~valid_indices] = 0
mx = np.max(T[valid_indices])
result = np.sum(T[valid_indices])
number_elem = np.sum(valid_indices)

result = result / number_elem

print("Средняя температура:", result)
plt.imshow(T_matrix, cmap='hot', interpolation='nearest', vmin=0)
plt.colorbar()
plt.show()
