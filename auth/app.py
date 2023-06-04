from authlib.integrations.flask_client import OAuth
from config import settings
from flasgger import Swagger
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_request_id_header.middleware import RequestID
from middleware import ExceptionHandlerMiddleware
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "Auth"
})


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.JAEGER_HOST,
                agent_port=settings.JAEGER_PORT
            )
        )
    )


app = Flask(__name__)
app.secret_key = settings.SECRET

oauth = OAuth(app)

if settings.ENABLE_JAEGER_TRACER:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    strategy='fixed-window',
    default_limits=[
        f'{settings.REQUEST_NUM_LIMIT} per {settings.REQUEST_TIME_LIMIT}'
    ]
)

swagger = Swagger(app)

app.config['REQUEST_ID_UNIQUE_VALUE_PREFIX'] = 'AUTH-'
RequestID(app)

app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
