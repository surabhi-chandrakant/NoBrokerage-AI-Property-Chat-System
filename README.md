# 🏠 NoBrokerage.com - AI Property Chat System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)


An intelligent, GPT-like chat interface that helps users discover properties through natural language queries. Built as part of the **NoBrokerage.com AI Engineer Intern Task**.

## 🌟 Live Demo

🔗 **[https://nobrokerage-ai-property-chat-system.streamlit.app/](#)**



## 🎯 Project Overview

This AI-powered chatbot understands queries like:
> *"3BHK flat in Pune under ₹1.2 Cr"*

And responds with:
1. ✨ **Intelligent Summary** - A concise 4-5 sentence overview of available properties
2. 🏠 **Property Cards** - Beautifully designed cards with all relevant details

### Key Features

- 🧠 **Natural Language Processing** - Understands complex property queries
- 🔍 **Smart Search** - Extracts filters (city, BHK, budget, locality, status)
- 📊 **Data-Driven Summaries** - 100% grounded in CSV data (no hallucinations)
- 💬 **ChatGPT-like Interface** - Familiar, intuitive chat experience
- ⚡ **Real-time Search** - Instant property filtering and retrieval
- 🎨 **Modern UI** - Gradient cards, responsive design

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/surabhi-chandrakant/NoBrokerage-AI-Property-Chat-System.git
   cd NoBrokerage-AI-Property-Chat-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure CSV files are in the root directory**
   ```
   project/
   ├── app.py
   ├── project.csv
   ├── ProjectAddress.csv
   ├── ProjectConfiguration.csv
   └── ProjectConfigurationVariant.csv
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---



---

## 💡 Usage Examples

### Example Queries

Try these natural language queries:

```
✅ "3BHK flat in Pune under ₹1.2 Cr"
✅ "Ready to move 2BHK in Chembur"
✅ "Properties in Mumbai under 50 lakhs"
✅ "Under construction flats in Punawale"
✅ "1BHK near Ghatkopar"
✅ "Commercial property in Andheri"
```

### Query Understanding

The system intelligently extracts:
- **BHK Type** - 1BHK, 2BHK, 3BHK, etc.
- **Budget** - Maximum/minimum price in Cr or Lakhs
- **Location** - City and locality
- **Status** - Ready-to-move or Under Construction
- **Property Type** - Residential or Commercial

---

## 🏗️ Architecture

### Core Components

#### 1. **PropertyDataLoader**
- Loads and merges 4 CSV files
- Handles data cleaning and normalization
- Implements caching for performance

#### 2. **QueryParser**
- Extracts filters from natural language
- Uses regex patterns for BHK, price, location
- Handles variations in user input

#### 3. **PropertySearchEngine**
- Applies filters to property database
- Performs multi-criteria search
- Returns sorted, relevant results

#### 4. **SummaryGenerator**
- Creates intelligent, concise summaries
- Provides insights (avg price, localities)
- Generates helpful suggestions for no-result cases

---

## 📊 Data Schema

### CSV Files Used

1. **project.csv** - Main project information
2. **ProjectAddress.csv** - Location and address details
3. **ProjectConfiguration.csv** - BHK configurations
4. **ProjectConfigurationVariant.csv** - Property variants with pricing

### Key Fields
- `projectName` - Name of the property
- `price` - Property price (in INR)
- `bhk_type` - Bedroom configuration
- `carpetArea` - Area in sq.ft
- `status` - READY_TO_MOVE / UNDER_CONSTRUCTION
- `fullAddress` - Complete address
- `landmark` - Nearby landmarks

---


---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.8+ |
| **Data Processing** | Pandas |
| **NLP** | Regex-based parsing |
| **Styling** | Custom CSS |
| **Version Control** | Git & GitHub |


---

## 🧪 Testing

Run manual tests with these queries:

```bash
# Budget-based search
"Properties under 1 crore in Mumbai"

# Location-based search
"Flats in Chembur"

# Combined filters
"Ready to move 2BHK in Pune under 80 lakhs"

# Edge cases
"10BHK" (should handle gracefully)
"Properties in Delhi" (should show no results for non-existing city)
```

---

## 📝 Future Enhancements

- [ ] Add semantic search using embeddings
- [ ] Implement user authentication
- [ ] Add property comparison feature
- [ ] Include property images in cards
- [ ] Add filters sidebar
- [ ] Integrate with real estate APIs
- [ ] Add voice input support
- [ ] Implement property recommendations

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




---

## 👨‍💻 Author

**Surabhi Chandrakant**

- GitHub: [@surabhi-chandrakant](https://github.com/surabhi-chandrakant)


---

## 🙏 Acknowledgments

- **NoBrokerage.com** - For the opportunity and assignment
- **Streamlit** - For the amazing framework
- **Python Community** - For excellent libraries

---





---

<div align="center">

**Made with ❤️ for NoBrokerage.com AI Engineer Internship**

</div>
