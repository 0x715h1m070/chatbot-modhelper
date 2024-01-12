EN | [RU](README-ru.md)

<img src="/src/logo.png" width="40%">

# Chatbot for monitoring a game project

<details>
  
<summary><b>Sequence diagram chatbot</b></summary>

```mermaid
sequenceDiagram
    ModHelper->>+Website: Receiving requests from players
    Website-->>-ModHelper: Sending a list of requests
    ModHelper->>+Script: Checking the list for new requests
    Script->>+DB_Temp_requests: Saving a request
    DB_Temp_requests-->>-Script: Request saved
    Script-->>-ModHelper: New requests found
    ModHelper->>+Chat: Sending a notification to the moderators' chat
    Chat-->>-ModHelper: Notification has been sent
    ModHelper->>+Website: Verification of requests for review
    Website-->>-ModHelper: Request reviewed by moderator
    ModHelper->>+Script: Retain the moderator who reviewed the request
    Script->>+DB_Moderators: Saving a moderator
    DB_Moderators-->>-Script: Moderator saved
    Script-->>-ModHelper: The moderator and the number of requests processed are stored in DB
    ModHelper->>+Script: Remove the reviewed request from the list
    Script->>+DB_Temp_requests: Deleting an entry
    DB_Temp_requests-->>-Script: Entry deleted
    Script-->>-ModHelper: Request removed from the list
    ModHelper->>+Chat: Sending a notification to the moderators' chat
    Chat-->>-ModHelper: Notification has been sent
```

</details>

<details>
  
<summary><b>Screenshots</b></summary>

<p align="center">
  <img src="/src/screenshots/new_request.png">
</p>

<p align="center"> 
  <b>Изображение 1</b> - Notification in the moderators' chat about receiving a new request from the game project site
</p>

<p align="center">
  <img src="/src/screenshots/reviewed_request.png">
</p>

<p align="center"> 
  <b>Изображение 2</b> - Notification in the chat moderators about the consideration of the request
</p>

<p align="center">
  <img src="/src/screenshots/website_request.png">
</p>

<p align="center"> 
  <b>Изображение 3</b> - Screenshot of data from the game project website
</p>

<p align="center">
  <img src="/src/screenshots/bot_stats.png">
</p>

<p align="center"> 
  <b>Изображение 4</b> - Screenshot of the command "/bot_stats" which displays the list of moderators sorted in descending order
</p>

</details>

Developed in 2019, this chatbot stands as my inaugural significant individual project, boasting seamless functionality up to the present day. The primary objective is to automate and streamline the handling and monitoring of player requests for account unlocks across two distinct gaming projects.

Given the potential overlap in moderator teams across these projects, the bot is intricately designed to analyze account unlocking requests across all gaming project servers, promptly notifying the relevant moderators for swift action.

## 🎯 Primary Tasks and Features

- **Data Collection & Analysis:** Compiles and analyzes data from players' account unlock requests from the official websites of both gaming projects.
- **Automated Notifications:** Sends instant notifications to moderators via a chosen messenger concerning new requests that necessitate their intervention across all server instances.
- **Workflow Enhancement:** Aims to optimize moderator tasks, increasing overall productivity, and reducing response times for player account unlocking requests.
- **Optimization of workflow:** Simplification and acceleration of moderators' work.
- **Reduction of waiting time:** Reduced waiting time for response to unlock requests.

<details>
  <summary><b>📜 Command list</b></summary>
  
  - `/add_steam_id <SteamID>` - Adds SteamID to the blacklist.
  - `/delete_steam_id <SteamID>` - Removes SteamID from the blacklist.
  - `/list` - Get SteamID blacklisted.
  - `/bot_stats` - Get a list *(TOP)* of moderators.
  - `/on` - Enable notifications of new requests *(for the moderator who entered this command)*
  - `/off` - Turn off notifications of new requests *(for the moderator who entered this command)*.
  
</details>

## 📊 Additional Functionalities

- **Moderator Leaderboard:** The bot dynamically generates a leaderboard of gaming project moderators, reflecting the volume of requests each has managed. This aids in workload distribution and efficiency monitoring.
- **Steam ID Blacklist:** Incorporates a blacklist functionality housing Steam IDs of specific players who should not be unlocked. Instant notifications are dispatched to moderators upon detecting any unban requests for these IDs, preventing potential errors.

## 🛠️ Libraries and Dependencies

- **vk_api:** Facilitates interaction with the VK social network API.
- **requests:** Enables HTTP request handling and data retrieval from web pages.
- **bs4 (Beautiful Soup):** Empowers HTML content parsing and data extraction.
- **telebot:** Enables seamless integration with Telegram messenger for moderator notifications.
- **pytz:** Ensures efficient time zone management and timestamp handling within the project.
