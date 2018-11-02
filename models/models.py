# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class CustomerLabels(models.Model):
    _name = 'repaircenter.customerlabel'
    type = fields.Selection([('device','Device Label'),('media','Media Label'),('donation','Donation Label'),('serial','Activation Label')],string="Label Type",track_visibility='onchange')
    device = fields.Char(string="Device Name")
    customer = fields.Char(string="Customer Name")
    donation = fields.Datetime(string="Date",default=fields.Datetime.now)
    serial = fields.Char(string="Serial Number")
    software = fields.Char(string="Software")
    qty = fields.Integer(string="Copies",default="1")

class Ticket(models.Model):
    _name = 'repaircenter.ticket'
    _rec_name = 'customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority asc, create_date asc'
    stage = fields.Many2one('repaircenter.stages',group_expand='_read_group_stage_ids',track_visibility='onchange',
     default=lambda self: self.env['repaircenter.stages'].search([('incoming','=','True')]))
    adminact = fields.Char(string="Admin Account")
    appleid = fields.Char(string="Apple ID")
    applepass = fields.Char(string="Apple Password")
    completed = fields.Char(string="Work Performed",track_visibility='onchange')
    customer = fields.Many2one('res.partner',string="Customer",required=True)
    device = fields.Char(string="Device",required=True)
    email = fields.Char(string="Email",related="customer.email")
    backup = fields.Many2many('repaircenter.backupsoftware',track_visibility='onchange')
    issue = fields.Char(string="Requested Work",track_visibility='onchange',required=True)
    login = fields.Char(string="Login",track_visibility='onchange')
    mobile = fields.Char(string="Mobile",related="customer.mobile")
    other = fields.Char(string="Other")
    password = fields.Char(string="Password/Passcode",track_visibility='onchange')
    phone = fields.Char(string="Phone",related="customer.phone")
    peripherals = fields.Many2many('repaircenter.peripherals',track_visibility='onchange')
    backupdevice = fields.Many2one('repaircenter.backuplocation',track_visibility='onchange')
    backupfolder = fields.Char(string="Backup Folder",track_visibility='onchange')
    priority = fields.Selection([["0","Normal"],["2","High"]],track_visibility='onchange' )
    type = fields.Many2one('repaircenter.services',required=True)
    technician = fields.Many2one('res.users',track_visibility='onchange',required=True)
    windows = fields.Char(string="Windows Email")
    @api.model
    def _read_group_stage_ids(self,stages,domain,order):
        stage_ids = self.env['repaircenter.stages'].search([])
        return stage_ids
    @api.multi
    def action_checkin(self):
         self.write({
         'stage': 'CHECKED IN',
         })
    def print_labels(self):
        for order in self:
            view_id=self.env['repaircenter.customerlabel']
            new = view_id.create(params[0])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print label for customer peripherals.',
            'res_model': 'repaircenter.customerlabel',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id'    : new.id,
            'target': 'new',
            }

    order_count = fields.Integer(string='Repair Ticket Orders')
#    def _compute_order_count(self):
#        sale_data = self.env['repaircenter.ticket'].read_group(domain=[('customer', 'in', self.ids)],
#                                                      fields=['customer'], groupby=['customer'])
#        # read to keep the child/parent relation while aggregating the read_group result in the loop
#        partner_child_ids = self.read(['child_ids'])
#        mapped_data = dict([(m['customer'][0], m['customer_count']) for m in sale_data])
#        for partner in self:
#            # let's obtain the partner id and all its child ids from the read up there
#            item = next(p for p in partner_child_ids if p['id'] == partner.id)
#            customers = [partner.id] + item.get('child_ids')
#            # then we can sum for all the partner's child
#            partner.order_count = sum(mapped_data.get(child, 0) for child in customers)



class Peripherals(models.Model):
    _name = 'repaircenter.peripherals'
    name = fields.Char()

class DeviceSoftware(models.Model):
    _name = 'repaircenter.devicesoftware'
    name = fields.Char(string="Software",required=True)
    username = fields.Char(string="Username")
    password = fields.Char(string="Password")

class BackupLocation(models.Model):
    _name = 'repaircenter.backuplocation'
    name = fields.Char(string="Device",required=True)
    folder = fields.Char(string="Folder Name")

class BackupSoftware(models.Model):
    _name = 'repaircenter.backupsoftware'
    _order = 'name asc'
    name = fields.Char(string="Location/Software")

class Services(models.Model):
    _name = 'repaircenter.services'
    _order = 'name asc'
    name = fields.Char(string="Services",required=True)

class Stages(models.Model):
    _name = 'repaircenter.stages'
    default = 'incoming'
    name = fields.Char(string="Stage")
    is_close = fields.Boolean(
        'Closing Stage',
        help='Tickets in this stage are considered as done.')
    fold = fields.Boolean(
        'Folded', help='Folded in kanban view')
    incoming = fields.Boolean('Default New',help='Default stage to be applied to new tickets. Should only be one.')

class DeviceManagement(models.Model):
    _name = 'repaircenter.devicemanagement'
    name = fields.Char(string="Device",required=True)
    account = fields.Char(string="Account")
    password = fields.Char(string="Password")
    gateway = fields.Char(string="Gateway")
    ip = fields.Char(string="IP")
    customer = fields.Many2many('res.partner')
    description = fields.Char(string="Description")
    model = fields.Char(string="Model/Serial No.")
    software = fields.Many2many('repaircenter.devicesoftware')
    subnet = fields.Char(string="Subnet")

class UserDevice(models.Model):
    _inherit = 'res.partner'
    device = fields.Many2many('repaircenter.devicemanagement')
    ticket_count = fields.Integer(compute='_compute_ticket_count', string='Repair Ticket Count')
    def _compute_ticket_count(self):
        sale_data = self.env['repaircenter.ticket'].read_group(domain=[('customer', 'in', self.ids)],
                                                      fields=['customer'], groupby=['customer'])
        # read to keep the child/parent relation while aggregating the read_group result in the loop
        partner_child_ids = self.read(['child_ids'])
        mapped_data = dict([(m['customer'][0], m['customer_count']) for m in sale_data])
        for partner in self:
            # let's obtain the partner id and all its child ids from the read up there
            item = next(p for p in partner_child_ids if p['id'] == partner.id)
            customers = [partner.id] + item.get('child_ids')
            # then we can sum for all the partner's child
            partner.ticket_count = sum(mapped_data.get(child, 0) for child in customers)
