from rest_framework import routers
from api.views import CreateIndividualInfoViewSet

router = routers.DefaultRouter()
router.register(
    r"create_individual_info",
    CreateIndividualInfoViewSet,
    basename="create-individual-info",
)
urlpatterns = router.urls
