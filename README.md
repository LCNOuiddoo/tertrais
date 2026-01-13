# tertrais Odoov16

Upgrade process:
- Import `res.partner.title (res.partner.title).csv`
- Import `Contact (res.partner).csv`
- Uninstall `sale_project_tertrais`, test if the sales are linked to project properly. If yes, remove it from the repo.
- Deactivate the view `access_restriction_by_ip.res_users_allowed_ips`
- Remove the `res_user.allowed_ips` field
- Re-push code
