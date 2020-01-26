# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class OmdbSearchWizard(models.TransientModel):
    _name = 'omdb.search.wizard'
    _inherit=['omdb.basic.abstract']
    _description = "OMDB Search Wizard"

    name = fields.Char(string="Title", required=True)
    year = fields.Integer(string="Year")
    season = fields.Integer(string="Season")
    episode = fields.Integer(string="Episode")
    api_key = fields.Many2one('omdb.api.key', string="Api Key", required=True)

    @api.multi
    @api.onchange('api_key')
    def _onchange_api_key(self):
        for rec in self:
            if rec.api_key:
                rec.type_id = rec.api_key.type_id
                rec.returned_value = rec.api_key.returned_value
                rec.pages = rec.api_key.pages
                rec.fullplot = rec.api_key.fullplot
                rec.tomatoes = rec.api_key.tomatoes
                rec.timeout = rec.api_key.timeout

    def _get_omdb_data(self):
        for rec in self:
            # Get OMDB Data
            try:
                from omdb import OMDBClient
                client = OMDBClient(apikey=rec.api_key.name)
                items = []
                if client:
                    for i in range(1, rec.pages+1):
                        page_items = client.get(
                            media_type=rec.type_id.name, 
                            search=rec.name, 
                            year=rec.year if rec.year else None, 
                            season=rec.season if rec.season else None, 
                            episode=rec.episode if rec.episode else None, 
                            fullplot=rec.fullplot, 
                            tomatoes=rec.tomatoes, 
                            timeout=rec.timeout,
                            page=i)
                        if page_items:
                            items += page_items
                return items
            except:
                raise UserError("There are Issue When Connect With OMDB Api and Get Data.")

    def _create_product(self, title, year):
        # Create Products
        product_id = self.env['product.product'].create({
            'name': "%s [%s]" % (title, year),
        })
        return product_id if product_id else False

    def _create_purchase_order(self, product_ids):
        # Create Purchase Order
        purchase_order_id = self.env['purchase.order'].create({
            'partner_id': self.env.ref('omdb_connector.omdb_partner_1').id,
            'order_line': [(0, 0, {
                'product_id': product.id, 
                'name': product.name, 
                'product_qty': 1, 
                'price_unit': 10, 
                'date_planned': fields.Datetime.now(), 
                'product_uom': product.uom_id.id, 
            }) for product in product_ids],
        })
        purchase_order_id.button_confirm()
        return purchase_order_id if purchase_order_id else False

    def _create_invoice(self, purchase_order_id):
        if purchase_order_id:
            # Create Invoice
            self.env['account.invoice'].create({
                'purchase_id': purchase_order_id.id,
                'partner_id': purchase_order_id.partner_id.id,
                'type': 'in_invoice',
                'origin': purchase_order_id.name,
                'invoice_line_ids': [(0, 0, {
                    'product_id': line.product_id.id, 
                    'name': line.product_id.name, 
                    'quantity': line.product_qty, 
                    'price_unit': line.price_unit, 
                    'account_id': purchase_order_id.partner_id.property_account_payable_id.id,
            }) for line in purchase_order_id.order_line],
        })

    @api.multi
    def action_get_data(self):
        for rec in self:
            omdb_data = rec._get_omdb_data()
            if omdb_data:
                product_ids = [rec._create_product(item['title'], item['year']) for item in omdb_data]
                if product_ids:
                    purchase_order_id = rec._create_purchase_order(product_ids)
                    if purchase_order_id:
                        rec._create_invoice(purchase_order_id)
            else:
                raise UserError("There are Not Data for Selected Title.")


