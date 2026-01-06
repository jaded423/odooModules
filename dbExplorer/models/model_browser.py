import base64
import csv
import io
from odoo import models, fields, api


class ModelBrowser(models.TransientModel):
  """Transient model for browsing database structure."""

  _name = "db.explorer.browser"
  _description = "Database Model Browser"

  model_id = fields.Many2one(
      "ir.model",
      string="Model",
      domain=[("transient", "=", False)],
      help="Select a model to explore its fields",
  )

  model_name = fields.Char(
      related="model_id.model",
      string="Technical Name",
  )
  model_description = fields.Char(
      related="model_id.name",
      string="Description",
  )
  record_count = fields.Integer(
      string="Records",
      compute="_compute_record_count",
  )
  field_count = fields.Integer(
      string="Fields",
      compute="_compute_field_count",
  )

  field_ids = fields.One2many(
      "ir.model.fields",
      compute="_compute_field_ids",
      string="Fields",
  )
  relation_field_ids = fields.One2many(
      "ir.model.fields",
      compute="_compute_relation_field_ids",
      string="Relationship Fields",
  )

  # Export fields
  export_file = fields.Binary(string="Export File", readonly=True)
  export_filename = fields.Char(string="Filename", readonly=True)

  @api.depends("model_id")
  def _compute_record_count(self):
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
  def _compute_field_count(self):
      for record in self:
          if record.model_id:
              record.field_count = len(record.model_id.field_id)
          else:
              record.field_count = 0

  @api.depends("model_id")
  def _compute_field_ids(self):
      for record in self:
          if record.model_id:
              record.field_ids = record.model_id.field_id
          else:
              record.field_ids = False

  @api.depends("model_id")
  def _compute_relation_field_ids(self):
      for record in self:
          if record.model_id:
              relation_types = ("many2one", "one2many", "many2many")
              record.relation_field_ids = record.model_id.field_id.filtered(
                  lambda f: f.ttype in relation_types
              )
          else:
              record.relation_field_ids = False

  def action_export_csv(self):
      """Export field list to CSV file."""
      self.ensure_one()
      if not self.model_id:
          return

      # Create CSV in memory
      output = io.StringIO()
      writer = csv.writer(output)

      # Header row
      writer.writerow([
          "Technical Name",
          "Label",
          "Type",
          "Related Model",
          "Required",
          "Stored",
          "Help Text",
      ])

      # Data rows
      for field in self.field_ids:
          writer.writerow([
              field.name,
              field.field_description,
              field.ttype,
              field.relation or "",
              "Yes" if field.required else "No",
              "Yes" if field.store else "No",
              field.help or "",
          ])

      # Encode to base64
      csv_data = output.getvalue().encode("utf-8")
      self.export_file = base64.b64encode(csv_data)
      self.export_filename = f"{self.model_name}_fields.csv"

      # Return download action
      return {
          "type": "ir.actions.act_url",
          "url": f"/web/content?model={self._name}&id={self.id}"
                 f"&field=export_file&filename_field=export_filename"
                 f"&download=true",
          "target": "new",
      }
