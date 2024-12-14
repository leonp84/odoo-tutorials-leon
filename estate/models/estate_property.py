from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

now = datetime.now()
new_date = now + relativedelta(months=+3)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The way to get flippen ryk"
    
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], default='new', string='Status', required=True)

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=new_date)
    expected_price = fields.Float(required=True)
    best_price = fields.Float(compute="_compute_best_price")
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ['south', 'South'],['east', 'East'],['west', 'West']])

    _order = "id desc"

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'Expected Price must be 0 or larger'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling Price must be 0 or larger'),
    ]

    total_area = fields.Integer(compute="_compute_total_area")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string='Buyer')
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError("A sold property cannot be cancelled.")
        return True
    
    def action_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError("A cancelled property cannot be sold.")
        return True

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        prices = []
        for record in self:
            for item in record.offer_ids:
                prices.append(item.price)
            record.best_price = max(prices) if prices else 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    @api.constrains('selling_price')
    def _check_selling_price_lowest(self):
        if self.selling_price != 0:
            if self.selling_price < (self.expected_price / 100 * 90):
                raise ValidationError('The Selling Price cannot be 90% lower than the expected price')

    @api.ondelete(at_uninstall=False)
    def cant_do_that(self):
        for record in self:
            if record.garden:
                 raise ValidationError('You can not delete a property with a garden! How cruel ;(')
