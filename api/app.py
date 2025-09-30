import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from etl.parse_xml import save_to_json

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "sms_records.json")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


class SMSHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            sms_data = load_data()
        except FileNotFoundError:
            self._send_json({"error": "sms_records.json not found"}, 404)
            return

        if path == "/transactions":
            self._send_json(sms_data)

        elif path.startswith("/transaction/"):
            tx_id = path.split("/")[-1]
            if not tx_id:
                self._send_json({"error": "transaction id required"}, 400)
                return

            record = next((sms for sms in sms_data if sms.get("transaction_id") == tx_id), None)

            if record:
                self._send_json(record)
            else:
                self._send_json({"error": f"Transaction {tx_id} not found"}, 404)

        else:
            self._send_json({"error": "endpoint not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/transactions":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                new_record = json.loads(post_data)

                # Basic validation
                required_fields = ["protocol", "address", "date", "type", "body", "type", "subject", "body", "toa",
                                   "sc_toa", "service_center", "read", "status", "locked", "date_sent", "sub_id",
                                   "readable_date", "contact_name"]

                for field in required_fields:
                    if field not in new_record:
                        self._send_json({"error": f"Missing required field: {field}"}, 400)
                        return

            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, 400)
                return

            try:
                sms_data = load_data()
            except FileNotFoundError:
                sms_data = []

            sms_data.append(new_record)

            save_to_json(sms_data)

            self._send_json(new_record, 201)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/transactions/"):
            tx_id = path.split("/")[-1]
            if not tx_id:
                self._send_json({"error": "transaction id required"}, 400)
                return

            content_length = int(self.headers.get('Content-Length', 0))
            put_data = self.rfile.read(content_length)

            try:
                updated_record = json.loads(put_data)

                # basic validation
                required_fields = ["protocol", "address", "date", "type", "body", "type", "subject", "body", "toa",
                                   "sc_toa", "service_center", "read", "status", "locked", "date_sent", "sub_id",
                                   "readable_date", "contact_name"]

                for field in required_fields:
                    if field not in updated_record:
                        self._send_json({"error": f"Missing required field: {field}"}, 400)
                        return

            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, 400)
                return

            try:
                sms_data = load_data()
            except FileNotFoundError:
                self._send_json({"error": "sms_records.json not found"}, 404)
                return

            record_index = next((i for i, sms in enumerate(sms_data) if sms.get("transaction_id") == tx_id), None)

            if record_index is not None:
                sms_data[record_index].update(updated_record)
                save_to_json(sms_data)
                self._send_json(sms_data[record_index])
            else:
                self._send_json({"error": f"Transaction {tx_id} not found"}, 404)
        else:
            self._send_json({"error": "endpoint not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/transactions/"):
            tx_id = path.split("/")[-1]
            if not tx_id:
                self._send_json({"error": "transaction id required"}, 400)
                return

            try:
                sms_data = load_data()
            except FileNotFoundError:
                self._send_json({"error": "sms_records.json not found"}, 404)
                return

            record_index = next((i for i, sms in enumerate(sms_data) if sms.get("transaction_id") == tx_id), None)

            if record_index is not None:
                deleted_record = sms_data.pop(record_index)
                save_to_json(sms_data)
                self._send_json(deleted_record)
            else:
                self._send_json({"error": f"Transaction {tx_id} not found"}, 404)
        else:
            self._send_json({"error": "endpoint not found"}, 404)


def run(server_class=HTTPServer, handler_class=SMSHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
