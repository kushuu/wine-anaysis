import pandas as pd


country_code_mapper = {
    'US':'USA',
    'France':'FRA',
    'Italy':'ITA',
    'Spain':'ESP',
    'Portugal':'PRT',
    'Australia':'AUS',
    'Chile':'CHL',
    'Argentina':'ARG',
    'Austria':'ART',
    'Germany':'DEU',
    'New Zealand':'NZL',
    'South Africa':'ZAF',
    'Israel':'ISR',
    'Greece':'GRC',
    'Buy Now': None,
    'Hungary':'HUN',
    'Romania':'ROU',
}

def get_country(val):
    if val == val and val:
        return val.split(',')[-1].strip()
    return

def get_c_code(val):
    if val:
        return country_code_mapper[val]
    return


df = pd.read_csv("clean_wine.csv")
df['appellation'] = df.appellation.apply(get_country)
df = df.rename(columns={'appellation':'country'})
df['country_code'] = df.country.apply(get_c_code)

df.to_csv('clean_winesV2.csv', index=False)