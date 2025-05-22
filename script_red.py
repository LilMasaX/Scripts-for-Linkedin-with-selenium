from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Parámetros
palabra_clave = "scrum, consultor"  # Cambia la palabra clave aquí
max_perfiles = 50  # Cambia si quieres más o menos conexiones

try:
    # LOGIN
    print("🔐 Iniciando sesión...")
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("" + Keys.RETURN)
    WebDriverWait(driver, 15).until(EC.url_contains("feed"))
    print("✅ Sesión iniciada.")

    # Buscar palabra clave
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={palabra_clave.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(5)

    # Conectar con perfiles
    conectados = 0
    while conectados < max_perfiles:
        perfiles = driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Conectar")]')

        if not perfiles:
            print("🚫 No se encontraron más perfiles con botón de Conectar.")
            break

        for boton in perfiles:
            if conectados >= max_perfiles:
                break
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                time.sleep(1)
                boton.click()
                print("🧷 Solicitud de conexión abierta.")
                time.sleep(2)

                # Si aparece modal para añadir nota o enviar
                try:
                    enviar_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar ahora"]'))
                    )
                    enviar_btn.click()
                    print(f"✅ Conexión enviada ({conectados + 1}).")
                except:
                    print("⚠️ No apareció modal de enviar.")

                conectados += 1
                time.sleep(10)  # Espera entre conexiones
            except Exception as e:
                print(f"❌ Error al conectar: {e}")
                continue

        # Intentar ir a siguiente página de resultados
        try:
            siguiente = driver.find_element(By.XPATH, '//button[@aria-label="Página siguiente"]')
            siguiente.click()
            time.sleep(5)
        except:
            print("📄 No hay más páginas de resultados.")
            break

except Exception as e:
    print(f"❌ Error general: {e}")

finally:
    print("🔒 Cerrando navegador.")
    driver.quit()
