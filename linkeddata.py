
from dissmodel.core import Model, Environment

from dissmodel.core.spatial import regular_grid, fill, dw_query

from dissmodel.visualization import Map

from dissmodel.visualization.streamlit import StreamlitMap, display_inputs


from matplotlib.colors import ListedColormap




############################
### Criação do espaço simulado


sparql = '''

prefix dbc-measure: <http://www.purl.org/linked-data/dbcells/measure#>
prefix qb: <http://purl.org/linked-data/cube#>
prefix dbc-code: <http://www.purl.org/linked-data/dbcells/code#>
prefix dbc-attribute: <http://www.purl.org/linked-data/dbcells/attribute#>
prefix sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
prefix ds: <https://purl.org/dbcells/dataset#> 

SELECT ?id ?dist_river ?wkt 
where {
    ?cell geo:asWKT ?wkt;
        sdmx-dimension:refArea "PA".

    ?id a qb:Observation;
        qb:dataSet ds:7bbec547-e601-40a4-9991-1b25d05d4af4;
        sdmx-dimension:refArea ?cell;
        dbc-measure:distance ?dist_river.

}
'''

gdf = dw_query ("lambdageo/luccmebrdrivers", sparql)

# Criação do ambiente de simulação, que integra espaço, tempo e agentes
env = Environment(
    gdf=gdf,
    end_time=2,
    start_time=0
)


############################
### Visualização da simulação



# Mapeamento de cores personalizado para os estados das células
plot_params={ "column":"dist_river","cmap": "Blues"}

# Componente de visualização do mapa
Map(
    plot_params=plot_params
)

############################
### Execução da simulação

# Inicia a simulação quando o botão for clicado
env.run()
