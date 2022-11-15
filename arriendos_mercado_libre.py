import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

from apk import hacer_click, enviar_texto, obtener_elementos

BUSCAR = 'arriendos'

def buscar_en_ml(driver) -> None:
    
    ## Cargar pagina de mercado libre en el navegador
    driver.get('https://www.mercadolibre.cl/')

    boton_aceptar_cookies = (By.XPATH, '//button[@class="cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept"]')

    hacer_click(driver, boton_aceptar_cookies)

    ## Buscar un producto en mercado libre
    buscador = (By.XPATH, '//*[@id="cb1-edit"]')

    enviar_texto(driver, buscador, BUSCAR)

    ## Clickear boton buscar
    boton_buscar = (By.XPATH, '//button[@class="nav-search-btn"]')

    hacer_click(driver, boton_buscar)

def buscar_urls(driver) -> list:
    lista_url_productos = []
    localizador_lista_productos = ("xpath", '//li[@class="ui-search-layout__item"]')
    lista_productos = obtener_elementos(driver, localizador_lista_productos)
    print(f'Cantidad de arriendos: {len(lista_productos)}')

    for producto in lista_productos:
        url_producto = producto.find_element("xpath", './/a[@class="ui-search-link"]').get_attribute('href')
        lista_url_productos.append(url_producto)
    
    return lista_url_productos

def encontrar_caracteristicas_arriendo(driver) -> dict:
    lista_valor_caracteristica = []
    lista_nombre_caracteristica = []

    nombre_arriendo = 'No encontrado'
    precio_departamento = 'No encontrado'
    ubicacion = 'Sin ubicacion'

    try:
        nombre_arriendo = driver.find_element("xpath",'//h1[@class="ui-pdp-title"]').get_attribute("textContent")
    except Exception as e:
        pass
    
    try:
        precio_departamento = driver.find_element("xpath",'//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]').get_attribute("textContent")
    except Exception as e:
        pass
    
    try:
        ubicacion = driver.find_element("xpath", 
            '//div[@class="ui-pdp-media ui-vip-location__subtitle ui-pdp-color--BLACK"]//p[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"]'
            ).get_attribute("textContent")
    except Exception as e:
        pass

    lista_valor_caracteristica.extend((nombre_arriendo, precio_departamento, ubicacion, ))
    lista_nombre_caracteristica.extend(('Nombre Arriendo', 'Precio Arriendo', 'Ubicacion'))

    caracteristicas = driver.find_elements("xpath", '//tr[@class="andes-table__row"]') 

    for caracteristica in caracteristicas:
        valor_caracteristica = caracteristica.find_element("xpath", './/span[@class="andes-table__column--value"]').get_attribute("textContent")
        nombre_caracteristica = caracteristica.find_element(
            "xpath", './/th[@class="andes-table__header andes-table__header--left ui-pdp-specs__table__column ui-pdp-specs__table__column-title"]'
        ).get_attribute("textContent")
        
        lista_valor_caracteristica.append(valor_caracteristica)
        lista_nombre_caracteristica.append(nombre_caracteristica)

    return dict(zip(lista_nombre_caracteristica, lista_valor_caracteristica))

def caracteristicas_por_pagina(nombre_valor:dict, url:str)->list:
    nombre_arriendo = 'Sin nombre'
    precio_departamento = 'Sin precio'
    superficie_total = 'Sin informacion'
    superficie_util = 'Sin informacion'
    ambientes = 'Sin informacion'
    dormitorios = 'Sin informacion'
    banos = 'Sin informacion'
    estacionamientos = 'Sin informacion'
    cantidad_maxima_habitantes = 'Sin informacion'
    admite_mascotas = 'Sin informacion'
    piso_de_la_unidad = 'Sin informacion'
    departamentos_por_piso = 'Sin informacion'
    cantidad_pisos_departamento = 'Sin informacion'
    orientacion = 'Sin informacion'
    gastos_comunes = 'Sin informacion'
    ubicacion = 'Sin informacion'
    bodega = 'Sin informacion'
    antiguedad = 'Sin informacion'

    try:
        nombre_arriendo = nombre_valor['Nombre Arriendo']
    except Exception as e:
        pass

    try:
        precio_departamento = nombre_valor['Precio Arriendo']
    except Exception as e:
        pass

    try:
        superficie_total = nombre_valor['Superficie total']
    except Exception as e:
        pass

    try:
        superficie_util = nombre_valor['Superficie útil']
    except Exception as e:
        pass

    try:
        ambientes = nombre_valor['Ambientes']
    except Exception as e:
        pass

    try:
        dormitorios = nombre_valor['Dormitorios']
    except Exception as e:
        pass

    try:
        banos = nombre_valor['Baños']
    except Exception as e:
        pass

    try:
        cantidad_maxima_habitantes = nombre_valor['Cantidad máxima de habitantes']
    except Exception as e:
        pass

    try:
        admite_mascotas = nombre_valor['Admite mascotas']
    except Exception as e:
        pass

    try:
        piso_de_la_unidad = nombre_valor['Número de piso de la unidad']
    except Exception as e:
        pass

    try:
        departamentos_por_piso = nombre_valor['Departamentos por piso'] 
    except Exception as e:
        pass

    try:
        cantidad_pisos_departamento = nombre_valor['Cantidad de pisos']
    except Exception as e:
        pass

    try:
        orientacion = nombre_valor['Orientación']
    except Exception as e:
        pass

    try:
        gastos_comunes = nombre_valor['Gastos comunes']
    except Exception as e:
        pass

    try:
        ubicacion = nombre_valor['Ubicacion']
    except Exception as e:
        pass

    try:
        bodega = nombre_valor['Bodegas']
    except Exception as e:
        pass

    try:
        antiguedad = nombre_valor['Antigüedad']
    except Exception as e:
        pass

    try:
        estacionamientos = nombre_valor['Estacionamientos'] 

    except Exception as e:
        pass
    
    pagina = str(url)
    

    arriendo = [nombre_arriendo, precio_departamento, superficie_total, superficie_util, ambientes, dormitorios, 
                banos, estacionamientos, cantidad_maxima_habitantes, admite_mascotas, piso_de_la_unidad, departamentos_por_piso, 
                cantidad_pisos_departamento, orientacion, gastos_comunes, ubicacion, bodega, antiguedad, pagina] 
    return arriendo

