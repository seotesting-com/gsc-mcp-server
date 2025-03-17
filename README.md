# Google Search Console MCP Server
## 🚀 Introduction: Setting Up MCP Server  

In this tutorial, we’ll walk you through the process of setting up your own MCP [Model Context Protocol](https://modelcontextprotocol.io/introduction) server, adding it to Claude Desktop, and integrating it with Google Search Console (GSC) data. This will allow you to compare time periods to identify SEO improvements, generate visual reports like bar charts and line graphs, and uncover optimization opportunities by analyzing click-through rates, impressions, and ranking shifts.

![image](https://github.com/user-attachments/assets/691fb2d0-4d37-4c16-aee6-98931dfbcc7c)

Let’s get started! 🚀

## 🔹 What We'll Cover:  
1. **Generate Google Cloud Credentials** – Create and download a service account JSON key to authenticate API access.  
2. **Install Required Tools** – Ensure Python, pip, uv, and Git (optional) are installed on your system.  
3. **Set Up the MCP Server** – Clone the repository, configure your environment, and install the MCP server.  
4. **Enable Search Console Insights** – Verify that the MCP server is running correctly in Claude Desktop and start using advanced search analytics tools.  

By the end of this guide, you'll be able to run queries, visualize data, and optimize your website’s search performance with ease. Let's get started! 🚀

## 🔹 What You Need to Know
This tutorial is designed to be beginner-friendly, and you don’t need any advanced technical skills. However, you should be comfortable running commands in the command line (also known as the terminal or command prompt).

Throughout this guide, you'll enter commands like:

```sh
python --version
git clone <repository-url>
```
If you’ve never used the command line before, don’t worry! Just follow the instructions step by step, and you'll be good to go.

That’s all you need— let’s get started! 🚀
---

# 🎯 Part 1 - Generate a JSON Credentials File

Follow these steps to create and download a **service account JSON key** from Google Cloud Console.  If you already have a JSON credentials file, you can skip this part.


## 📌 1. Go to Google Cloud Console  
🔗 [Visit Google Cloud Console](https://console.cloud.google.com/)  


## 📌 2. Select Your Project  
- Click on the **project selector** at the top.  
![image](https://github.com/user-attachments/assets/642ec31f-ae73-4a3f-b031-99c73af6803c)

- Select an **existing project** or create a **new one**.  

### If you're creating a new project:

#### Enable Search Console API
- Make sure your new project is selected 
- Click on **APIs and Services**:
![image](https://github.com/user-attachments/assets/75a33e90-b552-44a0-ab9e-8fd040762325)

- Find Google Search Console API (you may need to search at the top)
![image](https://github.com/user-attachments/assets/891eb3e2-5370-4770-a676-423d4c9fc437)

- Click **"Enable"**
- Return to the dashboard (click the **"Google Cloud"** icon)


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
6. Copy the path of JSON file (right click + 'Copy as path')

## 📌 8. Add the Service Account to Google Search Console
1. Open [Google Search Console](https://search.google.com/search-console).
2. Select the website property.
3. Click **Settings** (bottom left).
4. Under **Users and Permissions**, click **Add User**.
5. Enter the service account email (from step 4).
6. Assign permissions:
    - Restricted (view data only).
    - Full (view & manage property).
7. Click **Add**.

---

# 🎯 Part 2 - Install Required Tools

Before you begin working with the project, ensure that you have the necessary tools installed. Follow these steps to check if everything is ready.

## 📌 1. Check if Python is Installed

Check if Python is installed on your system by running the following command:

### On **Windows**:
```sh
python --version
```
### On **Linux/macOS**:
```sh
python3 --version
```

If Python is installed, you will see the version number. If not, download and install it from 🔗 [Download Python](https://www.python.org/downloads/)  

## 📌 3. Check if pip is Installed
pip is the package manager for Python. To check if it's installed, run the following command:

### On **Windows**:
```sh
pip --version
```

### On **Linux/macOS**:
```sh
pip3 --version
```
If pip is not installed, follow the official installation guide 🔗 [Download pip](https://pip.pypa.io/en/stable/installation/)

## 📌 2. Check if uv is Installed
uv is a Python package and project manager. To check if it's installed, run the following command:

### On **Linux/macOS/Windows**:
```sh
uv --version
```
If uv is not installed, follow the official installation guide 🔗 [Download uv](https://docs.astral.sh/uv/getting-started/installation/)

## 📌 3. Check if Claude Desktop is Installed

If Claude Desktop is not installed, follow the official installation guide 🔗 [Download Claude Desktop](https://claude.ai/) .

## 📌 4. Check if Git is Installed (optional)

Check if Git is installed on your system by running the following command:

### On **Linux/macOS/Windows**:
```sh
git --version
```
If Git is installed, you will see the version number. If not, you can still download the program files, or you can download and install Git from 🔗 [Download Git](https://git-scm.com/downloads)  

---

# 🎯 Part 3 - Add the MCP server to Claude Desktop

## Setup Instructions

### 1. Clone the Repository

Open a new terminal in the folder where the files will be downloaded to. Run the following commands:

```bash
git clone https://github.com/seotesting-com/gsc-mcp-server.git
cd gsc-mcp-server
```

#### If you don't have Git installed:

- Download the ZIP file:

![image](https://github.com/user-attachments/assets/10cdbb1f-c58e-4218-b5cc-c8f858f489c7)


### 2. Create and Activate a Virtual Environment

```bash
# Windows
uv venv
.venv\Scripts\activate

# macOS/Linux
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Windows/macOS/Linux
uv sync
```

### 4. Install MCP Server 

Add the path to your JSON credentials file and run the following command:

```bash
mcp install server.py -v GOOGLE_APPLICATION_CREDENTIALS=<path to credentials file>
```

Make sure you replace `<path to credentials file>` with the path to your JSON credentials file eg. `C:\Users\Me\Downloads\credentials.json` . 

### 5. Restart Claude Desktop

You may need to end Claude tasks in the task manager. 

---

# 🎯 Part 4 - Get Search Console Insights 

Open Claude Desktop. If the MCP server has been configured correctly, you should be able to see 5 additional tools available in the chat box:

![image](https://github.com/user-attachments/assets/8fe45b5b-afc1-4c39-849d-853297cab1d6)

You can use the tools by asking Claude to perform various search console analytics tasks. Before invoking a tool, Claude will ask permission. You should click one of the 'allow' options to use the MCP server:

![image](https://github.com/user-attachments/assets/6b63b312-c1c2-46ff-ab75-b3d640fe6a2a)

### Getting Started Prompts

- "List all my verified sites in Google Search Console"
- "Show me search analytics for example.com from January 1 to January 31, 2025"
- "Compare search performance for example.com between last month and the previous month"
- "What are my top 10 pages by clicks for the last 30 days?"
- "Show me search trends by week for the last 3 months"

### Data Visualization Prompts

- "Generate a bar chart of my top 5 performing pages by clicks for the past month"
- "Create a line graph showing impression trends over the last 90 days"
- "Visualize the CTR comparison between mobile and desktop traffic for my site"
- "Plot a heatmap of search performance by country for example.com"
- "Create a pie chart showing the distribution of traffic by device type"
- "Generate a scatter plot comparing CTR vs. position for my top 50 queries"
- "Show me a visual breakdown of traffic sources by search type (web, image, video)"
- "Create a stacked area chart showing clicks and impressions over time"
- "Visualize week-over-week search performance changes with a comparison chart"
- "Generate a visual report of my site's SEO performance with multiple graphs"

### Search Console Analysis Prompts

- "Identify keywords with high impressions but low CTR that I can optimize"
- "Show me pages that have dropped in rankings over the last month"
- "Find new keywords that my site started ranking for in the past 30 days"
- "Analyze which mobile pages have the biggest performance gap compared to desktop"
- "Show me queries where I rank on page 2 (positions 11-20) that I could push to page 1"
- "Identify seasonal trends in my search traffic over the past year"
- "Compare organic traffic before and after my site redesign on March 1st"
- "Show me which countries have the highest growth potential based on impressions vs. clicks"
- "Analyze the correlation between average position and CTR for my top 100 queries"
- "Generate a prioritized list of optimization opportunities based on potential traffic gains"

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

# 🛠 Troubleshooting
If you encounter any issues while setting up or using the MCP server, try the following solutions:

## 1️⃣ Restart Claude Desktop
Sometimes, tools don’t appear immediately. Restart Claude Desktop and try again.
You may need to end the Claude process in Task Manager (Windows) or Activity Monitor (Mac) before restarting.
## 2️⃣ Wait a Few Minutes
After setting up the MCP server, the new tools might take a few minutes to load.
If they don’t appear right away, wait a few minutes and try again.
## 3️⃣ Check the JSON Credentials File
Ensure the service account JSON file is in an accessible folder.
Avoid placing it in a restricted or admin-only folder (e.g., C:\Program Files\ on Windows or ~/Library/ on macOS).
If necessary, move it to a more accessible location like your Documents or Desktop folder.
## 3️⃣ Check the Claude configuration
Go to **File => Settings** and click on the **Developer** tab. When you click on **Search Console Analytics**, it should display a status of 'running'. If not, there may be an error message providing details of what is causing the connection issue.
![image](https://github.com/user-attachments/assets/acfd8ea2-17d8-4d01-8132-18a913b99766)

Click on **Edit Config** and open **'claude_desktop_config.json'** in a text editor. It should contain:

```sh
{
  "mcpServers": {
    "Search Console Analytics": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "google-api-python-client",
        "--with",
        "google-auth",
        "--with",
        "mcp[cli]",
        "--with",
        "pandas",
        "mcp",
        "run",
        "C:\\Documents\\gsc-mcp-server\\server.py"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\Path\\To\\Credentials\\gscaccess-credentials.json"
      }
    }
  }
}
```

If it contains something else, paste this data into file and make sure you update the file paths for the server.py file and the credentials file. Make sure to escape backslash characters (as shown). Restart Claude.

If you're still having issues, retrace your steps and ensure everything is set up correctly. 🚀
