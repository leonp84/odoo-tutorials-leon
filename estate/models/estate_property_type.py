from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type Definition"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Types")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_total_offers")

    sequence = fields.Integer('Sequence', default=1, help="Order Manually")

    _order = "sequence, name"

    _sql_constraints = [
        ('check_type_name_unique', 'UNIQUE(name)', 'Property Type Names must be unique'),
    ]

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)