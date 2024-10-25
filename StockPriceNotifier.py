import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Stock price notifier class
class StockPriceNotifier:
    def __init__(self, stock_symbol, threshold, email, password, recipient_email, check_interval=60):
        self.stock_symbol = stock_symbol
        self.threshold = threshold
        self.email = email
        self.password = password
        self.recipient_email = recipient_email
        self.check_interval = check_interval

    def get_stock_price(self):
        stock = yf.Ticker(self.stock_symbol)
        price = stock.history(period='1d')['Close'].iloc[-1]  # Get the latest closing price
        return price

    def send_email(self, current_price):
        subject = f"Stock Price Alert for {self.stock_symbol}"
        body = f"The current price of {self.stock_symbol} is {current_price}, which meets your threshold of {self.threshold}."
        
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.recipient_email  # Send to the specified recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, self.recipient_email, msg.as_string())
                print(f"Email sent: {subject}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def start_monitoring(self):
        while True:
            current_price = self.get_stock_price()
            print(f"Current price of {self.stock_symbol}: {current_price}")

            # Check if the current price meets the threshold
            if current_price >= self.threshold:
                self.send_email(current_price)
            
            time.sleep(self.check_interval)

# Example usage
if __name__ == "__main__":
    # User-defined values
    stock_symbol = 'AAPL'  # Apple Inc.
    threshold = 150.00  # Set your price threshold
    email = 'silasokanla2006@gmail.com'  # Your email address
    password = ''  # Your app password
    recipient_email = 'okanlawonsilas@gmail.com'  # Recipient email address
    check_interval = 60  # Check every minute

    notifier = StockPriceNotifier(stock_symbol, threshold, email, password, recipient_email, check_interval)
    notifier.start_monitoring()
