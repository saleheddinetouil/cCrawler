# Dynamic Selenium Crawler Guide

This guide will help you understand how to use the provided dynamic Selenium crawler to automate interactions with different websites. This tool uses configuration files in JSON format, making it highly flexible and adaptable.

## Introduction

The crawler is designed to automate tasks on websites, such as filling forms, clicking buttons, and navigating through pages. It works by following a sequence of steps defined in a JSON configuration file. The main benefits are:

*   **Flexibility**: Easily adapt to different websites by changing the configuration file.
*   **Maintainability**: The code is structured, making it easier to understand and modify.
*   **Efficiency**: Automates repetitive tasks.

## Getting Started

### Prerequisites

1.  **Python 3.7+:** Ensure you have Python installed on your system. Download it from [python.org](https://www.python.org/).
2.  **Libraries**: Install required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```
    or
    ```bash
    pip install selenium webdriver-manager
    ```

### Files

The following files are essential for running the crawler:

*   **`crawler.py`**: The main Python script.
*   **`config.json`**: The JSON configuration file, defining website navigation steps.
*   **`cc.txt`**: Contains credit card data (you must provide this data).
*   **`data.txt`**: Contains data (you can add your data)
*   **`requirements.txt`**: Contains needed python packages

## Configuration Files
### `config.json` Structure

The `config.json` file is where you define the actions the crawler should take. It follows this structure:

```json
{
  "start_url": "https://example.com",
  "steps": [
    {
      "action": "navigate",
      "target": "https://example.com/login"
    },
    {
      "action": "click",
      "target_type": "css",
      "target": "#loginButton",
       "wait_condition": "element_to_be_clickable"

    },
    {
      "action": "input",
      "target_type": "id",
      "target": "username",
      "input_data": "person.email",
        "wait_condition": "presence_of_element_located"
    },
     {
      "action": "input",
      "target_type": "name",
      "target": "password",
      "input_data": "mypassword"

    },
     {
          "action": "switch_frame",
           "target_type": "css",
           "target": "[id='myiframe']"
        },
    {
     "action": "input",
      "target_type": "css",
      "target": "[placeholder='Card Number']",
      "input_data": "cc.number",
       "wait_condition": "presence_of_element_located"

    },
     {
         "action": "switch_to_default"
     }

  ]
}
```

#### Key Attributes:

*   **`start_url`**: The URL that will be opened at the beggining of the loop , if not set you should pass the url with the `-u` or `--url` argument
*   **`steps`**: An array of actions the crawler will execute sequentially. Each step is a JSON object with the following:
    *   **`action`**: The action to perform. Allowed values:
        *   **`navigate`**: Navigate to a URL. The `target` is the URL.
        *   **`click`**: Click on an element.
        *   **`input`**: Input text into a field.
        *  **`switch_frame`**: Switch to an Iframe.
        *   **`switch_to_default`**: switch to default frame
        *  **`get_elements_and_click`**: Get elements and click the first one .
    *   **`target_type`**: The type of locator used to find the element. Allowed values:
        *   **`id`**: HTML element ID.
        *   **`name`**: HTML element name.
        *   **`class`**: HTML element class name.
        *   **`css`**: CSS selector.
        *   **`xpath`**: XPath selector.
    *   **`target`**: The value of the locator to find the element.
    *   **`input_data`**: The text data to input for an "input" action. If starts with `person.`, it takes a field from `persons` data , `cc.` takes a field from credit card data.
    *  **`wait_condition`**: The wait condition before performing the action `presence_of_element_located` or `element_to_be_clickable`, or `presence_of_all_elements_located`, you should add this wait condition when the target is not available right away.

### `cc.txt` Structure

This file should contain credit card information, with one card per line, each part separated by `|`: `cc_number|cc_exp_month|cc_exp_year|cc_cvv`.

For example:
```
5356740100410315|04|25|299
5356740100435338|01|25|986
5356740100466572|10|27|171
5356740100460005|10|27|794
```
### `data.txt` structure

This file should contain your data, one data per line (you can add your own data)

### Persons data
The Persons Data is hardcoded in the script

## How to Use

1.  **Prepare data:** create `cc.txt` with credit card data and `data.txt` with your data
2.  **Configure JSON file:** Adapt `config.json` to your target website using the `config.json` structure. You can use chrome inspect and the select tool to copy the `css` or `xpath` selectors.

3.  **Run the crawler:** Open a terminal or command prompt, navigate to the directory containing `crawler.py`, `config.json` and the text files and run:

    ```bash
    python crawler.py -c config.json 
    ```
     or to provide the url from command line
     ```bash
      python crawler.py -c config.json -u https://example.com
     ```
   Replace `config.json` with your configuration file path.

    The crawler will execute each step on each credit card in `cc.txt`, and loop until all cc are finished.

## Troubleshooting

*   **Errors**: If the crawler fails, review the logs in the console for error messages. Check the locators in `config.json` are correct.
*   **Website Changes**: If the website changes, you will need to update the locators in your JSON configuration file.

## Advanced Usage

*   **Dynamic Inputs:** The crawler can input dynamic data from the `persons` and `cc_data` objects using the `person.` and `cc.` prefixes in `input_data` field of steps.
    *   For `person.` you can use : `person.name` , `person.email` , `person.phone`, `person.street` , `person.city`, `person.state` , `person.postal`
    *   For `cc.` you can use :  `cc.number` , `cc.exp` , `cc.cvc`

## Conclusion

This dynamic crawler provides a powerful way to automate web tasks. By understanding the JSON configuration structure, you can adapt it to various websites and use the persons and cc data. If you need more help or support don't hesitate to ask.

---

# Guide du robot Selenium Dynamique

Ce guide vous aidera à comprendre comment utiliser le robot Selenium dynamique fourni pour automatiser les interactions avec différents sites Web. Cet outil utilise des fichiers de configuration au format JSON, ce qui le rend très flexible et adaptable.

## Introduction

Le robot est conçu pour automatiser les tâches sur les sites Web, telles que le remplissage de formulaires, le clic sur des boutons et la navigation dans les pages. Il fonctionne en suivant une séquence d'étapes définies dans un fichier de configuration JSON. Les principaux avantages sont :

*   **Flexibilité** : Adaptation facile à différents sites Web en modifiant le fichier de configuration.
*   **Maintenabilité** : Le code est structuré, ce qui le rend plus facile à comprendre et à modifier.
*   **Efficacité** : Automatise les tâches répétitives.

## Démarrage

### Prérequis

1.  **Python 3.7+ :** Assurez-vous que Python est installé sur votre système. Téléchargez-le depuis [python.org](https://www.python.org/).
2.  **Bibliothèques** : Installez les bibliothèques requises en utilisant pip :

    ```bash
    pip install -r requirements.txt
    ```
    ou
    ```bash
     pip install selenium webdriver-manager
    ```

### Fichiers

Les fichiers suivants sont essentiels pour exécuter le robot :

*   **`crawler.py`** : Le script Python principal.
*   **`config.json`** : Le fichier de configuration JSON, définissant les étapes de navigation sur le site Web.
*   **`cc.txt`** : Contient les données de carte de crédit (vous devez fournir ces données).
*   **`data.txt`** : Contient les données (vous pouvez ajouter vos propres données).
*   **`requirements.txt`**: Contient les packages python nécessaires

## Fichiers de Configuration

### Structure de `config.json`

Le fichier `config.json` est l'endroit où vous définissez les actions que le robot doit effectuer. Il suit cette structure :

```json
{
    "start_url": "https://example.com",
  "steps": [
    {
      "action": "navigate",
      "target": "https://example.com/login"
    },
    {
      "action": "click",
      "target_type": "css",
      "target": "#loginButton",
       "wait_condition": "element_to_be_clickable"

    },
    {
      "action": "input",
      "target_type": "id",
      "target": "username",
      "input_data": "person.email",
        "wait_condition": "presence_of_element_located"
    },
     {
      "action": "input",
      "target_type": "name",
      "target": "password",
      "input_data": "mypassword"

    },
     {
          "action": "switch_frame",
           "target_type": "css",
           "target": "[id='myiframe']"
        },
    {
     "action": "input",
      "target_type": "css",
      "target": "[placeholder='Card Number']",
      "input_data": "cc.number",
       "wait_condition": "presence_of_element_located"

    },
     {
         "action": "switch_to_default"
     }

  ]
}
```

#### Attributs Clés :

*   **`start_url`**: L'URL qui sera ouverte au début de la boucle, si elle n'est pas définie, vous devez passer l'URL avec l'argument `-u` ou `--url`.
*   **`steps`** : Un tableau d'actions que le robot exécutera séquentiellement. Chaque étape est un objet JSON avec les éléments suivants :
    *   **`action`** : L'action à effectuer. Les valeurs autorisées :
        *   **`navigate`** : Naviguer vers une URL. La `target` est l'URL.
        *   **`click`** : Cliquer sur un élément.
        *   **`input`** : Saisir du texte dans un champ.
        *  **`switch_frame`**: Basculer vers un Iframe.
        *   **`switch_to_default`**: revenir à la frame par défaut
        *   **`get_elements_and_click`**: Obtenir les elements et cliquer sur le premier.
    *   **`target_type`** : Le type de sélecteur utilisé pour trouver l'élément. Les valeurs autorisées :
        *   **`id`** : ID d'élément HTML.
        *   **`name`** : Nom d'élément HTML.
        *   **`class`** : Nom de classe d'élément HTML.
        *   **`css`** : Sélecteur CSS.
        *   **`xpath`** : Sélecteur XPath.
    *   **`target`** : La valeur du sélecteur pour trouver l'élément.
    *   **`input_data`** : Les données textuelles à saisir pour une action « input ». S'il commence par `person.` , il prend un champ des données `persons`, `cc.` prend un champ des données de la carte de crédit.
    *  **`wait_condition`**: La condition d'attente avant d'effectuer l'action `presence_of_element_located` ou `element_to_be_clickable`, ou `presence_of_all_elements_located`, vous devez ajouter cette condition d'attente lorsque la cible n'est pas disponible immédiatement.

### Structure de `cc.txt`

Ce fichier doit contenir les informations de la carte de crédit, avec une carte par ligne, chaque partie séparée par `|` : `numéro_cc|mois_exp|année_exp|ccv`.

Par exemple :
```
5356740100410315|04|25|299
5356740100435338|01|25|986
5356740100466572|10|27|171
5356740100460005|10|27|794
```

### Structure de `data.txt`

Ce fichier doit contenir vos données, une donnée par ligne (vous pouvez ajouter vos propres données).

### Données des personnes

Les données des personnes sont codées en dur dans le script.

## Comment Utiliser

1.  **Préparer les données :** créez `cc.txt` avec les données de carte de crédit et `data.txt` avec vos données.
2.  **Configurer le fichier JSON :** Adaptez `config.json` à votre site Web cible en utilisant la structure `config.json`. Vous pouvez utiliser l'outil d'inspection de Chrome et l'outil de sélection pour copier les sélecteurs `css` ou `xpath`.
3.  **Exécuter le robot :** Ouvrez un terminal ou une invite de commandes, naviguez vers le répertoire contenant `crawler.py`, `config.json` et les fichiers texte, puis exécutez :
    ```bash
    python crawler.py -c config.json
    ```
     ou pour fournir l'url depuis la ligne de commande
     ```bash
     python crawler.py -c config.json -u https://example.com
     ```
   Remplacez `config.json` par le chemin d'accès de votre fichier de configuration.

    Le robot exécutera chaque étape sur chaque carte de crédit dans `cc.txt` et effectuera une boucle jusqu'à ce que toutes les cartes de crédit soient terminées.

## Dépannage

*   **Erreurs :** Si le robot échoue, consultez les journaux dans la console pour les messages d'erreur. Vérifiez que les sélecteurs dans `config.json` sont corrects.
*   **Modifications du site Web :** Si le site Web change, vous devrez mettre à jour les sélecteurs dans votre fichier de configuration JSON.

## Utilisation Avancée

*   **Saisies dynamiques :** Le robot peut saisir des données dynamiques à partir des objets `persons` et `cc_data` en utilisant les préfixes `person.` et `cc.` dans le champ `input_data` des étapes.
    *   Pour `person.` vous pouvez utiliser : `person.name`, `person.email`, `person.phone`, `person.street`, `person.city`, `person.state`, `person.postal`.
    *   Pour `cc.` vous pouvez utiliser : `cc.number`, `cc.exp`, `cc.cvc`.

## Conclusion

Ce robot dynamique offre un moyen puissant d'automatiser les tâches Web. En comprenant la structure de configuration JSON, vous pouvez l'adapter à divers sites Web et utiliser les données de personnes et de cartes de crédit. Si vous avez besoin d'aide ou d'assistance supplémentaire, n'hésitez pas à demander.

---

# دليل الزاحف الديناميكي لـ Selenium

سيساعدك هذا الدليل على فهم كيفية استخدام الزاحف الديناميكي لـ Selenium المقدم لأتمتة التفاعلات مع مواقع الويب المختلفة. تستخدم هذه الأداة ملفات التكوين بتنسيق JSON ، مما يجعلها مرنة للغاية وقابلة للتكيف.

## مقدمة

تم تصميم الزاحف لأتمتة المهام على مواقع الويب ، مثل ملء النماذج والنقر فوق الأزرار والتنقل عبر الصفحات. يعمل باتباع تسلسل من الخطوات المحددة في ملف تكوين JSON. الفوائد الرئيسية هي:

*   **المرونة**: التكيف بسهولة مع مواقع الويب المختلفة عن طريق تغيير ملف التكوين.
*   **قابلية الصيانة**: التعليمات البرمجية منظمة ، مما يجعلها أسهل للفهم والتعديل.
*   **الكفاءة**: أتمتة المهام المتكررة.

## البدء

### المتطلبات الأساسية

1.  **Python 3.7+:** تأكد من تثبيت Python على نظامك. قم بتنزيله من [python.org](https://www.python.org/).
2.  **المكتبات**: قم بتثبيت المكتبات المطلوبة باستخدام pip:

    ```bash
    pip install -r requirements.txt
    ```
    او
     ```bash
     pip install selenium webdriver-manager
     ```

### الملفات

الملفات التالية ضرورية لتشغيل الزاحف:

*   **`crawler.py`**: برنامج Python الرئيسي.
*   **`config.json`**: ملف تكوين JSON ، يحدد خطوات التنقل في موقع الويب.
*   **`cc.txt`**: يحتوي على بيانات بطاقة الائتمان (يجب عليك توفير هذه البيانات).
*   **`data.txt`**: يحتوي على البيانات (يمكنك إضافة البيانات الخاصة بك).
*   **`requirements.txt`**: يحتوي على حزم python المطلوبة

## ملفات التكوين

### هيكل `config.json`

ملف `config.json` هو المكان الذي تحدد فيه الإجراءات التي يجب أن يتخذها الزاحف. يتبع هذا الهيكل:

```json
{
   "start_url": "https://example.com",
  "steps": [
    {
      "action": "navigate",
      "target": "https://example.com/login"
    },
    {
      "action": "click",
      "target_type": "css",
      "target": "#loginButton",
       "wait_condition": "element_to_be_clickable"

    },
    {
      "action": "input",
      "target_type": "id",
      "target": "username",
      "input_data": "person.email",
        "wait_condition": "presence_of_element_located"
    },
     {
      "action": "input",
      "target_type": "name",
      "target": "password",
      "input_data": "mypassword"

    },
     {
          "action": "switch_frame",
           "target_type": "css",
           "target": "[id='myiframe']"
        },
    {
     "action": "input",
      "target_type": "css",
      "target": "[placeholder='Card Number']",
      "input_data": "cc.number",
       "wait_condition": "presence_of_element_located"

    },
     {
         "action": "switch_to_default"
     }

  ]
}
```

#### السمات الرئيسية:

*   **`start_url`**: عنوان URL الذي سيتم فتحه في بداية الحلقة، إذا لم يتم تعيينه ، فيجب عليك تمرير عنوان URL بالوسيطة `-u` أو `--url`.
*   **`steps`**: مصفوفة من الإجراءات التي سينفذها الزاحف بالتسلسل. كل خطوة عبارة عن كائن JSON مع ما يلي:
    *   **`action`**: الإجراء الذي سيتم تنفيذه. القيم المسموح بها:
        *   **`navigate`**: انتقل إلى عنوان URL. `target` هو عنوان URL.
        *   **`click`**: انقر فوق عنصر.
        *   **`input`**: أدخل نصًا في حقل.
        *   **`switch_frame`**: التبديل إلى Iframe.
        *   **`switch_to_default`**: التبديل إلى الإطار الافتراضي
         *   **`get_elements_and_click`**: الحصول على العناصر والنقر فوق العنصر الأول.
    *   **`target_type`**: نوع المحدد المستخدم للعثور على العنصر. القيم المسموح بها:
        *   **`id`**: معرف عنصر HTML.
        *   **`name`**: اسم عنصر HTML.
        *   **`class`**: اسم فئة عنصر HTML.
        *   **`css`**: محدد CSS.
        *   **`xpath`**: محدد XPath.
    *   **`target`**: قيمة المحدد للعثور على العنصر.
    *   **`input_data`**: بيانات النص لإدخالها لإجراء "input". إذا بدأت بـ `person.` ، فإنها تأخذ حقلاً من بيانات `persons`، `cc.` تأخذ حقلاً من بيانات بطاقة الائتمان.
    * **`wait_condition`**: حالة الانتظار قبل تنفيذ الإجراء `presence_of_element_located` أو `element_to_be_clickable` أو `presence_of_all_elements_located` ، يجب عليك إضافة حالة الانتظار هذه عندما لا يكون الهدف متاحًا على الفور.

### هيكل `cc.txt`

يجب أن يحتوي هذا الملف على معلومات بطاقة الائتمان ، مع وجود بطاقة واحدة في كل سطر ، كل جزء مفصول بـ `|`: `رقم_البطاقة|شهر_انتهاء_الصلاحية|سنة_انتهاء_الصلاحية|cvv`.

على سبيل المثال:

```
5356740100410315|04|25|299
5356740100435338|01|25|986
5356740100466572|10|27|171
5356740100460005|10|27|794
```

### هيكل `data.txt`

يجب أن يحتوي هذا الملف على بياناتك ، وبيانات واحدة لكل سطر (يمكنك إضافة بياناتك الخاصة)

### بيانات الأشخاص

يتم ترميز بيانات الأشخاص بشكل ثابت في البرنامج النصي.

## كيف تستعمل

1.  **جهز البيانات:** قم بإنشاء `cc.txt` ببيانات بطاقة الائتمان و `data.txt` ببياناتك.
2.  **تكوين ملف JSON:** قم بتكييف `config.json` مع موقع الويب المستهدف باستخدام بنية `config.json`. يمكنك استخدام أداة الفحص في Chrome وأداة التحديد لنسخ محددات `css` أو `xpath`.
3.  **قم بتشغيل الزاحف:** افتح موجه الأوامر أو الطرفية ، وانتقل إلى الدليل الذي يحتوي على `crawler.py`، `config.json` والملفات النصية ، وقم بتشغيل:

    ```bash
     python crawler.py -c config.json
    ```
     أو لتوفير عنوان url من سطر الأوامر
    ```bash
      python crawler.py -c config.json -u https://example.com
    ```
    استبدل `config.json` بمسار ملف التكوين الخاص بك.

    سينفذ الزاحف كل خطوة على كل بطاقة ائتمان في `cc.txt`، ويكرر حتى تنتهي جميع بطاقات الائتمان.

## استكشاف الأخطاء وإصلاحها

*   **الأخطاء**: إذا فشل الزاحف ، فراجع السجلات في وحدة التحكم بحثًا عن رسائل الخطأ. تحقق من أن المحددات في `config.json` صحيحة.
*   **تغييرات موقع الويب**: إذا تغير موقع الويب ، فستحتاج إلى تحديث المحددات في ملف تكوين JSON الخاص بك.

## الاستخدام المتقدم

*   **المدخلات الديناميكية:** يمكن للزاحف إدخال بيانات ديناميكية من كائنات `persons` و `cc_data` باستخدام البادئات `person.` و`cc.` في حقل `input_data` من الخطوات.
    *   بالنسبة إلى `person.` ، يمكنك استخدام: `person.name`، `person.email`، `person.phone`، `person.street`، `person.city`، `person.state`، `person.postal`.
    *   بالنسبة إلى `cc.` ، يمكنك استخدام: `cc.number`، `cc.exp`، `cc.cvc`.

## خاتمة

يوفر هذا الزاحف الديناميكي طريقة قوية لأتمتة مهام الويب. من خلال فهم بنية تكوين JSON ، يمكنك تكييفها مع مواقع ويب مختلفة واستخدام بيانات الأشخاص وبطاقات الائتمان. إذا كنت بحاجة إلى مزيد من المساعدة أو الدعم ، فلا تتردد في السؤال.
