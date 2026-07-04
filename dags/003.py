# from airflow import DAG
# from airflow.operators.python import PythonOperator, BranchPythonOperator
# from airflow.operators.empty import EmptyOperator
# from airflow.operators.subdag import SubDagOperator
# from datetime import datetime, timedelta
# import random

# def decidir_subdag():
#     return random.choice(["subdag_etl", "subdag_auditoria"])

# def tarea_etl():
#     print("⚡ Ejecutando ETL simulado")

# def tarea_auditoria():
#     print("📑 Ejecutando Auditoría simulada")

# def crear_subdag_etl(parent_dag_name, child_dag_name, args):
#     with DAG(
#         dag_id=f"{parent_dag_name}.{child_dag_name}",
#         default_args=args,
#         schedule_interval=None,
#     ) as subdag:
#         PythonOperator(
#             task_id="etl_step",
#             python_callable=tarea_etl,
#         )
#     return subdag

# def crear_subdag_auditoria(parent_dag_name, child_dag_name, args):
#     with DAG(
#         dag_id=f"{parent_dag_name}.{child_dag_name}",
#         default_args=args,
#         schedule_interval=None,
#     ) as subdag:
#         PythonOperator(
#             task_id="auditoria_step",
#             python_callable=tarea_auditoria,
#         )
#     return subdag

# default_args = {
#     "owner": "manuel",
#     "retries": 1,
#     "retry_delay": timedelta(minutes=1),
# }

# with DAG(
#     dag_id="contenedor_dags",
#     start_date=datetime(2024, 1, 1),
#     schedule=None,
#     catchup=False,
#     default_args=default_args,
# ) as dag:

#     inicio = PythonOperator(
#         task_id="inicio",
#         python_callable=lambda: print("🚀 Inicio del contenedor"),
#     )

#     decision = BranchPythonOperator(
#         task_id="decidir_subdag",
#         python_callable=decidir_subdag,
#     )

#     subdag_etl = SubDagOperator(
#         task_id="subdag_etl",
#         subdag=crear_subdag_etl("contenedor_dags", "subdag_etl", default_args),
#     )

#     subdag_auditoria = SubDagOperator(
#         task_id="subdag_auditoria",
#         subdag=crear_subdag_auditoria("contenedor_dags", "subdag_auditoria", default_args),
#     )

#     fin = EmptyOperator(task_id="fin")

#     inicio >> decision >> [subdag_etl, subdag_auditoria] >> fin
