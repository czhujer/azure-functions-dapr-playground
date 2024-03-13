import azure.functions as func
import requests
import logging
import os
from dapr.clients import DaprClient

bp_cat = func.Blueprint()

dapr_port = os.getenv("DAPR_HTTP_PORT", 3500)
dapr_url = "http://localhost:{}/v1.0/invoke/".format(dapr_port)

# @bp_cat.function_name(name="HttpCat")
# @bp_cat.dapr_service_invocation_trigger(arg_name="payload", method_name="HttpCat")
# @bp_cat.dapr_state_output(arg_name="state", state_store="statestore", key="cat")
# def main(payload: str, state: func.Out[str] ):
@bp_cat.route(route="HttpCat")
def HttpCat(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HttpCat: Python HTTP trigger function processed a request.')

    try:
        response = requests.get(
            dapr_url + "https://http.cat/method/status/200", timeout=5, 
            # headers = {"dapr-app-id": "HttpCat"}
        )
        response_length = str(len(response.content.decode("utf-8")))

        print("HttpCat: HTTP %d => %s bytes" % (response.status_code,
                                    response_length), flush=True)
        return func.HttpResponse(
            f"HttpCat: This HTTP triggered function executed. Response length: ${response_length}",
            status_code=response.status_code
        )
    except Exception as e:
        print(e, flush=True)
        return func.HttpResponse(
            f"HttpCat: This HTTP triggered function failed. Reason: ${e}",
            status_code=500
        )
