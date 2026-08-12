from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.product import Product
from app.models.user import User
from app.services.product_service import get_current_user
from app.seed.excel import import_products

router = APIRouter(prefix="/products",tags=["Products"])

# 1. Get all products
@router.get("/")
def list_products(session: Session = Depends(get_session)):
    product = session.exec(select(Product)).all()

    if len(product) == 0:
        import_products()
        product = session.exec(select(Product)).all()
    return product

# 2. Create product
@router.post("/", status_code=201)
def create_product(name: str,sku: str,price: float,quantity: int = 0,category: str = None,session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    existing = session.exec(select(Product).where(Product.sku == sku)).first()
    if existing:
        raise HTTPException( status_code=400,detail="SKU already exists")
    product = Product( name=name,sku=sku,price=price,quantity=quantity, category=category)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product



# 3. Get products by category
@router.get("/category/{category}")
def get_by_category(category: str,session: Session = Depends(get_session)):
    return session.exec( select(Product).where(Product.category == category)).all()


# 4. Search products
@router.get("/search")
def search_products(name: str,session: Session = Depends(get_session)):
    return session.exec(select(Product).where(Product.name.ilike(f"%{name}%")) ).all()

# 5. Get low-stock products
@router.get("/low-stock")
def get_low_stock(limit: int = 10,session: Session = Depends(get_session)):
    return session.exec(select(Product).where( Product.quantity <= limit) ).all()


# 6. Get products by price range
@router.get("/price-range")
def get_price_range(min_price: float,max_price: float,session: Session = Depends(get_session)):
    return session.exec(select(Product).where(Product.price >= min_price,Product.price <= max_price )).all()


 

 
# get product by id
@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    return product


# 8. Update product
@router.put("/{product_id}")
def update_product(product_id: int,name: str,sku: str,price: float,quantity: int,category: str = None,session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    product = session.exec(select(Product).where(Product.id == product_id)).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found" )
    product.name = name
    product.sku = sku
    product.price = price
    product.quantity = quantity
    product.category = category

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# 9. Update quantity
@router.patch("/{product_id}/quantity")
def update_quantity(product_id: int,quantity: int,session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    product = session.exec(select(Product).where(Product.id == product_id)).first()

    if not product:
        raise HTTPException( status_code=404,detail="Product not found" )

    if quantity < 0:
        raise HTTPException( status_code=400, detail="Quantity cannot be negative")

    product.quantity = quantity

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# 10. Delete product
@router.delete("/{product_id}")
def delete_product(product_id: int,session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    product = session.exec(select(Product).where( Product.id == product_id)).first()
    if not product:
        raise HTTPException( status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {
        "message": "Product deleted successfully"
    }