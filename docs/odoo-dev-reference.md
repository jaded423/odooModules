# Odoo 17 Development Quick Reference

## Field Types

| Type | Description | Example |
|------|-------------|---------|
| `Char` | Short text | `name = fields.Char(string="Name", required=True)` |
| `Text` | Long text | `description = fields.Text()` |
| `Html` | Rich text HTML | `notes = fields.Html()` |
| `Integer` | Whole number | `quantity = fields.Integer(default=1)` |
| `Float` | Decimal number | `price = fields.Float(digits=(10, 2))` |
| `Boolean` | True/False | `active = fields.Boolean(default=True)` |
| `Date` | Date only | `date = fields.Date(default=fields.Date.today)` |
| `Datetime` | Date + time | `created = fields.Datetime(default=fields.Datetime.now)` |
| `Selection` | Dropdown | `state = fields.Selection([('draft','Draft'),('done','Done')])` |
| `Many2one` | Link to 1 record | `partner_id = fields.Many2one('res.partner')` |
| `One2many` | Link to many records | `line_ids = fields.One2many('model', 'parent_id')` |
| `Many2many` | Many-to-many | `tag_ids = fields.Many2many('tags.model')` |
| `Binary` | File/image | `image = fields.Binary()` |

## Common Field Attributes

```python
fields.Char(
    string="Display Label",      # UI label
    required=True,               # Cannot be empty
    readonly=True,               # Cannot edit
    default="value",             # Default value
    help="Tooltip text",         # Help text
    index=True,                  # Database index
    copy=False,                  # Don't copy when duplicating
    groups="base.group_user",    # Visibility restriction
)
```

## Decorators

```python
@api.depends('field1', 'field2')  # Recompute when these change
def _compute_total(self):
    for rec in self:
        rec.total = rec.field1 + rec.field2

@api.onchange('field1')           # UI-only, trigger on change
def _onchange_field1(self):
    if self.field1:
        self.field2 = self.field1 * 2

@api.constrains('field1')         # Validation
def _check_field1(self):
    if self.field1 < 0:
        raise ValidationError("Must be positive!")

@api.model                        # Class method (no self records)
def my_method(self):
    pass
```

## Model Types

```python
# Regular model - stored in database
class MyModel(models.Model):
    _name = "my.model"

# Transient model - temporary, auto-deleted
class MyWizard(models.TransientModel):
    _name = "my.wizard"

# Abstract model - inherited, no table
class MyMixin(models.AbstractModel):
    _name = "my.mixin"
```

## Inheritance

```python
# Add fields to existing model
class ResPartner(models.Model):
    _inherit = "res.partner"
    custom_field = fields.Char()

# Create new model based on existing
class MyPartner(models.Model):
    _name = "my.partner"
    _inherit = "res.partner"
```

## ORM Methods

```python
# Search
records = self.env['model'].search([('field', '=', value)])
records = self.env['model'].search([], limit=10, order='name')
count = self.env['model'].search_count([])

# Read
record = self.env['model'].browse(id)
records = self.env['model'].browse([1, 2, 3])

# Create
new = self.env['model'].create({'field': 'value'})

# Write
record.write({'field': 'new_value'})

# Delete
record.unlink()

# Filtered
active = records.filtered(lambda r: r.active)
active = records.filtered('active')

# Mapped
names = records.mapped('name')
partners = records.mapped('partner_id')

# Sorted
sorted_recs = records.sorted('name')
sorted_recs = records.sorted(lambda r: r.sequence)
```

## Search Domains

```python
[('field', '=', value)]           # Equals
[('field', '!=', value)]          # Not equals
[('field', '>', value)]           # Greater than
[('field', '>=', value)]          # Greater or equal
[('field', '<', value)]           # Less than
[('field', '<=', value)]          # Less or equal
[('field', 'in', [1, 2, 3])]      # In list
[('field', 'not in', [1, 2])]     # Not in list
[('field', 'like', '%text%')]     # SQL LIKE
[('field', 'ilike', '%text%')]    # Case-insensitive LIKE
[('field', '=like', 'text%')]     # Starts with
[('field', '=', False)]           # Is not set
[('field', '!=', False)]          # Is set

# Combining
['&', ('a', '=', 1), ('b', '=', 2)]    # AND (default)
['|', ('a', '=', 1), ('b', '=', 2)]    # OR
['!', ('a', '=', 1)]                    # NOT
```

## View Types

### Form View
```xml
<form>
    <header>
        <field name="state" widget="statusbar"/>
    </header>
    <sheet>
        <group>
            <field name="name"/>
        </group>
        <notebook>
            <page string="Details">
                <field name="description"/>
            </page>
        </notebook>
    </sheet>
</form>
```

### Tree/List View
```xml
<tree>
    <field name="name"/>
    <field name="state" widget="badge"/>
    <field name="amount" sum="Total"/>
</tree>
```

### Search View
```xml
<search>
    <field name="name"/>
    <filter string="Active" domain="[('active','=',True)]"/>
    <group expand="0" string="Group By">
        <filter string="State" context="{'group_by':'state'}"/>
    </group>
</search>
```

## Common Widgets

| Widget | Field Type | Description |
|--------|-----------|-------------|
| `statusbar` | Selection | Progress bar |
| `badge` | Selection/Char | Colored badge |
| `priority` | Selection | Star rating |
| `many2many_tags` | Many2many | Tag chips |
| `image` | Binary | Image display |
| `monetary` | Float | Currency format |
| `date` | Date | Date picker |
| `float_time` | Float | Hours:minutes |
| `progressbar` | Integer/Float | Progress bar |
| `handle` | Integer | Drag handle for ordering |

## Execute Raw SQL

```python
# Read-only query
self.env.cr.execute("SELECT id, name FROM res_partner LIMIT 10")
results = self.env.cr.fetchall()  # List of tuples
results = self.env.cr.dictfetchall()  # List of dicts

# With parameters (safe from injection)
self.env.cr.execute(
    "SELECT * FROM res_partner WHERE id = %s",
    (partner_id,)
)
```

## Useful self.env Attributes

```python
self.env.user          # Current user
self.env.company       # Current company
self.env.uid           # Current user ID
self.env.context       # Context dict
self.env.cr            # Database cursor
self.env.ref('xml_id') # Get record by XML ID
```

## Module Structure

```
my_module/
├── __manifest__.py       # Module metadata
├── __init__.py           # Import models
├── models/
│   ├── __init__.py       # Import model files
│   └── my_model.py       # Model definitions
├── views/
│   └── my_model_views.xml
├── security/
│   └── ir.model.access.csv
├── data/                 # Default data
├── demo/                 # Demo data
├── wizard/               # Transient models
├── report/               # Report templates
└── static/
    ├── description/
    │   └── icon.png      # App icon (128x128)
    └── src/
        ├── js/           # JavaScript
        ├── css/          # Stylesheets
        └── xml/          # QWeb templates
```
