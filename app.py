import streamlit as st
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional
import json

# Page Configuration
st.set_page_config(
    page_title="NoBrokerage.com - AI Property Search",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like interface
st.markdown("""
<style>
    .main {
        background-color: #343541;
    }
    .stChatMessage {
        background-color: #444654;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .property-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .property-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .property-detail {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem 0.3rem 0.3rem 0;
        font-size: 0.9rem;
    }
    .property-price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffd700;
        margin: 0.8rem 0;
    }
    .chat-input {
        background-color: #40414f !important;
        border: 1px solid #565869 !important;
        color: white !important;
    }
    h1 {
        color: white;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class PropertyDataLoader:
    """Handles loading and merging of CSV data"""
    
    @staticmethod
    @st.cache_data
    def load_data() -> pd.DataFrame:
        try:
            # Load all CSV files
            variants_df = pd.read_csv('ProjectConfigurationVariant.csv')
            config_df = pd.read_csv('ProjectConfiguration.csv')
            address_df = pd.read_csv('ProjectAddress.csv')
            project_df = pd.read_csv('project.csv')
            
            # Merge data
            df = variants_df.merge(config_df, left_on='configurationId', right_on='id', 
                                   how='left', suffixes=('', '_config'))
            df = df.merge(project_df, left_on='projectId', right_on='id', 
                         how='left', suffixes=('', '_project'))
            df = df.merge(address_df, on='projectId', how='left')
            
            # Data cleaning
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['carpetArea'] = pd.to_numeric(df['carpetArea'], errors='coerce')
            df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce')
            
            # Extract BHK type
            df['bhk_type'] = df['type'].fillna(df['customBHK']).fillna('Unknown')
            
            # Clean city/locality
            df['cityName'] = 'Mumbai'  # Default based on data
            df['localityName'] = df['landmark'].fillna(df['fullAddress'].str.split(',').str[0])
            
            return df
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()

class QueryParser:
    """Intelligent natural language query parser"""
    
    @staticmethod
    def parse_query(query: str) -> Dict:
        query_lower = query.lower()
        filters = {
            'bhk': None,
            'min_price': None,
            'max_price': None,
            'city': None,
            'locality': None,
            'status': None,
            'project_name': None,
            'property_type': None
        }
        
        # BHK extraction
        bhk_patterns = [
            r'(\d+)\s*bhk',
            r'(\d+)\s*bedroom',
            r'(\d+)\s*bed'
        ]
        for pattern in bhk_patterns:
            match = re.search(pattern, query_lower)
            if match:
                filters['bhk'] = f"{match.group(1)}BHK"
                break
        
        # Price extraction
        price_patterns = [
            (r'under\s+₹?\s*(\d+\.?\d*)\s*(cr|crore|l|lakh)', 'max'),
            (r'below\s+₹?\s*(\d+\.?\d*)\s*(cr|crore|l|lakh)', 'max'),
            (r'above\s+₹?\s*(\d+\.?\d*)\s*(cr|crore|l|lakh)', 'min'),
            (r'over\s+₹?\s*(\d+\.?\d*)\s*(cr|crore|l|lakh)', 'min'),
            (r'₹?\s*(\d+\.?\d*)\s*(cr|crore|l|lakh)', 'max')
        ]
        
        for pattern, price_type in price_patterns:
            match = re.search(pattern, query_lower)
            if match:
                amount = float(match.group(1))
                unit = match.group(2)
                
                if 'cr' in unit:
                    amount_inr = amount * 10000000
                elif 'l' in unit:
                    amount_inr = amount * 100000
                else:
                    amount_inr = amount * 10000000
                
                if price_type == 'max':
                    filters['max_price'] = amount_inr
                else:
                    filters['min_price'] = amount_inr
                break
        
        # City extraction
        cities = ['mumbai', 'pune', 'delhi', 'bangalore', 'hyderabad', 'chennai']
        for city in cities:
            if city in query_lower:
                filters['city'] = city.title()
                break
        
        # Locality extraction (Mumbai areas)
        localities = ['chembur', 'andheri', 'bandra', 'powai', 'mulund', 'ghatkopar', 
                      'worli', 'parel', 'marol', 'dombivli', 'shivajinagar', 'punawale',
                      'kharadi', 'mundhwa', 'camp']
        for locality in localities:
            if locality in query_lower:
                filters['locality'] = locality.title()
                break
        
        # Status extraction
        if any(word in query_lower for word in ['ready', 'ready to move', 'possession']):
            filters['status'] = 'READY_TO_MOVE'
        elif any(word in query_lower for word in ['under construction', 'upcoming', 'new launch']):
            filters['status'] = 'UNDER_CONSTRUCTION'
        
        # Property type
        if any(word in query_lower for word in ['commercial', 'office', 'shop']):
            filters['property_type'] = 'COMMERCIAL'
        elif 'residential' in query_lower:
            filters['property_type'] = 'RESIDENTIAL'
        
        return filters

class PropertySearchEngine:
    """Handles property search and filtering"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def search(self, filters: Dict) -> pd.DataFrame:
        result_df = self.df.copy()
        
        # Apply filters
        if filters['bhk']:
            result_df = result_df[result_df['bhk_type'].str.contains(filters['bhk'], case=False, na=False)]
        
        if filters['max_price']:
            result_df = result_df[result_df['price'] <= filters['max_price']]
        
        if filters['min_price']:
            result_df = result_df[result_df['price'] >= filters['min_price']]
        
        if filters['city']:
            # Search in address fields
            mask = (result_df['fullAddress'].str.contains(filters['city'], case=False, na=False))
            result_df = result_df[mask]
        
        if filters['locality']:
            mask = (
                result_df['landmark'].str.contains(filters['locality'], case=False, na=False) |
                result_df['fullAddress'].str.contains(filters['locality'], case=False, na=False) |
                result_df['localityName'].str.contains(filters['locality'], case=False, na=False)
            )
            result_df = result_df[mask]
        
        if filters['status']:
            result_df = result_df[result_df['status'] == filters['status']]
        
        if filters['property_type']:
            result_df = result_df[result_df['projectCategory'] == filters['property_type']]
        
        return result_df.dropna(subset=['price', 'projectName'])

class SummaryGenerator:
    """Generates intelligent summaries from search results"""
    
    @staticmethod
    def generate(df: pd.DataFrame, filters: Dict, original_query: str) -> str:
        if len(df) == 0:
            return SummaryGenerator._generate_no_results_summary(filters)
        
        count = len(df)
        avg_price = df['price'].mean()
        min_price = df['price'].min()
        max_price = df['price'].max()
        
        # Get unique localities
        localities = df['localityName'].dropna().unique()[:3]
        
        # Get BHK info
        bhk_types = df['bhk_type'].value_counts()
        
        # Get status info
        ready_count = len(df[df['status'] == 'READY_TO_MOVE'])
        under_construction_count = len(df[df['status'] == 'UNDER_CONSTRUCTION'])
        
        # Build summary
        summary_parts = []
        
        # Opening sentence
        if filters['bhk']:
            summary_parts.append(f"Found {count} {filters['bhk']} properties")
        else:
            summary_parts.append(f"Found {count} properties")
        
        # Location info
        if filters['city']:
            summary_parts.append(f"in {filters['city']}")
        if filters['locality']:
            summary_parts.append(f"near {filters['locality']}")
        
        # Price range
        if count > 0:
            price_range = f"ranging from ₹{SummaryGenerator._format_price(min_price)} to ₹{SummaryGenerator._format_price(max_price)}"
            summary_parts.append(f"with prices {price_range}")
        
        summary = " ".join(summary_parts) + ". "
        
        # Additional insights
        if len(localities) > 0:
            summary += f"Popular localities include {', '.join(localities)}. "
        
        if ready_count > 0 and under_construction_count > 0:
            summary += f"{ready_count} properties are ready-to-move, while {under_construction_count} are under construction. "
        elif ready_count > 0:
            summary += f"All {ready_count} properties are ready for immediate possession. "
        
        # Average price insight
        if count > 1:
            summary += f"Average price is approximately ₹{SummaryGenerator._format_price(avg_price)}."
        
        return summary
    
    @staticmethod
    def _generate_no_results_summary(filters: Dict) -> str:
        summary = "No properties found matching your exact criteria. "
        
        suggestions = []
        if filters['max_price']:
            new_budget = filters['max_price'] * 1.2
            suggestions.append(f"try increasing budget to ₹{SummaryGenerator._format_price(new_budget)}")
        
        if filters['locality']:
            suggestions.append("expand search to nearby localities")
        
        if filters['bhk']:
            suggestions.append("consider adjacent BHK configurations")
        
        if suggestions:
            summary += "You might want to " + " or ".join(suggestions) + "."
        
        return summary
    
    @staticmethod
    def _format_price(price: float) -> str:
        if price >= 10000000:
            return f"{price/10000000:.2f} Cr"
        else:
            return f"{price/100000:.2f} L"

def display_property_card(row: pd.Series, index: int):
    """Display a single property card"""
    
    # Format price
    price_formatted = SummaryGenerator._format_price(row['price'])
    
    # Status badge
    status_color = "🟢" if row['status'] == 'READY_TO_MOVE' else "🟡"
    status_text = "Ready to Move" if row['status'] == 'READY_TO_MOVE' else "Under Construction"
    
    # Build amenities list
    amenities = []
    if row['balcony'] > 0:
        amenities.append(f"{int(row['balcony'])} Balconies")
    if row['bathrooms'] > 0:
        amenities.append(f"{int(row['bathrooms'])} Bathrooms")
    if row['carpetArea'] > 0:
        amenities.append(f"{int(row['carpetArea'])} sq.ft")
    
    card_html = f"""
    <div class="property-card">
        <div class="property-title">🏠 {row['projectName']}</div>
        <div class="property-detail">{row['bhk_type']}</div>
        <div class="property-detail">📍 {row['localityName']}</div>
        <div class="property-detail">{status_color} {status_text}</div>
        <div class="property-price">₹ {price_formatted}</div>
        <div style="margin: 0.5rem 0;">
            {' | '.join(amenities) if amenities else 'Contact for details'}
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.9;">
            📍 {row['fullAddress'][:80]}...
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def main():
    # Title
    st.markdown("<h1>🏠 NoBrokerage.com - AI Property Search</h1>", unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading property database..."):
        df = PropertyDataLoader.load_data()
    
    if df.empty:
        st.error("Failed to load property data. Please check CSV files.")
        return
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I'm your AI property assistant. I can help you find properties in Mumbai and Pune.\n\nTry asking me things like:\n- '3BHK flat in Pune under ₹1.2 Cr'\n- 'Ready to move 2BHK in Chembur'\n- 'Properties in Mumbai under 50 lakhs'"
            }
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display properties if available
            if "properties" in message:
                for idx, prop in enumerate(message["properties"]):
                    display_property_card(prop, idx)
    
    # Chat input
    if query := st.chat_input("Ask me about properties... (e.g., '3BHK in Mumbai under 1 Cr')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Searching properties..."):
                # Parse query
                parser = QueryParser()
                filters = parser.parse_query(query)
                
                # Search properties
                search_engine = PropertySearchEngine(df)
                results = search_engine.search(filters)
                
                # Generate summary
                summary = SummaryGenerator.generate(results, filters, query)
                
                # Display summary
                st.markdown(summary)
                
                # Display property cards
                if len(results) > 0:
                    # Limit to top 10 results
                    top_results = results.head(10)
                    
                    # Convert to list of series for storage
                    properties_list = [row for _, row in top_results.iterrows()]
                    
                    # Display cards
                    for idx, row in top_results.iterrows():
                        display_property_card(row, idx)
                    
                    # Add to message history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": summary,
                        "properties": properties_list
                    })
                else:
                    st.info("💡 Tip: Try broadening your search criteria or exploring different localities.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": summary
                    })
    
    # Sidebar with stats
    with st.sidebar:
        st.markdown("### 📊 Database Stats")
        st.metric("Total Properties", len(df))
        st.metric("Cities", df['cityName'].nunique())
        st.metric("Projects", df['projectName'].nunique())
        
        st.markdown("---")
        st.markdown("### 🔍 Quick Filters")
        
        bhk_options = sorted(df['bhk_type'].dropna().unique())
        st.multiselect("BHK Type", bhk_options)
        
        st.markdown("---")
        st.markdown("Built with ❤️ for NoBrokerage.com")

if __name__ == "__main__":
    main()