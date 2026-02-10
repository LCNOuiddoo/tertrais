# tertrais Odoov19

Upgrade process:
- ⚠️ Follow the tutorial in the `partner_title` module
    - We may have to archive the following automations to allow the import (unarchive after the import):
        - Règle champ requis Contact : Type de Client et Equipe Commerciale
        - ALERTE Incohérence Contact Détectée OK (manque TSURV pro part lucon)
- Uninstall `sale_project_tertrais`, test if the sales are linked to project properly. If yes, remove it from the repo.
- Deactivate the view `access_restriction_by_ip.res_users_allowed_ips`
- Remove the `res_user.allowed_ips` field
- Re-push code


I copied and pasted the Odoo default code to fix some views. Here are their IDs:
- 5850
- 2783

This had to be done because the upgrade of the `base` module was blocked by conflicts within these views.



# Errors:
#### Recurring plans not set
- ⚠️ Do the exports before migrating prod. Also export the partners once before building staging to generate the external IDs
- Archive current plans
- Export recuring plans from v16
- Import them in v19
- Export subscriptions from v16 including partner IDs
- Import them in v19

#### `ValueError: Cannot convert product.template.product_variant_id to SQL because it is not stored`

# Studio fields:
x_studio_field_AvCGj (account.move) > auto_invoice_id.account_id.name > account_id doesn't exist
x_studio_field_XMwQG (account.move.line) > invoice_id.fiscal_position_id.id > invoice_id doesn't exist (replace by move_id ?)
x_studio_field_RqNgJ > Field doesn't exist at all
x_studio_field_XjDvN (account.move.line) > invoice_id.fiscal_position_id.id > invoice_id doesn't exist (replace by move_id ?)
x_studio_field_lJGkd (account.move.line) > move_id.display_name > No relation issue (display_name may not be stored)
x_studio_field_Yr1ty (helpdesk.ticket) > task_id.timesheet_ids.timesheet_invoice_id.name > task_id field doesn't exist in this model
x_studio_field_lQ1DI (helpdesk.ticket) > task_id.timesheet_ids.timesheet_invoice_id.id > task_id field doesn't exist in this model
x_studio_field_9Gl3k (helpdesk.ticket) > task_id.timesheet_ids.timesheet_invoice_id.name > task_id field doesn't exist in this model
x_studio_field_hfN84 (sale.order) > sale_order_template_id.quote_line.name > quote_line field doesn't exist


[("name", "in", ["x_studio_field_AvCGj", "x_studio_field_XMwQG", "x_studio_field_RqNgJ", "x_studio_field_XjDvN", "x_studio_field_lJGkd", "x_studio_field_Yr1ty", "x_studio_field_lQ1DI", "x_studio_field_9Gl3k", "x_studio_field_hfN84"])]

python3 odoo-bin db load tertraisb ../../../../Downloads/garbage_dl/tertrais-surveillance-staging2-26801019_2026-01-13_070733_test_nofs.zip