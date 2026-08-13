import os
import pandas as pd
from sqlmodel import Session, select
from app.database import engine
from app.models.product import Product

#Get file path in folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Gives the path of the current Python file
EXCEL_FILE = os.path.join(BASE_DIR, "Product_Data.xlsx")


def import_products():#Excel into the database.
    df = pd.read_excel(EXCEL_FILE,sheet_name="Product Data")
    with Session(engine) as session:
        for _, row in df.iterrows():#Looping through Excel rows
            sku = str(row["Product ID"])
            existing_product = session.exec(select(Product).where(Product.sku == sku )).first()
            if existing_product:
                continue
            product = Product(sku=sku,name=str(row["Product Name"]),category=str(row["Category"]), price=float(row["Unit Price ($)"]),quantity=0)
            session.add(product)
            session.commit()

if __name__ == "__main__":
    import_products()
    print("Products imported successfully!")
