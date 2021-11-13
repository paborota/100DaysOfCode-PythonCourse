from amazon_interface import AmazonInterface
from email_sender import EmailSender


PRODUCT_URL = "https://www.amazon.com/ZOTAC-GeForce-Graphics-IceStorm-ZT-A30600H-10M/dp/B08W8DGK3X/ref=sr_1_3?crid=1J0CA6D3XQE83&keywords=gpu+graphics+card&qid=1636785570&qsid=136-1673993-0237851&sprefix=gpu%2Caps%2C282&sr=8-3&sres=B08W8DGK3X%2CB09CG64Y3Q%2CB0985VND1G%2CB0985Z47C8%2CB09F8CWCFZ%2CB08ZZW34T3%2CB09GHZGD5X%2CB07Z8PWC6R%2CB07R18TH1X%2CB08WHJPBFX%2CB07P163DGH%2CB08YWZHJDZ%2CB06Y66K3XD%2CB08G5CQMJ3%2CB00Q7O7PQA%2CB08WPRMVWB&srpt=VIDEO_CARD"
STANDARD_PRICE = 878.00
SAVINGS_BEFORE_ALERT = 25.0  # if difference from STANDARD_PRICE exceeds this much, it will send the email alert


if __name__ == "__main__":

    amazon_interface = AmazonInterface()
    product_name, current_price = amazon_interface.get_item(product_url=PRODUCT_URL)
    current_price = float(current_price.replace('$', ''))
    current_discount = STANDARD_PRICE - current_price

    if current_discount > -20.0:

        msg = "Subject:The item you were watching is on sale!\n\n" \
              f"The item: '{product_name}' is on sale at ${current_discount:.2f} off!\n\n" \
              f"Current price: {current_price}\n\n\n" \
              f"Product page: {PRODUCT_URL}"

        email_sender = EmailSender()
        email_sender.send_email_to_self(msg=msg)
