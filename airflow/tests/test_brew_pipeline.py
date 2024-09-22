from http import HTTPStatus
import pytest
from airflow.models import DagBag

# Test if dag is OK
@pytest.fixture()
def dagbag():
    return DagBag()

def test_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id='breweries_pipeline')
    assert dag is not None