import time
from selenium import webdriver
import pandas as pd


## Crear una instancia de driver
driver = webdriver.Firefox(
    executable_path= r'/usr/local/bin/geckodriver'
)
## Cargar pagina de mercado libre en el navegador
driver.get('https://www.mercadolibre.cl/')

## Buscar un producto en mercado libre
time.sleep(5)
buscador = driver.find_element("xpath",'//*[@id="cb1-edit"]')
buscador.send_keys('mate stanley')

boton_buscar = driver.find_element("xpath",'//button[@class="nav-search-btn"]')
boton_buscar.click()

time.sleep(5)
lista_url_productos = []
lista_datos_producto = []

lista_productos = driver.find_elements("xpath", '//li[@class="ui-search-layout__item shops__layout-item"]')


for producto in lista_productos:
    url_producto = producto.find_element("xpath", './/a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]').get_attribute('href')
    lista_url_productos.append(url_producto)
   

for i, url_producto in enumerate(lista_url_productos):
    driver.get(url_producto)
    time.sleep(5)
    
    nombre_producto = 'Sin Nombre'
    precio_producto = 'Sin Precio'
    cantidad_de_comentarios = 'Sin Comentarios'
    puntuacion_producto = 'Sin Puntuacion'
    
    try:
        nombre_producto = driver.find_element("xpath",'//h1[@class="ui-pdp-title"]').text
        precio_producto = driver.find_element("xpath",'//div[@class="ui-pdp-price__second-line"]//span[@class="andes-visually-hidden"]').text
        cantidad_de_comentarios = driver.find_element("xpath",'//p[@class="ui-review-capability__rating__label"]').text
        puntuacion_producto = driver.find_element("xpath",'//p[@class="ui-review-capability__rating__average ui-review-capability__rating__average--desktop"]').text

    except Exception as e:
        pass

    print(f'NUMERO PRODUCTO -> {i}') 
    print(f'NOMBRE_PRODUCTO -> {nombre_producto}') 
    print(f'PRECIO_PRODUCTO -> {precio_producto}') 
    print(f'CANTIDAD_DE_COMENTARIOS -> {cantidad_de_comentarios}') 
    print(f'PUNTUACION_PRODUCTO -> {puntuacion_producto}')

    datos_productos = [nombre_producto, precio_producto, cantidad_de_comentarios, puntuacion_producto]

    lista_datos_producto.append(datos_productos)

    driver.back()

columnas = ['Nombre', 'Precio', 'Cantidad de Comentarios', 'Puntuación']
df_productos = pd.DataFrame(lista_datos_producto, columns=columnas)
df_productos.to_excel("Reporte_mates.xlsx", sheet_name='Detalles Mates', index = False)