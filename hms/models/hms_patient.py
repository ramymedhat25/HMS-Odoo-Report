from odoo import models, fields, api, exceptions
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = "Hospital Management System"

    # Patient Personal Information
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name', required=True)
    birth_date = fields.Date('Birth Date')
    age = fields.Integer('Age', compute='_compute_age', store=True)
    history = fields.Html('History')
    image = fields.Binary('Image')
    address = fields.Text('Address')

    # Medical Information
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], 'Blood Type')
    pcr = fields.Boolean('PCR', compute='_compute_pcr', store=True, readonly=False)

    # Hospital Information
    department_id = fields.Many2one('hms.department', string="Department", domain=[('is_opened', '=', True)])
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors", readonly=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], 'State', default='undetermined')
    log_history_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = date.today().year - record.birth_date.year - ((date.today().month, date.today().day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.depends('age')
    def _compute_pcr(self):
        for record in self:
            if record.age < 30:
                record.pcr = True
                return {
                    'warning': {
                        'title': "PCR Check",
                        'message': "PCR has been automatically checked as the patient's age is under 30.",
                    }
                }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(5,)]
            return {'domain': {'doctor_ids': [('id', 'in', self.department_id.doctor_ids.ids)]}}

    @api.onchange('state')
    def _onchange_state(self):
        for record in self:
            self.env['hms.patient.log'].create({
                'patient_id': record.id,
                'description': f"State changed to {record.state}",
            })

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise exceptions.ValidationError('CR ratio must be provided if PCR is checked.')

    @api.model
    def create(self, vals_list):
        record = super(HmsPatient, self).create(vals_list)
        # Optionally, add logic to create an initial log history record upon patient creation
        return record


class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text(string='Description')
