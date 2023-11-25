# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': "Project Job Costing Uploader",
    'version': '16.9.4.22',
    'depends': [
                'odoo_job_costing_management',
                ],
    'category' : 'Services/Project',
    'license': 'Other proprietary',
    'summary': """Construction and Job Contracting with Job Costing Sheet Management.""",
    'description': """
    """,
    'author': "Bilal.",
    'website': "https://www.alifzero.com",
    'data':[
            'security/ir.model.access.csv',
            'wizards/job_cost_uploader.xml',
            'views/project_task_view.xml',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
