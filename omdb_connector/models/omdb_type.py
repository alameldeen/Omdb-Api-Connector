# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class OmdbType(models.Model):
    _name = 'omdb.type'
    _inherit = ['omdb.abstract']
    _description = "OMDB Type"
