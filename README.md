# Rest Countries Info APP [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) ![Python](https://img.shields.io/badge/python-3.12-blue.svg) ![Django](https://img.shields.io/badge/django-5.0.9-darkgreen.svg) 

![Homepage](screenshots//countries.JPG)

## - Introduction -

**Rest Countries Info APP** is a small Django project that utilize [REST Countries API](https://restcountries.com/) and [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) to provide specific information about countries around the world. The project is built using Python 3.12, JavaScript, Bootstrap 5, HTML5, CSS3, and JSON.

## - Requirements -

Make sure you have Python installed on your system, you can check this by running on the command line:

```bash
    py --version # Windows
    python --version # Unix/macOS
```

If you don't have Python installed go to https://www.python.org/downloads/ and download the latest version.

## - Installation -

1. Clone the repository:

```bash
    git clone https://github.com/davevad93/rest-countries-django-app.git
```

2. Go to the repo directory:

```bash
    cd rest-countries-django-app
```
3. Create a virtual environment:

```bash
    py -m venv venv # Windows
    python -m venv venv # Unix/macOS
```

4. Activate the virtual environment:

```bash
    venv/Scripts/activate.bat # Windows
    source venv/bin/activate # Unix/macOS
```

5. Go to the project directory:

```bash
    cd myproject
```

6. Install the required dependencies:

```bash
    py -m pip install -r requirements.txt # Windows
    python -m pip install -r requirements.txt # Unix/macOS
```

7. Generate a random Secret Key and store it inside the .env file: <br/>
(This app doesn't utilize an authentication system and doesn't store any sensitive data, however it is always a good habit to generate a Secret Key and store it in your enviroment file). 

```bash
    # STEP 1: Open the Python Shell within the terminal.

    py manage.py shell # Windows
    python manage.py shell # Unix/macOS
```

```bash
    # STEP 2: Import the get_random_secret_key() function.

    from django.core.management.utils import get_random_secret_key
```

```bash
    # STEP 3: Generate the Secret Key using the get_random_secret_key() function.

    print(get_random_secret_key())
    # Copy the key.
```

```bash
    # STEP 4: Exit the Python Shell.

    exit()
```

```bash
    # STEP 5: Create .env file with the "SECRET_KEY" environment variable and paste the generated key in STEP 3. 

    echo SECRET_KEY = 'Paste here the key generated in STEP 3' > .env
```

8. Run the development server:

```bash
    py manage.py runserver # Windows
    python manage.py runserver # Unix/macOS
```

9. Access the application in your web browser at `http://localhost:8000`.

![Homepage](screenshots//homepage.JPG)

## - Features -

- ### Search for countries by name.

![Search](screenshots//search.gif)

- ### Filter for countries by region.

![Filter](screenshots//filter.gif)

- ### View detailed information about each country.

![Description](screenshots//description.gif)

- ### Search feature by clicking on the cards.

![Card](screenshots//card.gif)

## - Notes -

There may be some inconsistencies about the information of certain countries. This is due to the fact that to display the basic information of each country (e.g. population) I've used the **REST Countries API** (last updated in 2021) while to display countries descriptions I've used the **Wikipedia API** (which is constantly updated). To give an example, in the REST countries data, the most populated country in the world is China, but In 2022 India overtook it as the world's country with the largest population.

## - Made with -

- [![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
- [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com) 
- [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://www.javascript.com) 
- [![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com) 
- [![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://html.com) 
- [![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://css3.com) 

## - Acknowledgments -

- [REST Countries API](https://restcountries.com/) for the general **country data** showed in the app.

- [Wikipedia API](https://www.mediawiki.org/wiki/) for the **country descriptions** displayed in the app.

- [Font Awesome](https://fontawesome.com/) for the **fa-search** icon used in the app search bar.

- [Awesome Badges](https://github.com/Envoy-VC/awesome-badges) for the badges used in the "**Made with**" section.

## - Credits -

A few country emblems displayed in this project aren't from the [REST Countries API JSON](https://restcountries.com/v3.1/all) because some key values are null, so I have fetched the missing ones from [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page). Most of them are in the public domain and don't need attribution but some are under Creative Commons licenses hence, I'm going to give the due credit to the authors.

- [Demidow](https://commons.wikimedia.org/wiki/User:Demidow), [Coat of arms of the British Indian Ocean Territory](https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_the_British_Indian_Ocean_Territory.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)

- [Spedona](https://commons.wikimedia.org/wiki/User:Spedona), [Clunies-Ross family arms](https://commons.wikimedia.org/wiki/File:Clunies-Ross_family_arms.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)

- [Squiresy92](https://commons.wikimedia.org/wiki/User:Squiresy92) & [Sodacan](https://commons.wikimedia.org/wiki/User:Sodacan), [Coat of arms of Norfolk Island](https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_Norfolk_Island.svg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

- [Heralder](https://commons.wikimedia.org/wiki/User:Heralder), [Coat of arms of the Commonwealth of Puerto Rico](https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_the_Commonwealth_of_Puerto_Rico.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)

- [Superbenjamin](https://commons.wikimedia.org/wiki/User:Superbenjamin), [Armoiries Réunion](https://commons.wikimedia.org/wiki/File:Armoiries_R%C3%A9union.svg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

- [Manassas](https://commons.wikimedia.org/wiki/User_talk:Manassas~commonswiki), [Blason St Barthélémy TOM entire](https://commons.wikimedia.org/wiki/File:Blason_St_Barth%C3%A9l%C3%A9my_TOM_entire.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)


- [Di (they-them)](https://commons.wikimedia.org/wiki/User:Di_(they-them)), [Coat of Arms of Saint Helena](https://commons.wikimedia.org/wiki/File:Coat_of_Arms_of_Saint_Helena.svg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

- [Government of the Collectivity of Saint-Martin](https://www.com-saint-martin.fr), [Local flag of the Collectivity of Saint Martin](https://commons.wikimedia.org/wiki/File:Local_flag_of_the_Collectivity_of_Saint_Martin.svg), [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2018/11/open-licence.pdf)

- [Josedar](https://commons.wikimedia.org/wiki/User:Josedar), [Coat of arms of the Turks and Caicos Islands](https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_the_Turks_and_Caicos_Islands.svg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

## - Contributing -

Contributions are truly welcome! If you find any issues or have suggestions for improvements, please open an issue or fork the repository and submit a pull request. Don't forget to give this project a star. Thank you very much!

## - License -

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
