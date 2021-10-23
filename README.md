# Corona Priority List #

#### Video Demo: <https://youtu.be/lZpJ4KjuJrM>
#### Description: This project, using Python, creates an attention priority list of every region in Peru based on the impact Covid-19 had on the region. Taking into consideration the number of cases, mortality rate, medical centers available and more, each region gets a score that measures how much it has been affected by the pandemic.

-- BEFORE RUNNING THE PROGRAM --

The project starts by taking in databases (located inside the datos folder), which are the following:
* positivos_covid.csv (Covid-19 cases per region)
* fallecidos_covid.csv (Deaths due to Covid-19)
* dpto.csv (Population per region)
* Camas (1).csv (ICUs across the country)
* pob65.csv (Population that is 65 years old or older)
* IPRESS.csv (Medical centers per region)
All databases were taken from MINSA, Peru's health department, on June 12th 2021. Each database is updated on a daily basis.

When downloaded, the user will need to change each database location for the ones on their computer.

The user will change the following variable:
	- pob_location (location for: dpto.csv)

And the pd.read_csv strings at the beginning of the file.

Once that the program executes, it will return the list in the terminal and in a .csv file.


-- HOW DOES THE PROGRAM WORK --

The program reads each database and takes essential information into a central database (a list of dictionaries).
This central database contains the following:
    * The name of the region
    * The number of COVID-19 cases
    * The number of COVID-19 related deaths
    * Elderly population
    * Comorbidity rate

The number of centers available per region is available on another database called "centros_dep".

Afterwards, the program uses an algorithm to find the score for each region.
Each variable is weighted on its impact and influence on a region's state during COVID-19.
The variables are weighted like this:
    * Health centers available per citizen (30%)
    * Mortality rate (25%)
    * Comorbidity (20%)
    * Cases in the region (10%)
    * Elderly population (10%)
    * ICUs (5%)

At first I thought about including vaccination progress, but I decided to skip it to use variables that predict the evolution of the pandemic in the region, such as comorbidity and elderly population.

Once that the algorithm finds the score for the region, it adds it to the region's dictionary.
Then, the dictionary is added to the final list and the program returns a csv file with the region's rank and other data.

-- WEIGHT FACTORS --
The variables used by the program have been weighted according to my criteria. However, this doesn't mean that more objective and accurate results can't be found.
It would be a matter of tweaking each factor to obtain a desired result, which may change the list result from the default version.
In case the user wants to change each weight factor accordingly, he/she will have to change each of the coefficients in the punt variable.
It is recommended to make sure that sum of each coefficient always equal 100.


