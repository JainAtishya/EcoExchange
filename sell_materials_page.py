import streamlit as st
import json
import os
from datetime import datetime

# Path to the JSON file
JSON_DB = "listings.json"

# Helper Functions
def load_listings():
    """Load existing listings from the JSON file."""
    if not os.path.exists(JSON_DB):
        return []
    with open(JSON_DB, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_listing(listing_data):
    """Save a new listing to the JSON file."""
    listings = load_listings()
    listings.append(listing_data)
    with open(JSON_DB, "w") as file:
        json.dump(listings, file, indent=4)

def display_listings():
    """Display all listings from the JSON file."""
    listings = load_listings()
    if listings:
        for listing in listings:
            st.subheader(listing["material_title"])
            st.write(f"**Category:** {listing['category']}")
            st.write(f"**Quantity:** {listing['quantity']} {listing['unit']}")
            st.write(f"**Price per Unit:** ₹{listing['price_per_unit']}")
            st.write(f"**Location:** {listing['location']}")
            st.write(f"**Condition:** {listing['condition']}")
            st.write(f"**Description:** {listing['description']}")
            st.write(f"**Contact Name:** {listing['contact_name']}")
            st.write(f"**Preferred Contact:** {listing['preferred_contact']}")
            st.write(f"**Listing Date:** {listing['listing_time']}")
            if listing["uploaded_files"]:
                for image_name in listing["uploaded_files"]:
                    st.image(f"./uploads/{image_name}", caption=image_name)
            st.markdown("---")
    else:
        st.info("No listings found.")

# Streamlit App
def sell_materials_page():
    st.title("Sell Your Materials")
    
    # Section to list materials
    with st.expander("📄 View All Listings"):
        display_listings()
    
    # Section to add a new listing
    st.markdown("## List Your Materials")
    st.markdown("Provide the details below to list your materials.")

    with st.form("material_listing_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material_title = st.text_input("Material Title", placeholder="e.g., Clean Plastic Bottles")
            category = st.selectbox("Category", [
                "Organic Waste",
                "Paper & Cardboard",
                "Glass",
                "Plastics",
                "Textiles",
                "Metal Scraps",
                "Wood Waste",
                "Others"
            ])
            quantity = st.number_input("Quantity Available", min_value=1)
            unit = st.selectbox("Unit", ["kg", "piece", "ton", "bundle"])
            
        with col2:
            price_per_unit = st.number_input("Price per Unit (₹)", min_value=0.0, step=0.1)
            location = st.text_input("Location", placeholder="City, State")
            condition = st.selectbox("Material Condition", [
                "New/Unused", "Like New", "Good", "Fair", "As Is"
            ])
        
        description = st.text_area("Material Description", placeholder="Details about your material.")
        
        uploaded_files = st.file_uploader(
            "Upload images (optional, up to 5)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")
        contact_phone = st.text_input("Your Phone Number")
        preferred_contact = st.selectbox("Preferred Contact Method", ["Email", "Phone", "Both"])
        
        terms_accepted = st.checkbox("I accept the terms and conditions.")

        submit_button = st.form_submit_button("List Material")

        if submit_button:
            if not terms_accepted:
                st.error("You must accept the terms and conditions.")
            elif not (material_title and contact_name and contact_email and location):
                st.error("Please fill in all required fields.")
            else:
                # Process uploaded files
                uploaded_file_names = []
                if uploaded_files:
                    os.makedirs("uploads", exist_ok=True)
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join("uploads", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.read())
                        uploaded_file_names.append(uploaded_file.name)
                
                # Prepare listing data
                listing_data = {
                    "material_title": material_title,
                    "category": category,
                    "quantity": quantity,
                    "unit": unit,
                    "price_per_unit": price_per_unit,
                    "location": location,
                    "condition": condition,
                    "description": description,
                    "uploaded_files": uploaded_file_names,
                    "contact_name": contact_name,
                    "contact_email": contact_email,
                    "contact_phone": contact_phone,
                    "preferred_contact": preferred_contact,
                    "listing_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                
                # Save listing
                save_listing(listing_data)
                st.success("Your material has been listed successfully!")

if __name__ == "__main__":
    sell_materials_page()
