from channels import ProtocolTypeRouter
import satellite_telemetry_data_analysis.routing

application = routing.ProtocolTypeRouter({
    
})
# """
# DEPRECATION_MSG =
# Using ProtocolTypeRouter without an explicit "http" key is deprecated.
# Given that you have not passed the "http" you likely should use Django's
# get_asgi_application():
# """

# from django.core.asgi import get_asgi_application

# application = ProtocolTypeRouter(
#     "http": get_asgi_application()
#     # Other protocols here.
# )
