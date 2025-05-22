import streamlit as st
import pandas as pd
import csv
import time
import random
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Set page configuration
st.set_page_config(
    page_title="LinkedIn Profile Finder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        color: #0A66C2 !important;
        margin-bottom: 1rem !important;
        text-align: left;
    }
    .sub-header {
        font-size: 1.5rem !important;
        color: #0077B5 !important;
        margin-bottom: 1rem !important;
    }
    .stProgress > div > div > div > div {
        background-color: #0A66C2;
    }
    .highlight-box {
        background-color: #f0f2f5;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #0A66C2;
    }
    .success-box {
        background-color: #ecfdf5;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #10b981;
    }
    .warning-box {
        background-color: #fffbeb;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #f59e0b;
    }
    .stButton>button {
        background-color: #0A66C2;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #004182;
    }
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        background-color: white;
    }
    .found {
        color: #10b981;
    }
    .not-found {
        color: #ef4444;
    }
            .logod {
            display: flex;
            align-items: center;
            gap: 4px;
margin-bottom : -40px;
        }
        .logo {
            width: 40px;
            height: 40px;
        }
        .main-title {
            margin: 0;
            font-size: 24px;
        }
            .info{
           
            margin-top: -20px;
            }
</style>
""", unsafe_allow_html=True)

def setup_driver():
    with st.spinner("Setting up web driver..."):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        )
        
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            st.error(f"Error setting up driver: {str(e)}")
            return None

def check_for_captcha(driver):
    try:
        return (
            driver.find_elements(By.ID, "captcha-form")
            or driver.find_elements(By.CSS_SELECTOR, ".g-recaptcha")
            or "captcha" in driver.page_source.lower()
            or "verify you're not a robot" in driver.page_source.lower()
        )
    except:
        return False

def find_linkedin_profile(driver, name, designation, organization, use_bing=False):
    query = f"{name} {designation} {organization} linkedin profile"
    search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}" if use_bing else f"https://www.google.com/search?q={query.replace(' ', '+')}"

    try:
        driver.get(search_url)
        time.sleep(random.uniform(2, 4))

        if check_for_captcha(driver):
            st.markdown(
                """
                <div class="warning-box">
                    <h3>⚠️ CAPTCHA Detected</h3>
                    <p>Please solve the CAPTCHA manually in the browser window and press Enter.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            st.stop()

        if use_bing:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.b_algo")))
            search_results = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")
        else:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g, div[data-sokoban-container]")))
            search_results = driver.find_elements(By.CSS_SELECTOR, "div.g, div[data-sokoban-container]")

        for result in search_results:
            links = result.find_elements(By.CSS_SELECTOR, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and 'linkedin.com/in/' in href:
                    match = re.search(r"(https://\w+\.linkedin\.com/in/[^?#]+)", href)
                    if match:
                        return match.group(1)
        return "Not found"

    except TimeoutException:
        return "Timeout error"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Sidebar for settings
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #0A66C2;'>⚙️ Settings</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
        use_bing = st.radio("Choose search engine:", ["Google", "Bing"], index=1)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
        st.subheader("Scraping Range")
        start_row = st.number_input("Start Row (0-indexed)", min_value=0, value=0)
        end_row = st.number_input("End Row (0 = full dataset)", min_value=0, value=0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
        st.subheader("Search Delay")
        min_delay = st.slider("Minimum Delay (seconds)", min_value=5, max_value=20, value=10)
        max_delay = st.slider("Maximum Delay (seconds)", min_value=min_delay, max_value=30, value=min(15, min_delay+5))
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box">
            <h3>📋 Instructions</h3>
            <ol>
                <li>Upload a CSV file with Name, Designation, and Organization columns</li>
                <li>Configure your settings</li>
                <li>Click "Start Scraping" to begin</li>
                <li>Download results when complete</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    # Main content
    st.markdown(
    '''
       <div class="logod">
        <img class="logo" src="https://images.rawpixel.com/image_png_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjk4Mi1kMy0xMC5wbmc.png" />
        <h1 class="main-title">Linkintel</h1>
    </div>
        <h5 class="info"> An Intelligence based Linkedin extractor Tool</h5>

    ''',
    unsafe_allow_html=True
)

    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<p class='sub-header'>Upload your CSV with contact information</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["csv"])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if uploaded_file:
            st.success("File uploaded successfully!")
            file_details = {"filename": uploaded_file.name, "size": f"{uploaded_file.size/1024:.2f} KB"}
            st.json(file_details)
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Validate the required columns
        required_columns = ['Name', 'Designation', 'Organization']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.markdown(
                f"""
                <div class="warning-box">
                    <h3>⚠️ Missing Columns</h3>
                    <p>Your CSV file is missing these required columns: {', '.join(missing_columns)}</p>
                    <p>Please make sure your file contains columns for Name, Designation, and Organization.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown("<p class='sub-header'>Preview Data</p>", unsafe_allow_html=True)
            st.dataframe(df.head())
            
            st.markdown(f"<p>Total records: <b>{len(df)}</b></p>", unsafe_allow_html=True)
            
            if st.button("Start Scraping"):
                driver = setup_driver()
                
                if driver:
                    output = []
                    total = len(df)
                    final_end = end_row if end_row > 0 else total
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    result_placeholder = st.container()
                    
                    # Create status columns
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        profiles_found_count = st.empty()
                    with col2:
                        profiles_not_found_count = st.empty()
                    with col3:
                        time_remaining = st.empty()
                    
                    profiles_found = 0
                    profiles_not_found = 0
                    start_time = time.time()
                    
                    for i in range(start_row, min(final_end, total)):
                        # Update progress bar
                        progress = (i - start_row + 1) / (min(final_end, total) - start_row)
                        progress_bar.progress(progress)
                        
                        # Calculate time remaining
                        if i > start_row:
                            elapsed = time.time() - start_time
                            items_processed = i - start_row + 1
                            time_per_item = elapsed / items_processed
                            remaining_items = min(final_end, total) - i - 1
                            remaining_seconds = remaining_items * time_per_item
                            time_remaining.markdown(f"⏱️ Est. time remaining: **{remaining_seconds/60:.1f}** minutes")
                        
                        row = df.iloc[i]
                        name = row['Name']
                        desig = row['Designation']
                        org = row['Organization']
                        
                        status_text.markdown(f"<h3>Searching for: {name} ({i+1}/{min(final_end, total)})</h3>", unsafe_allow_html=True)
                        
                        profile_url = find_linkedin_profile(driver, name, desig, org, use_bing == "Bing")
                        
                        # Count found/not found profiles
                        if profile_url == "Not found" or profile_url.startswith("Error") or profile_url == "Timeout error":
                            profiles_not_found += 1
                            status_class = "not-found"
                        else:
                            profiles_found += 1
                            status_class = "found"
                        
                        profiles_found_count.markdown(f"✅ Profiles found: **{profiles_found}**")
                        profiles_not_found_count.markdown(f"❌ Not found: **{profiles_not_found}**")
                        
                        with result_placeholder:
                            st.markdown(
                                f"""
                                <div class="result-card">
                                    <p><b>{name}</b> | {desig} at {org}</p>
                                    <p class="{status_class}">Result: {profile_url}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        output.append([name, desig, org, profile_url])
                        time.sleep(random.uniform(min_delay, max_delay))  # mimic human delay
                    
                    driver.quit()
                    
                    # Complete progress bar
                    progress_bar.progress(1.0)
                    
                    # Save result
                    result_df = pd.DataFrame(output, columns=["Name", "Designation", "Organization", "LinkedIn Profile"])
                    
                    st.markdown(
                        """
                        <div class="success-box">
                            <h2>🎉 Scraping Completed!</h2>
                            <p>Your LinkedIn profile search has been completed. View and download your results below.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Create tabs for different views
                    tab1, tab2, tab3 = st.tabs(["📊 Results Table", "📈 Statistics", "📥 Download"])
                    
                    with tab1:
                        st.dataframe(result_df)
                    
                    with tab2:
                        # Calculate statistics
                        total_profiles = len(result_df)
                        found_profiles = result_df['LinkedIn Profile'].apply(lambda x: x != "Not found" and not str(x).startswith("Error") and x != "Timeout error").sum()
                        not_found = total_profiles - found_profiles
                        found_percentage = (found_profiles / total_profiles) * 100 if total_profiles > 0 else 0
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Profiles Searched", total_profiles)
                            st.metric("Profiles Found", found_profiles)
                            st.metric("Success Rate", f"{found_percentage:.1f}%")
                        
                        with col2:
                            # Create a pie chart
                            labels = ['Found', 'Not Found']
                            sizes = [found_profiles, not_found]
                            
                            if total_profiles > 0:
                                import matplotlib.pyplot as plt
                                fig, ax = plt.subplots(figsize=(4, 4))
                                ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#10b981', '#ef4444'])
                                ax.set_title('Search Results')
                                st.pyplot(fig)
                    
                    with tab3:
                        csv_output = result_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Download Results as CSV",
                            data=csv_output,
                            file_name="contacts_with_linkedin.csv",
                            mime="text/csv",
                            key="download-csv"
                        )
                        
                        # Add Excel download option
                        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='xlsxwriter')
                        result_df.to_excel(excel_buffer, sheet_name='LinkedIn Profiles', index=False)
                        excel_buffer.close()
                        
                        with open('temp.xlsx', 'rb') as f:
                            excel_data = f.read()
                        
                        st.download_button(
                            "Download Results as Excel",
                            data=excel_data,
                            file_name="contacts_with_linkedin.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download-excel"
                        )
                        
                        # Remove temporary file
                        if os.path.exists('temp.xlsx'):
                            os.remove('temp.xlsx')

if __name__ == "__main__":
    main()
