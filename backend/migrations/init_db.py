import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal
from models import Base, Category, Product
from sqlalchemy import inspect
from datetime import datetime

def create_tables():
    """Создание таблиц в базе данных"""
    print("Создание таблиц...")
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)  
    print("Таблицы успешно созданы!")

def init_test_data():
    """Инициализация тестовых данных"""
    session = SessionLocal()
    
    
    session.query(Product).delete()
    session.query(Category).delete()
    session.commit()
    
    print("Добавление тестовых данных...")
    
   
    categories = [
        Category(name="Электроника", description="Смартфоны, ноутбуки, гаджеты"),
        Category(name="Одежда", description="Мужская и женская одежда"),
        Category(name="Книги", description="Художественная и учебная литература"),
        Category(name="Спорт", description="Спортивные товары и инвентарь"),
        Category(name="Дом и сад", description="Товары для дома и дачи"),
        Category(name="Автотовары", description="Автомобильные аксессуары"),
    ]
    
    for category in categories:
        session.add(category)
    
    session.commit()
    print(f"Добавлено {len(categories)} категорий")
    
    
    products = [
        Product(
            name="Смартфон iPhone 14",
            description="Apple iPhone 14, 128GB, синий",
            price=79990.00,
            stock=15,
            category_id=1,
            image_url="https://avatars.mds.yandex.net/get-mpic/7467475/img_id3965542126320051143.jpeg/orig"
        ),
        Product(
            name="Ноутбук MacBook Air",
            description="Apple MacBook Air M1, 8GB RAM, 256GB SSD",
            price=89990.00,
            stock=8,
            category_id=1,
            image_url="https://avatars.mds.yandex.net/get-mpic/3927509/2a00000192542da9a437a42d437566d55da5/orig"
        ),
        Product(
            name="Футболка хлопковая",
            description="Футболка из 100% хлопка, белая, размер M",
            price=1990.00,
            stock=50,
            category_id=2,
            image_url="https://ir.ozone.ru/s3/multimedia-r/6855038235.jpg"
        ),
        Product(
            name="Джинсы Classic",
            description="Классические джинсы, синие, размер 32",
            price=3990.00,
            stock=30,
            category_id=2,
            image_url="https://avatars.mds.yandex.net/get-mpic/12527500/2a0000019641000c601af96ba05b3345449d/orig"
        ),
        Product(
            name="Книга 'Python для начинающих'",
            description="Основы программирования на Python",
            price=1290.00,
            stock=25,
            category_id=3,
            image_url="https://ir.ozone.ru/s3/multimedia-1-h/7429863545.jpg"
        ),
        Product(
            name="Мяч футбольный",
            description="Футбольный мяч, размер 5, профессиональный",
            price=2490.00,
            stock=20,
            category_id=4,
            image_url="https://main-cdn.sbermegamarket.ru/big2/hlr-system/164/866/973/511/111/051/600022640231b1.png"
        ),
        Product(
            name="Наушники беспроводные",
            description="Bluetooth наушники с шумоподавлением",
            price=5990.00,
            stock=12,
            category_id=1,
            image_url="https://avatars.mds.yandex.net/get-mpic/16111726/2a0000019acad815a1103a5385181a4fdf91/orig"
        ),
        Product(
            name="Кофемашина",
            description="Автоматическая кофемашина для эспрессо",
            price=45990.00,
            stock=5,
            category_id=5,
            image_url="https://ir.ozone.ru/s3/multimedia-f/6854773371.jpg"
        ),
        Product(
            name="Видеорегистратор",
            description="Автомобильный видеорегистратор, Full HD",
            price=3490.00,
            stock=18,
            category_id=6,
            image_url="https://m.media-amazon.com/images/I/51KhzzFT6jL.jpg"
        ),
        Product(
            name="Кроссовки для бега",
            description="Легкие кроссовки для бега, размер 42",
            price=5490.00,
            stock=22,
            category_id=4,
            image_url="https://cdn1.ozone.ru/s3/multimedia-1-x/7586305665.jpg"
        ),
    ]
    
    for product in products:
        session.add(product)
    
    session.commit()
    print(f"Добавлено {len(products)} товаров")
    
    session.close()

def show_tables():
    """Показать структуру таблиц и данные"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n" + "="*50)
    print("СТРУКТУРА БАЗЫ ДАННЫХ")
    print("="*50)
    
    for table in tables:
        print(f"\nТаблица: {table}")
        print("-" * 30)
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  • {column['name']}: {column['type']}")
    
    
    session = SessionLocal()
    
    print("\n" + "="*50)
    print("ДАННЫЕ В БАЗЕ")
    print("="*50)
    
    categories = session.query(Category).all()
    print(f"\nКатегории ({len(categories)}):")
    for cat in categories:
        products_count = len(cat.products)
        print(f"  • {cat.id}: {cat.name} - {cat.description} (товаров: {products_count})")
    
    products = session.query(Product).all()
    print(f"\nТовары ({len(products)}):")
    for prod in products[:5]:  
        print(f"  • {prod.id}: {prod.name} - {prod.price:.2f} руб.")
    
    if len(products) > 5:
        print(f"  • ... и еще {len(products) - 5} товаров")
    
    session.close()

if __name__ == "__main__":
    print("="*50)
    print("ЗАПУСК МИГРАЦИЙ")
    print("="*50)
    
    create_tables()
    init_test_data()
    show_tables()
    
    print("\n" + "="*50)
    print("МИГРАЦИИ ЗАВЕРШЕНЫ УСПЕШНО!")
    print("="*50)
   