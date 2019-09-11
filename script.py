#@author : Thibaut Ehlinger
#Summary : execute this script and you'll have the most common
#first letters of names in France per gender (1=male,2=female) and you can
#specify the desired slices of age

#Namesfile are here : https://www.insee.fr/fr/statistiques/2540004

#My conclusions : there is no magic letter like in the US where M+J is 20% of
#the population.
#In France, the first letters are very evenly distributed, as can be seen
#when you execute the script
import pandas as pd

def get_data():
    return pd.read_csv("nat2018.csv",sep=";")

def get_top_first_letter(original_df=None,gender=1,oldest=1920,youngest=2018,nb=5):
    df = pd.DataFrame(get_top(original_df,gender,oldest,youngest))
    df["first_letter"] = [i[0] for i in list(df.index)]
    return df.groupby(["first_letter"]).nombre.sum().sort_values(ascending=False).iloc[:nb]

def get_top(original_df=None,gender=1,oldest=1920,youngest=2018,nb=None):
    if original_df is None :
        df = pd.read_csv("nat2018.csv",sep=";")
    else:
        df = original_df.copy()
    df["annee"] = pd.to_numeric(df["annais"],errors='coerce')
    df = df.dropna()
    df = df.loc[~df["preusuel"].str.match("_PRENOMS_RARES")]
    df = df.loc[df.sexe==gender]
    df = df.loc[df.annee.gt(oldest)]
    df = df.loc[df.annee.lt(youngest)]
    result = df.groupby(["preusuel"]).nombre.sum().sort_values(ascending=False)
    if nb is not None:
        return result.iloc[:nb]
    else:
        return result

#def get_top_first_letter(original_df=None,gender=1,oldest=1920,youngest=2018):
orig_df = get_data()
for gender in [1,2]:
    print("VIEUX :")
    print(get_top_first_letter(orig_df,gender,1959,1989,nb=10))
    print("JEUNE :")
    print(get_top_first_letter(orig_df,gender,1989,2019,nb=10))
