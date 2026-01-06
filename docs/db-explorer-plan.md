# DB Explorer Module - Development Plan

A database exploration and SQL query tool for Odoo 17 Community Edition.

---

## Overview

**Purpose:** Give users easy access to view Odoo's data structure and run queries without needing direct database access.

**Key Features:**
- Browse all Odoo models (tables) with search
- View fields, types, and relationships for any model
- Run read-only SQL queries
- Save and reuse favorite queries
- Export results to CSV

---

## Development Phases

### Phase 1: Model Browser (Start Here)

**Goal:** List all models, click to see fields

**Files to create:**
```
db_explorer/
├── __manifest__.py      # Module metadata
├── __init__.py          # Python package init
├── models/
│   ├── __init__.py
│   └── model_browser.py # Transient model for browsing
├── views/
│   └── model_browser_views.xml  # UI views
└── security/
    └── ir.model.access.csv      # Permissions
```

**What you'll learn:**
- Module structure and manifest
- Transient models (temporary data, not saved to DB)
- Using Odoo's ir.model and ir.model.fields
- Form and tree views
- Computed fields

---

### Phase 2: SQL Query Runner

**Goal:** Execute custom SQL queries, display results

**Additional files:**
```
db_explorer/
├── models/
│   └── sql_query.py     # Model to store saved queries
├── wizard/
│   ├── __init__.py
│   └── query_wizard.py  # Wizard to run queries
└── views/
    ├── sql_query_views.xml
    └── query_wizard_views.xml
```

**What you'll learn:**
- Wizards (popup dialogs)
- Executing raw SQL safely
- Dynamic table rendering
- Security considerations

---

### Phase 3: Enhancements

**Goal:** Polish and add useful features

**Features:**
- Export results to CSV/Excel
- Query templates for common tasks
- Field relationship diagram (Many2one, One2many visualization)
- Query history
- Syntax highlighting for SQL

---

## Phase 1 Implementation Guide

### File 1: `__manifest__.py`

The module's "ID card" - tells Odoo about your module.

```python
{
    "name": "DB Explorer",
    "version": "17.0.1.0.0",
    "summary": "Browse database models and fields",
    "description": """
        Database Explorer for Odoo
        ==========================
        - View all models/tables
        - Explore fields and relationships
        - Run SQL queries (Phase 2)
    """,
    "author": "Joshua",
    "category": "Technical",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/model_browser_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
```

**Key fields explained:**
- `depends`: Other modules this requires (base = core Odoo)
- `data`: Files loaded in order (security first!)
- `application`: True = shows in app drawer with icon

---

### File 2: `__init__.py` (root)

```python
from . import models
```

Just imports the models folder.

---

### File 3: `models/__init__.py`

```python
from . import model_browser
```

Imports each model file.

---

### File 4: `models/model_browser.py`

The main Python logic.

```python
from odoo import models, fields, api


class ModelBrowser(models.TransientModel):
    """Transient model for browsing database structure."""

    _name = "db.explorer.browser"
    _description = "Database Model Browser"

    # Selection field - user picks a model
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        domain=[("transient", "=", False)],  # Exclude temp models
        help="Select a model to explore its fields",
    )

    # Related fields - auto-filled from selected model
    model_name = fields.Char(
        related="model_id.model",
        string="Technical Name",
    )
    model_description = fields.Char(
        related="model_id.name",
        string="Description",
    )
    record_count = fields.Integer(
        string="Record Count",
        compute="_compute_record_count",
    )

    # One2many - shows all fields for selected model
    field_ids = fields.One2many(
        "ir.model.fields",
        compute="_compute_field_ids",
        string="Fields",
    )

    @api.depends("model_id")
    def _compute_record_count(self):
        """Count records in selected model."""
        for record in self:
            if record.model_id and record.model_name:
                try:
                    count = self.env[record.model_name].search_count([])
                    record.record_count = count
                except Exception:
                    record.record_count = 0
            else:
                record.record_count = 0

    @api.depends("model_id")
    def _compute_field_ids(self):
        """Get all fields for selected model."""
        for record in self:
            if record.model_id:
                record.field_ids = record.model_id.field_id
            else:
                record.field_ids = False
```

