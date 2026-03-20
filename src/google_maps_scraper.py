"""
Google Maps Scraper usando Playwright
Extrae información de negocios desde Google Maps
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class GoogleMapsScraper:
    """Scraper para extraer información de negocios desde Google Maps"""

    def __init__(self, headless: bool = True):
        """
        Inicializa el scraper

        Args:
            headless: Si True, el navegador se ejecuta sin interfaz gráfica
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        """Permite usar el scraper con context manager (with statement)"""
        logger.info("🎭 Iniciando Playwright...")
        try:
            self.playwright = sync_playwright().start()
            logger.info("✅ Playwright iniciado correctamente")

            logger.info(f"🌐 Lanzando Chromium (headless={self.headless})...")
            chromium_path = self.playwright.chromium.executable_path
            logger.info(f"📂 Ejecutable de Chromium: {chromium_path}")

            self.browser = self.playwright.chromium.launch(headless=self.headless)
            logger.info("✅ Chromium lanzado exitosamente")

            self.page = self.browser.new_page()
            logger.info("✅ Nueva página creada")

            return self
        except Exception as e:
            logger.error(f"❌ Error en __enter__: {str(e)}", exc_info=True)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador automáticamente"""
        self.close()

    def close(self):
        """Cierra el navegador y libera recursos"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def search_businesses(self, city: str, business_type: str, max_results: int = 50) -> List[Dict[str, str]]:
        """
        Busca negocios en Google Maps

        Args:
            city: Ciudad donde buscar (ej: "Bogotá, Colombia")
            business_type: Tipo de negocio (ej: "lavadero de autos")
            max_results: Número máximo de resultados a extraer

        Returns:
            Lista de diccionarios con información de cada negocio
        """
        if not self.page:
            raise RuntimeError("Scraper no inicializado. Usa 'with GoogleMapsScraper()' o llama __enter__()")

        # Construir URL de búsqueda
        query = f"{business_type} en {city}"
        search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

        logger.info(f"🔍 Navegando a Google Maps: {search_url}")
        print(f"🔍 Navegando a Google Maps...")
        self.page.goto(search_url)
        logger.info("✅ Página cargada")

        # Esperar a que carguen los resultados
        try:
            logger.info("⏳ Esperando selector div[role='feed']...")
            self.page.wait_for_selector('div[role="feed"]', timeout=10000)
            logger.info("✅ Resultados cargados correctamente")
            print("✓ Resultados cargados")
        except PlaywrightTimeout:
            logger.warning("⚠️  Timeout esperando resultados")
            print("⚠ No se encontraron resultados o timeout")
            return []

        # Hacer scroll para cargar más resultados
        logger.info(f"📜 Iniciando scroll para cargar hasta {max_results} resultados...")
        print(f"📜 Cargando resultados (máximo {max_results})...")
        self._scroll_results_panel(max_results)

        # Obtener todos los enlaces de negocios
        logger.info("🔗 Extrayendo enlaces de negocios...")
        business_links = self._extract_business_links(max_results)
        logger.info(f"✅ {len(business_links)} enlaces extraídos")
        print(f"✓ Encontrados {len(business_links)} negocios")

        # Extraer detalles de cada negocio
        businesses = []
        logger.info(f"🏢 Iniciando extracción de detalles de {len(business_links)} negocios...")
        for idx, link in enumerate(business_links, 1):
            logger.info(f"📍 Procesando negocio {idx}/{len(business_links)}: {link}")
            print(f"📍 Procesando {idx}/{len(business_links)}...")
            business_data = self._extract_business_details(link)
            if business_data:
                businesses.append(business_data)
                logger.info(f"✅ Negocio extraído: {business_data.get('nombre', 'N/A')}")
            else:
                logger.warning(f"⚠️  No se pudo extraer información del negocio {idx}")
            time.sleep(1)  # Delay para no ser detectado como bot

        logger.info(f"🎉 Extracción completada: {len(businesses)} negocios procesados")
        return businesses

    def _scroll_results_panel(self, max_results: int):
        """
        Hace scroll en el panel de resultados para cargar más negocios

        Args:
            max_results: Número máximo de resultados a cargar
        """
        scrollable_div = self.page.query_selector('div[role="feed"]')
        if not scrollable_div:
            return

        # Scroll gradual para cargar resultados
        for _ in range(10):  # Máximo 10 scrolls
            # Contar resultados actuales
            current_results = len(self.page.query_selector_all('a[href*="/maps/place/"]'))
            if current_results >= max_results:
                break

            # Scroll down
            scrollable_div.evaluate('el => el.scrollTop = el.scrollHeight')
            time.sleep(2)  # Esperar a que carguen nuevos resultados

    def _extract_business_links(self, max_results: int) -> List[str]:
        """
        Extrae los enlaces de todos los negocios en los resultados

        Args:
            max_results: Número máximo de enlaces a extraer

        Returns:
            Lista de URLs de negocios
        """
        links = []
        elements = self.page.query_selector_all('a[href*="/maps/place/"]')

        for element in elements[:max_results]:
            href = element.get_attribute('href')
            if href and href not in links:
                links.append(href)

        return links[:max_results]

    def _extract_business_details(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extrae detalles de un negocio específico

        Args:
            url: URL del negocio en Google Maps

        Returns:
            Diccionario con información del negocio o None si hay error
        """
        try:
            self.page.goto(url, timeout=15000)
            time.sleep(2)  # Esperar a que cargue completamente

            # Extraer nombre
            nombre = self._extract_text('h1')

            # Extraer teléfono
            telefono = self._extract_phone()

            # Extraer dirección
            direccion = self._extract_address()

            # Extraer website
            website = self._extract_website()

            return {
                'nombre': nombre or 'N/A',
                'telefono': telefono or 'N/A',
                'direccion': direccion or 'N/A',
                'website': website or 'N/A',
                'google_maps_url': url
            }

        except Exception as e:
            print(f"⚠ Error extrayendo detalles: {str(e)}")
            return None

    def _extract_text(self, selector: str) -> Optional[str]:
        """Extrae texto de un selector CSS"""
        try:
            element = self.page.query_selector(selector)
            return element.inner_text().strip() if element else None
        except:
            return None

    def _extract_phone(self) -> Optional[str]:
        """Extrae el número de teléfono"""
        try:
            # Buscar botón de teléfono
            phone_button = self.page.query_selector('button[data-item-id*="phone"]')
            if phone_button:
                phone_text = phone_button.get_attribute('data-item-id')
                if phone_text and 'phone:tel:' in phone_text:
                    return phone_text.split('phone:tel:')[1]

            # Intentar buscar en aria-label
            phone_elements = self.page.query_selector_all('[aria-label*="Phone"]')
            for elem in phone_elements:
                aria_label = elem.get_attribute('aria-label')
                if aria_label and ':' in aria_label:
                    return aria_label.split(':')[-1].strip()

            return None
        except:
            return None

    def _extract_address(self) -> Optional[str]:
        """Extrae la dirección"""
        try:
            # Buscar botón de dirección
            address_button = self.page.query_selector('button[data-item-id*="address"]')
            if address_button:
                return address_button.inner_text().strip()

            # Intentar con aria-label
            address_elements = self.page.query_selector_all('[aria-label*="Address"]')
            for elem in address_elements:
                text = elem.inner_text().strip()
                if text:
                    return text

            return None
        except:
            return None

    def _extract_website(self) -> Optional[str]:
        """Extrae el sitio web"""
        try:
            # Buscar enlace de website
            website_link = self.page.query_selector('a[data-item-id*="authority"]')
            if website_link:
                return website_link.get_attribute('href')

            # Intentar buscar links externos
            links = self.page.query_selector_all('a[href^="http"]')
            for link in links:
                href = link.get_attribute('href')
                # Filtrar URLs que no sean de Google
                if href and 'google.com' not in href and 'gstatic.com' not in href:
                    return href

            return None
        except:
            return None