def imprimir_en_consola(caracteristicas_arriendo:list) -> None:
    print('##################################################################################################')
    print(f'NOMBRE: {caracteristicas_arriendo[0]}')
    print(f'PRECIO: {caracteristicas_arriendo[1]}')
    print(f'SUPERFICIE TOTAL: {caracteristicas_arriendo[2]}') 
    print(f'SUPERFICIE UTIL: {caracteristicas_arriendo[3]}') 
    print(f'AMBIENTES: {caracteristicas_arriendo[4]}') 
    print(f'DORMITORIOS: {caracteristicas_arriendo[5]}') 
    print(f'BANOS: {caracteristicas_arriendo[6]}') 
    print(f'ESTACIONAMIENTOS: {caracteristicas_arriendo[7]}')
    print(f'CANTIDAD DE HABITANTES: {caracteristicas_arriendo[8]}') 
    print(f'ADMITE MASCOTA: {caracteristicas_arriendo[9]}') 
    print(f'PISO DE LA UNIDAD: {caracteristicas_arriendo[10]}') 
    print(f'DEPARTAMENTOS POR PISO: {caracteristicas_arriendo[11]}') 
    print(f'CANTIDAD DE PISOS DEL DEPARTAMENTO: {caracteristicas_arriendo[12]}')
    print(f'ORIENTACION: {caracteristicas_arriendo[13]}') 
    print(f'GASTOS COMUNES: {caracteristicas_arriendo[14]}') 
    print(f'UBICACION: {caracteristicas_arriendo[15]}')
    print(f'BODEGA: {caracteristicas_arriendo[16]}')
    print(f'ANTIGUEDAD: {caracteristicas_arriendo[17]}')
    print(f'URL: {caracteristicas_arriendo[18]}')
    print('##################################################################################################')

def cambiar_pagina(driver) -> None:
    try:
        boton_siguiente = (By.XPATH, '//span[contains(text(),"Siguiente")]')
        hacer_click(driver, boton_siguiente)
        existe_boton_siguiente = True
        print('------------------------------------------------------------------')
        print('                                                                  ')
        print('Hace click en siguiente')
        print('                                                                  ')
        print('------------------------------------------------------------------')
            

    except Exception as e:
        print('------------------------------------------------------------------')
        print('                                                                  ')
        print('NO hace click en siguiente')
        print('                                                                  ')
        print('------------------------------------------------------------------')
        existe_boton_siguiente = False
        traceback.print_exc()
    return existe_boton_siguiente

def creacion_data_set(data_set: list):
    columnas = ['nombre_arriendo', 'precio_departamento', 'superficie_total', 'superficie_util', 'ambientes', 'dormitorios', 
                'banos', 'estacionamientos', 'cantidad_maxima_habitantes', 'admite_mascotas', 'piso_de_la_unidad', 'departamentos_por_piso', 
                'cantidad_pisos_departamento', 'orientacion', 'gastos_comunes', 'ubicacion', 'bodega', 'antiguedad', 'pagina']

    df_productos = pd.DataFrame(data_set, columns=columnas)
    df_productos.to_excel("arriendos.xlsx", sheet_name='detalle arriendos', index = False)
# dentro de cada pagina

def main() -> None:
    ## Crear una instancia de driver
    driver = webdriver.Firefox(
    executable_path= r'/home/seba/Documentos/mercado_libre/geckodriver')
    
    buscar_en_ml(driver)
    
    lista_arriendos = []
    existe_boton_siguiente = True

    while existe_boton_siguiente:
        
        lista_url_productos = buscar_urls(driver)

        print(f'Cantidad de URL: {len(lista_url_productos)}')
        
        for url_producto in lista_url_productos:
        
            driver.get(url_producto)
            print(url_producto)
            time.sleep(5)
        
            lista_nombre_valor = encontrar_caracteristicas_arriendo(driver)
            print(lista_nombre_valor)

            arriendo = caracteristicas_por_pagina(lista_nombre_valor, str(url_producto))
            
            imprimir_en_consola(arriendo)            
            
            lista_arriendos.append(arriendo) 
        
           
            driver.back()

        existe_boton_siguiente = cambiar_pagina(driver)
    
    creacion_data_set(lista_arriendos)
 

if __name__ == "__main__": 
    main()