from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('animals', views.AnimalViewSet)
router.register('animals/winterp-laces', views.WinterPlaceViewSet)

router.register('food/diets', views.DietViewSet)
router.register('habitats', views.HabitatViewSet)

router.register('locations', views.AreaViewSet)
router.register('locations/cage', views.CageViewSet)
router.register('locations/locations', views.AnimalInCageViewSet)

urlpatterns = router.urls
