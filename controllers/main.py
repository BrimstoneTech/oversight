# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class OversightPortal(http.Controller):

    @http.route(['/my/oversight'], type='http', auth='user', website=True)
    def portal_my_oversight(self, **kw):
        """
        Renders the OVERSIGHT performance dashboard for the logged-in user.
        If the user is an employee, their KPI metrics are passed to the template.
        """
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        
        values = {
            'employee': employee,
            'page_name': 'oversight_dashboard',
        }
        
        return request.render("oversight_module.portal_oversight_dashboard", values)
