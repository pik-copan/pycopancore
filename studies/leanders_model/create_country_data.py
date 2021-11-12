# ATTENTION: run from studies folder for correct paths

import numpy as np
import pandas as pd

data_folder = "leanders_model/data/"

# update ISO codes from Marc to existing ones
mw_to_iso_dict = {  902: 260,
                    903:  74,
                    904: 334,
                    905:  86,
                    906: 239,
                    907: 998, # made up Spratly Islands
                    908: 581,
                    999: 999  # made up Kosovo
                    }

def main():
    # create dataframe with both Marc's and official ISO codes
    country_codes_mw = np.load(data_folder+"List_of_country_ids.npy") # from Marc Wiedermann/ Nils Dunker

    country_codes_iso = np.array([mw_to_iso_dict[c] if c in mw_to_iso_dict else c for c in country_codes_mw])

    countries_df = pd.DataFrame({"mw_numeric": country_codes_mw, 
                                        "iso_numeric": country_codes_iso})



    # add official ISO-alpha-codes and inofficial Spratly Islands and Kosovo
    usecols_country_codes = [0,1,2,3]

    country_codes_df = pd.read_csv(data_folder + "all.csv", usecols=usecols_country_codes, na_filter=False) # from https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
    country_codes_df.columns = ["name", "alpha2", "alpha3", "iso_numeric"]

    missing_list = [c for c in country_codes_df["iso_numeric"] if c not in country_codes_iso] # These are 10 Antarctica, 162 Christmas Island and 162 Cocos (Keeling) Island
    print("\nCountries not in MW's dataset: ")
    print(country_codes_df[country_codes_df["iso_numeric"].isin(missing_list)])

    countries_df = countries_df.merge(country_codes_df, how="left", on="iso_numeric")

    countries_df.loc[245, ["alpha2", "alpha3", "name"]] = ["XS", "XSX", "Spratly Islands"] # made up codes
    countries_df.loc[247, ["alpha2", "alpha3", "name"]] = ["XK", "XKX", "Kosovo"] # inofficial codes

    countries_df = countries_df[["name", "mw_numeric", "iso_numeric", "alpha2", "alpha3"]]



    # add land area
    usecols_land_area = ["cca2", "area"]

    land_area_df = pd.read_csv(data_folder + "countries.csv", usecols=usecols_land_area, na_filter=False) # from https://github.com/mledoze/countries

    countries_df = countries_df.merge(land_area_df, how="left", left_on="alpha2", right_on="cca2").drop(columns=["cca2"])

    countries_df.loc[245, ["area"]] = 2.0



    # add population data
    population_array = np.load(data_folder + "country_pops.npy")

    countries_df["population"] = population_array

    # missing population data from Nils' hdf5 and the one smaller where it's not apparently not missing
    print("\nCountries with no population in Nils' dataset (mostly those with inoffial ISO): ")
    print(countries_df[countries_df["population"]==0])
    print(countries_df.loc[240, "name"] + " did not have an official ISO in MW's dataset but has population " + str(countries_df.loc[240, "population"]) + " =/= 0")



    # add gdp data
    usecols_gdp = ["Country Code", "2000", "2007", "2011", "2014", "2015", "2018", "2019", "2020"]

    gdp_df = pd.read_csv(data_folder + "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3263806.csv", skiprows=4, usecols=usecols_gdp) # from https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
    
    # if no data for 2020 exists, instead take the latest data
    gdp_df["gdp"] = gdp_df["2020"]
    
    years_used_to_fill = list(reversed(usecols_gdp[1:-1]))
    for y in years_used_to_fill:
        gdp_df["gdp"] = gdp_df["gdp"].fillna(gdp_df[y])

    countries_df = countries_df.merge(gdp_df[["Country Code", "gdp"]], how="left", left_on="alpha3", right_on="Country Code").drop(columns=["Country Code"])

    # add gdp for missing countries with pop > 1 Mio
    countries_df.loc[41, "gdp"] = 669034000000 # Taiwan from 2019 UN, according to Wikipedia https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29
    countries_df.loc[107, "gdp"] = 16331452312.852224 # North Korea from 2019 UN, https://unstats.un.org/unsd/snaama/basic

    # still missing gdp data
    print("\nCountries with no GDP data: ")
    print(countries_df[countries_df["gdp"].isna()])

    # add some with average GDP (1.1e4 per capita) where we don't have data
    countries_df["gdp"] = countries_df["gdp"].fillna(countries_df["population"]*1.1e4)


    # save to csv
    countries_df.to_csv(data_folder + "country_data.csv")

if __name__ == "__main__":
    main()
