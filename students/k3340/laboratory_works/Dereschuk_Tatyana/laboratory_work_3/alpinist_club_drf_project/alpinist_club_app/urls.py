from django.urls import path

from alpinist_club_app.views import MountainAPIVIew, MountainUpdateView, MountainRetrieveView, ClubAPIView, \
    AlpinistAPIView, AlpinistRetrieveView, AlpinistUpdateView, AscendingAPIView, AscendingRetrieveView, \
    AscendingUpdateView, AscendingGroupAPIView, AscendingGroupRetrieveView, AscendingGroupUpdateView, \
    AlpinistInGroupAPIView, AlpinistInGroupRetrieveView, AlpinistInGroupUpdateView, AlpinistsAscendingInPeriodView, \
    AscendingsInPeriodView, CountOfAlpinistsOnMountainsView, MountainsWithoutAscendingsView, \
    AlpinistMountainAscendingsView, ReportAPIView

urlpatterns = [
    path('mountains', MountainAPIVIew.as_view()),
    path('mountains/<int:id>/update', MountainUpdateView.as_view()),
    path('mountains/<int:id>', MountainRetrieveView.as_view()),
    path('mountains/alpinists_count', CountOfAlpinistsOnMountainsView.as_view()),
    path('mountains/without_ascendings', MountainsWithoutAscendingsView.as_view()),
    path('clubs', ClubAPIView.as_view()),
    path('alpinists', AlpinistAPIView.as_view()),
    path('alpinists/<int:id>', AlpinistRetrieveView.as_view()),
    path('alpinists/<int:id>/update', AlpinistUpdateView.as_view()),
    path('alpinists/ascendings_period', AlpinistsAscendingInPeriodView.as_view()),
    path('alpinists/mountain_ascendings', AlpinistMountainAscendingsView.as_view()),
    path('ascendings', AscendingAPIView.as_view()),
    path('ascendings/<int:id>', AscendingRetrieveView.as_view()),
    path('ascendings/<int:id>/update', AscendingUpdateView.as_view()),
    path('ascendings/groups', AscendingGroupAPIView.as_view()),
    path('ascendings/period', AscendingsInPeriodView.as_view()),
    path('ascendings/groups/<int:id>', AscendingGroupRetrieveView.as_view()),
    path('ascendings/groups/<int:id>/update', AscendingGroupUpdateView.as_view()),

    path('ascendings/groups/<int:group_id>/members', AlpinistInGroupAPIView.as_view()),
    path('ascendings/groups/members/<int:id>', AlpinistInGroupRetrieveView.as_view()),
    path('ascendings/groups/members/<int:id>/update', AlpinistInGroupUpdateView.as_view()),

    path('report', ReportAPIView.as_view())

]