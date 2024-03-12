import azure.functions as func
import datetime
import json
import logging
import uuid
from dapr.clients import DaprClient

sql_binding = 'mysqldb'

bp_he = func.Blueprint()

@bp_he.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    log_message = name if name else "empty"

    with DaprClient() as d:
        sqlTableCmd = ('create table if not exists logs (id VARCHAR(50), message VARCHAR(50))')
        sqlCmd = ('insert into logs (id, message) values ' +
                '(\'%s\', \'%s\')' % (uuid.uuid4(), log_message))
        tablePayload = {'sql': sqlTableCmd}
        payload = {'sql': sqlCmd}

        print("SQL Table: " + sqlTableCmd, flush=True)
        print("SQL: " + sqlCmd, flush=True)

        try:
            # Insert data using Dapr output binding via HTTP Post
            resp = d.invoke_binding(binding_name=sql_binding, operation='exec',
                                    binding_metadata=tablePayload, data='')
            print("SQL response: ")
            print(resp.get_headers())

            resp = d.invoke_binding(binding_name=sql_binding, operation='exec',
                                    binding_metadata=payload, data='')
            print("SQL response: ")
            print(resp.get_headers())

        except Exception as e:
            print(e, flush=True)
            return func.HttpResponse(
                f"This HTTP triggered function failed. Reason: ${e}",
                status_code=500
            )
    
    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=422
        )