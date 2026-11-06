from config import *

ROLES = {
    "worker":     
    {
        "label": "Работник",
        "emoji": "🔧", 
        "permissions": {
            VIEW_WORKS, CREATE_WORK, VIEW_PRICE
        }
    },
    "employer":   
    {
        "label": "Работодатель", 
        "emoji": "💼", 
        "permissions": {
            VIEW_WORKS, EDIT_PRICE, VIEW_PRICE, CREATE_PRICE, VIEW_PAYOUTS
        }
    },
    "accountant": 
    {
        "label": "Бухгалтер",    
        "emoji": "🧮", 
        "permissions": {
            VIEW_WORKS, VIEW_PAYOUTS, CREATE_PRICE, EDIT_PRICE
        }
    },
    "admin":      
    {
        "label": "Админ",        
        "emoji": "👑", 
        "permissions": {
            MANAGE_USERS
        }
    },
}

def has_permission(role: str, permission: str) -> bool:
    return permission in ROLES.get(role, {}).get("permissions", set())