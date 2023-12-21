# FORK IN PROGRESS

Hi all, I'm a newbie trying to make my first Home Assistant Custom Component and my first Python work.
This repo is a modified fork from [ldotlopez/ha-ideenergy](https://github.com/ldotlopez/ha-ideenergy) but I'm trying to adapt it to get water consumption from GlobalOmnium / Emivasa / Aguas de Valencia.

# Global Omnium Custom Integration for Home Assistant

<!-- HomeAssistant badges -->
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![hassfest validation](https://github.com/carlos-48/ha-globalomnium/workflows/Validate%20with%20hassfest/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/hassfest.yml)
[![HACS validation](https://github.com/carlos-48/ha-globalomnium/workflows/Validate%20with%20HACS/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/hacs.yml)

<!-- Code and releases -->
![GitHub Release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/carlos-48/ha-globalomnium?include_prereleases)
[![CodeQL](https://github.com/carlos-48/ha-globalomnium/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/carlos-48/ha-globalomnium/actions/workflows/codeql-analysis.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[globalomnium](https://github.com/carlos-48/globalomnium) integration for [home-assistant](https://home-assistant.io/)

Global Omnium Custom Integration for Home Assistant, providing sensors for Spanish Water Distributor [Global Omnium](https://www.globalomnium.com).

**⚠️ Make sure to read the '[FAQ](https://github.com/carlos-48/ha-globalomnium/blob/main/FAQ.md)', 'Dependencies' and 'Warning' sections**

## Features

* Integration with the Home Assistant Energy Panel.

* Accumulated and Instant consumption sensors.

* Historical sensors with better precision. This data is not realtime and usually has a 24-hour to 48-hour offset.

* Support for multiple contracts (service points).

* Configuration through [Home Assistant Interface](https://developers.home-assistant.io/docs/config_entries_options_flow_handler) without the need to edit YAML files.

* Update algorithm to read the meter near the end of each hourly period (between minute 50 and 59)
with a better representation of consumption in the Home Assistant energy panel.

* Fully [asynchronous](https://developers.home-assistant.io/docs/asyncio_index) and integrated with HomeAssistant.

## Dependencies

You must have an Global Omnium username and access to the Clients' website. You may register here: [Oficina Virtual | Golbal Omnium](https://www.globalomnium.com/VirtualOffice/Registro).

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

1. Copy this repository URL: [https://github.com/carlos-48/ha-globalomnium/](https://github.com/carlos-48/ha-globalomnium)

2. In the HACS section, add this repository as a custom one:

* On the "repository" field put the URL copied before
* On the "Category" select "Integration"
* Click the "Download" button and download latest version.

  ![Custom repositorysitory](https://user-images.githubusercontent.com/59612788/171965822-4a89c14e-9eb2-4134-8de2-1d3f380663e4.png)

1. Restart HA

2. Configure the integration

* (Option A) Click the "Add integration" button → [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=globalomnium)

* (Option B) Go to "Settings"  "Devices & Services" and click "+ ADD INTEGRATION" and select "Global Omnium Water Consumption".  

1. Follow the configuration steps: provide your credentials for access to Global Omnium and select the contract that you want to monitor. (Should you need to add more contracts, just follow the previous step as many times as needed).

### Manually

1. Download/clone this repository: [https://github.com/carlos-48/ha-globalomnium/](https://github.com/carlos-48/ha-globalomnium)

2. Copy the [custom_components/globalomnium](custom_components/globalomnium) folder into your custom_components folder into your HA installation

3. Restart HA

4. Configure the integration

* (Option A) Click on this button → [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=globalomnium)
* (Option B) Go to "Settings" → "Devices & Services" and click "+ ADD INTEGRATION" and select "Global Omnium Water Consumption".

1. Follow the configuration steps: provide your credentials for access to Global Omnium and select the contract that you want to monitor. (Should you need to add more contracts, just follow the previous step as many times as needed).

## Warnings

This extension provides an 'historical' sensor to incorporate data from the past into Home Assistant database. For your own safety the sensor is not enabled by default and must be enabled manually.

☠️ Historic sensor is based on a **high experimental hack** and can broke and/or corrupt your database and/or statistics. **Use at your own risk**.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE file for details

## Disclaimer

THIS PROJECT IS NOT IN ANY WAY ASSOCIATED WITH OR RELATED TO THE GLOBAL OMNIUM GROUP COMPANIES OR ANY OTHER. The information here and online is for educational and resource purposes only and therefore the developers do not endorse or condone any inappropriate use of it, and take no legal responsibility for the functionality or security of your devices.
