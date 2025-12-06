"""
Middleware для production-ready бота
Rate limiting, analytics, error handling
"""
import time
import os
from collections import defaultdict
from typing import Callable
from functools import wraps
import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


# ============================================
# RATE LIMITING
# ============================================

class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        """
        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # user_id -> [timestamps]

    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to make a request"""
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove old requests
        self.requests[user_id] = [
            ts for ts in self.requests[user_id]
            if ts > cutoff
        ]

        # Check limit
        if len(self.requests[user_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False

        # Add new request
        self.requests[user_id].append(now)
        return True

    def get_remaining(self, user_id: int) -> int:
        """Get remaining requests for user"""
        now = time.time()
        cutoff = now - self.window_seconds

        # Count recent requests
        recent = [ts for ts in self.requests[user_id] if ts > cutoff]
        return max(0, self.max_requests - len(recent))


# Global rate limiter instance
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        max_requests = int(os.getenv('RATE_LIMIT_PER_MINUTE', '30'))
        _rate_limiter = RateLimiter(max_requests=max_requests, window_seconds=60)
    return _rate_limiter


def rate_limit(func: Callable):
    """Decorator for rate limiting handlers"""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return await func(update, context)

        user_id = update.effective_user.id
        limiter = get_rate_limiter()

        if not limiter.is_allowed(user_id):
            # Send rate limit message
            await update.effective_message.reply_text(
                "⚠️ Слишком много запросов. Пожалуйста, подождите немного.\n\n"
                "⚠️ Хеле зиёд дархостҳо. Лутфан каме интизор шавед."
            )
            return None

        return await func(update, context)

    return wrapper


# ============================================
# USER ACTIVITY TRACKING
# ============================================

async def track_user_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track user activity for analytics"""
    if not update.effective_user:
        return

    try:
        from .models import create_user, track_event

        user = update.effective_user
        create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

        # Track event
        if update.message and update.message.text:
            event_type = 'message'
            if update.message.text.startswith('/'):
                event_type = 'command'
        elif update.callback_query:
            event_type = 'callback'
        else:
            event_type = 'other'

        track_event(user.id, event_type)

    except Exception as e:
        logger.error(f"Failed to track user activity: {e}")


# ============================================
# ADMIN CHECK
# ============================================

def admin_only(func: Callable):
    """Decorator to restrict handler to admin only"""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return None

        admin_id = int(os.getenv('ADMIN_ID', '0'))
        if update.effective_user.id != admin_id:
            await update.effective_message.reply_text(
                "❌ Эта команда доступна только администратору.\n"
                "❌ Ин фармон танҳо барои маъмур дастрас аст."
            )
            return None

        return await func(update, context)

    return wrapper


# ============================================
# ERROR RECOVERY
# ============================================

def auto_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator to automatically retry failed operations"""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))

            # All retries failed
            logger.error(f"All {max_retries} attempts failed: {last_exception}")
            raise last_exception

        return wrapper

    return decorator


# ============================================
# PERFORMANCE MONITORING
# ============================================

def monitor_performance(func: Callable):
    """Decorator to monitor function performance"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time

            if duration > 1.0:  # Log slow operations
                logger.warning(
                    f"Slow operation: {func.__name__} took {duration:.2f}s"
                )

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Operation failed: {func.__name__} after {duration:.2f}s: {e}"
            )
            raise

    return wrapper
