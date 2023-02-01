# https://hatarilabs.com/ih-en/how-to-create-a-geospatial-raster-from-xy-data-with-python-pandas-and-rasterio-tutorial

import os
import pickle
import argparse
import warnings
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from libs.concentration import *
from scipy.interpolate import griddata

warnings.filterwarnings('ignore')


def get_args_parser():

    parser = argparse.ArgumentParser(description='Generate Concentration dataset')
    parser.add_argument('--dataset_root', type=str, default='./data/LAEI2019/LAEI2019-Concentrations-Data-CSV/CSV', required=False, help='root dir of dataset')
    parser.add_argument('--pollutant', type=str, default='no2', required=False, help='which pollutant is focused on')
    parser.add_argument('--epsg', type=int, default=4326, required=False, help='crs')

    args = parser.parse_args()
    assert args.pollutant in ['pm25', 'no2'], f'{args.pollutant} is not supported'
    assert args.epsg in [27700, 4326], f'{args.epsg} is not supported'
    return args


def generate_aq_raster(args):

    # --------------------------------------------------------------------------
    # settings

    pollutant = args.pollutant
    dataset_root = args.dataset_root
    epsg = args.epsg

    # output_name = f'conc_{pollutant}'
    # output_dir = os.path.join(dataset_root, output_name)
    # os.makedirs(output_dir, exist_ok=True)

    # --------------------------------------------------------------------------
    # information

    print('-' * 100)
    print(f'Pollutant:  {pollutant}')


    # --------------------------------------------------------------------------
    # Extract data of given pollutant

    conc_file = CONC_FILE[pollutant]
    conc_path = os.path.join(dataset_root, conc_file)
    conc_data = load_concentration(conc_path, True)

    # --------------------------------------------------------------------------
    # Generating raster data
    resolution = 0.001
    # x 纵的，y横的
    # xRange = np.arange(conc_data.x.min(), conc_data.x.max(), resolution)
    xRange = np.arange(conc_data.x.max(), conc_data.x.min(), -resolution)
    yRange = np.arange(conc_data.y.min(), conc_data.y.max(), resolution)
    # yRange = np.arange(conc_data.y.max(), conc_data.y.min(), -resolution)
    gridY, gridX  = np.meshgrid(yRange, xRange)
    grid_conc = griddata(list(zip(conc_data.y, conc_data.x)), conc_data.conc, (gridY, gridX), method='nearest')

    # --------------------------------------------------------------------------
    # Visualization

    plt.figure(figsize=(5, 3))
    im = plt.imshow(grid_conc, cmap='coolwarm')
    plt.colorbar(im, fraction=0.0275, pad=0.04)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------------------------
    # Save data

    from rasterio.transform import Affine
    transform = Affine.translation(gridY[0][0] - resolution / 2, gridX[0][0] - resolution / 2) * Affine.scale(resolution, -resolution)
    print(transform)
    from rasterio.crs import CRS
    rasterCrs = CRS.from_epsg(epsg)

    interpRaster = rasterio.open(f'data/{pollutant}.tif',
                                 'w',
                                 driver='GTiff',
                                 height=grid_conc.shape[0],
                                 width=grid_conc.shape[1],
                                 count=1,
                                 dtype=grid_conc.dtype,
                                 crs=rasterCrs,
                                 transform=transform,
                                 )
    interpRaster.write(grid_conc, 1)
    interpRaster.close()






if __name__ == '__main__':

    args = get_args_parser()
    generate_aq_raster(args)


