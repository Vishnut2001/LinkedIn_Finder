##  LinkedIn Profile Finder using Selenium

### Overview

This project automates the process of finding LinkedIn profiles using names, designations, and organizations listed in a CSV file. It utilizes Selenium WebDriver (with optional undetected Chromedriver support) to perform Google or Bing searches and extract the first available LinkedIn profile link for each individual.

### Features
* Automates browser-based LinkedIn profile search

* Works with Google and Bing search engines

* Handles CAPTCHAs with manual intervention

* Bypasses bot detection using undetected Chromedriver

* Supports resuming from previously processed CSV files

* Includes delays and randomization to mimic human behavior

### Dependencies
* selenium

* webdriver_manager

* undetected_chromedriver (optional)

* csv, os, time, random, re


### Install requirements:
```bash
pip install selenium webdriver-manager undetected-chromedriver
```

### Usage
To Run the script

Open the file in jupyter notebook and then run the file
### You will be prompted to enter:

Starting row :

Ending row :

Whether to use Bing instead of Google :

The script will search for LinkedIn profiles and append the results to

``` contacts_with_linkedin.csv. ```
### Input File Format
``` Exhibitors Subset.csv```  must be a CSV with the following columns:

``` Name, Designation, Organization``` 

### Output
Appends the following to each row:


``` LinkedIn Profile (URL or error message) ```

###  CAPTCHA Handling
If a CAPTCHA appears:
* You will be prompted to solve it manually in the browser.

* After solving, press Enter to resume the automation.

### Limitations
* Google may block access if requests are too frequent.

* CAPTCHA solving is manual by default (can be integrated with services like Anti-Captcha).

### Customization

To bypass CAPTCHA using services like AntiCaptcha, uncomment and configure the relevant sections in
``` check_for_captcha().```
### License

This project is for educational and personal automation use only. Avoid violating terms of service of websites you interact with.

[MIT](https://choosealicense.com/licenses/mit/)


### Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
