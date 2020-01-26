# -*- coding: utf-8 -*-

from odoo import models

import logging
_logger = logging.getLogger(__name__)


class OmdbApiKeys(models.Model):
    _name = 'omdb.api.key'
    _inherit = ['omdb.abstract', 'omdb.basic.abstract']
    _description = "OMDB Api Key"
