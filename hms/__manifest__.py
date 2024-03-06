{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Health',
    'summary': 'Manage hospital patient records',
    'author': 'Ramy Medhat',
    'website': '',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/department.xml',
    ],

    'application': True,
}
