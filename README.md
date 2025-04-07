# FactLens

FactLens is a web application designed to verify the authenticity of headlines and generate credibility scores based on multiple factors. It combines advanced APIs, keyword-based analysis, and domain reputation checks to help users assess the reliability of online content.

## Features

- **Headline Authenticity Verification**: Uses web search APIs to cross-check headlines for accuracy.
- **Credibility Scoring System**: Calculates a score out of 100 based on:
  - Source credibility
  - Cross-verification with independent sources
  - Fact-check presence
  - Temporal consistency
- **Web Search Integration**: Fetches search results using Google Custom Search API.
- **Keyword Analysis**: Identifies clickbait, emotionally charged, and manipulative content using predefined keyword lists.
- **Domain Reputation Check**: Matches domains against a CSV database of reliable and unreliable sources.
- **Grammar Error Detection**: Leverages LanguageTool API to identify spelling and grammar errors in headlines and descriptions.
- **User Authentication**:
  - Supports login and registration via Flask and MongoDB.
  - Integrates Google OAuth for seamless authentication.
- **Interactive Web Interface**:
  - Submit headlines, descriptions, and URLs for verification.
  - View credibility scores and supporting evidence in real-time.
- **Session Management**: Allows users to start new sessions and manage their history of verified headlines.
- **Responsive Design**: Provides a clean and user-friendly interface with custom CSS styling.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FactLens.git
   cd FactLens
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your credentials for Google Custom Search API, MongoDB, LanguageTool API, and Google OAuth.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://localhost:5000`.

## Usage

1. Navigate to the homepage.
2. Register or log in using your credentials or Google account.
3. Enter a headline, description (optional), and URL for verification.
4. View the credibility score along with supporting evidence.

## Technologies Used

- **Backend**: Flask, MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **APIs**:
  - Google Custom Search API
  - LanguageTool API
- **Authentication**: Google OAuth integration

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.

