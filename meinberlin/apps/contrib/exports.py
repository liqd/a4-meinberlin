from django.utils.translation import gettext as _


class ContactInfoExportMixin:
    """Add the contact information fields to an item export."""

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["contact_email"] = _("Contact E-Mail")
        virtual["contact_phone"] = _("Contact Phone")
        return virtual
