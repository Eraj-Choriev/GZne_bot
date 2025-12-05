# GEMINI.md

## Project Overview

This project is a Telegram bot for selling digital goods. It is built using Python and the `python-telegram-bot` library. The bot supports multiple languages (Russian and Tajik) and allows users to browse products, initiate a purchase, and upload a proof of payment (receipt).

**Key Features:**

*   **Multi-language Support:** The bot's interface is available in Russian and Tajik, with localization strings stored in JSON files in the `locales/` directory.
*   **Product Catalog:** The bot features a hardcoded catalog of digital products, including game subscriptions, gift cards, and software.
*   **Simple "Purchase" Flow:** Users can select a product and a payment method. The bot then provides payment details and asks the user to upload a photo of their receipt to confirm the purchase.
*   **In-Memory State Management:** The bot currently uses a simple Python dictionary to manage user sessions and state. **Note: This is not suitable for production and will lose all data on restart.**

**Core Technologies:**

*   **Language:** Python 3
*   **Telegram Bot Framework:** `python-telegram-bot`
*   **Dependencies:** `python-dotenv` (inferred from `run.py`)

## Building and Running

1.  **Install Dependencies:**

    It appears the project is missing a `requirements.txt` file. Based on the source code, you will need to install the following packages:

    ```bash
    pip install python-telegram-bot python-dotenv
    ```

2.  **Configure Environment:**

    Create a `.env` file in the root of the project with the following content:

    ```
    BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
    ADMIN_ID=<YOUR_TELEGRAM_USER_ID>
    ADMIN_USERNAME=<YOUR_TELEGRAM_USERNAME>
    ```

3.  **Run the Bot:**

    ```bash
    python run.py
    ```

## Development Conventions

*   **Configuration:** All configuration and secrets are managed via environment variables loaded from a `.env` file, as defined in `bot/config.py`.
*   **Localization:** All user-facing strings are managed through the `bot/localization.py` module, which loads text from the JSON files in the `locales/` directory. To add a new string, add it to both `locales/ru.json` and `locales/tj.json`.
*   **State Management:** User state is currently handled by a global `USER_DATA` dictionary in `bot/main.py`. This is a major limitation and should be replaced with a persistent storage solution.
*   **Handlers:** The project has a `bot/handlers/` directory, but most of the handler logic is currently implemented directly in `bot/main.py`. New handlers should be added to the appropriate files in this directory.
*   **Entry Point:** The application is launched from `run.py`, which loads the environment variables and then calls the `run()` function in `bot/main.py`.
