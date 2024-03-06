from odoo import models, fields


class HmsLog(models.Model):
    _name = 'hms.log'
    _description = 'Patient Log'

    created_by = fields.Many2one('res.users', string="Created by", default=lambda self: self.env.uid)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    patient_id = fields.Many2one('hms.patient', string="Patient")
