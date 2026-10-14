import pytest

from meinberlin.apps.budgeting.forms import ProposalForm


@pytest.mark.django_db
def test_proposal_form_media_uses_existing_bundle(module, area_settings_factory, user):
    area_settings_factory(module=module)
    form = ProposalForm(
        module=module, settings_instance=module.settings_instance, user=user
    )

    # The proposal form must load the same contact script as the other forms;
    # the former "budgeting_disable_contact.js" entry no longer exists and
    # breaks rendering when static files are served from a manifest.
    assert "contact_information.js" in form.media._js
    assert "budgeting_disable_contact.js" not in form.media._js
