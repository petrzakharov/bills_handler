from typing import Type, Union

import numpy as np
import pandas as pd
from rest_framework.exceptions import APIException

from app.models import Client, Organisation, Service


class WrongFileFormatException(APIException):
    status_code = 503
    default_detail = 'Wrong file format :('


def create_or_get_unique_db(
    model: Type[Union[Client, Organisation, Service]], values: list
) -> dict:
    objects = {}
    for value in values:
        db_obj, created = model.objects.get_or_create(name=value)
        objects[value] = db_obj
    return objects


def file_prepare(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    if len(df.columns) != 6:
        raise WrongFileFormatException
    df.columns = ["client", "organisation", "bill_number", "summa", "date", "service"]
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="coerce")
    df[["bill_number", "summa"]] = df[["bill_number", "summa"]].apply(
        pd.to_numeric, errors="coerce"
    )
    df["service"] = df["service"].replace("-", np.nan)
    df = df.dropna()
    df = df.astype({"bill_number": "int"})
    return df
