# -*- coding: utf-8 -*-

from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)


class OmdbBasicAbstract(models.AbstractModel):
    _name = 'omdb.basic.abstract'
    _description = "OMDB Basic Abstract"

    RETURNED_VALUE = [
        ('json', 'json'),
        ('xml', 'xml'),
    ]

    type_id = fields.Many2one('omdb.type', string='Type', required=True)
    returned_value = fields.Selection(RETURNED_VALUE, string='Returned Value', default='json', required=True)
    pages = fields.Integer(string="Pages", required=True, default=1)
    fullplot = fields.Boolean(string='Fullplot', default=True)
    tomatoes = fields.Boolean(string='Tomatoes', default=True)
    timeout = fields.Integer(string="TimeOut", required=True, default=5)
