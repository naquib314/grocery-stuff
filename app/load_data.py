import json
import os
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud

def load_dummy_data():
    """Load dummy data from JSON file into the database"""
    
    # Create database tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_stores = crud.get_stores(db)
        if existing_stores:
            print("Data already exists in database. Skipping load.")
            return
        
        # Load JSON data
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dummy_products.json")
        
        if not os.path.exists(data_file):
            print(f"Data file not found: {data_file}")
            return
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Load stores and products
        for store_data in data['stores']:
            # Create store
            store_create = schemas.StoreCreate(
                store_id=store_data['store_id'],
                store_name=store_data['store_name'],
                location=store_data['location']
            )
            
            print(f"Creating store: {store_create.store_name}")
            db_store = crud.create_store(db=db, store=store_create)
            
            # Create products for this store
            for product_data in store_data['products']:
                product_create = schemas.ProductCreate(
                    product_id=product_data['product_id'],
                    name=product_data['name'],
                    price=product_data['price'],
                    category=product_data['category'],
                    unit=product_data['unit']
                )
                
                print(f"  Creating product: {product_create.name}")
                crud.create_product(db=db, product=product_create, store_id=db_store.id)
        
        print("Dummy data loaded successfully!")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    load_dummy_data()
