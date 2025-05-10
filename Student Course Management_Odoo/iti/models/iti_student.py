from odoo import api, models, fields
from odoo.exceptions import UserError

class Itistudent(models.Model):
    _name = "iti.student"
    
    name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    address = fields.Text()
    tax = fields.Float(compute = "calc_tax", store = True)
    net_salary = fields.Float(compute = "calc_tax")
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')],
        string="Gender"
    )
    accepted = fields.Boolean(default=False)
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related = "track_id.capacity")
    skills_ids = fields.Many2many("iti.skill")
    grade_ids = fields.One2many("student.course.line", "student_id")
    state = fields.Selection([
        ('applied','Applied'),
        ('first','First Interview'),
        ('second','Second Interview'),
        ('passed','Passed'),
        ('rejected','Rejected'),
    ],default = 'applied')

    @api.constrains('track_id')
    def check_track_id(self):
        track_count = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("Track is full")


    @api.model
    def create(self, vals):
        name = vals.get('name')
        if name:
            name_split = name.split()
            if len(name_split) >= 2:
                vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"

        search_student = self.search([('email','=',vals['email'])])
        if search_student:
            raise UserError('Email already exist')
        return super().create(vals)


    def write(self, vals):
        if 'name' in vals:
            name_split = vals['name'].split()
            if len(name_split) >= 2:
                vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().write(vals)


    def unlink(self):
        for record in self:
            if record.state in ['passed','rejected']:
                raise UserError("You can't delete passed/rejected students")
        super().unlink()

    @api.depends("salary")
    def calc_tax(self):
        for student in self:
            student.tax = student.salary * 0.20
            student.net_salary = student.salary - student.tax
        

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed','rejected']:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'
    

    def set_rejected(self):
        self.state = "rejected"
    
    
    
    @api.onchange("gender")
    def _on_channge_gender(self):
        domain = {'track_id': ['is_open']}
        if self.gender == 'm':
            domain = {'track_id': [('is_open','=',True)]}
            self.salary = 1000
        else:
            self.salary = 5000
        return{
            'warning': {
                'title': 'Hello',
                'message': 'You have change the gender'
            },
            'domain':domain
        }




class ItiCourse(models.Model):
    _name = "iti.course"

    name = fields.Char()


class StudentCourseGrades(models.Model):
    _name = "student.course.line"

    student_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([
        ("g" , "Good"),
        ("vg" , "Very Good"),
    ])
