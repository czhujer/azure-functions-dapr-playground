.PHONY: dapr-init
dapr-init:
	dapr init --slim

.PHONY: she-deps
she-deps:
	cd simpleHttpExamplePython && \
	source venv/bin/activate; \
	python3.10 -m pip install -r requirements.txt

.PHONY: she-start
she-start:
	cd simpleHttpExamplePython && \
	source venv/bin/activate; \
	dapr run \
		--app-id function-app \
		--placement-host-address 127.0.0.1:50006 \
		--resources-path ./resources/ \
		--dapr-http-port 3501 \
		--app-port 7071 \
		--config ./tracing.yaml \
		-- func start -p 7071

.PHONY: she-test
she-test:
	echo "test test222: "
	curl http://localhost:7071/api/HttpExample?name=test222 -i
	echo ""
	echo "test xxx2: "
	curl http://localhost:3501/v1.0/invoke/function-app/method/api/HttpExample?name=xxx2 -i
	echo ""
