import json

def process_sub_resources(resources):
    if not resources:
        return None
    
    processed = {}
    for key, value in resources.items():
        items = {}
        for sub_value in value:
            item = {}
            sub = {}
            sub['id'] = sub_value['id']
            if 'kind' in sub_value:
                sub['kind'] = sub_value['kind']
            if 'sku' in sub_value:
                sub['sku_name'] = sub_value['sku']['name']
                if 'tier' in sub_value['sku']:
                    sub['sku_tier'] = sub_value['sku']['tier']
            if 'retention_in_days' in sub_value:
                sub['retention_in_days'] = sub_value['retention_in_days']
            if 'enabled_protocols' in sub_value:
                sub['enabled_protocols'] = sub_value['enabled_protocols']
            if 'zone_type' in sub_value:
                sub['zone_type'] = sub_value['zone_type']
            if 'hardware_profile' in sub_value:
                sub['hardware_profile'] = sub_value['hardware_profile']['vm_size']
            if 'storage_profile' in sub_value:
                sub['storage_profile'] = sub_value['storage_profile']['os_disk']['os_type']

            item[sub_value['name']] = sub
            items.update(item)
        processed[key] = items 
    return processed if processed else None

# hardware_profile > vm_size & os_disk > os_type




def process_resources(resources):
    if not resources:
        return None
    
    processed = {}
    for key, value in resources.items():
        if isinstance(value, dict):
            processed[key] = process_sub_resources(value)
    return processed if processed else None

def process_resource_groups(resource_groups):
    filtered = []
    for group in resource_groups:
        resources = process_resources(group.get('resources', {}))
        if resources:
            filtered.append({
                'resourceGroupName': group.get('resourceGroupName'),
                'resources': resources
            })
    return filtered if filtered else None

def process_subscriptions(data):
    result = []
    for sub in data.get('subscriptions', []):
        resource_groups = process_resource_groups(sub.get('resourceGroups', []))
        if resource_groups:
            result.append({
                'displayName': sub.get('displayName'),
                'resourceGroups': resource_groups
            })
    return {'subscriptions': result} if result else {}

def filter_json_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        filtered_data = process_subscriptions(data)
        
        with open(output_file, 'w') as f:
            json.dump(filtered_data, f, indent=2)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python script.py input.json output.json")
        sys.exit(1)
        
    filter_json_file(sys.argv[1], sys.argv[2])