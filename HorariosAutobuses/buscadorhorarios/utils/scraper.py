from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from ..models import Ruta


def scraper(origen, destino):

    origen_id = origen.estacion_id
    origen_db = origen.id
    destino_id = destino.estacion_id
    destino_db = destino.id

    URL = f"http://estacionautobuses.es/en/index.php?option=com_estacionautobuses&view=buscador&task=buscarhorarios&Itemid=101&origen={origen_id}&destino={destino_id}&fechaida=00/00/0000&fechavuelta=00/00/0000&criterio=directo"

    # So-so script to get bus schedules

    web_request = requests.get(url=URL)
    soup = BeautifulSoup(web_request.text, 'html.parser')
    try:
        table_html = soup.select("#listado > table:nth-child(3)")[0]
    except:
        ruta = Ruta.objects.create(estacion_origen_id=origen_db,
                                   estacion_destino_id=destino_db, raw_json_data=None, raw_json_periodicidad=None, ruta_valida=False)
        return None
    else:
        periodicidad = []
        for fila in table_html.find_all(name="tr")[1:]:
            rutas = fila.find_all(name="td", class_="resultado")
            if rutas:
                for ruta in rutas:
                    if ruta.find_all(name="td", class_="viajeSI"):
                        viajes_si = ruta.find_all(name="td", class_="viajeSI")
                        temp_list = []
                        for viaje in viajes_si:
                            if viaje.text not in temp_list:
                                temp_list.append(viaje.text)
                        periodicidad.append(temp_list)

        json_periodicidad = json.dumps(periodicidad)

        # Scraper for estacionautobuses.es
        pd_table = pd.read_html(str(table_html))[0]
        pd_table.columns = pd_table.iloc[0]
        df = pd_table[1:]
        json_data = df.to_json(orient='records')

        ruta = Ruta.objects.create(estacion_origen_id=origen_db,
                                   estacion_destino_id=destino_db, raw_json_data=json_data, raw_json_periodicidad=json_periodicidad, ruta_valida=True)
        return ruta.slug
