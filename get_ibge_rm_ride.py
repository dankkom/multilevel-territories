import os
import pathlib
import shutil
import urllib.request as request
from contextlib import closing
from itertools import islice, repeat

import dotenv
import pandas as pd

RM_RIDE_URL = (
    "https://geoftp.ibge.gov.br"
    "/organizacao_do_territorio"
    "/estrutura_territorial"
    "/municipios_por_regioes_metropolitanas"
    "/Situacao_2020a2029"
    "/Composicao_RMs_RIDEs_AglomUrbanas_2020_12_31.xlsx"
)

dotenv.load_dotenv()

# PATHS
DATADIR_DOWNLOADED = pathlib.Path(os.getenv("DATADIR_DOWNLOADED"))
if not DATADIR_DOWNLOADED.exists():
    DATADIR_DOWNLOADED.mkdir(parents=True)

DATADIR_OUTPUT = pathlib.Path(os.getenv("DATADIR_OUTPUT"))
if not DATADIR_OUTPUT.exists():
    DATADIR_OUTPUT.mkdir(parents=True)

RM_RIDE_XLSX_PATH = DATADIR_DOWNLOADED / "IBGE_RM_RIDE.xlsx"
RM_RIDE_CSV_PATH = DATADIR_OUTPUT / "ibge_rm_ride.csv"


def download_rm_ride():
    with closing(request.urlopen(RM_RIDE_URL)) as r:
        with open(RM_RIDE_XLSX_PATH, "wb") as f:
            shutil.copyfileobj(r, f)


def expand_cod_cat_assoc(rm_ride):
    index = rm_ride["cod_cat_assoc"].str.contains("a", na=False, regex=True)
    r = rm_ride[index]
    rm_ride = rm_ride.drop(labels=r.index)
    start, end = r["cod_cat_assoc"].iloc[0].split(" a ")
    cod_cat_assoc = list(range(int(start), int(end)+1))
    s = pd.concat(islice(repeat(r), len(cod_cat_assoc)), ignore_index=True)
    s = s.assign(cod_cat_assoc=cod_cat_assoc)
    rm_ride = pd.concat((rm_ride, s), ignore_index=True)
    rm_ride = rm_ride.assign(
        cod_cat_assoc=rm_ride["cod_cat_assoc"].astype(int),
    )
    return rm_ride


def main():
    if not RM_RIDE_XLSX_PATH.exists():
        download_rm_ride()
    rm_ride = pd.read_excel(RM_RIDE_XLSX_PATH)
    rm_ride = rm_ride.rename(columns=lambda x: x.lower())
    rm_ride = expand_cod_cat_assoc(rm_ride)
    rm_ride.to_csv(
        RM_RIDE_CSV_PATH,
        sep=",",
        decimal=".",
        encoding="utf-8",
        index=False,
    )


if __name__ == "__main__":
    main()
