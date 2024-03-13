import azure.functions as func
# import azure.durable_functions as df
from http_example_blueprint import bp_he
from http_cat_blueprint import bp_cat

# app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_blueprint(bp_he)
app.register_blueprint(bp_cat)
