from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

now = date.today()

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    
    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_dealine", inverse="_inverse_date_deadline")
    status = fields.Selection([('accepted', 'Accepted'), ['refused', 'Refused']])

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "date_deadline")
    def _compute_date_dealine(self):
        for record in self:
            record.date_deadline = now + relativedelta(days=+record.validity)
        
    def _inverse_date_deadline(self):
        for record in self:
            difference = record.date_deadline - date.today()
            record.validity = difference.days