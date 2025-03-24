import xmlrpc.client
import pandas as pd

# Odoo server details
url = "https://ai-project.odoo.com"
db = "ai-project-prod-18920551"
username = "admin"
password = "02237893fe13a920800ce1975f1f2fb32551552a"

# output_file = "crm_data.txt"
output_file = "event.sale.report.txt"

with open(output_file, "w", encoding="utf-8") as f:
    # Authenticate with Odoo
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})

    if uid:
        f.write(f"Authenticated as user {uid}\n")
        # Object endpoint for data operations
        models_rpc = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

        # Retrieve CRM functionalities (models whose technical names contain 'crm.')
        models = models_rpc.execute_kw(
            db, uid, password,
            'ir.model', 'search_read',
            [[('model', 'ilike', 'crm.')]],
            {'fields': ['model', 'name']}
        )

        if models:
            f.write("\nFetching data from Odoo Database (models):\n")
            for model in models:
                model_name = model['model']
                model_purpose = model['name']
                f.write(f"\n--- Model: {model_name} | Purpose: {model_purpose} ---\n")
                try:
                    # Retrieve available fields for the current model
                    fields_def = models_rpc.execute_kw(
                        db, uid, password,
                        model_name, 'fields_get',
                        [],
                        {'attributes': ['string', 'type']}
                    )
                    # Get the list of field names
                    field_list = list(fields_def.keys())

                    # Fetch all records from the model using all available fields
                    records = models_rpc.execute_kw(
                        db, uid, password,
                        model_name, 'search_read',
                        [[]],  # No filter domain; adjust if needed
                        {'fields': field_list}
                    )
                    f.write(f"Found {len(records)} record(s) in {model_name}:\n")
                    
                    # Create a pandas DataFrame from the records
                    df = pd.DataFrame(records, columns=field_list)
                    # Save the DataFrame to a CSV file named after the model
                    df.to_csv(f"csv file/{model_name}.csv", index=False, encoding='utf-8')
                    # Log the save action
                    f.write(f"Saved {len(records)} records to {model_name}.csv\n")
                    
                    f.write(f"Found {len(records)} record(s) in {model_name}:\n")
                    
                    for record in records:
                        f.write(str(record) + "\n")

                except xmlrpc.client.Fault as e:
                    f.write(f"Error fetching data for model {model_name}: {e}\n")
        else:
            f.write("No CRM functionalities found.\n")
    else:
        f.write("Authentication failed!\n")

print(f"Output saved in {output_file}")
