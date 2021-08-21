import json
import os
import pathlib

import pandas as pd
import requests
import dotenv

URL_LOCALITIES = "https://servicodados.ibge.gov.br/api/v1/localidades"

dotenv.load_dotenv()

# PATHS
DATADIR_DOWNLOADED = pathlib.Path(os.getenv("DATADIR_DOWNLOADED"))
if not DATADIR_DOWNLOADED.exists():
    DATADIR_DOWNLOADED.mkdir(parents=True)

DATADIR_OUTPUT = pathlib.Path(os.getenv("DATADIR_OUTPUT"))
if not DATADIR_OUTPUT.exists():
    DATADIR_OUTPUT.mkdir(parents=True)

MUNICIPALITIES_PATH = DATADIR_DOWNLOADED / "municipalities.json"
COUNTRIES_PATH = DATADIR_DOWNLOADED / "countries.json"

RM_RIDE_CSV_PATH = DATADIR_OUTPUT / "ibge_rm_ride.csv"
GEO_DEST_PATH = DATADIR_OUTPUT / "d_geografia.csv"

RM_CODE_MULTIPLIER_FACTOR = 10_000


def get_municipalities():
    if MUNICIPALITIES_PATH.exists():
        with open(MUNICIPALITIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        url = URL_LOCALITIES + "/municipios"
        r = requests.get(url)
        data = r.json()
        with open(MUNICIPALITIES_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data


def get_countries():
    if COUNTRIES_PATH.exists():
        with open(COUNTRIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        url = URL_LOCALITIES + "/paises"
        r = requests.get(url)
        data = r.json()
        with open(COUNTRIES_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data


def iter_municipalities(data):
    for mun in data:
        mun_id = mun["id"]
        mun_name = mun["nome"]
        micro = mun["microrregiao"]
        micro_id = micro["id"]
        micro_name = micro["nome"]
        meso = micro["mesorregiao"]
        meso_id = meso["id"]
        meso_name = meso["nome"]
        uf = meso["UF"]
        uf_id = uf["id"]
        uf_sigla = uf["sigla"]
        uf_name = uf["nome"]
        region = uf["regiao"]
        region_id = region["id"]
        region_abbr = region["sigla"]
        region_name = region["nome"]
        yield {
            "municipio_id": mun_id,
            "municipio": mun_name,
            "microrregiao_id": micro_id,
            "microrregiao": micro_name,
            "mesorregiao_id": meso_id,
            "mesorregiao": meso_name,
            "uf_id": uf_id,
            "uf_sigla": uf_sigla,
            "uf": uf_name,
            "regiao_id": region_id,
            "regiao_sigla": region_abbr,
            "regiao": region_name,
        }


def municipalities_to_df(data):
    df = pd.DataFrame(iter_municipalities(data))
    return df


def get_brazil_geography(municipalities_df):
    mu = (
        municipalities_df[["municipio_id", "municipio"]]
        .drop_duplicates()
        .assign(
            nivel_territorial="Município",
            municipio=(
                municipalities_df["municipio"]
                + " - "
                + municipalities_df["uf_sigla"]
            ),
        )
        .rename(
            columns={
                "municipio_id": "unidade_territorial_id",
                "municipio": "unidade_territorial",
            }
        )
    )
    mi = (
        municipalities_df[["microrregiao_id", "microrregiao"]]
        .drop_duplicates()
        .assign(nivel_territorial="Microrregião")
        .rename(
            columns={
                "microrregiao_id": "unidade_territorial_id",
                "microrregiao": "unidade_territorial",
            }
        )
    )
    me = (
        municipalities_df[["mesorregiao_id", "mesorregiao"]]
        .drop_duplicates()
        .assign(nivel_territorial="Mesorregião")
        .rename(
            columns={
                "mesorregiao_id": "unidade_territorial_id",
                "mesorregiao": "unidade_territorial",
            }
        )
    )
    uf = (
        municipalities_df[["uf_id", "uf"]]
        .drop_duplicates()
        .assign(nivel_territorial="Unidade da Federação")
        .rename(
            columns={
                "uf_id": "unidade_territorial_id",
                "uf": "unidade_territorial",
            }
        )
    )
    re = (
        municipalities_df[["regiao_id", "regiao"]]
        .drop_duplicates()
        .assign(nivel_territorial="Grande Região")
        .rename(
            columns={
                "regiao_id": "unidade_territorial_id",
                "regiao": "unidade_territorial",
            }
        )
    )
    br = pd.DataFrame(
        {
            "unidade_territorial_id": [-76],
            "unidade_territorial": ["Brasil"],
            "nivel_territorial": ["País"],
        }
    )

    geo = pd.concat(
        (
            mu,
            mi,
            me,
            uf,
            re,
            br,
        ),
        ignore_index=True,
    )

    return geo


def iter_countries(data):
    for country in data:
        country_id = country["id"]
        country_id_iso_alpha_2 = country_id["ISO-ALPHA-2"]
        country_id_iso_alpha_3 = country_id["ISO-ALPHA-3"]
        country_id_m49 = country_id["M49"]
        country_name = country["nome"]
        intermediary_region = country["regiao-intermediaria"]
        if intermediary_region:
            intermediary_region_id = intermediary_region["id"]
            intermediary_region_id_m49 = intermediary_region_id["M49"]
            intermediary_region_name = intermediary_region["nome"]
        else:
            intermediary_region_id_m49 = intermediary_region_name = None
        sub_region = country["sub-regiao"]
        sub_region_id = sub_region["id"]
        sub_region_id_m49 = sub_region_id["M49"]
        sub_region_name = sub_region["nome"]
        region = sub_region["regiao"]
        region_id = region["id"]
        region_id_m49 = region_id["M49"]
        region_name = region["nome"]
        yield {
            "pais_id_iso_alpha_2": country_id_iso_alpha_2,
            "pais_id_iso_alpha_3": country_id_iso_alpha_3,
            "pais_id_m49": country_id_m49,
            "pais": country_name,
            "regiao_intermediaria_id_m49": intermediary_region_id_m49,
            "regiao_intermediaria": intermediary_region_name,
            "sub_regiao_id_m49": sub_region_id_m49,
            "sub_regiao": sub_region_name,
            "regiao_id_m49": region_id_m49,
            "regiao": region_name,
        }


def countries_to_df(data):
    df = pd.DataFrame(iter_countries(data))
    return df


def get_countries_geo(countries_df):
    pais = (
        countries_df[["pais_id_m49", "pais"]]
        .drop_duplicates()
        .assign(nivel_territorial="País")
        .rename(
            columns={
                "pais_id_m49": "unidade_territorial_id",
                "pais": "unidade_territorial",
            }
        )
    )

    subregiao = (
        countries_df[["sub_regiao_id_m49", "sub_regiao"]]
        .drop_duplicates()
        .assign(nivel_territorial="Sub-Região")
        .rename(
            columns={
                "sub_regiao_id_m49": "unidade_territorial_id",
                "sub_regiao": "unidade_territorial",
            }
        )
    )

    continente = (
        countries_df[["regiao_id_m49", "regiao"]]
        .drop_duplicates()
        .assign(nivel_territorial="Continente")
        .rename(
            columns={
                "regiao_id_m49": "unidade_territorial_id",
                "regiao": "unidade_territorial",
            }
        )
    )

    geo = pd.concat(
        (
            pais,
            subregiao,
            continente,
        ),
        ignore_index=True,
    )
    geo.loc[:, "unidade_territorial_id"] *= -1

    return geo


def get_rm_geo(rm_ride_df):
    rm_geo = (
        rm_ride_df
        .loc[
            rm_ride_df["tipo"] == "RM",
            ["cod", "nome", "sigla_uf"]
        ]
        .drop_duplicates()
        .assign(
            cod=rm_ride_df["cod"] * RM_CODE_MULTIPLIER_FACTOR,
            nome=(
                rm_ride_df["nome"]
                .replace(r"^Região Metropolitana d(a|e|o) ", "", regex=True)
                + " - "
                + rm_ride_df["sigla_uf"]
            ),
            nivel_territorial="Região Metropolitana",
        )
        .rename(
            columns={
                "cod": "unidade_territorial_id",
                "nome": "unidade_territorial",
            },
        )
        .loc[
            :,
            [
                "unidade_territorial_id",
                "unidade_territorial",
                "nivel_territorial",
            ]
        ]
    )

    return rm_geo


def main():
    data_mun = get_municipalities()
    municipalities_df = municipalities_to_df(data_mun)
    br_geo = get_brazil_geography(municipalities_df)

    countries_data = get_countries()
    countries_df = countries_to_df(countries_data)
    countries_geo = get_countries_geo(countries_df)

    rm_ride_df = pd.read_csv(RM_RIDE_CSV_PATH)
    rm_geo = get_rm_geo(rm_ride_df)

    geo = (
        pd.concat(
            (br_geo, countries_geo, rm_geo),
            ignore_index=True,
        )
        .drop_duplicates()
    )

    geo.to_csv(
        GEO_DEST_PATH,
        sep=",",
        decimal=".",
        encoding="utf-8",
        index=False,
    )


if __name__ == "__main__":
    main()