**Key concepts:**
- `TransientModel`: Temporary data, auto-deleted (good for tools/wizards)
- `Many2one`: Link to another model (dropdown)
- `One2many`: Show related records (list of fields)
- `@api.depends`: Recompute when dependency changes
- `self.env[model_name]`: Access any model dynamically

---

### File 5: `views/model_browser_views.xml`

The user interface.

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Form View -->
    <record id="db_explorer_browser_form" model="ir.ui.view">
        <field name="name">db.explorer.browser.form</field>
        <field name="model">db.explorer.browser</field>
        <field name="arch" type="xml">
            <form string="Database Explorer">
                <sheet>
                    <group>
                        <group string="Select Model">
                            <field name="model_id" options="{'no_create': True}"/>
                            <field name="model_name"/>
                            <field name="record_count"/>
                        </group>
                        <group string="Model Info">
                            <field name="model_description"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Fields" name="fields">
                            <field name="field_ids" readonly="1">
                                <tree>
                                    <field name="name" string="Technical Name"/>
                                    <field name="field_description" string="Label"/>
                                    <field name="ttype" string="Type"/>
                                    <field name="relation" string="Related Model"/>
                                    <field name="required"/>
                                    <field name="store" string="Stored"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="db_explorer_browser_action" model="ir.actions.act_window">
        <field name="name">Model Browser</field>
        <field name="res_model">db.explorer.browser</field>
        <field name="view_mode">form</field>
        <field name="target">current</field>
    </record>

    <!-- Menu -->
    <menuitem id="db_explorer_menu_root"
              name="DB Explorer"
              sequence="100"/>

    <menuitem id="db_explorer_menu_browser"
              name="Model Browser"
              parent="db_explorer_menu_root"
              action="db_explorer_browser_action"
              sequence="10"/>
</odoo>
```

**Key concepts:**
- `<form>`: Main editing view
- `<group>`: Organizes fields in columns
- `<notebook>/<page>`: Tabbed sections
- `<tree>`: List/table display (inside One2many)
- `options="{'no_create': True}"`: Disable creating new records from dropdown

---

### File 6: `security/ir.model.access.csv`

Permissions - who can use this.

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_db_explorer_browser,db.explorer.browser.user,model_db_explorer_browser,base.group_user,1,1,1,1
```

**Columns:**
- `id`: Unique identifier
- `model_id:id`: The model (use `model_` + technical name with dots→underscores)
- `group_id:id`: Who gets access (base.group_user = all employees)
- `perm_*`: Read/Write/Create/Delete permissions

---

## Step-by-Step Commands

### Create the module structure:
```bash
ssh ubuntu "sudo mkdir -p /var/lib/docker/volumes/odoo_odoo-addons/_data/db_explorer/{models,views,security}"
```

### Create each file:
```bash
# Example - create __manifest__.py
ssh ubuntu "sudo nano /var/lib/docker/volumes/odoo_odoo-addons/_data/db_explorer/__manifest__.py"
# Paste content, save with Ctrl+O, exit with Ctrl+X
```

### After creating all files:
```bash
# Restart Odoo
ssh ubuntu "cd ~/odoo && docker compose restart odoo"

# Then in Odoo UI:
# 1. Apps → Update Apps List
# 2. Search "DB Explorer" (remove Apps filter)
# 3. Install
```

---

## Testing Checklist

### Phase 1 Complete When:
- [ ] Module installs without errors
- [ ] "DB Explorer" appears in app drawer
- [ ] Can select any model from dropdown
- [ ] Fields list populates when model selected
- [ ] Record count shows correctly
- [ ] Field types and relations display properly

---

## Phase 2 Preview: SQL Query Runner

Will add:
- Text area for SQL input
- Execute button (read-only queries only)
- Results displayed in dynamic table
- Save query with name for reuse
- Safety: Only SELECT allowed, no INSERT/UPDATE/DELETE

---

## Resources

- [Odoo 17 Developer Docs](https://www.odoo.com/documentation/17.0/developer.html)
- [ORM API Reference](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
- [View Architecture](https://www.odoo.com/documentation/17.0/developer/reference/backend/views.html)
- [QWeb Templates](https://www.odoo.com/documentation/17.0/developer/reference/frontend/qweb.html)
