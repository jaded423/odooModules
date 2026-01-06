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

**Status:** Phase 1 & 2 complete, fully functional

**Features:**
- Model Browser - Browse all Odoo models, view fields, types, relationships
- All Models list - Searchable/filterable model directory
- SQL Query Runner - Execute read-only SQL queries with results table
- Saved Queries - Store and organize favorite queries by category
- CSV Export - Export field lists and query results

**Module Structure (on server):**
```
/var/lib/docker/volumes/odoo_odoo-addons/_data/db_explorer/
├── __manifest__.py          # Module metadata (v17.0.2.0.0)
├── __init__.py              # Root imports
├── models/
│   ├── __init__.py
│   ├── model_browser.py     # Model Browser transient model
│   └── sql_query.py         # Saved Queries model
├── wizard/
│   ├── __init__.py
│   └── query_wizard.py      # SQL Query Runner wizard
├── views/
│   ├── model_browser_views.xml
│   ├── sql_query_views.xml
│   └── query_wizard_views.xml
├── security/
│   └── ir.model.access.csv
└── static/description/
    └── icon.png             # Purple database icon
```

### Quick Commands

```bash
# SSH to server
ssh ubuntu

# Addons directory
cd /var/lib/docker/volumes/odoo_odoo-addons/_data/

# Create/edit module files (use sudo)
sudo nvim db_explorer/__manifest__.py

# Restart Odoo (alias on server)
odooUp

# View Odoo logs (alias on server)
odooLogs

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
| 2026-01-06 | **DB Explorer Phase 2 complete** - SQL Query Runner with saved queries, execute button, results table, CSV export |
| 2026-01-06 | **DB Explorer Phase 1 enhanced** - Added search/filter, CSV export, app icon, styling, relationships tab |
| 2026-01-06 | **DB Explorer Phase 1 complete** - Model Browser with field list, record counts, working UI |
| 2026-01-06 | Created server aliases: `odooUp` (restart), `odooLogs` (view logs) |
| 2026-01-06 | Project created, DB Explorer planning started |
| 2026-01-06 | Installed OCA accounting modules (mis_builder, account_financial_report) |
| 2026-01-06 | Installed web_responsive for app drawer grid menu |
| 2026-01-06 | Created library_app as first learning module |
| 2026-01-06 | Set up Odoo 17 on VM 101 with Docker |
