from pf_flask_web.system12.pweb_requests import PWebRequests, HTTPResponse
from pf_messaging.structure.sms_abc import SMSABC


class GreenWebSMS(SMSABC):
    api_url: str = None
    token: str = None
    pweb_requests: PWebRequests = None
    send_to: str = None
    send_message: str = "Test SMS"
    send_others: dict = None

    def run(self):
        try:
            if not self.pweb_requests or not self.token or not self.send_to:
                return None
            data = {
                "token": self.token,
                "to": self.send_to,
                "message": self.send_message,
                "json": 1
            }
            response: HTTPResponse = self.pweb_requests.post(url="api.php", data=data)
            if response.httpCode != 200:
                print(f"Unable to send sms: {self.send_to}. Error: {response.data}")
                return None
            return response.data
        except Exception as e:
            print("Unable to sent GreenWeb sms: " + str(e))

    def setup(self, url: str, token: str, others: dict = None):
        self.api_url = url
        self.token = token
        self.pweb_requests = PWebRequests()
        self.pweb_requests.set_base(self.api_url)
        return self

    def send(self, to: str, message: str, others: dict = None):
        if not self.pweb_requests or not self.token:
            return None
        self.send_to = to
        self.send_message = message
        self.send_others = others
        self.start()

    def get_subscription_expiry(self, params: dict = None):
        pass

    def get_sent_total_count(self, params: dict = None):
        pass

    def check_sms_balance(self, params: dict = None):
        pass

    @staticmethod
    def send_sms(to: str, message: str):
        greenweb_sms = GreenWebSMS().setup(url="http://api.greenweb.com.bd/", token="9285091707168956382784ffb9250887582646b6c04034fb6abc")
        greenweb_sms.send(to=to, message=message)



