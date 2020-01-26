# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class OmdbAbstract(models.AbstractModel):
    _name = 'omdb.abstract'
    _description = "OMDB Abstract"

    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'This data found!'),
    ]
