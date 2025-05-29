
from dissmodel.core import Model, Environment

from dissmodel.core.spatial import regular_grid, fill, dw_query

from dissmodel.visualization import Map

from dissmodel.visualization.streamlit import StreamlitMap, display_inputs


from matplotlib.colors import ListedColormap

import streamlit as st

import random



############################
### Interface do usuário com Streamlit

# Configuração inicial da página
st.set_page_config(page_title="Carregando dados do DBCells", layout="centered")
st.title("Dados DBCells (DisSModel)")

# Painel lateral com parâmetros ajustáveis pelo usuário
st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)

plot_info = st.empty()
plot_info.text("Carregando espaço celular do DBCells ....")

############################
### Criação do espaço simulado

@st.cache_data
def carregar_dados():
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
    return dw_query("lambdageo/luccmebrdrivers", sparql)


gdf = carregar_dados()


rows, _ = gdf.shape

plot_info.text(f"Carregado espaço com {rows} linhas")

# Botão principal para iniciar a simulação
executar = st.button("Executar Simulação")


# Criação do ambiente de simulação, que integra espaço, tempo e agentes
env = Environment(
    gdf=gdf,
    end_time=steps,
    start_time=0
)


############################
### Visualização da simulação

# Área da interface reservada para o mapa interativo
plot_area = st.empty()

# Mapeamento de cores personalizado para os estados das células
plot_params={ "column":"dist_river","cmap": "Blues_r"}

# Componente de visualização do mapa
StreamlitMap(
    plot_area=plot_area,
    plot_params=plot_params
)

############################
### Execução da simulação

# Inicia a simulação quando o botão for clicado
if executar:
    env.run()
