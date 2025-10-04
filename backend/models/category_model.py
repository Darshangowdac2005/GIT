# backend/models/category_model.py

class Category:
    TABLE_NAME = "Categories"
    
    # Static list to represent categories for frontend dropdowns
    CATEGORIES = {
        1: "Electronics",
        2: "ID/Documents",
        3: "Apparel/Clothing",
        4: "Keys/Wallets",
        # Add more categories as needed
    }

    @staticmethod
    def get_name(category_id):
        return Category.CATEGORIES.get(category_id, "Unknown")