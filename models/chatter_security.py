# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)


# This prevents non-users from autofollowing records. They can still be added manually. 
class MailThread(models.AbstractModel):
	_inherit = 'mail.thread'

	@api.model
	def create(self, vals):
		ctx = {}
		# _logger.info(vals)

		if 'partner_id' in vals:
			partner_id = self.env['res.partner'].browse([vals['partner_id']])
			if not partner_id.user_ids:
				ctx['mail_create_nosubscribe'] = True
				# ctx['mail_post_autofollow'] = False
		message = super(MailThread, self.with_context(ctx)).create(vals)
		# _logger.info(self.env.context)
		return message

	@api.multi
	@api.returns('self', lambda value: value.id)
	def message_post(self, body='', subject=None, message_type='notification', subtype=None, parent_id=False, attachments=None, content_subtype='html', **kwargs):
		ctx = self.env.context.copy()
		author_id = kwargs.get('author_id')
		# _logger.info(author_id)
		pid = self.env['res.partner'].browse([author_id])
		# _logger.info(pid)
		if author_id and not pid.user_ids:
			ctx['mail_create_nosubscribe'] = True
			# ctx['mail_post_autofollow'] = False
		message = super(MailThread, self.with_context(ctx)).message_post(body=body, subject=subject, message_type=message_type, subtype=subtype, parent_id=parent_id, attachments=attachments, content_subtype=content_subtype, **kwargs)
		return message

class Lead(models.Model):
	_inherit = 'crm.lead'

	comment_ids = fields.One2many(
		'mail.message', 'res_id', string='Messages',
		domain=lambda self: [('model', '=', self._name),('subtype_id.name','=','Discussions')], auto_join=True)
	message_ids = fields.One2many(
		'mail.message', 'res_id', string='Messages',
		domain=lambda self: [('model', '=', self._name),('subtype_id.name','!=','Discussions')], auto_join=True)
	# notification_ids = fields.One2many(
 #        'mail.message', 'res_id', string='Messages',
 #        domain=lambda self: [('model', '=', self._name),('message_type','=','notification')], auto_join=True)

#   @api.multi
#   @api.returns('self', lambda value: value.id)
#   def message_post(self, body='', subject=None, message_type='notification', subtype=None, parent_id=False, attachments=None, content_subtype='html', **kwargs):
#       message = super(Lead, self.with_context(mail_create_nosubscribe=True)).message_post(body=body, subject=subject, message_type=message_type, subtype=subtype, parent_id=parent_id, attachments=attachments, content_subtype=content_subtype, **kwargs)
#       return message

# class Order(models.Model):
#   _inherit = 'sale.order'

#   @api.multi
#   @api.returns('self', lambda value: value.id)
#   def message_post(self, body='', subject=None, message_type='notification', subtype=None, parent_id=False, attachments=None, content_subtype='html', **kwargs):
#       message = super(Order, self.with_context(mail_create_nosubscribe=True)).message_post(body=body, subject=subject, message_type=message_type, subtype=subtype, parent_id=parent_id, attachments=attachments, content_subtype=content_subtype, **kwargs)
#       return message

#   @api.model
#   def create(self, vals):
#       message = super(Order, self.with_context(mail_create_nosubscribe=True)).create(vals)
#       return message

#   @api.multi
#     def action_confirm(self):

#         message = super(Order, self.with_context(mail_create_nosubscribe=True)).action_confirm()
#         return message


# This is going be a module that prevents the creation of a follower record for certain model types and user categories.
# Right now it prevents the creatiion of non-user followers across all models.
# I need to adapt it to all the administrator to set security based on model type and ACL/security group
# Could also be on a per record basis
class Followers(models.Model):
	_inherit = 'mail.followers'

	@api.model
	def create (self, vals):
		
		user_ids = self.env['res.partner'].browse([vals['partner_id']]).user_ids.ids
		# _logger.info(user_ids)
		if not user_ids:
			return
		else:
			return super(Followers, self).create(vals)

	# The following commented out code may be necessary or not. It should be tested.

	@api.model
	def write (self, vals):
		
		user_ids = self.env['res.partner'].browse([vals['partner_id']]).user_ids.ids
		# _logger.info(user_ids)
		if not user_ids:
			return
		else:
			return super(Followers, self).write(vals)

	partner_id = fields.Many2one(
		'res.partner', string='Related Partner/User', ondelete='cascade', domain=[('user_ids','!=',False)])



