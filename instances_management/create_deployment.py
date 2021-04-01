"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""

from kubernetes import client, config

WORKER_BASE_NAME = "spike-worker-"

TIERS = {
    0: {
        "requests": {"cpu": "10m", "memory": "10Mi"},
        "limits": {"cpu": "10m", "memory": "10Mi"},
    },
    1: {
        "requests": {"cpu": "110m", "memory": "210Mi"},
        "limits": {"cpu": "510m", "memory": "510Mi"},
    },
    2: {
        "requests": {"cpu": "120m", "memory": "220Mi"},
        "limits": {"cpu": "520m", "memory": "520Mi"},
    },
}


def create_deployment_object(name, tier: int = 1):
    name = f"{WORKER_BASE_NAME}{name}"
    # Configureate Pod template container
    container = client.V1Container(
        name=name,
        image="instances-management_worker",
        ports=[client.V1ContainerPort(container_port=80)],
        resources=client.V1ResourceRequirements(**TIERS[tier]),
        image_pull_policy="IfNotPresent",
        env=[
            client.V1EnvVar(name="WORKER_NAME", value=name),
        ],
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container]),
    )
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=tier,
        template=template,
        selector={"matchLabels": {"app": name}},
    )
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )

    return deployment


def create_deployment(deployment):
    config.load_incluster_config()
    api_instance = client.AppsV1Api()
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment, namespace="default"
    )
    print("Deployment created. status='%s'" % str(api_response.status))


def update_deployment(deployment):
    config.load_incluster_config()
    api_instance = client.AppsV1Api()
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=deployment.metadata.name, namespace="default", body=deployment
    )
    print("Deployment updated. status='%s'" % str(api_response.status))


def delete_deployment(name):
    name = f"{WORKER_BASE_NAME}{name}"
    config.load_incluster_config()
    api_instance = client.AppsV1Api()
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        ),
    )
    print("Deployment deleted. status='%s'" % str(api_response.status))
