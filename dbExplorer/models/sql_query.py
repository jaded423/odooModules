from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class SqlQuery(models.Model):
  """Stored SQL queries for reuse."""

  _name = "db.explorer.query"
  _description = "Saved SQL Query"
  _order = "sequence, name"

  name = fields.Char(string="Query Name", required=True)
  description = fields.Text(string="Description")
  query = fields.Text(string="SQL Query", required=True)
  sequence = fields.Integer(string="Sequence", default=10)
  category = fields.Selection([
      ("accounting", "Accounting"),
      ("inventory", "Inventory"),
      ("sales", "Sales"),
      ("purchase", "Purchases"),
      ("hr", "HR"),
      ("other", "Other"),
  ], string="Category", default="other")
  active = fields.Boolean(default=True)
  last_run = fields.Datetime(string="Last Run", readonly=True)
  run_count = fields.Integer(string="Run Count", readonly=True, default=0)

  @api.constrains("query")
  def _check_query_safety(self):
      """Ensure only SELECT queries are saved."""
      for record in self:
          if record.query:
              normalized = record.query.strip().upper()
              # Check for dangerous keywords
              dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
                         "TRUNCATE", "CREATE", "GRANT", "REVOKE"]
              for keyword in dangerous:
                  if re.search(rf'\b{keyword}\b', normalized):
                      raise UserError(
                          f"Unsafe SQL: {keyword} statements are not allowed.\n"
                          "Only SELECT queries are permitted."
                      )
              # Must start with SELECT or WITH (for CTEs)
              if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
                  raise UserError(
                      "Query must start with SELECT or WITH.\n"
                      "Only read-only queries are permitted."
                  )

  def action_run_query(self):
      """Open wizard to run this query."""
      self.ensure_one()
      return {
          "name": f"Run: {self.name}",
          "type": "ir.actions.act_window",
          "res_model": "db.explorer.query.wizard",
          "view_mode": "form",
          "target": "new",
          "context": {
              "default_saved_query_id": self.id,
              "default_query": self.query,
          },
      }
