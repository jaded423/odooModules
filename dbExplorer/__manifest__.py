{
  "name": "DB Explorer",
  "version": "17.0.2.0.0",
  "summary": "Browse database models and run SQL queries",
  "description": """
      Database Explorer for Odoo
      ==========================
      - View all models/tables
      - Explore fields and relationships
      - Run SQL queries (read-only)
      - Save favorite queries
      - Export results to CSV
  """,
  "author": "Joshua",
  "category": "Technical",
  "license": "LGPL-3",
  "depends": ["base"],
  "data": [
      "security/ir.model.access.csv",
      "views/model_browser_views.xml",
      "views/sql_query_views.xml",
      "views/query_wizard_views.xml",
  ],
  "installable": True,
  "application": True,
  "auto_install": False,
}
