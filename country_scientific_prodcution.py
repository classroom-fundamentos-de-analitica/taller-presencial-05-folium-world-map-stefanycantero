"""Taller Presencial Evaluable"""

import pandas as pd
import folium as fo

def load_affiliations():
    dataframe = pd.read_csv(
        "https://raw.githubusercontent.com/jdvelasq/datalabs/master/datasets/scopus-papers.csv",
        sep=",", index_col=None
    )[['Affiliations']]
    return dataframe


def remove_na_rows(affiliations):
    affiliations = affiliations.copy()
    affiliations = affiliations.dropna(subset=['Affiliations'])
    return affiliations


def add_countries_column(affiliations):
    """Transforma la columna 'Affiliations' a una lista de paises."""

    affiliations = affiliations.copy()
    affiliations["country"] = affiliations["Affiliations"].copy()
    # Separar las afiliaciones por punto y coma
    affiliations["country"] = affiliations["country"].str.split(";")
    # Separa cada afiliación por coma creando una lista de listas
    affiliations["country"] = affiliations["country"].map(
        lambda x: [y.split(",") for y in x]
    )
    # Obtener el pais de cada afiliación (último elemento de la lista)
    affiliations["country"] = affiliations["country"].map(
        lambda x: [y[-1].strip() for y in x]
    )
    # Eliminar los paises repetidos de cada lista
    affiliations["country"] = affiliations["country"].map(set)
    # Unir los paises en una cadena separada por coma
    affiliations["country"] = affiliations["country"].str.join(", ")

    return affiliations


def clean_countries(affiliations):
    affiliations = affiliations.copy()
    affiliations["country"] = affiliations["country"].str.replace("United States", "United States of America")

    return affiliations


def count_country_frequency(affiliations):
    """Cuenta la cantidad de afiliaciones por país."""

    affiliations = affiliations.copy()
    countries = affiliations["country"].str.split(", ")
    countries = countries.explode()
    countries = countries.value_counts()
    return countries

def plot_world_map(countries):
    """Grafica un mapa mundial con la frecuencia de cada país."""

    countries = countries.copy()
    countries = countries.to_frame()
    countries = countries.reset_index()

    m = fo.Map(location=[0, 0], zoom_start=2)

    fo.Choropleth(
        geo_data="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json",
        data=countries,
        columns=["country", "count"],
        key_on="feature.properties.name",
        fill_color="Greens",
    ).add_to(m)

    m.save("map.html")


def main():
    """Función principal"""
    affiliations = load_affiliations()
    affiliations = remove_na_rows(affiliations)
    affiliations = add_countries_column(affiliations)
    affiliations = clean_countries(affiliations)
    countries = count_country_frequency(affiliations)
    countries.to_csv("countries.csv")
    plot_world_map(countries)


if __name__ == "__main__":
    main()
