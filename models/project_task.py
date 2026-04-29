# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TaskOversight(models.Model):
    _inherit = 'project.task'

    # ------------------------------------------------------------------
    # Fields (Strictly Prefixed to prevent Odoo 17 Search crashes)
    # ------------------------------------------------------------------
    oversight_progress = fields.Float(
        string="Progress (%)",
        compute='_compute_oversight_metrics',
        store=True,
    )
    oversight_remaining_hours = fields.Float(
        string="Remaining Hours",
        compute='_compute_oversight_metrics',
        store=True,
    )
    oversight_is_delayed = fields.Boolean(
        string="Is Delayed",
        compute='_compute_oversight_metrics',
        store=True,
    )

    # ------------------------------------------------------------------
    # Single Compute Method (More Efficient in Odoo 17)
    # ------------------------------------------------------------------
    @api.depends('timesheet_ids.unit_amount', 'allocated_hours', 'date_deadline')
    def _compute_oversight_metrics(self):
        today = fields.Date.today()
        for task in self:
            # 1. Calculate Progress
            total_logged = sum(task.timesheet_ids.mapped('unit_amount'))
            task.oversight_progress = (total_logged / task.allocated_hours * 100) if task.allocated_hours > 0 else 0.0

            # 2. Calculate Remaining Hours
            task.oversight_remaining_hours = max(task.allocated_hours - total_logged, 0.0)

            # 3. Calculate Delay Status
            task.oversight_is_delayed = bool(
                task.date_deadline and 
                task.date_deadline < today and 
                task.oversight_progress < 100.0
            )

    # ------------------------------------------------------------------
    # Automation Logic
    # ------------------------------------------------------------------
    def _send_delay_alert(self):
        """Cron job entry point."""
        delayed_tasks = self.search([('oversight_is_delayed', '=', True)])
        for task in delayed_tasks:
            task.message_post(
                body=f"⚠️ Task '{task.name}' is delayed! Progress: {task.oversight_progress:.1f}%",
                subject=f"OVERSIGHT: Task Delay Alert"
            )
