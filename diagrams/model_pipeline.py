from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import Pubsub, Bigquery
from diagrams.gcp.storage import Storage
from diagrams.onprem.workflow import Airflow
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.iot import IotCore
from diagrams.onprem.database import Postgresql
from diagrams.custom import Custom
from diagrams.programming.framework import Fastapi


with Diagram("Model pipeline", filename="./images/model_pipeline"):
    pubsub = Pubsub("pubsub")
    with Cluster("Source of Data"):
        source = [
            IotCore("source 1"),
            IotCore("source 2"),
            IotCore("source 3"),
        ]

    with Cluster("data pipeline"):
        gcs = Storage("gcs")
        feature_engineering_task = Airflow("feature engineering")
        feature_store = Bigquery("feature_store")

    with Cluster("model-pipeline"):
        scheduler = Airflow("scheduler")
        aiplatform = AIPlatform("aiplatform")

    with Cluster("model-storage"):
        wandb = Custom("wandb", "../assets/wandb.png")
        neptune = Custom("neptune.ai", "../assets/neptuneai.png")
        mlflow = Custom("mlflow", "../assets/mlflow.png")
        model_storage = [wandb, neptune, mlflow]

    with Cluster("prediction-storage"):
        postgresql = Postgresql("postgresql")
        bigquery = Bigquery("bigquery")
        prediction_storage = [postgresql, bigquery]

    with Cluster("serving"):
        fastapi = Fastapi("fastapi")

    source >> pubsub
    pubsub >> gcs >> feature_engineering_task >> feature_store
    scheduler >> Edge(label="validate", style="dotted") >> feature_store
    scheduler >> Edge(label="trigger") >> aiplatform
    feature_store >> aiplatform
    aiplatform >> Edge(label="optional", style="dotted") >> prediction_storage
    aiplatform >> model_storage

    prediction_storage >> Edge(label="optional", style="dotted") >> fastapi
    model_storage >> Edge(label="optional", style="dotted") >> fastapi
