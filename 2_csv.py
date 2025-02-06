import json
import csv
import pprint

def print_others(dct):
    result = ""
    for key, value in dct.items():
        if value != "":
            result += str(key) + ":" + str(value) + " | "  
    return result[:-3]


def flatten_json(json_file, csv_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        rows = []
        for sub in data.get('subscriptions', []):
            sub_name = sub.get('displayName', '')
            
            for rg in sub.get('resourceGroups', []):
                rg_name = rg.get('resourceGroupName', '')
                resources = rg.get('resources', {})
                
                for res_type, res_list in resources.items():
                    if isinstance(res_list, dict):
                        for resource, items in res_list.items():
                            for name, extras in items.items():
                                other = {}
                                other['retention_in_days'] = extras.get('retention_in_days', '')
                                other['enabled_protocols'] = extras.get('enabled_protocols', '')
                                other['zone_type'] = extras.get('zone_type', '')
                                other['hardware_profile'] = extras.get('hardware_profile', '')  
                                other['storage_profile'] = extras.get('storage_profile', '')
                                rows.append({
                                    'subscription': sub_name,
                                    'resource_group': rg_name,
                                    'resource_type': res_type,
                                    'resource': resource,
                                    'name': name,
                                    'kind': extras.get('kind', ''),
                                    'sku_name': extras.get('sku_name', ''),
                                    'sku_tier': extras.get('sku_tier', ''),
                                    'other': print_others(other),
                                    'id': extras['id']
                                })
        # Write to CSV
        if rows:
            fields = ['subscription', 'resource_group', 'resource_type', 'resource', 'name', 'kind', 'sku_name', 'sku_tier', 'other', 'id']
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Successfully converted to CSV: {csv_file}")
        else:
            print("No data to write")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python script.py input.json output.csv")
        sys.exit(1)
        
    flatten_json(sys.argv[1], sys.argv[2])