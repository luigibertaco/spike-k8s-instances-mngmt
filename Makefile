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

redeploy-worker: delete-worker deploy-worker

delete-worker:
	kubectl delete pod spike-worker

deploy-worker:
	kubectl apply -f deploy/pod-spike-worker.yaml
