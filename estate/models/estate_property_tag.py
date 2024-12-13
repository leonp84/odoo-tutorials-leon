from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    
    name = fields.Char('Title', required=True)
    color = fields.Integer()

    _order = "name"

    _sql_constraints = [
        ('check_tag_name_unique', 'UNIQUE(name)', 'Tag Names must be unique'),
    ]