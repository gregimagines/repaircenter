# -*- coding: utf-8 -*-
from odoo import http

# class Repaircenter(http.Controller):
#     @http.route('/repaircenter/repaircenter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/repaircenter/repaircenter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('repaircenter.listing', {
#             'root': '/repaircenter/repaircenter',
#             'objects': http.request.env['repaircenter.repaircenter'].search([]),
#         })

#     @http.route('/repaircenter/repaircenter/objects/<model("repaircenter.repaircenter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('repaircenter.object', {
#             'object': obj
#         })