"""
Admin panel configuration using SQLAdmin
"""

from sqladmin import ModelView
from ..models.models import User, Wallet, Offer, Trade, TradeMessage, Transaction

class UserAdmin(ModelView, model=User):
    """Admin interface for User model."""
    column_list = [User.id, User.email, User.username, User.role, User.is_active, User.is_blocked]
    column_details_exclude_list = [User.hashed_password]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"

class WalletAdmin(ModelView, model=Wallet):
    """Admin interface for Wallet model."""
    column_list = [Wallet.id, Wallet.user_id, Wallet.currency, Wallet.balance, Wallet.is_escrow]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Wallet"
    name_plural = "Wallets"
    icon = "fa-solid fa-wallet"

class OfferAdmin(ModelView, model=Offer):
    """Admin interface for Offer model."""
    column_list = [Offer.id, Offer.seller_id, Offer.currency, Offer.min_amount, Offer.max_amount, Offer.price_per_unit, Offer.is_active]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Offer"
    name_plural = "Offers"
    icon = "fa-solid fa-tag"

class TradeAdmin(ModelView, model=Trade):
    """Admin interface for Trade model."""
    column_list = [Trade.id, Trade.trade_id, Trade.buyer_id, Trade.seller_id, Trade.amount, Trade.price_per_unit, Trade.total_price, Trade.status]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Trade"
    name_plural = "Trades"
    icon = "fa-solid fa-exchange-alt"

class TradeMessageAdmin(ModelView, model=TradeMessage):
    """Admin interface for TradeMessage model."""
    column_list = [TradeMessage.id, TradeMessage.trade_id, TradeMessage.sender_id, TradeMessage.content]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Trade Message"
    name_plural = "Trade Messages"
    icon = "fa-solid fa-comments"

class TransactionAdmin(ModelView, model=Transaction):
    """Admin interface for Transaction model."""
    column_list = [Transaction.id, Transaction.wallet_id, Transaction.amount, Transaction.transaction_type, Transaction.status]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Transaction"
    name_plural = "Transactions"
    icon = "fa-solid fa-money-bill-wave"

# List of admin views
ADMIN_VIEWS = [
    UserAdmin,
    WalletAdmin,
    OfferAdmin,
    TradeAdmin,
    TradeMessageAdmin,
    TransactionAdmin,
] 