
import dissmodel


import geopandas as gpd
import numpy as np
from shapely.geometry import box

import matplotlib.pyplot as plt

# gera celulas menores
def regular_grid_(gdf=None, bounds=None, resolution=1000, attrs={}, crs="EPSG:29902"):
    """
    Cria um grid regular de quadrados com resolução fixa.
    
    Parameters:
        gdf (GeoDataFrame, opcional): Para calcular os limites.
        bounds (tuple, opcional): (xmin, ymin, xmax, ymax) se gdf não for passado.
        resolution (float): Tamanho da célula do grid (largura e altura).
        attrs (dict): Atributos adicionais.
        crs (str): Sistema de referência (ex.: "EPSG:4326").
    
    Returns:
        GeoDataFrame: Células do grid como polígonos.
    """
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    elif gdf is not None:
        xmin, ymin, xmax, ymax = gdf.total_bounds
    else:
        raise ValueError("Forneça um GeoDataFrame ou bounds.")

    # Calcular número de células necessárias para cobrir os limites
    x_count = int(np.ceil((xmax - xmin) / resolution))
    y_count = int(np.ceil((ymax - ymin) / resolution))

    # Reajustar limites para evitar 'buracos'
    xmax_adj = xmin + x_count * resolution
    ymax_adj = ymin + y_count * resolution

    x_edges = np.arange(xmin, xmax_adj, resolution)
    y_edges = np.arange(ymin, ymax_adj, resolution)

    # Criar as células do grid
    grid_cells = []
    ids = []
    for i, x0 in enumerate(x_edges):
        for j, y0 in enumerate(y_edges):
            x1, y1 = x0 + resolution, y0 + resolution
            poly = box(x0, y0, x1, y1)
            # Validar se interseção com bounds originais existe
            if poly.intersects(box(xmin, ymin, xmax, ymax)):
                grid_cells.append(poly.intersection(box(xmin, ymin, xmax, ymax)))
                ids.append(f"{j}-{i}")

    # Criar GeoDataFrame
    data = {"geometry": grid_cells, "id": ids}
    for key, value in attrs.items():
        data[key] = [value] * len(grid_cells)

    grid_gdf = gpd.GeoDataFrame(data, crs=crs).set_index("id")

    return grid_gdf


def regular_grid_fixed(gdf=None, bounds=None, resolution=1000, attrs={}, crs="EPSG:29902"):
    """
    Cria um grid regular com células de tamanho fixo (homogêneo) que cobre um GeoDataFrame ou bounds.
    
    Parameters:
        gdf (GeoDataFrame): GeoDataFrame para extrair bounds.
        bounds (tuple): (xmin, ymin, xmax, ymax) se não quiser usar gdf.
        resolution (float): Tamanho das células (em unidades do CRS).
        attrs (dict): Atributos adicionais a adicionar ao grid.
        crs (str): CRS do grid.
    
    Returns:
        GeoDataFrame: Grid com células regulares (mesmo tamanho).
    """
    # Obter bounds
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    elif gdf is not None:
        xmin, ymin, xmax, ymax = gdf.total_bounds
    else:
        raise ValueError("Forneça um GeoDataFrame ou bounds explícito.")
    
    # Calcular largura e altura
    width = xmax - xmin
    height = ymax - ymin
    
    # Calcular o número necessário de células para cobrir a área
    n_cols = int(np.ceil(width / resolution))
    n_rows = int(np.ceil(height / resolution))
    
    # Ajustar xmax e ymax para que o grid tenha células completas
    xmax_adj = xmin + n_cols * resolution
    ymax_adj = ymin + n_rows * resolution
    
    # Gerar os limites das células
    x_edges = np.arange(xmin, xmax_adj, resolution)
    y_edges = np.arange(ymin, ymax_adj, resolution)
    
    grid_cells = []
    ids = []
    for i, x0 in enumerate(x_edges):
        for j, y0 in enumerate(y_edges):
            x1, y1 = x0 + resolution, y0 + resolution
            poly = box(x0, y0, x1, y1)
            grid_cells.append(poly)
            ids.append(f"{j}-{i}")
    
    data = {"geometry": grid_cells, "id": ids}
    for key, value in attrs.items():
        data[key] = [value] * len(grid_cells)
    
    grid_gdf = gpd.GeoDataFrame(data, crs=crs).set_index("id")
    return grid_gdf

gdf = gpd.read_file("/home/scosta/Insync/sergio.costa@ufma.br/Google Drive/Drive/dados/shapefiles/ibge/MA_Municipios_2022.zip")

# Se quiser usar limites fixos:
#grid = regular_grid(bounds=(0, 0, 10, 10), resolution=1)

grid = regular_grid_fixed(gdf=gdf, resolution=1, attrs={'source': 'teste'})

ax = grid.plot(edgecolor="black", facecolor="none")
gdf.plot(ax=ax)
plt.show()