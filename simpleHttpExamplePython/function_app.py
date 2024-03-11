import azure.functions as func
# import azure.durable_functions as df
from http_example_blueprint import bp_he

# app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(bp_he)
