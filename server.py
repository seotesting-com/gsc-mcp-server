from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import pandas as pd
from io import StringIO

from mcp.server.fastmcp import FastMCP, Context

# OAuth 2.0 scope required for Search Console API
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

# Create a simple MCP server
mcp = FastMCP(
    "Search Console Analytics",
    dependencies=["google-api-python-client", "google-auth", "pandas"]
)

@mcp.tool()
def list_sites(ctx: Context) -> str:
    """List all verified sites in Search Console."""
    try:
        # Get credentials file path from environment variable
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_file:
            return "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            
        if not os.path.exists(credentials_file):
            return f"Error: Credentials file not found at {credentials_file}"
        
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
            
        # Set up the Search Console API service
        service = build('webmasters', 'v3', credentials=credentials)
        
        # Get the list of verified sites
        sites_list = service.sites().list().execute()
        sites = [site['siteUrl'] for site in sites_list.get('siteEntry', [])]
        
        if not sites:
            return "No verified sites found."
        
        return "\n".join([f"- {site}" for site in sites])
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def query_search_analytics(
    site_url: str, 
    start_date: str, 
    end_date: str, 
    ctx: Context,
    dimensions: list = None,
    search_type: str = "web",
    row_limit: int = 1000
) -> str:
    """
    Query Search Console analytics data for a site.
    
    Args:
        site_url: Full URL of your website (e.g., https://www.example.com/ or sc-domain:example.com)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        dimensions: List of dimensions (query, page, device, country, date)
        search_type: Type of search results (web, image, video, news, discover, googleNews)
        row_limit: Number of rows to return (max 25000)
    """
    try:
        # Get credentials file path from environment variable
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_file:
            return "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            
        if not os.path.exists(credentials_file):
            return f"Error: Credentials file not found at {credentials_file}"
        
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
            
        # Set up the Search Console API service
        service = build('webmasters', 'v3', credentials=credentials)
        
        # Validate inputs
        valid_dimensions = ['query', 'page', 'country', 'device', 'date']
        if dimensions:
            for dim in dimensions:
                if dim not in valid_dimensions:
                    return f"Invalid dimension: {dim}. Valid dimensions are: {', '.join(valid_dimensions)}"
        
        # Validate row_limit
        if row_limit < 1 or row_limit > 25000:
            return "row_limit must be between 1 and 25000"
            
        # Validate search_type
        valid_search_types = ['web', 'image', 'video', 'news', 'discover', 'googleNews']
        if search_type not in valid_search_types:
            return f"Invalid search_type: {search_type}. Valid types are: {', '.join(valid_search_types)}"
        
        # Build the request body
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions or [],
            'searchType': search_type,
            'rowLimit': row_limit
        }
        
        # Execute the search analytics query
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        
        # Process and format the results
        if 'rows' not in response or not response['rows']:
            return "No data found for the specified parameters."
        
        rows = response['rows']
        
        # Format the output based on dimensions
        result = []
        headers = []
        
        # Add dimension headers
        if dimensions:
            headers.extend(dimensions)
        
        # Add metric headers
        headers.extend(['clicks', 'impressions', 'ctr', 'position'])
        
        # Add headers to result
        result.append(" | ".join(headers))
        result.append("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
        
        # Add data rows
        for row in rows:
            row_data = []
            
            # Add dimension values
            if dimensions:
                for i, dim_value in enumerate(row.get('keys', [])):
                    row_data.append(dim_value)
            
            # Add metric values
            row_data.append(str(row.get('clicks', 0)))
            row_data.append(str(row.get('impressions', 0)))
            row_data.append(f"{row.get('ctr', 0) * 100:.2f}%")
            row_data.append(f"{row.get('position', 0):.2f}")
            
            result.append(" | ".join(row_data))
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def compare_time_periods(
    site_url: str,
    current_start_date: str,
    current_end_date: str,
    previous_start_date: str,
    previous_end_date: str,
    ctx: Context,
    dimensions: list = None,
    search_type: str = "web",
    row_limit: int = 1000
) -> str:
    """
    Compare Search Console metrics between two time periods.
    
    Args:
        site_url: Full URL of your website (e.g., https://www.example.com/ or sc-domain:example.com)
        current_start_date: Start date for current period in YYYY-MM-DD format
        current_end_date: End date for current period in YYYY-MM-DD format
        previous_start_date: Start date for previous period in YYYY-MM-DD format
        previous_end_date: End date for previous period in YYYY-MM-DD format
        dimensions: List of dimensions (query, page, device, country, date)
        search_type: Type of search results (web, image, video, news, discover, googleNews)
        row_limit: Number of rows to return (max 25000)
    """
    try:
        # Get credentials file path from environment variable
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_file:
            return "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            
        if not os.path.exists(credentials_file):
            return f"Error: Credentials file not found at {credentials_file}"
        
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
            
        # Set up the Search Console API service
        service = build('webmasters', 'v3', credentials=credentials)
        
        # Validate inputs
        valid_dimensions = ['query', 'page', 'country', 'device', 'date']
        if dimensions:
            for dim in dimensions:
                if dim not in valid_dimensions:
                    return f"Invalid dimension: {dim}. Valid dimensions are: {', '.join(valid_dimensions)}"
        
        # Validate row_limit
        if row_limit < 1 or row_limit > 25000:
            return "row_limit must be between 1 and 25000"
            
        # Validate search_type
        valid_search_types = ['web', 'image', 'video', 'news', 'discover', 'googleNews']
        if search_type not in valid_search_types:
            return f"Invalid search_type: {search_type}. Valid types are: {', '.join(valid_search_types)}"
        
        # Build the request body for current period
        current_request_body = {
            'startDate': current_start_date,
            'endDate': current_end_date,
            'dimensions': dimensions or [],
            'searchType': search_type,
            'rowLimit': row_limit
        }
        
        # Build the request body for previous period
        previous_request_body = {
            'startDate': previous_start_date,
            'endDate': previous_end_date,
            'dimensions': dimensions or [],
            'searchType': search_type,
            'rowLimit': row_limit
        }
        
        # Execute the search analytics query for current period
        current_response = service.searchanalytics().query(
            siteUrl=site_url, body=current_request_body).execute()
        
        # Execute the search analytics query for previous period
        previous_response = service.searchanalytics().query(
            siteUrl=site_url, body=previous_request_body).execute()
        
        # Process and format the results
        if ('rows' not in current_response or not current_response['rows']) and \
           ('rows' not in previous_response or not previous_response['rows']):
            return "No data found for the specified parameters in either period."
        
        # Convert responses to DataFrames for easier comparison
        current_df = _response_to_dataframe(current_response, dimensions)
        previous_df = _response_to_dataframe(previous_response, dimensions)
        
        # Merge the DataFrames on dimensions
        if dimensions:
            merged_df = pd.merge(
                current_df, previous_df, 
                on=dimensions, 
                how='outer', 
                suffixes=('_current', '_previous')
            )
        else:
            # If no dimensions, create a single row DataFrame with totals
            merged_df = pd.DataFrame({
                'clicks_current': [current_df['clicks'].sum() if not current_df.empty else 0],
                'impressions_current': [current_df['impressions'].sum() if not current_df.empty else 0],
                'ctr_current': [current_df['ctr'].mean() if not current_df.empty else 0],
                'position_current': [current_df['position'].mean() if not current_df.empty else 0],
                'clicks_previous': [previous_df['clicks'].sum() if not previous_df.empty else 0],
                'impressions_previous': [previous_df['impressions'].sum() if not previous_df.empty else 0],
                'ctr_previous': [previous_df['ctr'].mean() if not previous_df.empty else 0],
                'position_previous': [previous_df['position'].mean() if not previous_df.empty else 0]
            })
        
        # Calculate changes
        merged_df['clicks_change'] = merged_df['clicks_current'].fillna(0) - merged_df['clicks_previous'].fillna(0)
        merged_df['clicks_change_pct'] = (
            (merged_df['clicks_current'].fillna(0) - merged_df['clicks_previous'].fillna(0)) / 
            merged_df['clicks_previous'].fillna(1) * 100
        )
        
        merged_df['impressions_change'] = merged_df['impressions_current'].fillna(0) - merged_df['impressions_previous'].fillna(0)
        merged_df['impressions_change_pct'] = (
            (merged_df['impressions_current'].fillna(0) - merged_df['impressions_previous'].fillna(0)) / 
            merged_df['impressions_previous'].fillna(1) * 100
        )
        
        merged_df['ctr_change'] = merged_df['ctr_current'].fillna(0) - merged_df['ctr_previous'].fillna(0)
        merged_df['ctr_change_pct'] = (
            (merged_df['ctr_current'].fillna(0) - merged_df['ctr_previous'].fillna(0)) / 
            merged_df['ctr_previous'].fillna(0.01) * 100
        )
        
        merged_df['position_change'] = merged_df['position_previous'].fillna(0) - merged_df['position_current'].fillna(0)
        
        # Format the output
        result = []
        
        # Add period information
        result.append(f"Comparison between:")
        result.append(f"Current period: {current_start_date} to {current_end_date}")
        result.append(f"Previous period: {previous_start_date} to {previous_end_date}")
        result.append("")
        
        # Format the DataFrame as a string table
        if dimensions:
            # Select columns for display
            display_cols = dimensions + [
                'clicks_current', 'clicks_previous', 'clicks_change', 'clicks_change_pct',
                'impressions_current', 'impressions_previous', 'impressions_change', 'impressions_change_pct',
                'ctr_current', 'ctr_previous', 'ctr_change', 'ctr_change_pct',
                'position_current', 'position_previous', 'position_change'
            ]
            display_df = merged_df[display_cols].fillna(0)
            
            # Sort by current clicks (descending)
            display_df = display_df.sort_values('clicks_current', ascending=False)
            
            # Format the DataFrame as a string
            output = StringIO()
            
            # Format float columns
            for col in display_df.columns:
                if 'ctr' in col:
                    display_df[col] = display_df[col].apply(lambda x: f"{x*100:.2f}%" if 'change_pct' not in col else f"{x:.2f}%")
                elif 'position' in col:
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")
                elif 'change_pct' in col:
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%")
            
            # Convert to string table
            table_str = display_df.to_string(index=False)
            result.append(table_str)
        else:
            # For no dimensions, just show the totals
            row = merged_df.iloc[0]
            result.append("Overall Metrics:")
            result.append(f"Clicks: {row['clicks_current']:.0f} vs {row['clicks_previous']:.0f} ({row['clicks_change']:.0f}, {row['clicks_change_pct']:.2f}%)")
            result.append(f"Impressions: {row['impressions_current']:.0f} vs {row['impressions_previous']:.0f} ({row['impressions_change']:.0f}, {row['impressions_change_pct']:.2f}%)")
            result.append(f"CTR: {row['ctr_current']*100:.2f}% vs {row['ctr_previous']*100:.2f}% ({row['ctr_change']*100:.2f}%, {row['ctr_change_pct']:.2f}%)")
            result.append(f"Position: {row['position_current']:.2f} vs {row['position_previous']:.2f} ({row['position_change']:.2f})")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_top_performing_content(
    site_url: str,
    start_date: str,
    end_date: str,
    ctx: Context,
    metric: str = "clicks",
    limit: int = 10
) -> str:
    """
    Get the top performing content based on a specific metric.
    
    Args:
        site_url: Full URL of your website (e.g., https://www.example.com/ or sc-domain:example.com)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        metric: Metric to sort by (clicks, impressions, ctr, position)
        limit: Number of results to return
    """
    try:
        # Get credentials file path from environment variable
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_file:
            return "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            
        if not os.path.exists(credentials_file):
            return f"Error: Credentials file not found at {credentials_file}"
        
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
            
        # Set up the Search Console API service
        service = build('webmasters', 'v3', credentials=credentials)
        
        # Validate metric
        valid_metrics = ['clicks', 'impressions', 'ctr', 'position']
        if metric not in valid_metrics:
            return f"Invalid metric: {metric}. Valid metrics are: {', '.join(valid_metrics)}"
        
        # Build the request body
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'searchType': 'web',
            'rowLimit': 1000  # Get a large number to ensure we have enough data
        }
        
        # Execute the search analytics query
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        
        # Process and format the results
        if 'rows' not in response or not response['rows']:
            return "No data found for the specified parameters."
        
        rows = response['rows']
        
        # Sort by the specified metric
        if metric == 'position':
            # For position, lower is better
            sorted_rows = sorted(rows, key=lambda x: x.get(metric, 0))
        else:
            # For other metrics, higher is better
            sorted_rows = sorted(rows, key=lambda x: x.get(metric, 0), reverse=True)
        
        # Take the top N results
        top_rows = sorted_rows[:limit]
        
        # Format the output
        result = []
        result.append(f"Top {limit} Pages by {metric.capitalize()} ({start_date} to {end_date}):")
        result.append("-" * 80)
        
        # Add headers
        result.append(f"{'Page':<50} | {'Clicks':<10} | {'Impressions':<12} | {'CTR':<8} | {'Position':<8}")
        result.append("-" * 80)
        
        # Add data rows
        for row in top_rows:
            page = row.get('keys', [''])[0]
            clicks = row.get('clicks', 0)
            impressions = row.get('impressions', 0)
            ctr = row.get('ctr', 0) * 100  # Convert to percentage
            position = row.get('position', 0)
            
            result.append(f"{page[:50]:<50} | {clicks:<10.0f} | {impressions:<12.0f} | {ctr:<8.2f}% | {position:<8.2f}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_search_trends(
    site_url: str,
    start_date: str,
    end_date: str,
    ctx: Context,
    interval: str = "week"
) -> str:
    """
    Get search trends over time for a site.
    
    Args:
        site_url: Full URL of your website (e.g., https://www.example.com/ or sc-domain:example.com)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        interval: Time interval for grouping (day, week, month)
    """
    try:
        # Get credentials file path from environment variable
        credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not credentials_file:
            return "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            
        if not os.path.exists(credentials_file):
            return f"Error: Credentials file not found at {credentials_file}"
        
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
            
        # Set up the Search Console API service
        service = build('webmasters', 'v3', credentials=credentials)
        
        # Validate interval
        valid_intervals = ['day', 'week', 'month']
        if interval not in valid_intervals:
            return f"Invalid interval: {interval}. Valid intervals are: {', '.join(valid_intervals)}"
        
        # Build the request body
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['date'],
            'searchType': 'web',
            'rowLimit': 1000
        }
        
        # Execute the search analytics query
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        
        # Process and format the results
        if 'rows' not in response or not response['rows']:
            return "No data found for the specified parameters."
        
        rows = response['rows']
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame([
            {
                'date': row['keys'][0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0),
                'position': row.get('position', 0)
            }
            for row in rows
        ])
        
        # Convert date string to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by the specified interval
        if interval == 'day':
            # Already grouped by day
            grouped_df = df
        elif interval == 'week':
            # Group by week
            df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
            grouped_df = df.groupby('week').agg({
                'clicks': 'sum',
                'impressions': 'sum',
                'ctr': 'mean',
                'position': 'mean'
            }).reset_index()
            grouped_df.rename(columns={'week': 'date'}, inplace=True)
        elif interval == 'month':
            # Group by month
            df['month'] = df['date'].dt.to_period('M').apply(lambda r: r.start_time)
            grouped_df = df.groupby('month').agg({
                'clicks': 'sum',
                'impressions': 'sum',
                'ctr': 'mean',
                'position': 'mean'
            }).reset_index()
            grouped_df.rename(columns={'month': 'date'}, inplace=True)
        
        # Sort by date
        grouped_df = grouped_df.sort_values('date')
        
        # Format the output
        result = []
        result.append(f"Search Trends by {interval.capitalize()} ({start_date} to {end_date}):")
        result.append("-" * 80)
        
        # Add headers
        result.append(f"{'Date':<12} | {'Clicks':<10} | {'Impressions':<12} | {'CTR':<8} | {'Position':<8}")
        result.append("-" * 80)
        
        # Add data rows
        for _, row in grouped_df.iterrows():
            date_str = row['date'].strftime('%Y-%m-%d')
            clicks = row['clicks']
            impressions = row['impressions']
            ctr = row['ctr'] * 100  # Convert to percentage
            position = row['position']
            
            result.append(f"{date_str:<12} | {clicks:<10.0f} | {impressions:<12.0f} | {ctr:<8.2f}% | {position:<8.2f}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error: {str(e)}"

def _response_to_dataframe(response, dimensions):
    """Helper function to convert API response to pandas DataFrame"""
    if 'rows' not in response or not response['rows']:
        return pd.DataFrame()
    
    rows = response['rows']
    data = []
    
    for row in rows:
        row_data = {}
        
        # Add dimension values
        if dimensions:
            for i, dim in enumerate(dimensions):
                if i < len(row.get('keys', [])):
                    row_data[dim] = row['keys'][i]
                else:
                    row_data[dim] = None
        
        # Add metric values
        row_data['clicks'] = row.get('clicks', 0)
        row_data['impressions'] = row.get('impressions', 0)
        row_data['ctr'] = row.get('ctr', 0)
        row_data['position'] = row.get('position', 0)
        
        data.append(row_data)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    mcp.run()