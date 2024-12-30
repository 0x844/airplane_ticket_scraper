# ✈️ Airline Ticket Price Scraper
This project automates the process of scraping flight ticket prices from websites, providing users with affordable ticket options and notifications.

### ✨ Features
💰 Price Extraction: Automatically retrieves affordable airline ticket prices.
🌐 Efficient Web Scraping: Employs XPath queries to collect airline details and travel locations.
📧 Email Notifications: Sends scraped flight data to users through automated emails.

### 🛠️ Technologies Used
**💻 Programming Language:** Python

**📦 Libraries and Tools:**
- Selenium for web scraping and browser automation.
- Pandas for data organization and manipulation.
- Email Automation for timely updates to users.
  
### 🚀 Code Workflow
- **🌍 Initialize Browser:** Configure headless Chrome for scraping.
- **🛫 User Inputs:** Gather departure, destination, and travel dates.
- **🔍 Scrape Flight Data:** Navigate to travel websites, input search details, and collect flight information using Selenium and XPath queries.
- 📄 **Format Data**: Organize extracted data into a readable format with departure time, arrival time, price, and travel duration.
- **📧 Send Notifications:** Email the formatted data to users with Pandas and EmailMessage.

**🎯 Goal:** Enable users to make informed travel decisions by providing timely and accurate flight price updates through automation.
