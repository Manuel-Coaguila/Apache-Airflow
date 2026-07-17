"""Tests for proyecto_001 DAG."""

import pytest
from airflow.models import DagBag

DAGS_FOLDER = "/opt/airflow/dags"


@pytest.fixture
def dagbag():
    return DagBag(dag_folder=DAGS_FOLDER, include_examples=False)


def test_dag_import(dagbag):
    dag = dagbag.get_dag("proyecto_001_dag")
    assert dag is not None
    assert len(dagbag.import_errors) == 0
