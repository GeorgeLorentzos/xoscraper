import re
import csv
import sys
from pathlib import Path

class ClinicExtractor:
    def __init__(self, html_file):
        self.html_file = html_file
        self.clinics = []
    
    def extract_html(self):
        with open(self.html_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse_clinics(self, html_content):
        blocks = re.findall(r'<div class="basicInfo".*?</li>\s*</div>', html_content, re.DOTALL)
        
        for block in blocks:
            clinic = self.extract_clinic_data(block)
            if clinic['name']:
                self.clinics.append(clinic)
        
        return self.clinics
    
    def extract_clinic_data(self, block):
        name_match = re.search(r'<span itemprop="name">([^<]+)</span>', block)
        street_match = re.search(r'<span itemprop="streetAddress">([^<]+)</span>', block)
        postal_match = re.search(r'<span itemprop="postalCode">([^<]+)</span>', block)
        city_match = re.search(r'<span itemprop="addressLocality">([^<]+)</span>', block)
        
        phones = re.findall(r'href="tel:\+30([0-9]+)"', block)
        unique_phones = list(dict.fromkeys(phones))
        
        website_match = re.search(r'itemprop="url"[^>]*href="(https?://[^"]+)"', block)
        if not website_match:
            website_match = re.search(r'href="(https?://[^"]+)"[^>]*itemprop="url"', block)
        
        phone1 = unique_phones[0] if len(unique_phones) > 0 else ''
        phone2 = unique_phones[1] if len(unique_phones) > 1 else ''
        
        return {
            'name': name_match.group(1).strip() if name_match else '',
            'street': street_match.group(1).strip() if street_match else '',
            'city': city_match.group(1).strip() if city_match else '',
            'postal': postal_match.group(1).strip() if postal_match else '',
            'phone1': phone1,
            'phone2': phone2,
            'website': website_match.group(1).strip() if website_match else ''
        }
    
    def save_to_csv(self, output_file):
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company Name', 'Street Address', 'City', 'Postal Code', 'Phone 1', 'Phone 2', 'Website'])
            
            for clinic in self.clinics:
                writer.writerow([
                    clinic['name'],
                    clinic['street'],
                    clinic['city'],
                    clinic['postal'],
                    clinic['phone1'],
                    clinic['phone2'],
                    clinic['website']
                ])
        
        return len(self.clinics)

def main():
    data_input = 'data.txt'
    csv_output = 'clinics.csv'
    
    extractor = ClinicExtractor(data_input)
    html_content = extractor.extract_html()
    extractor.parse_clinics(html_content)
    count = extractor.save_to_csv(csv_output)
    
    print(f"Επιτυχής εξαγωγή {count} κλινικών στο {csv_output}")

if __name__ == '__main__':
    main()
