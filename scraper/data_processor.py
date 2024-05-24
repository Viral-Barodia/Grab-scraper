import json
import gzip
import logging

class DataProcessor:
    @staticmethod
    def save_to_ndjson(data, filename):
        with open(filename, 'w') as f:
            for entry in data:
                json.dump(entry, f)
                f.write('\n')
                
    @staticmethod
    def unique_restaurants(data):
        seen = set()
        unique_data = []
        for entry in data:
            identifier = entry['Restaurant ID']
            if identifier not in seen:
                unique_data.append(entry)
                seen.add(identifier)
        logging.info(f"Filtered {len(data) - len(unique_data)} duplicate entries.")
        return unique_data
