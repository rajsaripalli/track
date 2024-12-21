import smtplib
import time
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # SMTP server (e.g., smtp.gmail.com)
SMTP_PORT = 587  # Typically 587 for TLS
SMTP_USER = 'raj.gautam41@gmail.com'  # Your Gmail address
SMTP_PASSWORD = 'tole tpwz opco zzyw'  # Your generated App Password (NOT your regular Gmail password)
FROM_EMAIL = 'raj.gautam41@gmail.com'

# List of recipient email addresses
TO_EMAILS = ['raj.gautam41@gmail.com', 'yashwanthprakaash@gmail.com','kuthadi.jayanthika01@gmail.com']  # Add multiple email addresses here

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = ', '.join(TO_EMAILS)  # Join the recipient list as a comma-separated string

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USER, SMTP_PASSWORD)  # Log in using your credentials
            server.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())  # Send the email to all recipients
            print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to fetch job listings and send email
def fetch_and_send_jobs():
    # Start the Safari browser and open the URL
    driver = webdriver.Safari()

    # Open the Sodexo job listings URL
    driver.get(
        'https://jobs.us.sodexo.com/hourly-jobs?page_size=20&page_number=1&location=1-33628&radius=0&locationDescription=city&locationName=Flagstaff%2C%20AZ&sort_by=start_date&sort_order=DESC&custom_categories=Culinary%20and%20Food%20Services&custom_categories=Administrative&custom_categories=Facilities%20Maintenance&custom_categories=Nutrition%20and%20Dietetics&custom_categories=Custodial&custom_categories=Transportation&custom_categories=Student&custom_categories=Retail%20and%20Customer%20Services&custom_categories=Sodexo%20Live!%20-%20Hourly&custom_categories=Sodexo%20-%20Hourly&custom_categories=SodexoMagic%20-%20Hourly&custom_categories=Vending%20-%20Hourly&custom_categories=Food%20Service%20-%20Hourly&custom_categories=Environmental%20Services%20%2F%20Custodial%20-%20Hourly&custom_categories=not%20set%20-%20Hourly&custom_categories=Facilities%20-%20Hourly&custom_categories=Administrative%20-%20Hourly&custom_categories=Culinary%20-%20Hourly&custom_categories=Laundries%20-%20Hourly&custom_categories=Marketing%20-%20Hourly&custom_categories=Nutrition%20-%20Hourly&custom_categories=Hidden%20(14237)%20-%20Hourly&custom_categories=Human%20Resources%20-%20Hourly&custom_categories=Engineering%20-%20Hourly&custom_categories=Hidden%20(8723)%20-%20Hourly&custom_categories=Labor%20Management%20-%20Hourly&custom_categories=Hidden%20(221676)%20-%20Hourly&custom_categories=Communications%20-%20Hourly&custom_categories=Hidden%20(14226)%20-%20Hourly&custom_categories=SodexoLive!%20-%20Hourly'
    )

    # Wait for the page to load fully (adjust the wait time if needed)
    time.sleep(3)

    # Find the total number of job listings
    total_jobs_element = driver.find_element(By.CLASS_NAME, 'results-header__content-total')
    total_jobs_text = total_jobs_element.text.strip()

    # Prepare email body with total number of jobs
    email_body = f"Total number of job listings found: {total_jobs_text}\n\n"
    print(f"Total number of job listings found: {total_jobs_text}\n")  # Print the total count to the screen

    # Find all the job listing containers by class name
    job_listings = driver.find_elements(By.CLASS_NAME, 'c-jobs-list')

    if job_listings:
        # Iterate over each job listing container
        for job_container in job_listings:
            # Extract the <a> tags that hold the job titles and links
            job_links = job_container.find_elements(By.TAG_NAME, 'a')

            # For each <a> tag, extract job title and link (excluding "Apply Now")
            for job in job_links:
                job_title = job.text.strip()  # Clean up any extra whitespace
                job_link = job.get_attribute('href')

                # Only append job links that are not "Apply Now"
                if job_link and job_title and job_title != "Apply Now":
                    email_body += f"{job_link} {job_title}\n"
                    print(f"{job_link} {job_title}")  # Print the job link and title to the screen
    else:
        email_body += "No job listings found."
        print("No job listings found.")

    # Send the email
    send_email("Sodexo Job Listings Update", email_body)

    # Close the browser
    driver.quit()

# Function to print the timer countdown
def print_timer(next_time):
    while True:
        now = datetime.now()
        time_left = next_time - now
        if time_left.total_seconds() > 0:
            minutes_left = time_left.total_seconds() / 60
            print(f"\rNext email will be sent in {minutes_left:.0f} minutes.", end="")
            time.sleep(10)  # Update every 10 seconds
        else:
            break

# Run the script every minute
while True:
    fetch_and_send_jobs()

    # Calculate the time when the next email will be sent (in 30 minutes)
    next_email_time = datetime.now() + timedelta(minutes=30)

    # Print the time until the next email is sent (live countdown)
    print_timer(next_email_time)

    # Wait for the next cycle to begin (1 minute)
    time.sleep(60)
