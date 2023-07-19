# import json
#
# import matplotlib.pyplot as plt
# import numpy as np
# from osgeo import gdal
#
#
# def find_keys(data, target_keys):
#     for key, value in data.items():
#         if key in target_keys:
#             print(f"Найден ключ '{key}': {float(value)}")
#         if isinstance(value, dict):
#             find_keys(value, target_keys)
#
#
# # Открытие снимка
# dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B10.TIF", gdal.GA_ReadOnly)
# # dataset = gdal.Open("recources2/LC08_L1TP_186018_20230618_20230623_02_T1_B10.TIF", gdal.GA_ReadOnly)
# if dataset is None:
#     exit(1)
#
# infraredBand = dataset.GetRasterBand(1)
#
# if infraredBand is None:
#     exit(1)
#
# # Получение размеров
# width = infraredBand.XSize
# height = infraredBand.YSize
#
# # Запись изображения в массив
# infraredData = infraredBand.ReadAsArray().astype(np.float64)
# # Создаем маску на основе NDVI
# Band5_dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B5.TIF", gdal.GA_ReadOnly)
# Band4_dataset = gdal.Open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_B4.TIF", gdal.GA_ReadOnly)
# # Band5_dataset = gdal.Open("recources2/LC08_L1TP_186018_20230618_20230623_02_T1_B5.TIF", gdal.GA_ReadOnly)
# # Band4_dataset = gdal.Open("recources2/LC08_L1TP_186018_20230618_20230623_02_T1_B4.TIF", gdal.GA_ReadOnly)
# if Band5_dataset is None or Band4_dataset is None:
#     exit(1)
#
# nir_band = Band5_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)
# red_band = Band4_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
# k = 0
# ndvi = (nir_band - red_band) / (nir_band + red_band)
#
# # Считываем метаданные, необходимые для вычисления
# metadataFile = open("resources/LC08_L1TP_016030_20140704_20200911_02_T1_MTL.txt", "r")
# # metadataFile = open("recources2/LC08_L1TP_016030_20140704_20200911_02_T1_MTL.txt", "r")
# if metadataFile is None:
#     exit(1)
#
# with open('resources/LC08_L1TP_016030_20140704_20200911_02_T1_MTL.json') as json_file:
#     data = json.load(json_file)
#     target_keys = ['K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10', 'RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10']
#     find_keys(data, target_keys)
#
# k1 = 0
# k2 = 0
# scale = 0
# offset = 0
# #
# # for line in metadataFile:
# #     add_index = line.find('K1_CONSTANT_BAND_10')
# #     if "K1_CONSTANT_BAND_10" in line:
# #         k1Value = line[21 + add_index:].strip()
# #         k1 = float(k1Value)
# #     add_index = line.find('K2_CONSTANT_BAND_10')
# #     if "K2_CONSTANT_BAND_10" in line:
# #         k2Value = line[21 + add_index:].strip()
# #         k2 = float(k2Value)
# #     add_index = line.find('RADIANCE_MULT_BAND_10')
# #     if "RADIANCE_MULT_BAND_10" in line:
# #         scaleValue = line[24 + add_index:].strip()
# #         scale = float(scaleValue)
# #     add_index = line.find('RADIANCE_ADD_BAND_10')
# #     if "RADIANCE_ADD_BAND_10" in line:
# #         offsetValue = line[23 + add_index:].strip()
# #         offset = float(offsetValue)
# #
# #     if k1 != 0 and k2 != 0 and scale != 0 and offset != 0:
# #         print("-_-_-_-_-_-_-_-_-_-")
# #         print("K1 =", k1)
# #         print("K2 =", k2)
# #         print("SCALE =", scale)
# #         print("OFFSET =", offset)
# #         print("-_-_-_-_-_-_-_-_-_-")
# #         break
# exit(-1)
# metadataFile.close()
#
# # Считаем температуру
#
# ln1 = len(ndvi)
# ln2 = len(ndvi[0])
# T_matrix = np.zeros((ln1, ln2))
#
# valid_indices = np.logical_and(~np.isnan(ndvi), ndvi <= 0)
# Li = scale * infraredData + offset
# T = k2 / np.log((k1 / Li) + 1) - 273.15
# T_matrix[valid_indices] = T[valid_indices]
# T_matrix[~valid_indices] = 0
# mx = np.max(T[valid_indices])
# result = np.sum(T[valid_indices])
# number_elem = np.sum(valid_indices)
#
# # print(T_matrix)
# result = result / number_elem
# # Извлечение ненулевых элементов
# non_zero_elements = T_matrix[T_matrix != 0]
#
# # Вывод ненулевых элементов
#
# print("Средняя температура:", result)
# plt.imshow(T_matrix, cmap='hot', interpolation='nearest', vmin=0)
# plt.colorbar()  # Добавление цветовой шкалы
# plt.show()
