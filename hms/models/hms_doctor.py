from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = "Doctors"
    _rec_name = 'full_name'

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    patient_ids = fields.Many2many('hms.patient', string="Patients")
    full_name = fields.Char(compute='_compute_full_name', store=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"Dr. {record.first_name}" if record.first_name else ""
