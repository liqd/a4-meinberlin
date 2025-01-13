import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_kiezradar_user_limit(user, kiez_radar_factory):
    kiezradar = kiez_radar_factory(creator=user)
    with pytest.raises(ValidationError) as error:
        for i in range(kiezradar.KIEZRADAR_LIMIT):
            kiez_radar_factory(creator=user)
        assert "Users can only have up to 5 radius filters." in error
