build-deploy-api: build-api register-api redeploy-api

build-api:
	docker-compose build api

register-api:
	kind load docker-image instances-management_api --name kind

redeploy-api: delete-api deploy-api

delete-api:
	kubectl delete pod spike-api

deploy-api:
	kubectl apply -f deploy/pod-spike-api.yaml

deploy-broker:
	kubectl apply -f deploy/pod-rabbitmq.yaml

build-deploy-worker: build-worker register-worker redeploy-worker

build-worker:
	docker-compose build worker

register-worker:
	kind load docker-image instances-management_worker --name kind

apply-cluster-roles:
	kubectl apply -f deploy/roles.yaml

setup: apply-cluster-roles build-api register-api build-worker register-worker deploy-api deploy-broker
