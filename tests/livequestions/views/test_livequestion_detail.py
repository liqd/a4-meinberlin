import pytest
from dateutil.parser import parse
from django.utils import translation
from freezegun import freeze_time

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.livequestions import phases


@pytest.mark.django_db
def test_detail_view(
    client, user, phase_factory, live_question_factory, live_stream_factory
):
    phase, module, project, live_question = setup_phase(
        phase_factory,
        live_question_factory,
        phases.IssuePhase,
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
    )
    url = module.get_absolute_url()

    with freeze_time(parse("2013-01-01 18:00:00 UTC")):
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_livequestions/question_module_detail.html"
        )
        assert "Live" not in response.content.decode()

    live_stream = live_stream_factory(module=module, creator_id=user.id)
    live_stream.live_stream = (
        '<div><div><iframe src="https://some.video" style=""></iframe>' "</div></div>"
    )
    live_stream.save()

    with freeze_time(parse("2013-01-01 18:00:00 UTC")):
        with translation.override("en_GB"):
            response = client.get(url)
            assert "Live" in response.content.decode()

    with freeze_time(parse("2013-01-01 19:30:00 UTC")):
        with translation.override("en_GB"):
            response = client.get(url)
            assert "Live" not in response.content.decode()
