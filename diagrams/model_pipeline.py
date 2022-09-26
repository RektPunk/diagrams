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
    with Cluster("Source of Data"):
        source = [
            IotCore("source 1"),
            IotCore("source 2"),
            IotCore("source 3"),
        ]
        pubsub = Pubsub("pubsub")
        gcs = Storage("gcs")

    with Cluster("Scheduler"):
        with Cluster("model-pipeline"):
            feature_store = Bigquery("feature_store")
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
    pubsub >> gcs >> feature_store
    feature_store >> aiplatform
    aiplatform >> Edge(style="dotted") >> prediction_storage
    aiplatform >> Edge(style="dotted") >> model_storage

    prediction_storage >> Edge(style="dotted") >> fastapi
    model_storage >> Edge(style="dotted") >> fastapi
