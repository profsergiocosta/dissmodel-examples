from dissmodel.core.spatial import regular_grid, fill, dw_query

import geopandas as gpd

import matplotlib.pyplot as plt

sparql = '''
        prefix geo: <http://www.opengis.net/ont/geosparql#>
        prefix sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#>
        prefix dbc: <https://purl.org/linked-data/dbcells#>

        SELECT ?cell ?resolution ?wkt 
        WHERE {
        ?cell geo:asWKT ?wkt;
            sdmx-dimension:refArea "PA".
        ?cell dbc:resolution ?resolution.
        }   
    '''
grid = dw_query("dbcells/dbcells", sparql)
grid = grid.set_crs(epsg=4326)

print (grid.head())

grid_5880 = grid.to_crs(epsg=5880)

rivers = gpd.read_file ("/home/scosta/Insync/sergio.costa@ufma.br/Google Drive/Drive/dados/paperluccmebr/dados_luccmBR/centros_urbanos_pnlt/centros_urbanos_m_10_pnlt_poly_sirgas2000.shp")
print ("preencher")
fill (

    strategy="min_distance",
    from_gdf=grid_5880,
    to_gdf=rivers,
    attr_name="min_distance"

)
print (grid_5880.head())
fig, ax = plt.subplots(figsize=(10, 10))

# Plotar os polígonos coloridos pelo valor de min_distance
grid_5880.plot(
    column='min_distance',  # Coluna usada para coloração
    cmap='viridis',         # Mapa de cores
    legend=True,            # Exibir legenda
    edgecolor=None,      # Cor das bordas
    ax=ax
)
rivers.plot(ax=ax, color='red', markersize=10, label='Pontos')  # Pontos

# Título e legenda
plt.title("Polígonos coloridos pela menor distância aos pontos")
plt.legend()
plt.show()
