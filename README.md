# LexArb Components

AI-powered arbitration management system.

## Project Structure

```
├── backend/
│   ├── src/
│   │   └── pipelines/
│   │       ├── case_filing/      # Case management functionality
│   │       ├── document_request/ # Document processing and storage
│   │       ├── ai_etl/          # AI-powered document analysis
│   │       └── award/           # Award generation and management
│   └── tests/                   # Backend test suite
├── frontend/
│   ├── src/
│   └── tests/
├── templates/                   # Email and document templates
└── docker-compose.yml           # Container configuration
```

## Features

- Case Filing: Generate unique case numbers and manage case lifecycle
- Document Management: Process and organize case-related documents
- AI ETL Pipeline: Analyze and categorize documents using LLMs
- Award Generation: Create and manage arbitration awards

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jreyes-beyond/Lexarb-components.git
   cd Lexarb-components
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   pytest backend/tests/
   ```

## Development

1. Start containers:
   ```bash
   docker-compose up -d
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

3. Start development server:
   ```bash
   uvicorn backend.src.main:app --reload
   ```

## Testing

Run all tests:
```bash
pytest
```

Run specific test suite:
```bash
pytest backend/tests/test_case_filing.py
```

## Contributing

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

3. Push changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```