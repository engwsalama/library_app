from odoo import api, fields, models
from odoo.exceptions import Warning


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _order='name, date_published desc'

    # String fields: name=fields.Char('Title')
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    book_type=fields.Selection(
        [('paper','Paperback'),
         ('hard','Hardcover'),
         ('electronic','Electronic'),
         ('other','Other')],'Type')
    notes=fields.Text('Internal Notes')
    descr=fields.Html('Description')

    # Numeric fields:
    copies=fields.Integer(default=1)
    avg_rating=fields.Float('Average Rating',(3,2))
    price=fields.Monetray('Price','currency_id')
    currency_id=fields.Many2one('res.currrency')

    # Date and time fields:
    date_published = fields.Date()
    last_borrow_date=fields.Datetime('Last Borrowed On',default=lambda self: fields.Datetime.now())

    #Other fields:

    active = fields.Boolean('Active?')
    image = fields.Binary('Cover')

    # Relational Fields:


    publisher_id = fields.Many2one('res.partner', string='Publisher')
    author_ids = fields.Many2many('res.partner', string='Authors')

    @api.multi
    def _check_isbn(self):
        """Check one Book's ISBN"""
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderators = [1, 3] * 6
            total = sum(a * b for a, b in zip(digits[:12], ponderators))
            remain = total % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check



    @api.multi
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning(
                    'Please provide an ISBN13 for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning(
                    '%s is an invalid ISBN' % book.isbn)
        return True
