import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Корінь проєкту, щоб Python бачив data_generator.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from data_generator import generate_and_load  # noqa: E402

default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

DBT = "/home/samri/dbt-venv/bin/dbt"
DBT_DIR = "/home/samri/proj/ecommerce_dbt"
DBT_FLAGS = f"--project-dir {DBT_DIR} --profiles-dir {DBT_DIR}"

with DAG(
    "airline_elt_pipeline",
    default_args=default_args,
    description="ELT конвеєр авіакомпанії: генерація, dbt run, dbt test",
    schedule="@daily",
    catchup=False,
) as dag:

    extract_load_task = PythonOperator(
        task_id="extract_and_load_raw_data",
        python_callable=generate_and_load,
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run_transformations",
        bash_command=f"{DBT} run {DBT_FLAGS}",
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test_quality_gate",
        bash_command=f"{DBT} test {DBT_FLAGS}",
    )

    extract_load_task >> dbt_run_task >> dbt_test_task