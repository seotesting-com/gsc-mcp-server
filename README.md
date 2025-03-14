# 🎯 Part 1 - Generate a JSON Credentials File for Google Cloud Console  

Follow these steps to create and download a **service account JSON key** from Google Cloud Console.  


## 📌 1. Go to Google Cloud Console  
🔗 [Visit Google Cloud Console](https://console.cloud.google.com/)  


## 📌 2. Select Your Project  
- Click on the **project selector** at the top.  
- Select an **existing project** or create a **new one**.  


## 📌 3. Open the IAM & Admin Section  
- In the left menu, go to **"IAM & Admin" > "Service Accounts"**.  


## 📌 4. Create a New Service Account  
1. Click **"Create Service Account"**.  
2. Enter a **name** (e.g., `my-app-service-account`).  
3. Click **"Create and Continue"**.  


## 📌 5. Assign Permissions  
- Choose a role (e.g., **Editor**, **Owner**).  
- Click **"Continue"**.  


## 📌 6. Skip Granting Users Access (Optional)  
- Click **"Done"** (no need to add users).  


## 📌 7. Generate the JSON Key  
1. Find your **service account** in the list.  
2. Click the **3 dots (⋮)** on the right and select **"Manage Keys"**.  
3. Click **"Add Key" > "Create New Key"**.  
4. Choose **"JSON"** format and click **"Create"**.  
5. **✅ The JSON file will download automatically.**  

---

# 🎯 Part 2 - Check that All Necessary Tools Are Installed  

Before you begin working with the project, ensure that you have the necessary tools installed. Follow these steps to check if everything is ready.

## 📌 1. Check if Git is Installed

Check if Python is installed on your system by running the following command:

### On **Linux/macOS/Windows**:
```sh
git --version
```
If Git is installed, you will see the version number. If not, download and install it from 🔗 [Download Git](https://git-scm.com/downloads)  

## 📌 2. Check if Python is Installed

Check if Python is installed on your system by running the following command:

### On **Linux/macOS/Windows**:
```sh
python --version
```
If Python is installed, you will see the version number. If not, download and install it from 🔗 [Download Python](https://www.python.org/downloads/)  

## 📌 3. Check if pip is Installed
pip is the package manager for Python. To check if it's installed, run the following command:

### On **Linux/macOS/Windows**:
```sh
pip --version
```
If pip is not installed, follow the official installation guide 🔗 [Download pip](https://pip.pypa.io/en/stable/installation/)

## 📌 3. Check if uv is Installed
uv is a Python package and project manager. To check if it's installed, run the following command:

### On **Linux/macOS/Windows**:
```sh
uv --version
```
If uv is not installed, follow the official installation guide 🔗 [Download uv](https://docs.astral.sh/uv/getting-started/installation/)

## 📌 4. Check if Claude Desktop is Installed

If Claude Desktop is not installed, follow the instructions in the official Claude installation guide.

---

# 🎯 Part 3 - Add the MCP server to Claude Desktop

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <https://github.com/yourusername/mcp-test-v3.git>
cd <mcp-test-v3>
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install MCP Server 

```bash
mcp install server.py -v GOOGLE_APPLICATION_CREDENTIALS=<path to credentials file>
```
### 5. Restart Claude Desktop

## Usage

Once installed in Claude Desktop, you can use the tool by asking Claude to perform various search console analytics tasks:

### Example Prompts

- "List all my verified sites in Google Search Console"
- "Show me search analytics for example.com from January 1 to January 31, 2025"
- "Compare search performance for example.com between last month and the previous month"
- "What are my top 10 pages by clicks for the last 30 days?"
- "Show me search trends by week for the last 3 months"

## Available Tools

### list_sites

Lists all verified sites in your Google Search Console account.

### query_search_analytics

```
Parameters:
- site_url: Full URL of your website (e.g., https://www.example.com/)
- start_date: Start date in YYYY-MM-DD format
- end_date: End date in YYYY-MM-DD format
- dimensions: List of dimensions (query, page, device, country, date)
- search_type: Type of search results (web, image, video, news, discover, googleNews)
- row_limit: Number of rows to return (max 25000)
```

### compare_time_periods

```
Parameters:
- site_url: Full URL of your website
- current_start_date: Start date for current period in YYYY-MM-DD format
- current_end_date: End date for current period in YYYY-MM-DD format
- previous_start_date: Start date for previous period in YYYY-MM-DD format
- previous_end_date: End date for previous period in YYYY-MM-DD format
- dimensions: List of dimensions (query, page, device, country, date)
- search_type: Type of search results
- row_limit: Number of rows to return
```

### get_top_performing_content

```
Parameters:
- site_url: Full URL of your website
- start_date: Start date in YYYY-MM-DD format
- end_date: End date in YYYY-MM-DD format
- metric: Metric to sort by (clicks, impressions, ctr, position)
- limit: Number of results to return
```

### get_search_trends

```
Parameters:
- site_url: Full URL of your website
- start_date: Start date in YYYY-MM-DD format
- end_date: End date in YYYY-MM-DD format
- interval: Time interval for grouping (day, week, month)
```
