import xmlrpc.client

# Odoo server details
url = "https://ai-project.odoo.com"
db = "ai-project-prod-18920551"
username = "admin"
password = "02237893fe13a920800ce1975f1f2fb32551552a"

# Authenticate with Odoo
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"Authenticated as user {uid}")

    # Object endpoint for data operations
    models_rpc = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Fetch models whose technical names start with 'crm.' (i.e., CRM functionalities)
    crm_models = models_rpc.execute_kw(
        db, uid, password,
        'ir.model', 'search_read',
        [[('model', 'ilike', 'project_todo.')]],
        {'fields': ['model', 'name']}
    )

    if crm_models:
        print("\nCRM Functionalities (Models):")
        for crm_model in crm_models:
            print(f"Model: {crm_model['model']}  |  Purpose: {crm_model['name']}")
    else:
        print("No CRM functionalities found.")
else:
    print("Authentication failed!")
