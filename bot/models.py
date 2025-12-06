"""
Database models for production
Using SQLAlchemy ORM
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from pathlib import Path

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language = Column(String(2), default='ru')  # ru or tj
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_blocked = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Order(Base):
    """Order model"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Product info
    product_id = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_category = Column(String(50), nullable=False)

    # Payment info
    price_tjs = Column(Float, nullable=False)
    price_usd = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=True)  # pay_dc, pay_eskhata, etc.
    payment_screenshot = Column(String(500), nullable=True)  # file_id or path

    # Status
    status = Column(String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Admin notes
    admin_notes = Column(Text, nullable=True)

    # Relationships
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order(order_id={self.order_id}, status={self.status})>"


class Analytics(Base):
    """Analytics events"""
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # view_product, add_to_cart, purchase, etc.
    event_data = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Analytics(event_type={self.event_type}, user={self.user_telegram_id})>"


# Database setup
def get_db_path() -> Path:
    """Get database file path"""
    db_dir = Path('data')
    db_dir.mkdir(exist_ok=True)
    return db_dir / 'bot.db'


def get_engine():
    """Get SQLAlchemy engine"""
    db_path = get_db_path()
    database_url = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
    engine = create_engine(
        database_url,
        echo=os.getenv('SQL_ECHO', 'false').lower() == 'true'
    )
    return engine


def init_db():
    """Initialize database - create all tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """Get database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


# Database helper functions
def create_user(telegram_id: int, username: str = None, first_name: str = None,
                last_name: str = None, language: str = 'ru') -> User:
    """Create or update user"""
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            # Update existing user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.last_active = datetime.utcnow()
        else:
            # Create new user
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                language=language
            )
            session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()


def create_order(telegram_id: int, order_id: str, product_id: str,
                 product_name: str, product_category: str,
                 price_tjs: float, price_usd: float) -> Order:
    """Create new order"""
    session = get_session()
    try:
        # Get or create user
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = create_user(telegram_id)

        # Create order
        order = Order(
            order_id=order_id,
            user_id=user.id,
            product_id=product_id,
            product_name=product_name,
            product_category=product_category,
            price_tjs=price_tjs,
            price_usd=price_usd,
            status='pending'
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    finally:
        session.close()


def update_order_status(order_id: str, status: str, admin_notes: str = None) -> bool:
    """Update order status"""
    session = get_session()
    try:
        order = session.query(Order).filter_by(order_id=order_id).first()
        if order:
            order.status = status
            if admin_notes:
                order.admin_notes = admin_notes
            if status == 'completed':
                order.completed_at = datetime.utcnow()
            session.commit()
            return True
        return False
    finally:
        session.close()


def get_user_orders(telegram_id: int, limit: int = 10) -> list:
    """Get user orders"""
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            orders = session.query(Order).filter_by(user_id=user.id)\
                .order_by(Order.created_at.desc()).limit(limit).all()
            return orders
        return []
    finally:
        session.close()


def track_event(telegram_id: int, event_type: str, event_data: str = None):
    """Track analytics event"""
    session = get_session()
    try:
        event = Analytics(
            user_telegram_id=telegram_id,
            event_type=event_type,
            event_data=event_data
        )
        session.add(event)
        session.commit()
    finally:
        session.close()
