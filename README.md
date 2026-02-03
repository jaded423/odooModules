# Odoo Modules

Production-ready modules for Odoo 17.

## Modules

### global_search

Google-style global search across multiple models from the systray.

**Features:**
- Search across 7 models from one search box
- Real-time results as you type
- Click to navigate directly to the record
- Clean, modern UI

**Searchable Models:**
| Model | Searches By |
|-------|-------------|
| Contacts | name, email, phone |
| Invoices / Bills | name, reference, partner |
| Products | name, SKU |
| Product Variants | name, SKU, barcode |
| Sale Orders | name, customer |
| Purchase Orders | name, vendor |
| Manufacturing Orders | name, product |

**Installation:**
1. Copy `global_search/` to your Odoo addons directory
2. Restart Odoo
3. Go to Apps → Update Apps List
4. Search for "Global Search" and install

**Requirements:**
- Odoo 17.0
- Depends on: `base`, `web`
- Optional: `sale`, `purchase`, `mrp` (for respective search features)

## License

MIT License - see [LICENSE](LICENSE)
