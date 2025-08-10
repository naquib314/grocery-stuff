# 🛒 Grocery Price Checker
### Prerequisites
- Python 3.9+
- Poetry (for dependency management)

### Installation

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Run the application:**
   ```bash
   poetry run python run.py
   ```

3. **Access the application:**
   - **Web App**: http://localhost:8000/app
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative API Docs**: http://localhost:8000/redoc

## 📖 Usage

### Web Interface

1. Open http://localhost:8000/app in your browser
2. Use the search bar to find products (e.g., "milk", "bread", "bananas")
3. Click "Search" to see all matching products across stores
4. Click "Compare Prices" to see price comparison for a specific product

### API Endpoints

- `GET /api/products/search?q={query}` - Search for products
- `GET /api/products/compare?product_name={name}` - Compare product prices
- `GET /api/stores/` - Get all stores
- `GET /api/products/` - Get all products

## 🛠️ Development

### Project Structure

```
grocery-stuff/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── load_data.py         # Data loading utilities
│   └── routers/
│       ├── __init__.py
│       ├── stores.py        # Store endpoints
│       └── products.py      # Product endpoints
├── alembic/                 # Database migrations
├── data/
│   └── dummy_products.json  # Sample data
├── frontend/
│   └── index.html           # Web interface
├── pyproject.toml           # Poetry configuration
├── run.py                   # Application entry point
└── README.md
```

### Database Management

**Create a new migration:**
```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**
```bash
poetry run alembic upgrade head
```

**Reset database (development only):**
```bash
poetry run python -c "from app.load_data import reset_database; reset_database()"
poetry run python -m app.load_data
```

### Running Tests

```bash
poetry run pytest
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database URL (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite:///./grocery_app.db

# Server configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Production Deployment

For production, update the database URL to use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/grocery_db
```

## 🎯 API Features

- **Validation**: Comprehensive input validation using Pydantic
- **Error Handling**: Proper HTTP status codes and error messages
- **Documentation**: Automatic API documentation with Swagger UI
- **CORS**: Configured for cross-origin requests
- **Search**: Full-text search across product names and categories
- **Filtering**: Filter products by store, category, price range

## 🔍 Example API Calls

**Search for products:**
```bash
curl "http://localhost:8000/api/products/search?q=milk"
```

**Compare product prices:**
```bash
curl "http://localhost:8000/api/products/compare?product_name=milk"
```

**Get all stores:**
```bash
curl "http://localhost:8000/api/stores/"
```

## 🧪 Sample Data

The application comes with sample data for 3 stores and 10 products each:

- **Walmart**: Competitive pricing, Main Street location
- **Target**: Premium positioning, Shopping Center location  
- **Hannaford**: Local favorite, Market Square location

Products include common grocery items like:
- Organic Bananas
- Whole Milk
- Bread
- Ground Beef
- Chicken Breast
- Eggs
- And more...

## 🚀 Future Enhancements

- [ ] User authentication and favorites
- [ ] Price history tracking
- [ ] Email price alerts
- [ ] Barcode scanning
- [ ] Store location-based filtering
- [ ] Shopping list features
- [ ] Mobile app
- [ ] Real-time price updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
