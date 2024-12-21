import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
import time  # Import the time module to resolve the error

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'raj.gautam41@gmail.com'  # Replace with your email
SMTP_PASSWORD = 'tole tpwz opco zzyw'  # Replace with your app password (not regular password)
FROM_EMAIL = 'raj.gautam41@gmail.com'
TO_EMAILS = ['raj.gautam41@gmail.com', 'yashwanthprakaash@gmail.com', 'kuthadi.jayanthika01@gmail.com']


def send_email(subject, body):
    """Sends an email with the given subject and body."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = ', '.join(TO_EMAILS)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())
            print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def fetch_and_send_jobs():
    """Fetches job listings from Sodexo and sends an email with the details."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(
            'https://jobs.us.sodexo.com/hourly-jobs?page_size=50&page_number=1&location=1-33628&radius=0&locationDescription=city&locationName=Flagstaff%2C%20AZ&sort_by=start_date&sort_order=DESC&custom_categories=Culinary%20and%20Food%20Services&custom_categories=Administrative&custom_categories=Facilities%20Maintenance&custom_categories=Nutrition%20and%20Dietetics&custom_categories=Custodial&custom_categories=Transportation&custom_categories=Student&custom_categories=Retail%20and%20Customer%20Services&custom_categories=Sodexo%20Live!%20-%20Hourly&custom_categories=Sodexo%20-%20Hourly&custom_categories=SodexoMagic%20-%20Hourly&custom_categories=Vending%20-%20Hourly&custom_categories=Food%20Service%20-%20Hourly&custom_categories=Environmental%20Services%20%2F%20Custodial%20-%20Hourly&custom_categories=not%20set%20-%20Hourly&custom_categories=Facilities%20-%20Hourly&custom_categories=Administrative%20-%20Hourly&custom_categories=Culinary%20-%20Hourly&custom_categories=Laundries%20-%20Hourly&custom_categories=Marketing%20-%20Hourly&custom_categories=Nutrition%20-%20Hourly&custom_categories=Hidden%20(14237)%20-%20Hourly&custom_categories=Human%20Resources%20-%20Hourly&custom_categories=Engineering%20-%20Hourly&custom_categories=Hidden%20(8723)%20-%20Hourly&custom_categories=Labor%20Management%20-%20Hourly&custom_categories=Hidden%20(221676)%20-%20Hourly&custom_categories=Communications%20-%20Hourly&custom_categories=Hidden%20(14226)%20-%20Hourly&custom_categories=SodexoLive!%20-%20Hourly')

        # Wait for the element with total jobs count to load
        wait = WebDriverWait(driver, 15)
        total_jobs_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".results-header__content-total"))
        )
        total_jobs_text = total_jobs_element.text.strip()

        # Prepare email body with the total jobs count
        email_body = f"Total number of job listings found: {total_jobs_text}\n\n"
        print(f"Total jobs: {total_jobs_text}")

        # Find job listings and extract job titles and links
        job_containers = driver.find_elements(By.CLASS_NAME, 'c-jobs-list')

        if job_containers:
            for job_container in job_containers:
                job_links = job_container.find_elements(By.TAG_NAME, 'a')
                for job in job_links:
                    job_title = job.text.strip()
                    job_link = job.get_attribute('href')
                    if job_link and job_title and job_title != "Apply Now":
                        email_body += f"{job_title}: {job_link}\n"
                        print(f"{job_title}: {job_link}")
        else:
            email_body += "No job listings found."

        # Send the email
        send_email("Sodexo Job Listings Update", email_body)

    except Exception as e:
        print(f"Error fetching jobs: {e}")

    finally:
        driver.quit()


def main():
    """Main function to repeatedly fetch and send job updates."""
    while True:
        fetch_and_send_jobs()
        next_email_time = datetime.now() + timedelta(minutes=30)
        print(f"Next email scheduled for {next_email_time.strftime('%Y-%m-%d %H:%M:%S')}.")

        while datetime.now() < next_email_time:
            remaining = next_email_time - datetime.now()
            minutes_left = remaining.seconds // 60
            seconds_left = remaining.seconds % 60
            print(f"\rTime until next email: {minutes_left:02d}:{seconds_left:02d}", end="")
            time.sleep(1)  # Update every second to show live countdown


if __name__ == "__main__":
    main()
