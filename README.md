# DropWire

**DropWire** is a lightweight, open-source automation pipeline that syncs research articles and bookmarked content from [Raindrop.io](https://raindrop.io) to Microsoft Teams channels and Google Sheets, enabling collaborative knowledge sharing and transparent tracking across a distributed team.

---

## 🚀 Features

- 📥 Authenticates with Raindrop.io using OAuth2 and pulls new bookmarks
- 🧠 Parses tags to determine destination (`#research` or `#article`)
- 🧾 Appends data to a Google Sheet for tracking and searchability
- 📣 Sends a formatted message to the correct Microsoft Teams channel via webhook
- 🕒 Runs automatically every 5 minutes via GitHub Actions (optional)

---

## 🧰 Tech Stack

- **Python** – core logic
- **Raindrop.io API** – fetch bookmarks
- **Google Sheets API** – log entries
- **Microsoft Teams Webhooks** – send messages
- **GitHub Actions** – schedule jobs for free

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/dropwire.git
cd dropwire
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with the following:

```env
RAINDROP_TOKEN=your_raindrop_access_token
RAINDROP_CLIENT_ID=your_raindrop_client_id
RAINDROP_CLIENT_SECRET=your_raindrop_client_secret
GOOGLE_SERVICE_ACCOUNT_JSON=path_to_google_creds.json
TEAMS_RESEARCH_WEBHOOK=https://outlook.office.com/webhook/...
TEAMS_ARTICLE_WEBHOOK=https://outlook.office.com/webhook/...
```

Also ensure your `.gitignore` excludes:
```
.env
*.json
```

### OAuth2 Authentication

DropWire now uses Raindrop's OAuth2 flow to securely authenticate access to your bookmarks. During the initial run, the script will open your browser, prompt you to log into Raindrop, and return an access token.

Once the token is displayed in your terminal, copy it into your `.env` file under `RAINDROP_TOKEN`.

You will also need to register an OAuth application in Raindrop.io and provide your:

- `RAINDROP_CLIENT_ID`
- `RAINDROP_CLIENT_SECRET`

You can set your redirect URI to `http://localhost:8000/callback` during app registration.

### 4. Set Up Google Sheets

- Create a Google Sheet with appropriate columns:  
  `Title | URL | Notes | Tags | Added By | Date Added | Category`
- Share it with your Google service account email (found in the JSON creds file).

---

## ⏰ Automation (Optional)

DropWire can run on a schedule using GitHub Actions. See `.github/workflows/dropwire.yml` for setup. This allows near real-time sync (~every 5 minutes).

---

## 📌 Tagging Conventions

Use hashtags in Raindrop notes or tags to define routing and metadata:
- `#research` → Research Teams Channel
- `#article` → Articles Teams Channel
- `#Ben`, `#Tom` → Contributor attribution
- `#April_2025`, `#AI`, `#Google` → Category/timestamping

---

## 🛣️ Roadmap

- [ ] Edit tracking from Raindrop to Sheet
- [ ] Teams → Raindrop two-way sync
- [ ] AI-powered tagging and summarization
- [ ] Notion or Airtable backend compatibility

---

## 📄 License

MIT License. Built for the Jisc AI Team.