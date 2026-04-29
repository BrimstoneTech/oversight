# -*- coding: utf-8 -*-
from . import models
from . import controllers

def pre_init_hook(env):
    """
    Clean up legacy non-prefixed fields and corrupted views from older versions
    to prevent installation crashes related to field name collisions.
    """
    env.cr.execute("""
        DELETE FROM ir_model_fields 
        WHERE name IN ('task_progress', 'efficiency_score', 'total_hours', 'delayed_tasks', 'efficiency')
        AND model IN ('hr.employee', 'project.task', 'account.analytic.line')
    """)
    env.cr.execute("""
        DELETE FROM ir_ui_view 
        WHERE name ILIKE '%oversight%' 
        AND id NOT IN (
            SELECT res_id FROM ir_model_data WHERE model='ir.ui.view' AND module='oversight_module'
        )
    """)

