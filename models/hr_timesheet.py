# -*- coding: utf-8 -*-
# OVERSIGHT Module — Timesheet Enhancements
# Extends hr.timesheet.line (account.analytic.line) to add task progress
# tracking and efficiency scoring. The 'hr_timesheet.sheet' model is only
# available when the hr_timesheet_sheet module is installed. Because that
# module is optional, we inherit the base analytic line (hr.timesheet) and
# aggregate data at the employee + date level instead.

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AccountAnalyticLineOversight(models.Model):
    """
    Extend the core timesheet line model to expose oversight metrics directly
    on each line. Progress / efficiency are computed relative to the parent
    task's planned hours so the numbers are always up-to-date.
    """
    _inherit = 'account.analytic.line'

    # ------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------
    oversight_task_progress = fields.Float(
        string="Task Progress (%)",
        compute='_compute_oversight_task_progress',
        store=True,
        help="Percentage of allocated hours logged on the linked task so far.",
    )
    oversight_efficiency_score = fields.Float(
        string="Efficiency Score",
        compute='_compute_oversight_efficiency_score',
        store=True,
        help="Weighted score combining task completion rate and activity level.",
    )

    # ------------------------------------------------------------------
    # Compute Methods
    # ------------------------------------------------------------------
    @api.depends('task_id', 'task_id.timesheet_ids', 'task_id.allocated_hours')
    def _compute_oversight_task_progress(self):
        """Compute percentage of allocated hours that have been logged."""
        for line in self:
            task = line.task_id
            if task and task.allocated_hours:
                total_logged = sum(task.timesheet_ids.mapped('unit_amount'))
                line.oversight_task_progress = (total_logged / task.allocated_hours) * 100
            else:
                line.oversight_task_progress = 0.0

    @api.depends('oversight_task_progress', 'task_id', 'task_id.timesheet_ids')
    def _compute_oversight_efficiency_score(self):
        """
        Composite efficiency score:
          score = (task_progress × 0.70) + (line_count / 7 × 30)
        A perfect score (~100) means 100 % task completion with ≥7 time entries.
        """
        for line in self:
            task = line.task_id
            line_count = len(task.timesheet_ids) if task else 1
            line.oversight_efficiency_score = (
                line.oversight_task_progress * 0.70 + (line_count / 7) * 30
            )
