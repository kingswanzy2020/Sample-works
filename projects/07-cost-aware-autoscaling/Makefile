# Lab workflow on kind. Requires: docker, kind, kubectl, k6.
APP_DIR ?= app

cluster:
	kind create cluster --config kind/cluster.yaml

image:
	docker build -t sample-service:v1 $(APP_DIR)
	kind load docker-image sample-service:v1 --name scale

hpa: image
	kubectl apply -k k8s/hpa-cpu
	kubectl -n scale rollout status deploy/app

clean:
	kind delete cluster --name scale

.PHONY: cluster image hpa clean
