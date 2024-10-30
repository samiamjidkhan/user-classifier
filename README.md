# Website Intent Analyzer

A web application that analyzes website content to understand visitor intent through AI-powered question generation. This tool takes a URL as input, scrapes the website content, and generates relevant multiple-choice questions to classify visitor interests.

## Features

- 🔍 Real-time website content analysis
- 🤖 AI-powered question generation using Groq API
- 💾 Content caching with Redis
- 🗄️ Persistent storage with PostgreSQL
- ⚡ Fast and responsive React frontend

## Tech Stack

### Frontend
- React
- Redux for state management
- Tailwind CSS for styling
- Lucide React for icons
- Shadcn UI components

### Backend
- Python 3.x
- Flask web framework
- BeautifulSoup4 for web scraping
- Groq API for AI-powered analysis
- Redis for content caching
- PostgreSQL for data persistence
- SQLAlchemy ORM
- Flask-Migrate for database migrations

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm
- Redis server
- PostgreSQL database
- Groq API key

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/samiamjidkhan/website-intent-analyzer.git
cd website-intent-analyzer
```

2. Set up the backend environment:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

3. Set up the frontend environment:
```bash
cd frontend
npm install
```

4. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://localhost:6379
PORT=5001
```

### Running the Application

1. Start the Redis server:
```bash
redis-server
```

2. Start the backend server:
```bash
python app.py # Or python3 app.py
```

3. Start the frontend development server:
```bash
cd frontend
npm run dev
```

## Project Structure

```
user-classifier/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── URLAnalyzer.jsx
│   │   ├── store/
│   │   │   └── urlAnalyzerSlice.js
|   |   |   └── store.js
│   │   └── App.jsx
│   └── package.json
├── backend/
│   ├── services/
│   │   ├── intent_analyzer.py
│   │   └── scraper.py
│   ├── models/
│   │   └── website.py
│   ├── extensions.py
│   └── app.py
├── requirements.txt
└── README.md
```

## How It Works

1. **URL Submission**: User submits a website URL through the frontend interface.

2. **Content Scraping**: The backend scrapes the website content using BeautifulSoup4:
   - Checks Redis cache for previously scraped content
   - If not cached, scrapes the website and stores in Redis for 1 hour

3. **Intent Analysis**: 
   - Scraped content is processed by the Groq API
   - Generates a contextual multiple-choice question
   - Creates 4 relevant options based on the content

4. **Result Storage**:
   - Analysis results are stored in PostgreSQL
   - Cached for 7 days to prevent redundant processing

5. **Response Display**:
   - Question and options are displayed to the user
   - Interface automatically resets after selection

## API Endpoints

### POST /analyze
Analyzes a website and generates an intent classification question.

**Request Body:**
```json
{
    "url": "https://example.com"
}
```

**Example response:**
```json
{
    "url": "https://example.com",
    "question": "Which product category are you interested in?",
    "options": ["Smartphones", "Laptops", "Smart Home", "Wearables"]
}
```

### GET /health
Health check endpoint for monitoring service status.

## Contributing

Many improvements can be made with regards to scraping and generating questions. Feel free to jump in!