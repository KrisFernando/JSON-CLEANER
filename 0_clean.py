import json

def clean_json(data):
    if isinstance(data, dict):
        return {k: v for k, v in ((k, clean_json(v)) for k, v in data.items())
                if v not in (None, "", [], {}, ())}
    elif isinstance(data, list):
        return [v for v in (clean_json(v) for v in data)
                if v not in (None, "", [], {}, ())]
    return data

def clean_json_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        cleaned_data = clean_json(data)
        
        with open(output_file, 'w') as f:
            json.dump(cleaned_data, f, indent=2)
            
        print(f"Successfully cleaned JSON and saved to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python script.py input.json output.json")
        sys.exit(1)
        
    clean_json_file(sys.argv[1], sys.argv[2])