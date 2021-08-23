# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from user import User
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# takes in two users.buyer and seller, and the listing and sends the seller email to the seller.


def sendSellerPurchaseEmail(buyer, seller, listing):
    receiver_email = seller.getEmail()
    subject = 'Rebook Purchase'
    body = '<p>This email is to notify you that <strong>{buyer}</strong>  has decided to buy your book, <em>{title}</em>, for ${price}.</p>'.format(buyer=buyer.getNetID(), title=listing['title'], price=listing['price']) + \
        '<p>Their contact information is <strong>{email}</strong>. They have received your contact information too. Please get in touch with the buyer to work out the logistics of the payment and delivery.</p>'.format(email=buyer.getEmail()) + \
        '<p>Also, please <strong>Confirm</strong> the transaction on our website by clicking the check mark button in the "pending" tab of your Seller Station once you have delivered the book! This will keep the listing status up to date.</p>' + \
        '<p>You can always cancel the transaction on the rebook website!</p>' + \
        '<p>Thanks for choosing Rebook!</p>' + \
        '<p>The <a href=https://princetonrebook.herokuapp.com>Rebook</a> Team </p>'
    
    sendEmail(receiver_email, subject, body)

# takes in two users.buyer and seller, and the listing and sends the buyer email to the buyer.


def sendBuyerPurchaseEmail(buyer, seller, listing):
    receiver_email = buyer.getEmail()
    subject = 'Rebook Purchase'
    body = '<p>You have successfully placed your order on <em>{title}</em> for ${price}.</p>'.format(title=listing['title'], price=listing['price']) + \
        '<p>The seller is <strong>{seller}.</strong> Their contact information is <strong>{email}</strong>. They have received your contact information too. Please organize payment and delivery conditions amongst yourselves. </p>'.format(seller=seller.getNetID(), email=seller.getEmail()) + \
        '<p>Once you have received your book from the seller, be sure to remind the seller to click the check mark button in the "pending" tab of their Seller Station to ensure that the records are updated.</p>' + \
        '<p>You can always find this information in your Buyer Bookbag tab.</p>' + \
        '<p>Thanks for choosing Rebook!</p>' + \
        '<p>The <a href=https://princetonrebook.herokuapp.com>Rebook</a> Team </p>'
    
    sendEmail(receiver_email, subject, body)


def sendBuyerCancelEmail(buyer, seller, listing):
    receiver_email = buyer.getEmail()
    subject = 'Rebook Cancellation'
    body = '<p>Your order on <em>{title}</em> for ${price} has been cancelled.</p>'.format(title=listing['title'], price=listing['price']) + \
        '<p>The listing is now back on the search page and is up for grabs by another buyer.</p>' + \
        '<p>If you did not make this cancellation, please contact the seller <strong>{seller}</strong> at <strong>{email}</strong> for more information.</p>'.format(seller=seller.getNetID(), email=seller.getEmail()) + \
        '<p>Thanks for choosing Rebook!</p>' + \
        '<p>The <a href=https://princetonrebook.herokuapp.com>Rebook</a> Team </p>'
    
    sendEmail(receiver_email, subject, body)


def sendSellerCancelEmail(buyer, seller, listing):
    receiver_email = seller.getEmail()
    subject = 'Rebook Cancellation'
    body = '<p>The order on your book, <em>{title}</em>, for ${price} has been cancelled.</p>'.format(title=listing['title'], price=listing['price']) + \
        '<p>The listing is now back on the search page and is up for grabs by another buyer.</p>' + \
        '<p>If you did not make this cancellation, please contact the buyer <strong>{buyer}</strong> at <strong>{email}</strong> for more information.</p>'.format(buyer=buyer.getNetID(), email=buyer.getEmail()) + \
        '<p>Thanks for choosing Rebook!</p>' + \
        '<p>The <a href=https://princetonrebook.herokuapp.com>Rebook</a> Team </p>'

    sendEmail(receiver_email, subject, body)
    

# Takes in an receiver email, subject, and body as an html string and then sends the email from princetonrebook@gmail.com


def sendEmail(receiver_email, subject, body):
    load_dotenv()
    sender_email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Add HTML parts to MIMEMultipart message
    body = MIMEText(body, "html")
    message.attach(body)

    try: 
    # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print('Email failed to send')
        print(e)

if __name__ == "__main__":
    main()

