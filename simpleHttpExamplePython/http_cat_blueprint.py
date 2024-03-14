import azure.functions as func
import requests
import logging
import os
from dapr.clients import DaprClient
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

bp_cat = func.Blueprint()

otelLogger = logging.getLogger("otel")
configure_azure_monitor(
    disable_offline_storage=True,
    logger_name="otelLogger"
)

dapr_port = os.getenv("DAPR_HTTP_PORT", 3500)
dapr_url = "http://localhost:{}/v1.0/invoke/".format(dapr_port)

# @bp_cat.function_name(name="HttpCat")
# @bp_cat.dapr_service_invocation_trigger(arg_name="payload", method_name="HttpCat")
# @bp_cat.dapr_state_output(arg_name="state", state_store="statestore", key="cat")
# def main(payload: str, state: func.Out[str] ):
@bp_cat.route(route="HttpCat")
def HttpCat(req: func.HttpRequest, context) -> func.HttpResponse:
    logging.info('HttpCat: Python HTTP trigger function processed a request.')

    # Store current TraceContext in dictionary format
    carrier = {
        "traceparent": context.trace_context.Traceparent,
        "tracestate": context.trace_context.Tracestate,
    }

    tracer = trace.get_tracer(__name__)
    # Start a span using the current context

    with tracer.start_as_current_span(
        "http_trigger_span",
        context=extract(carrier),
    ) as span:
        try:
            headers = {}
            ctx = baggage.set_baggage("hello", "world")
            W3CBaggagePropagator().inject(headers, ctx)
            TraceContextTextMapPropagator().inject(headers, ctx)
            print("HttpCat: headers: " + str(headers))

            # opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()
            response = requests.get(
                dapr_url + "https://http.cat/method/status/200",
                timeout=5, 
                # headers=headers
            )
            response_length = str(len(response.content.decode("utf-8")))

            response_log = f"HttpCat: Response: HTTP {response.status_code} => {response_length} bytes"
            print(response_log , flush=True)
            span.add_event(response_log)
            print("HttpCat: response header: traceparent: " + response.headers['Traceparent'])

            return func.HttpResponse(
                f"HttpCat: This HTTP triggered function executed. Response length: ${response_length}",
                status_code=response.status_code
            )
        except Exception as e:
            print(e, flush=True)
            span.set_attribute("status", "exception")
            span.record_exception(e)
            return func.HttpResponse(
                f"HttpCat: This HTTP triggered function failed. Reason: {e}",
                status_code=500
            )
