# FORK IN PROGRESS

Hola a todos, soy un novato intentando hacer mi primer Custom Component de Home Assistant y mi primer trabajo en Python.
Este repositorio es una modificación de [carlos-48/ha-globalomnium](https://github.com/carlos-48/ha-globalomnium) pero estoy intentando adaptarlo para obtener los consumos de agua desde GlobalOmnium / Emivasa / Aguas de Valencia.

# Integración Personalizada de Global Omnium para Home Assistant

<!-- Home Assistant badges -->
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![hassfest validation](https://github.com/carlos-48/ha-globalomnium/workflows/Validate%20with%20hassfest/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/hassfest.yml)
[![HACS validation](https://github.com/carlos-48/ha-globalomnium/workflows/Validate%20with%20HACS/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/hacs.yml)

<!-- Code and releases -->
![GitHub Release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/carlos-48/ha-globalomnium?include_prereleases)
[![CodeQL](https://github.com/carlos-48/ha-globalomnium/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/codeql-analysis.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Integración de [globalomnium](https://github.com/carlos-48/globalomnium) para [home-assistant](https://home-assistant.io/)

Esta integración provee sensores para el distribuidor de agua español [Global Omnium](globalomnium.com).

**⚠️ Asegurese de leer las '[FAQ](https://github.com/carlos-48/ha-globalomnium/blob/main/FAQ.md)' y las secciones 'advertencias' y 'dependencias'.**

## Características

* Integración con el panel del energía de Home Assistant

* Sensores de consumo instantaneo y acumulado.

* Sensores históricos con mayor precisión. Estos datos no son en tiempo real y normalmente llevan un retraso de entre 24 y 48 horas.

* Soporte para varios contratos (puntos de servicio).

* Configuración a través del [interfaz web de Home Assistant](https://developers.home-assistant.io/docs/config_entries_options_flow_handler) sin necesidad de editar ficheros YAML.

* Algoritmo de actualización para leer el contador cerca del final de cada periodo horario (entre el minuto 50 y 59) y una mejor representación del consumo en el panel de energía de Home Assistant

* Totalmente [asíncrono](https://developers.home-assistant.io/docs/asyncio_index) e integrado en Home Assistant.

## Dependencias

Es necesario disponer de acceso al área de clientes de Global Omnium.
Puedes registrarte en el siguiente link: [Oficina Virtual | Global Omnium](https://www.globalomnium.com/VirtualOffice/Registro).

### Usando [HACS](https://hacs.xyz/) (recomendado)

1. Copia la dirección de este repositorio: [https://github.com/carlos-48/ha-globalomnium/](https://github.com/carlos-48/ha-globalomnium)

2. Añade este repositorio en HACS como "repositorio manual":

   * En el campo "Repositorio" pega la URL anterior.
   * En el campo "Categoría" elige "Integración"
   * Pulsa el botón "Descargar" y elige la última versión.

    ![Custom repository](https://user-images.githubusercontent.com/59612788/171965822-4a89c14e-9eb2-4134-8de2-1d3f380663e4.png)

3. Reinicia Home Assistant

4. Configura la integración

   * (Opción A) Pulsa el botón "Añadir integración" → [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=globalomnium)

   * (Opción B) Navega a "Ajustes" → "Dispositivos y servicios" y pulsa "Añadir integración". Elige "Global Omnium Water Consumption".  

5. Sigue los pasos del asistente: Proporciona tus credenciales de acceso para el área de cliente de "Global Omnium", después elige el contrato que deseas monitorizar. Si necesitas añadir más contratos repite los pasos anteriores para cada uno de ellos.

## Instalación

A través de custom_components o [HACS](https://hacs.xyz/)

1. Descarga o clona este repositorio: [https://github.com/carlos-48/ha-globalomnium](https://github.com/carlos-48/ha-globalomnium)

2. Copia la carpeta [custom_components/globalomnium](custom_components/globalomnium) en tu carpeta `custom_components` de tu instalación de Home Assistant.

3. Reinicia Home Assistant
4. Configura la integración

   * (Opción A) Pulsa el botón "Añadir integración" → [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=globalomnium)

   * (Opción B) Navega a "Ajustes" → "Dispositivos y servicios" y pulsa "Añadir integración". Elige "Global Omnium Water Consumption".  

5. Sigue los pasos del asistente: Proporciona tus credenciales de acceso para el área de cliente de "Global Omnium", después elige el contrato que deseas monitorizar. Si necesitas añadir más contratos repite los pasos anteriores para cada uno de ellos.

## Advertencias

Esta integración provee un sensor 'histórico' que incorpora datos del pasado en la base de datos de Home Assistant. Por su propia seguridad este sensor no está habilitado y debe activarse manualmente.

☠️ El sensor histórico está basado en un **hack extremadamente experimental** y puede romper y/o corromper su base de datos y/o estadísticas. **Use lo bajo su propio riesgo**.
