# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import xlrd

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
class JobCostingWizard(models.TransientModel):
    _name = 'jobcost.xls.uploader'
    
    file_xls = fields.Binary("Select Filed")
    file_name = fields.Char(string="File Name")
    task_id = fields.Many2one('project.task')

    def _create_product(self, name, type, uom, cost):
        if type == 'MATERIAL':
            type = 'product'
        else:
            type = 'service'
        
        product = self.env['product.product'].create({
            'name' : name,
            'uom_id': uom.id,
            'uom_po_id': uom.id,
            'lst_price': cost,
            'standard_price': cost,
            'detailed_type': type
        })
        return product

    def create_jobcost_sheet(self):
        
        job_costsheet_obj = self.env['job.costing']
        partner_obj = self.task_id.partner_id.id
        project_obj = self.env['project.project']
        task_obj = self.env['project.task']
        analytic_account_obj = self.env['account.analytic.account']
        costsheet_line_obj = self.env['job.cost.line']
        
        try:
            # workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.files))
             workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.file_xls))
        except:
            raise ValidationError("Please select .xls/xlsx file...")
        
        Sheet_name = workbook.sheet_names()
        job_costsheet_ids = []
        for inx in Sheet_name:
            sheet = workbook.sheet_by_name(inx)
            name = sheet.cell(0, 1).value
            notes_job = sheet.cell(2, 1).value
            # description = "Descritp"
            assumed_qty = sheet.cell(3, 1).value
            overhead_profit = sheet.cell(4, 1).value
            # description = sheet.cell(1, 3).value
            
            
                
            job_costsheet_id = job_costsheet_obj.create({
                'name': name,
                #  'description': description,
                'notes_job': notes_job,
                'task_id': self.task_id.id,
                'project_id': self.task_id.project_id.id,
                'assumed_qty': assumed_qty,
                'overhead_profit': overhead_profit , 
                'partner_id': partner_obj,
            })
            if not job_costsheet_id:
                raise ValidationError(_("Cost Sheet Error" ))
            job_costsheet_ids.append(job_costsheet_id.id)
            number_of_rows = sheet.nrows
            row = 1
            
            material_row = True
            labour_row = True
            overhead_row = True
            
            for row in range(8, sheet.nrows):
                # if sheet.cell(row, 0).value == 'MATERIAL':
                    date = sheet.cell(row, 0).value
                    # date = datetime.strptime(str(date), '%d/%m/%Y').strftime(DEFAULT_SERVER_DATE_FORMAT)
                    if not date:
                        raise ValidationError(_("Date not found for %s" %(sheet.cell(row, 0).value)))
                    
                    col_job_type = sheet.cell(row, 0).value
                    product_col = sheet.cell(row, 2).value
                    product_qty = sheet.cell(row, 4).value
                    unit = sheet.cell(row, 5).value
                    rate = sheet.cell(row, 6).value
                    reference = sheet.cell(row, 8).value
                    
                    job_type_id = self.env['job.type'].search([('name','=',sheet.cell(row, 1).value)])
                    product_id = self.env['product.product'].search([('name','=', product_col)], limit=1)
                    job_type = col_job_type
                    
                    if col_job_type == 'MATERIAL':
                        job_type = 'material'
                    elif col_job_type == 'MANPOWER':
                        job_type = 'labour'
                    elif col_job_type == 'EQUIPMENT':
                            job_type = 'overhead'
                    
                    uom_id = self.env['uom.uom'].search([('name', '=', unit)],limit=1)
                    if not uom_id:
                        raise ValidationError(_("Sheet: %s Row: %s  ,Unit is not define %s" %(sheet.name ,sheet.cell(row + 1 , 0).value , unit))) 
                    if not product_id:
                        product_id = self._create_product(product_col, job_type, uom_id, rate)

                    vals  = {}
                    if job_type == 'material':
                        vals = {
                                'date': datetime.today(),
                                'job_type_id': job_type_id.id, 
                                'product_id': product_id.id,
                                'reference': reference,
                                'product_qty': product_qty,
                                'direct_id': job_costsheet_id.id,
                                'cost_price': rate,
                                'uom_id': uom_id.id,
                                'job_type':job_type,
                        }
                    if job_type == 'labour':
                        product_qty = sheet.cell(row, 3).value
                        planned = sheet.cell(row, 4).value
                        vals = {
                                'date': datetime.today(),
                                'job_type_id': job_type_id.id, 
                                'product_id': product_id.id,
                                'reference': reference,
                                'product_qty': product_qty,
                                'hours': planned,
                                'direct_id': job_costsheet_id.id,
                                'cost_price': rate,
                                'uom_id': uom_id.id,

                                'job_type':job_type,
                        }
                    if job_type == 'overhead':
                        product_qty = sheet.cell(row, 3).value
                        planned = sheet.cell(row, 4).value
                        vals = {
                                'date': datetime.today(),
                                'job_type_id': job_type_id.id, 
                                'product_id': product_id.id,
                                'reference': reference,
                                'product_qty': product_qty,
                                'hours': planned,
                                'uom_id': uom_id.id,
                                'direct_id': job_costsheet_id.id,
                                'cost_price': rate,
                                'job_type':job_type,
                        }

                        
                        # jobcost_line_new = costsheet_line_obj.new(vals)
                        # jobcost_line_new._onchange_product_id()
                        # jcs_line_values = jobcost_line_new._convert_to_write({
                        #     name: jobcost_line_new[name] for name in jobcost_line_new._cache
                        # })
                        # jcs_line_values.update({
                        #     'product_qty': sheet.cell(row, 5).value,
                        #     'direct_id' : job_costsheet_id.id,
                        # })
                    jobcostsheet_line = costsheet_line_obj.create(vals)
                    row = row + 1
                            
            # for row in range(sheet.nrows):     
            #     if sheet.cell(row, 0).value == 'Labours':
            #         row = row + 2
            #         if labour_row != False:
            #             while sheet.cell(row, 0).value != 'Overhead':
            #                 date = sheet.cell(row, 0).value
            #                 date = datetime.strptime(str(date), '%d/%m/%Y').strftime(DEFAULT_SERVER_DATE_FORMAT)
            #                 if not date:
            #                     raise ValidationError(_("Date not found for %s" %(sheet.cell(line_row, 0).value)))
                            
            #                 job_type_id = self.env['job.type'].search([('name','=',sheet.cell(row, 1).value)])
            #                 product_id = self.env['product.product'].search([('name','=', sheet.cell(row, 2).value)], limit=1)
            #                 reference = sheet.cell(row, 4).value
            #                 hours = sheet.cell(row, 5).value
                            
            #                 if not product_id:
            #                     raise ValidationError(_("Product not found for %s" %(sheet.cell(row, 0).value)))
            #                 if job_costsheet_id:
            #                     vals = {
            #                          'date': date,
            #                          'job_type_id': job_type_id.id, 
            #                          'product_id': product_id.id,
            #                          'reference': reference,
            #                          'hours': hours,
            #                          'direct_id': job_costsheet_id.id,
            #                          'job_type':'labour',
            #                     }
            #                     job_line = costsheet_line_obj.create(vals)
            #                     job_line._onchange_product_id()
            #                     row = row + 1
                            
            # for row in range(sheet.nrows):
            #     if sheet.cell(row, 0).value == 'Overhead':
            #         row = row + 2
            #         if overhead_row != False:
            #             while (row < sheet.nrows):
            #                 date = sheet.cell(row, 0).value
            #                 date = datetime.strptime(date, '%d/%m/%Y').strftime(DEFAULT_SERVER_DATE_FORMAT)
            #                 if not date:
            #                     raise ValidationError(_("Date not found for %s" %(sheet.cell(line_row, 0).value)))
                            
            #                 job_type_id = self.env['job.type'].search([('name','=',sheet.cell(row, 1).value)])
            #                 product_id = self.env['product.product'].search([('name','=', sheet.cell(row, 2).value)], limit=1)
            #                 product_qty = sheet.cell(row, 5).value
            #                 reference = sheet.cell(row, 4).value
                            
            #                 if not product_id:
            #                     raise ValidationError(_("Product not found for %s" %(sheet.cell(row, 0).value)))
            #                 if job_costsheet_id:
            #                     vals = {
            #                          'date': date,
            #                          'job_type_id': job_type_id.id, 
            #                          'product_id': product_id.id,
            #                          'reference': reference,
            #                          'product_qty': product_qty,
            #                          'direct_id': job_costsheet_id.id,
            #                          'job_type':'overhead',
                                    
            #                     }
            #                     jobcost_line_new = costsheet_line_obj.new(vals)
            #                     jobcost_line_new._onchange_product_id()
            #                     jcs_line_values = jobcost_line_new._convert_to_write({
            #                        name: jobcost_line_new[name] for name in jobcost_line_new._cache
            #                     })
            #                     jcs_line_values.update({
            #                         'product_qty': sheet.cell(row, 5).value,
            #                         'direct_id' : job_costsheet_id.id,
            #                     })
            #                     jobcostsheet_line = costsheet_line_obj.create(jcs_line_values)
            #                     row = row + 1
                        
        # result = self.env.ref('odoo_job_costing_management.action_job_costing')
        # action_ref = result or False
        # action = action_ref.sudo().read()[0]
        action = self.env["ir.actions.actions"]._for_xml_id("odoo_job_costing_management.action_job_costing")
        action['domain'] = [('id', 'in', job_costsheet_ids)]
        return action