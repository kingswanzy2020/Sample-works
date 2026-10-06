# Lab workflow. Requires: docker, kind, kubectl, k6.
APP_DIR ?= app

cluster:
	kind create cluster --config kind/cluster.yaml

images:
	docker build -t sample-service:v1 --build-arg APP_VERSION=v1 $(APP_DIR)
	docker build -t sample-service:v2 --build-arg APP_VERSION=v2 $(APP_DIR)
	kind load docker-image sample-service:v1 sample-service:v2 --name zdd

rolling: images
	kubectl apply -k k8s/rolling
	kubectl -n zdd wait --for=condition=available deploy/postgres --timeout=120s
	kubectl apply -f k8s/base/migrate-job.yaml
	kubectl -n zdd wait --for=condition=complete job/migrate --timeout=120s
	kubectl -n zdd rollout status deploy/app

deploy-v2:
	scripts/deploy-under-load.sh sample-service:v2

clean:
	kind delete cluster --name zdd

.PHONY: cluster images rolling deploy-v2 clean
