from config import *

ROLES = {
    "worker":     
    {
        "label": "Работник",
        "emoji": "🔧", 
        "permissions": {
            VIEW_WORKS, CREATE_WORKS, VIEW_PRICE
        }
    },
    "employer":   
    {
        "label": "Работодатель", 
        "emoji": "💼", 
        "permissions": {
            VIEW_WORKS, EDIT_PRICE, VIEW_PRICE, CREATE_PRICE, VIEW_PAYOUTS, VIEW_WORKERS, EDIT_SECTION
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
    "unknown":      
        {
            "label": "Неизвестный",        
            "emoji": "👑", 
            "permissions": {
                VIEW_PRICE
            }
        },
    "admin":      
    {
        "label": "Админ",        
        "emoji": "👑", 
        "permissions": {
            MANAGE_USERS, VIEW_USERS
        }
    },
    "developer": 
    {
        "label": "Админ",        
        "emoji": "👑", 
        "permissions": {
            MANAGE_USERS, VIEW_USERS
        }
    }     
}

def has_permission(role: str, permission: str) -> bool:
    return permission in ROLES.get(role, {}).get("permissions", set())