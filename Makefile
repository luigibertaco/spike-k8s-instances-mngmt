build-deploy-api: build-api register-api redeploy-api

build-api:
	docker-compose build

register-api:
	kind load docker-image instances-management_api --name kind

redeploy-api: delete-api deploy-api

delete-api:
	kubectl delete pod spike-api

deploy-api:
	kubectl apply -f deploy/pod-spike-api.yaml

deploy-broker:
	kubectl apply -f deploy/pod-rabbitmq.yaml

