from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Crear carpeta para screenshots si no existe
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

try:
    print("🔐 Iniciando sesión en LinkedIn...")
    driver.get("https://www.linkedin.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("" + Keys.RETURN)

    WebDriverWait(driver, 15).until(EC.url_contains("feed"))
    print("✅ Login exitoso.")

    if "checkpoint" in driver.current_url:
        print("⚠️ Checkpoint de seguridad detectado.")
        driver.save_screenshot("screenshots/checkpoint.png")
        raise Exception("Checkpoint activado.")

    contactos = [
        "https://www.linkedin.com/in/",
    ]

    for contacto in contactos:
        try:
            print(f"\n🔗 Visitando: {contacto}")
            driver.get(contacto)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(1)

            boton_mensaje = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Enviar mensaje")]'))
            )
            boton_mensaje.click()
            print("✉️ Botón de mensaje presionado.")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-form__msg-content-container'))
            )
            print("🟢 Modal del chat cargado.")

            mensaje_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.msg-form__contenteditable'))
            )
            mensaje_box.click()

            mensaje = (

            )
            mensaje_box.send_keys(mensaje)
            print("📝 Mensaje escrito.")

            boton_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.msg-form__send-button[type="submit"]'))
            )
            boton_enviar.click()
            print("✅ Mensaje enviado.")

            # Cerrar burbuja de chat
            try:
                print("🔄 Intentando cerrar burbuja(s) de chat...")
                botones_cerrar = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'button.msg-overlay-bubble-header__control')
                    )
                )
                for boton in botones_cerrar:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(boton)).click()
                        print("❎ Burbuja cerrada.")
                        time.sleep(1)
                    except Exception as e:
                        print(f"⚠️ No se pudo cerrar una burbuja: {e}")
            except Exception as e:
                print(f"⚠️ No se encontraron burbujas para cerrar: {e}")

            # Screenshot de confirmación
            driver.save_screenshot(f"screenshots/enviado_{contacto.split('/')[-2]}.png")
            print("⏳ Esperando entre 100 y 160 segundos antes del siguiente contacto...")
            time.sleep(100 + random.randint(30, 60))  # Espera entre 100 y 160 segundos

        except Exception as e:
            print(f"❌ Error con {contacto}: {e}")
            driver.save_screenshot(f"screenshots/error_{contacto.split('/')[-2]}.png")
            continue

except Exception as e:
    print(f"❌ Error general: {e}")
    driver.save_screenshot("screenshots/error_general.png")

finally:
    print("\n🔒 Cerrando navegador.")
    driver.quit()
