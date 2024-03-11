.PHONY: she-start
she-start:
	cd simpleHttpExamplePython && \
	source venv/bin/activate; \
	dapr run \
		--app-id function-app \
		--dapr-http-port 3501 \
		--app-port 7071 \
		-- func start -p 7071

.PHONY: she-test
she-test:
	curl http://localhost:7071/api/HttpExample?name=test222 
	curl http://localhost:3501/v1.0/invoke/function-app/method/api/HttpExample?name=xxx2
