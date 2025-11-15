from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def main():
    url = 'https://www.alza.cz/graficke-karty/18842862.htm'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # Počkej na načtení stránky

    produkty = []
    containers = driver.find_elements(By.CLASS_NAME, 'browsingitemcontainer')
    print(f'Na stránce nalezeno {len(containers)} elementů s třídou "browsingitemcontainer".')
    for cidx, container in enumerate(containers):
        items = container.find_elements(By.CLASS_NAME, 'browsingitem')
        print(f'  Container {cidx}: {len(items)} browsingitem')
        for i, item in enumerate(items):
            print(f'    Produkt {i}: třídy: {item.get_attribute("class")}')
            try:
                nazev = item.find_element(By.CLASS_NAME, 'name').text
                cena = item.find_element(By.CLASS_NAME, 'price').text
                print(f'      Název: {nazev}, Cena: {cena}')
                produkty.append({'Název': nazev, 'Cena': cena})
            except Exception as e:
                print(f'      Chyba: {e}')
                continue
    driver.quit()
    df = pd.DataFrame(produkty)
    print(df)
    df.to_csv('data.csv', index=False)
    print('Data byla uložena do souboru data.csv')

if __name__ == '__main__':
    main()
