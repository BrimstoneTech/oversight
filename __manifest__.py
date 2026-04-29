# -*- coding: utf-8 -*-
{
    'name': 'OVERSIGHT: Timesheet, Task & Appraisal Integration',
    'version': '1.0.0',
    'summary': 'Real-time oversight for managers, HR, and executives',
    'description': """
OVERSIGHT Module
================
This module provides a robust integration between Timesheets, Task Progress,
and Appraisals. Designed for CEOs, COOs, managers, and HR to ensure labour
efficiency, on-time task completion, and data-driven performance appraisals.

Key Features:
- Real-time task progress tracking with visual progress bars
- Automated efficiency scoring per employee
- Seamless integration: Timesheets ↔ Tasks ↔ Appraisals
- Manager/HR dashboards for oversight and alerts
- Automated email alerts for delayed tasks
- Mobile-friendly and easy to use
    """,
    'author': 'BRIMSTONE Tech | brimstonetech1@gmail.com | +256 744 429 293',
    'category': 'Human Resources/Timesheets',
    'depends': [
        'hr_timesheet',
        'project',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_timesheet_views.xml',
        'views/project_task_views.xml',
        # 'views/hr_appraisal_views.xml',
        'views/hr_employee_views.xml',
        'views/templates.xml',
        'data/oversight_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 400.00,
    'currency': 'USD',
    'license': 'OPL-1',
    'images': [],
    'pre_init_hook': 'pre_init_hook',
}
