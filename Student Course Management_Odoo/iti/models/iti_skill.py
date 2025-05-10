from odoo import models, fields

class ItiSkill(models.Model):
    _name = "iti.skill"

    name = fields.Char()