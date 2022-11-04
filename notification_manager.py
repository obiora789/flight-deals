from twilio.rest import Client
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.to_phone = os.getenv("TO_PHONE")
        self.from_phone = os.environ.get("FROM_PHONE")

    def send_notification(self, deal_price, dept_city, iata_dep, dest_city, iata_dest, date_7, date_28):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=f"Low price alert! Only ₦{deal_price} to fly from {dept_city}({iata_dep}) to "
                 f"{dest_city}({iata_dest}), from {date_7} to {date_28}.",
            from_=self.from_phone,
            to=self.to_phone
        )
        print(message.status)
