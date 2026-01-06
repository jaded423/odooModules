import base64
import csv
import io
import re
from odoo import models, fields, api
from odoo.exceptions import UserError


class QueryWizard(models.TransientModel):
  """Wizard to execute SQL queries."""

  _name = "db.explorer.query.wizard"
  _description = "SQL Query Runner"

  saved_query_id = fields.Many2one(
      "db.explorer.query",
      string="Saved Query",
      help="Select a saved query or write your own below",
  )
  query = fields.Text(
      string="SQL Query",
      required=True,
      default="SELECT id, name FROM res_partner LIMIT 10",
  )
  result_html = fields.Html(
      string="Results",
      readonly=True,
      sanitize=False,
  )
  row_count = fields.Integer(string="Rows Returned", readonly=True)
  execution_time = fields.Float(string="Execution Time (s)", readonly=True)
  has_results = fields.Boolean(compute="_compute_has_results")

  # Export
  export_file = fields.Binary(string="Export File", readonly=True)
  export_filename = fields.Char(string="Filename", readonly=True)

  @api.depends("result_html")
  def _compute_has_results(self):
      for record in self:
          record.has_results = bool(record.result_html)

  @api.onchange("saved_query_id")
  def _onchange_saved_query(self):
      if self.saved_query_id:
          self.query = self.saved_query_id.query

  def _validate_query(self, query):
      """Validate query is safe to run."""
      if not query or not query.strip():
          raise UserError("Please enter a SQL query.")

      normalized = query.strip().upper()

      # Block dangerous operations
      dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
                  "TRUNCATE", "CREATE", "GRANT", "REVOKE", "COMMIT", "ROLLBACK"]
      for keyword in dangerous:
          if re.search(rf'\b{keyword}\b', normalized):
              raise UserError(
                  f"Unsafe SQL: {keyword} statements are not allowed.\n"
                  "Only SELECT queries are permitted."
              )

      # Must be a SELECT or WITH
      if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
          raise UserError(
              "Query must start with SELECT or WITH.\n"
              "Only read-only queries are permitted."
          )

      return True

  def action_execute(self):
      """Execute the SQL query and display results."""
      self.ensure_one()
      self._validate_query(self.query)

      import time
      start_time = time.time()

      try:
          # Execute query
          self.env.cr.execute(self.query)
          columns = [desc[0] for desc in self.env.cr.description]
          rows = self.env.cr.fetchall()

          execution_time = time.time() - start_time

          # Build HTML table
          html = self._build_html_table(columns, rows)

          # Update record
          self.write({
              "result_html": html,
              "row_count": len(rows),
              "execution_time": round(execution_time, 4),
          })

          # Update saved query stats if using one
          if self.saved_query_id:
              self.saved_query_id.sudo().write({
                  "last_run": fields.Datetime.now(),
                  "run_count": self.saved_query_id.run_count + 1,
              })

      except Exception as e:
          raise UserError(f"Query Error:\n{str(e)}")

      # Keep wizard open with results
      return {
          "type": "ir.actions.act_window",
          "res_model": self._name,
          "res_id": self.id,
          "view_mode": "form",
          "target": "new",
      }

  def _build_html_table(self, columns, rows):
      """Build an HTML table from query results."""
      if not rows:
          return "<p class='text-muted'>Query returned no results.</p>"

      html = """
      <div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">
      <table class="table table-sm table-striped table-hover" style="font-size: 12px;">
      <thead class="thead-dark" style="position: sticky; top: 0;">
      <tr>
      """

      # Header
      for col in columns:
          html += f"<th style='background: #875A7B; color: white; padding: 8px;'>{col}</th>"
      html += "</tr></thead><tbody>"

      # Rows (limit display to 500 for performance)
      for row in rows[:500]:
          html += "<tr>"
          for cell in row:
              # Truncate long values
              display = str(cell) if cell is not None else ""
              if len(display) > 100:
                  display = display[:100] + "..."
              html += f"<td style='padding: 6px; max-width: 300px; overflow: hidden; text-overflow: ellipsis;'>{display}</td>"
          html += "</tr>"

      html += "</tbody></table></div>"

      if len(rows) > 500:
          html += f"<p class='text-warning'>Showing first 500 of {len(rows)} rows.</p>"

      return html

  def action_export_csv(self):
      """Export results to CSV."""
      self.ensure_one()
      if not self.query:
          raise UserError("No query to export.")

      self._validate_query(self.query)

      try:
          self.env.cr.execute(self.query)
          columns = [desc[0] for desc in self.env.cr.description]
          rows = self.env.cr.fetchall()
      except Exception as e:
          raise UserError(f"Query Error:\n{str(e)}")

      # Build CSV
      output = io.StringIO()
      writer = csv.writer(output)
      writer.writerow(columns)
      writer.writerows(rows)

      # Encode
      csv_data = output.getvalue().encode("utf-8")
      self.export_file = base64.b64encode(csv_data)
      self.export_filename = "query_results.csv"

      return {
          "type": "ir.actions.act_url",
          "url": f"/web/content?model={self._name}&id={self.id}"
                 f"&field=export_file&filename_field=export_filename"
                 f"&download=true",
          "target": "new",
      }

  def action_save_query(self):
      """Save current query for reuse."""
      self.ensure_one()
      if not self.query:
          raise UserError("No query to save.")

      self._validate_query(self.query)

      return {
          "name": "Save Query",
          "type": "ir.actions.act_window",
          "res_model": "db.explorer.query",
          "view_mode": "form",
          "target": "new",
          "context": {
              "default_query": self.query,
              "default_name": "New Query",
          },
      }
