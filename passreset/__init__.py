from django.contrib import admin
# override admin login template
admin.site.login_template = 'passreset/admin/login.html'
