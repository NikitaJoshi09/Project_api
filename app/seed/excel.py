import pandas as pd
from pathlib import Path
from sqlmodel import Session, select
from app.database import engine
from app.models.product import Product

# Excel file path


BASE_DIR = Path(__file__).resolve().parent

EXCEL_PATH = BASE_DIR / "Product_Data.xlsx"



# Import products
def import_products():

    # Check Excel file
    if not EXCEL_PATH.exists():
        print(f"Excel file not found: {EXCEL_PATH}")
        return

    # Read Excel
    df = pd.read_excel(EXCEL_PATH,sheet_name="Product Data")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()
    print("Excel columns:")
    print(df.columns.tolist())

    
    # Required columns
   

    required_columns = [
        "Product ID",
        "Product Name",
        "Category",
        "Unit Price ($)"
    ]

    for column in required_columns:

        if column not in df.columns:
            print(f"Missing column: {column}")
            return

    
    # Database session
    

    with Session(engine) as session:

        added_count = 0
        skipped_count = 0

        
        # Read each Excel row
        

        for _, row in df.iterrows():

            
            # SKU
            

            sku = str(row["Product ID"]).strip()

            if not sku or sku == "nan":
                print("Skipping product: SKU is empty")
                skipped_count += 1
                continue

            
            # Check duplicate SKU
            

            existing_product = session.exec(select(Product).where( Product.sku == sku)).first()

            if existing_product:
                print(f"Skipping duplicate SKU: {sku}")

                skipped_count += 1
                continue

            
            # Product name
            

            name = row["Product Name"]
            if pd.isna(name):
                print(f"Skipping {sku}: Product name is empty")
                skipped_count += 1
                continue
            name = str(name).strip()

            
            # Category
            

            category = row["Category"]
            if pd.isna(category):
                category = None
            else:
                category = str(category).strip()

            
            # Price
            

            price = row["Unit Price ($)"]
            if pd.isna(price):
                print(f"Skipping {sku}: Price is empty")
                skipped_count += 1
                continue
            price = float(price)

           
            # Create Product
          

            product = Product(
                name=name,
                sku=sku,
                price=price,
                quantity=0,
                category=category
            )

            session.add(product)
            added_count += 1

      
        # Commit
     

        session.commit()

    
        # Result
      

        print("----------------------------------------")
        print("Product import completed successfully")
        print(f"Products added   : {added_count}")
        print(f"Products skipped : {skipped_count}")
        print("----------------------------------------")


# Run


if __name__ == "__main__":
    import_products()

