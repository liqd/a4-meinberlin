from meinberlin.apps.ideas.exports import IdeaExportView
from meinberlin.apps.mapideas.exports import MapIdeaExportView


def test_idea_export_contains_contact_fields():
    export = IdeaExportView()
    virtual = export.get_virtual_fields({})
    assert "contact_email" in virtual
    assert "contact_phone" in virtual


def test_mapidea_export_contains_contact_fields():
    export = MapIdeaExportView()
    virtual = export.get_virtual_fields({})
    assert "contact_email" in virtual
    assert "contact_phone" in virtual
