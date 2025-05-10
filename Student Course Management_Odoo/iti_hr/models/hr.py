from odoo import models,fields

class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    military_certificate = fields.Binary()