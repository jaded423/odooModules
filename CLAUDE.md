# Odoo Modules Development

Custom Odoo 17 module development for self-hosted instance.

**Server:** VM 101 (Ubuntu Server) @ 192.168.1.126
**Odoo Port:** 8069
**Database:** jaded (PostgreSQL)
**Addons Path:** `/var/lib/docker/volumes/odoo_odoo-addons/_data/`

**Detailed Documentation:** See `docs/` directory:
- **[db-explorer-plan.md](docs/db-explorer-plan.md)** - DB Explorer module development plan
- **[odoo-dev-reference.md](docs/odoo-dev-reference.md)** - Odoo development quick reference

---

## Current Project: DB Explorer

A database exploration and query tool for Odoo - view models, fields, relationships, and run SQL queries.

### Quick Commands

```bash
# SSH to server
ssh ubuntu

# Addons directory
cd /var/lib/docker/volumes/odoo_odoo-addons/_data/

# Create/edit module files (use sudo)
sudo nano db_explorer/__manifest__.py

# Restart Odoo after Python changes
cd ~/odoo && docker compose restart odoo

# View Odoo logs
docker logs -f odoo

# Access Odoo
# URL: http://192.168.1.126:8069
# DB: jaded
```

### Module Location

All custom modules go in:
```
/var/lib/docker/volumes/odoo_odoo-addons/_data/
├── library_app/        # First test module (books)
├── db_explorer/        # Current project
└── [future modules]
```

### Development Workflow

1. **Create/edit files** on server via SSH + sudo
2. **Restart Odoo** for Python changes: `docker compose restart odoo`
3. **Update Apps List** in Odoo UI for new modules
4. **Upgrade module** in Odoo UI for XML/view changes

---

## Installed OCA Modules

| Module | Purpose |
|--------|---------|
| mis_builder | Financial report builder |
| account_financial_report | Balance Sheet, P&L, Ledgers |
| report_xlsx | Excel export support |
| date_range | Date range picker |
| web_responsive | App drawer grid menu |

---

## Odoo Credentials

**Web Login:**
- Email: jaded423@gmail.com
- Password: [stored securely]

**XML-RPC API:**
```python
import xmlrpc.client
url = "http://localhost:8069"
db = "jaded"
username = "jaded423@gmail.com"
# Use API for bulk data operations
```

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-06 | Project created, DB Explorer planning started |
| 2026-01-06 | Installed OCA accounting modules (mis_builder, account_financial_report) |
| 2026-01-06 | Installed web_responsive for app drawer grid menu |
| 2026-01-06 | Created library_app as first learning module |
| 2026-01-06 | Set up Odoo 17 on VM 101 with Docker |
