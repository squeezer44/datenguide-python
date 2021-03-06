import pandas as pd
import pytest
import os

from datenguidepy.output_transformer import QueryOutputTransformer
from tests.case_construction import construct_execution_results


@pytest.fixture
def query_result():
    abs_path = os.path.abspath(os.path.dirname(__file__))
    example_path = "examples/transformer_example1.json"
    full_path = os.path.join(abs_path, example_path)
    return construct_execution_results(full_path)


@pytest.fixture
def query_results_with_enum():
    abs_path = os.path.abspath(os.path.dirname(__file__))
    example_path = "examples/transformer_example2.json"
    full_path = os.path.join(abs_path, example_path)
    return construct_execution_results(full_path)


def test_output_transformer_defaults(query_result):

    """ start test of output transformer """
    qOutTrans = QueryOutputTransformer(query_result)

    data_transformed = qOutTrans.transform()

    # test whether transformed output data is a dataframe
    assert type(data_transformed) == pd.DataFrame, "transformed data is not a dataframe"

    assert "id" in data_transformed.columns, "no id colum"
    assert "name" in data_transformed.columns, "no name colum"
    assert "year" in data_transformed.columns, "no year colum"
    assert "BEVMK3" in data_transformed.columns, "statistic values are missing"
    assert (
        "BEVMK3_value" not in data_transformed.columns
    ), "old statistics name still present"

    # columns of outdata should not contain json format
    lenlist = len(data_transformed.columns)
    checklist = ["." in data_transformed.columns[x] for x in range(lenlist)]
    assert not any(checklist), "hierarchy not properly transformed"


def test_output_transformer_format_options(query_result, query_results_with_enum):

    qOutTrans = QueryOutputTransformer(query_result)
    data_transformed = qOutTrans.transform(verbose_statistic_names=True)
    assert (
        # "Von der Scheidung betroffene Kinder (BEVMK3)" in data_transformed.columns
        "BEVMK3 (BEVMK3)"
        in data_transformed.columns
    ), "statistic values are missing"

    enum_values = {
        "AFD",
        "B90_GRUENE",
        "CDU",
        "DIELINKE",
        "FDP",
        "SONSTIGE",
        "SPD",
        "GESAMT",
        None,
    }
    enum_descriptions = {
        "AfD",
        "GRÜNE",
        "CDU/CSU",
        "DIE LINKE",
        "FDP",
        "Sonstige Parteien",
        "SPD",
        "Gesamt",
    }

    qOutTrans = QueryOutputTransformer(query_results_with_enum)
    data_transformed = qOutTrans.transform()
    assert set(data_transformed["PART04"]).issubset(enum_values)

    qOutTrans = QueryOutputTransformer(query_results_with_enum)
    data_transformed = qOutTrans.transform(verbose_enum_values=True)
    assert set(data_transformed["PART04"]).issubset(enum_descriptions)

    qOutTrans = QueryOutputTransformer(query_results_with_enum)
    data_transformed = qOutTrans.transform(
        verbose_enum_values=True, verbose_statistic_names=True
    )
    # assert "Gültige Zweitstimmen (WAHL09)" in data_transformed
    assert "WAHL09 (WAHL09)" in data_transformed
