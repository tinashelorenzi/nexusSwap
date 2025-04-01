from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from ..core.security import SECRET_KEY
from ..models.models import User, Offer, Trade, Wallet, Transaction
import os
from dotenv import load_dotenv

load_dotenv()

# Admin configuration
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@nexusswap.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin-password-here")

# Configure admin resources
resources = [
    {
        "model": User,
        "icon": "fas fa-users",
        "name": "Users",
        "label": "User Management",
    },
    {
        "model": Offer,
        "icon": "fas fa-tag",
        "name": "Offers",
        "label": "Offer Management",
    },
    {
        "model": Trade,
        "icon": "fas fa-exchange-alt",
        "name": "Trades",
        "label": "Trade Management",
    },
    {
        "model": Wallet,
        "icon": "fas fa-wallet",
        "name": "Wallets",
        "label": "Wallet Management",
    },
    {
        "model": Transaction,
        "icon": "fas fa-history",
        "name": "Transactions",
        "label": "Transaction History",
    },
]

# Configure admin login
login_provider = UsernamePasswordProvider(
    login_logo_url="https://preview.tabler.io/static/logo-white.svg",
    admin_secret=SECRET_KEY,
    admin_path="/admin",
    providers={
        "admin": {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        }
    },
) 