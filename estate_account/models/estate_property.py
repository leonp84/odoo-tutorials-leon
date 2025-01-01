from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'name': self.name, 
            "line_ids": [
                Command.create({
                    "name": '6% Sales Commission',
                    "quantity": 1,
                    "price_unit": self.selling_price / 100 * 6,
                }),
                Command.create({
                    "name": 'Administrative Fees',
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ],
        }

        new_invoice = self.env['account.move'].create(invoice_vals)
        print('############')
        print(new_invoice)
        print('############')
        return super().action_sold()