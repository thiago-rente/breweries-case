AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'

ENABLE_PROXY_FIX = True
SECRET_KEY = "brew4321"

FEATURE_FLAGS = {
  "ALERT_REPORTS": True,
  "ENABLE_TEMPLATE_PROCESSING": True
}

def delta_table(table_name):
    from deltalake import DeltaTable
    dt = DeltaTable(table_name)
    return dt.file_uris()

JINJA_CONTEXT_ADDONS = {
    'delta_table': delta_table
}