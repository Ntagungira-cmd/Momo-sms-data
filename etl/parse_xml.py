import json
import os
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xml_file_path = os.path.join(BASE_DIR, "../data/raw/modified_sms_v2.xml")


def parse_sms_xml_to_json(xml_data):
    try:
        # Parse the XML content
        root = ET.fromstring(xml_data)

        # List to store all sms records as dictionaries
        sms_records = []

        # Iterate through all SMS elements
        for sms in root.findall('sms'):
            sms_data = {
                'protocol': sms.get('protocol'),
                'address': sms.get('address'),
                'date': sms.get('date'),
                'type': sms.get('type'),
                'subject': sms.get('subject'),
                'body': sms.get('body'),
                'toa': sms.get('toa'),
                'sc_toa': sms.get('sc_toa'),
                'service_center': sms.get('service_center'),
                'read': sms.get('read'),
                'status': sms.get('status'),
                'locked': sms.get('locked'),
                'date_sent': sms.get('date_sent'),
                'sub_id': sms.get('sub_id'),
                'readable_date': sms.get('readable_date'),
                'contact_name': sms.get('contact_name')
            }

            # Parse and add additional useful fields from the body

            body = sms.get('body', '')
            sms_data.update(parse_transaction_details(body))

            sms_records.append(sms_data)

        return sms_records

    except ET.ParseError as exception:
        print(f"Error parsing XML: {exception}")
        return []


def parse_transaction_details(body):
    details = {}

    # Extract amount
    amount_patterns = [
        r'received (\d+) RWF',
        r'payment of (\d+[,]?\d*) RWF',
        r'deposit of (\d+[,]?\d*) RWF',
        r'transferred to.*?(\d+[,]?\d*) RWF'
    ]

    for pattern in amount_patterns:
        match = re.search(pattern, body)
        if match:
            details['amount'] = match.group(1).replace(',', '')
            break

    # Extract transaction type
    if 'received' in body.lower():
        details['transaction_type'] = 'credit'
    elif 'payment' in body.lower() or 'transferred' in body.lower():
        details['transaction_type'] = 'debit'
    elif 'deposit' in body.lower():
        details['transaction_type'] = 'deposit'
    elif 'withdrawn' in body.lower():
        details['transaction_type'] = 'withdrawal'
    else:
        details['transaction_type'] = 'other'

    # Extract balance
    balance_match = re.search(r'balance[:\s]*([\d,]+)', body, re.IGNORECASE)
    if balance_match:
        details['balance'] = balance_match.group(1).replace(',', '')

    # Extract recipient/sender
    recipient_patterns = [
        r'to (.*?) \d',
        r'from (.*?) \(',
        r'received.*?from (.*?) \('
    ]

    for pattern in recipient_patterns:
        match = re.search(pattern, body)
        if match:
            details['counterparty'] = match.group(1).strip()
            break

    # Extract transaction ID
    tx_id_match = re.search(r'[Tt]x[Ii]d:?\s*(\d+)', body)
    if tx_id_match:
        details['transaction_id'] = tx_id_match.group(1)

    # Extract date from body
    date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
    if date_match:
        details['transaction_date'] = date_match.group(1)

    return details


def save_to_json(sms_data, filename='sms_records.json'):
    """
  Save SMS records to JSON file
  """

    parse_folder = os.path.join(BASE_DIR, "../data/processed")

    os.makedirs(parse_folder, exist_ok=True)

    json_file_path = os.path.join(parse_folder, filename)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(sms_data, f, indent=2, ensure_ascii=False)

    return json_file_path


# Example usage
if __name__ == "__main__":

    try:
        with open(xml_file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        # Parse XML to JSON objects
        sms_data_records = parse_sms_xml_to_json(xml_content)

        # Will print first few records as example
        print(f"Total SMS records: {len(sms_data_records)}")
        print("\nFirst 3 records:")

        for i, record in enumerate(sms_data_records[:3]):
            print(f"\nRecord {i + 1}:")
            print(json.dumps(record, indent=2, ensure_ascii=False))

        # Save all records to JSON file in the processed folder
        file_path = save_to_json(sms_data_records)
        print(f"\nAll records saved to: {file_path}")

        # Print some statistics
        transaction_types = {}

        for record in sms_data_records:
            tx_type = record.get('transaction_type', 'unknown')
            transaction_types[tx_type] = transaction_types.get(tx_type, 0) + 1

        print("\nTransaction Statistics:")
        for tx_type, count in transaction_types.items():
            print(f"{tx_type}: {count} transactions")

    except FileNotFoundError:
        print(f"Error: File not found at {xml_file_path}")
        print("Please check the file path and make sure the XML file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
