# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Restore Title Field",
    "version": "19.0.1",
    "category": "Base",
    "summary": "This module restores the title field in the partner form",
    "author": "Ouiddoo",
    "website": "https://www.ouiddoo.com",
    "maintainers": ["Louis-de-Bontin"],
    "license": "AGPL-3",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_partner_title_views.xml",
    ],
    "installable": True,
}
