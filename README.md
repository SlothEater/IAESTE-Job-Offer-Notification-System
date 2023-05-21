IAESTE Job Offer Notification System
====================================

This project extracts job offer data from the IAESTE website and notifies users of new job offers that match their interests via a Telegram bot. IAESTE, or the International Association for the Exchange of Students for Technical Experience, is a global organization that provides students in STEM fields with opportunities for internships and work experience abroad. The IAESTE website is regularly updated with new job offers, and it can be time-consuming for users to manually check for new offers that match their interests.

Project Overview
----------------

The IAESTE Job Offer Notification System automates the process of checking for new job offers and sends notifications to users via a Telegram bot. The system consists of three main components:

1.  Web scraper - A Python script that logs into the IAESTE website, downloads the latest job offer data in CSV format, and saves it to a local directory.

2.  Data transformer - A Python script that transforms the CSV data into a more user-friendly format by cleaning, filtering, and sorting the data.

3.  Notification system - A Telegram bot that sends notifications to users of new job offers that match their interests.

How It Works
------------

1.  The web scraper logs into the IAESTE website using user credentials stored in a configuration file.

2.  The scraper downloads the latest job offer data in CSV format and saves it to a local directory.

3.  The data transformer script reads in the CSV data and applies several cleaning, filtering, and sorting operations to create a more user-friendly format.

4.  The notification system (Telegram bot) is configured with a list of relevant faculty codes (e.g. "14D" for mechanical engineering) that users can subscribe to (by adding them to [this](src/constants/relevantFacultyCodes.py)).

5.  The notification system reads in the transformed data and compares it with the previously saved data to identify new job offers that match the users' subscribed faculty codes.

6.  If there are new job offers, the notification system sends notifications to the subscribed users via the Telegram bot.

Getting Started
---------------

To get started with the IAESTE Job Offer Notification System, you will need to have Python 3.x installed. Packages can be installed via terminal using:

```
pip install -r requirements.txt
```

You will also need to set up a Telegram bot and obtain a bot token. Instructions for setting up a Telegram bot can be found [here](https://core.telegram.org/bots#creating-a-new-bot).

Next, you need to follow the steps mentioned [here](https://developers.google.com/gmail/api/quickstart/python) to get the `credentials.json` file for Gmail API. Once you have obtained the file, place it in the `src/config` directory as `credentials.json`.

In addition to the Gmail API credentials, you will also need to add your IAESTE Platform login credentials to the system. Create a file named `credentials.ini` in the `src/config` directory and add your login credentials in the following format:

```ini
[login]
email = 'email_on_IAESTE_platform_account'
password = 'password_on_IAESTE_platform_account'
```

Note that you may need to modify other configuration settings (e.g., save locations, faculty codes) to fit your specific use case.

Once you have installed the required packages, obtained the Telegram bot token, and set up the credentials files, you can run the main script to start the system.

```
python main.py
```

The system will automatically check for new job offers and send notifications to the subscribed users via the Telegram bot.

Please make sure to follow the steps accurately and replace `email_on_IAESTE_platform_account` and `password_on_IAESTE_platform_account` in the `credentials.ini` file with your actual IAESTE Platform login credentials.

Conclusion
----------

The IAESTE Job Offer Notification System provides a simple and efficient way for IAESTE users to stay up-to-date on the latest job offers that match their interests. By automating the process of checking for new offers and sending notifications via Telegram, users can save time and focus on applying for the best opportunities available to them.

Contributors
------------

-   [Daniel Azzopardi](https://github.com/SlothEater) - Creator and Maintainer
-   [Amy Calleja](https://github.com/AmyCalleja) - Tester and Passenger Princess

License
-------

This project is licensed under the MIT License
