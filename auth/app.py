from flasgger import Swagger
from flask import Flask
from flask_request_id_header.middleware import RequestID

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from middleware import ExceptionHandlerMiddleware

resource = Resource(attributes={
    SERVICE_NAME: "Auth"
})


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='jaeger',
                agent_port=6831
            )
        )
    )


configure_tracer()

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)

swagger = Swagger(app)

app.config['REQUEST_ID_UNIQUE_VALUE_PREFIX'] = 'AUTH-'
RequestID(app)

app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
