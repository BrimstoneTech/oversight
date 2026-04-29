# -*- coding: utf-8 -*-
# OVERSIGHT Module — Employee Performance Dashboard Fields
# Adds real-time performance metrics to hr.employee by aggregating data from
# their most recent confirmed timesheets. These fields power the employee
# "Performance" smart-button and dashboard views.

from odoo import models, fields, api
import datetime
import logging

_logger = logging.getLogger(__name__)


class HrEmployeeOversight(models.Model):
    """
    Extend hr.employee with live performance KPIs derived from timesheets.
    The compute methods deliberately avoid searching inside the depends
    decorator to stay compatible with Odoo's ORM recompute mechanism.
    """
    _inherit = 'hr.employee'

    # ------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------
    oversight_task_progress = fields.Float(
        string="Current Task Progress (%)",
        compute='_compute_oversight_kpis',
        store=False,
        help="Average timesheet progress across all recent tasks.",
    )
    oversight_efficiency = fields.Float(
        string="Current Efficiency Score",
        compute='_compute_oversight_kpis',
        store=False,
        help="Average efficiency score across all recent tasks.",
    )
    oversight_total_hours = fields.Float(
        string="Total Hours Logged (30 days)",
        compute='_compute_oversight_kpis',
        store=False,
        help="Total hours logged via timesheets in the last 30 days.",
    )
    oversight_delayed_tasks = fields.Integer(
        string="Delayed Tasks",
        compute='_compute_oversight_delayed_tasks',
        store=False,
        help="Number of tasks currently flagged as delayed for this employee.",
    )

    # ------------------------------------------------------------------
    # Compute Methods
    # ------------------------------------------------------------------
    def _compute_oversight_kpis(self):
        """Aggregate timesheet KPIs for the last 30 days."""
        TimesheetLine = self.env['account.analytic.line']
        cutoff = fields.Date.today()
        start_date = cutoff - datetime.timedelta(days=30)

        for employee in self:
            lines = TimesheetLine.search([
                ('employee_id', '=', employee.id),
                ('date', '>=', start_date),
            ])
            if lines:
                employee.oversight_task_progress = (
                    sum(lines.mapped('oversight_task_progress')) / len(lines)
                )
                employee.oversight_efficiency = (
                    sum(lines.mapped('oversight_efficiency_score')) / len(lines)
                )
                employee.oversight_total_hours = sum(lines.mapped('unit_amount'))
            else:
                employee.oversight_task_progress = 0.0
                employee.oversight_efficiency = 0.0
                employee.oversight_total_hours = 0.0

    def _compute_oversight_delayed_tasks(self):
        """Count tasks assigned to this employee that are currently delayed."""
        Task = self.env['project.task']
        for employee in self:
            delayed = Task.search_count([
                ('user_ids', 'in', employee.user_id.ids),
                ('oversight_is_delayed', '=', True),
            ])
            employee.oversight_delayed_tasks = delayed

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_view_delayed_tasks(self):
        """Open a filtered list of delayed tasks for this employee."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delayed Tasks',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [
                ('user_ids', 'in', self.user_id.ids),
                ('oversight_is_delayed', '=', True),
            ],
            'context': {'default_user_ids': self.user_id.ids},
        }
