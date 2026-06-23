import pandas as pd
import os
import re

# ============================================================
# 1. DEFINE FOLDER PATHS
# ============================================================

# Change this path if your project folder is somewhere else
BASE_DIR = r"C:\Users\kh\PhonePe_Visualisation"

RAW_DIR = os.path.join(BASE_DIR, "data_raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data_cleaned")

# Create cleaned folder if it doesn't exist
os.makedirs(CLEAN_DIR, exist_ok=True)

# ============================================================
# 2. FILE PATHS
# ============================================================

agg_trans_path = os.path.join(RAW_DIR, "aggregated_transaction.csv")
agg_user_path = os.path.join(RAW_DIR, "aggregated_user.csv")
map_trans_path = os.path.join(RAW_DIR, "map_transaction.csv")
map_user_path = os.path.join(RAW_DIR, "map_user.csv")
top_trans_path = os.path.join(RAW_DIR, "top_transaction.csv")
top_user_path = os.path.join(RAW_DIR, "top_user.csv")

# ============================================================
# 3. LOAD FILES
# ============================================================

agg_trans = pd.read_csv(agg_trans_path)
agg_user = pd.read_csv(agg_user_path)
map_trans = pd.read_csv(map_trans_path)
map_user = pd.read_csv(map_user_path)
top_trans = pd.read_csv(top_trans_path)
top_user = pd.read_csv(top_user_path)

print("Files loaded successfully!")
print("aggregated_transaction:", agg_trans.shape)
print("aggregated_user:", agg_user.shape)
print("map_transaction:", map_trans.shape)
print("map_user:", map_user.shape)
print("top_transaction:", top_trans.shape)
print("top_user:", top_user.shape)

# ============================================================
# 4. COMMON CLEANING FUNCTIONS
# ============================================================

def remove_unnamed_columns(df):
    """
    Removes columns like 'Unnamed: 0'
    """
    return df.loc[:, ~df.columns.str.contains("^Unnamed")]

def clean_column_names(df):
    """
    Standardize column names:
    - strip spaces
    - replace spaces with underscore
    - keep consistent casing
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df

def clean_state_name(state):
    """
    Converts state slug to readable title format
    Example:
    'andaman-&-nicobar-islands' -> 'Andaman & Nicobar Islands'
    """
    if pd.isna(state):
        return state

    state = str(state).strip().lower()

    # replace hyphens with spaces
    state = state.replace("-", " ")

    # clean multiple spaces
    state = re.sub(r"\s+", " ", state).strip()

    # title case
    state = state.title()

    # fix specific known patterns
    replacements = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar Islands",
        "Dadra & Nagar Haveli & Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
        "Jammu & Kashmir": "Jammu & Kashmir",
        "Delhi": "Delhi",
        "Odisha": "Odisha",
        "Tamil Nadu": "Tamil Nadu",
        "Uttar Pradesh": "Uttar Pradesh",
        "Madhya Pradesh": "Madhya Pradesh",
        "West Bengal": "West Bengal",
        "Arunachal Pradesh": "Arunachal Pradesh",
        "Himachal Pradesh": "Himachal Pradesh",
        "Andhra Pradesh": "Andhra Pradesh",
    }

    if state in replacements:
        return replacements[state]

    return state

def clean_district_name(district):
    """
    Cleans district names for consistency across map/top tables.
    Examples:
    'south andaman district' -> 'South Andaman'
    """
    if pd.isna(district):
        return district

    district = str(district).strip().lower()

    # remove common suffixes
    district = district.replace(" district", "")
    district = district.replace(" district.", "")
    district = district.replace("-", " ")

    # remove extra spaces
    district = re.sub(r"\s+", " ", district).strip()

    # title case
    district = district.title()

    # manual fixes if needed
    district_fixes = {
        "North And Middle Andaman": "North and Middle Andaman",
        "South West": "South West",
    }

    if district in district_fixes:
        return district_fixes[district]

    return district

def add_year_quarter_key(df):
    """
    Creates YearQuarter field for easier analysis
    Example: 2018-Q1
    """
    if "year" in df.columns and "quarter" in df.columns:
        df["YearQuarter"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)
    elif "Year" in df.columns and "Quarter" in df.columns:
        df["YearQuarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    return df

def clean_common(df):
    """
    Applies basic cleaning to every table
    """
    df = remove_unnamed_columns(df)
    df = clean_column_names(df)
    return df

# ============================================================
# 5. CLEAN ALL TABLES
# ============================================================

agg_trans = clean_common(agg_trans)
agg_user = clean_common(agg_user)
map_trans = clean_common(map_trans)
map_user = clean_common(map_user)
top_trans = clean_common(top_trans)
top_user = clean_common(top_user)

# ============================================================
# 6. RENAME COLUMNS TABLE-WISE
# ============================================================

# aggregated_transaction
agg_trans = agg_trans.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "trans_type": "Transaction_Type",
    "trans_counts": "Transaction_Count",
    "amount": "Transaction_Amount"
})

# aggregated_user
agg_user = agg_user.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "brand": "Brand",
    "user_counts": "User_Count",
    "percentage": "Brand_Percentage"
})

# map_transaction
map_trans = map_trans.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "district": "District",
    "trans_counts": "Transaction_Count",
    "amount": "Transaction_Amount"
})

# map_user
map_user = map_user.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "district": "District",
    "registered_user_counts": "Registered_Users"
})

# top_transaction
top_trans = top_trans.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "district": "District",
    "trans_counts": "Transaction_Count",
    "amount": "Transaction_Amount"
})

# top_user
top_user = top_user.rename(columns={
    "states": "State",
    "year": "Year",
    "quarter": "Quarter",
    "district": "District",
    "registered_user_counts": "Registered_Users"
})

# ============================================================
# 7. CLEAN STATE NAMES
# ============================================================

for df in [agg_trans, agg_user, map_trans, map_user, top_trans, top_user]:
    if "State" in df.columns:
        df["State"] = df["State"].apply(clean_state_name)

# ============================================================
# 8. CLEAN DISTRICT NAMES WHEREVER AVAILABLE
# ============================================================

for df in [map_trans, map_user, top_trans, top_user]:
    if "District" in df.columns:
        df["District"] = df["District"].apply(clean_district_name)

# ============================================================
# 9. STANDARDIZE BRAND NAMES
# ============================================================

if "Brand" in agg_user.columns:
    agg_user["Brand"] = agg_user["Brand"].astype(str).str.strip().str.title()

# ============================================================
# 10. ADD YEARQUARTER KEY
# ============================================================

agg_trans = add_year_quarter_key(agg_trans)
agg_user = add_year_quarter_key(agg_user)
map_trans = add_year_quarter_key(map_trans)
map_user = add_year_quarter_key(map_user)
top_trans = add_year_quarter_key(top_trans)
top_user = add_year_quarter_key(top_user)

# ============================================================
# 11. DATA TYPE FIXES
# ============================================================

# aggregated_transaction
agg_trans["Year"] = agg_trans["Year"].astype(int)
agg_trans["Quarter"] = agg_trans["Quarter"].astype(int)
agg_trans["Transaction_Count"] = pd.to_numeric(agg_trans["Transaction_Count"], errors="coerce")
agg_trans["Transaction_Amount"] = pd.to_numeric(agg_trans["Transaction_Amount"], errors="coerce")

# aggregated_user
agg_user["Year"] = agg_user["Year"].astype(int)
agg_user["Quarter"] = agg_user["Quarter"].astype(int)
agg_user["User_Count"] = pd.to_numeric(agg_user["User_Count"], errors="coerce")
agg_user["Brand_Percentage"] = pd.to_numeric(agg_user["Brand_Percentage"], errors="coerce")

# map_transaction
map_trans["Year"] = map_trans["Year"].astype(int)
map_trans["Quarter"] = map_trans["Quarter"].astype(int)
map_trans["Transaction_Count"] = pd.to_numeric(map_trans["Transaction_Count"], errors="coerce")
map_trans["Transaction_Amount"] = pd.to_numeric(map_trans["Transaction_Amount"], errors="coerce")

# map_user
map_user["Year"] = map_user["Year"].astype(int)
map_user["Quarter"] = map_user["Quarter"].astype(int)
map_user["Registered_Users"] = pd.to_numeric(map_user["Registered_Users"], errors="coerce")

# top_transaction
top_trans["Year"] = top_trans["Year"].astype(int)
top_trans["Quarter"] = top_trans["Quarter"].astype(int)
top_trans["Transaction_Count"] = pd.to_numeric(top_trans["Transaction_Count"], errors="coerce")
top_trans["Transaction_Amount"] = pd.to_numeric(top_trans["Transaction_Amount"], errors="coerce")

# top_user
top_user["Year"] = top_user["Year"].astype(int)
top_user["Quarter"] = top_user["Quarter"].astype(int)
top_user["Registered_Users"] = pd.to_numeric(top_user["Registered_Users"], errors="coerce")

# ============================================================
# 12. REMOVE DUPLICATES
# ============================================================

agg_trans = agg_trans.drop_duplicates()
agg_user = agg_user.drop_duplicates()
map_trans = map_trans.drop_duplicates()
map_user = map_user.drop_duplicates()
top_trans = top_trans.drop_duplicates()
top_user = top_user.drop_duplicates()

# ============================================================
# 13. CREATE DIMENSION TABLES
# ============================================================

# State dimension
all_states = pd.concat([
    agg_trans[["State"]],
    agg_user[["State"]],
    map_trans[["State"]],
    map_user[["State"]],
    top_trans[["State"]],
    top_user[["State"]]
], ignore_index=True).drop_duplicates().sort_values("State").reset_index(drop=True)

dim_state = all_states.copy()
dim_state["State_ID"] = range(1, len(dim_state) + 1)

# District dimension
district_frames = []
for df in [map_trans, map_user, top_trans, top_user]:
    if "District" in df.columns:
        district_frames.append(df[["State", "District"]])

dim_district = pd.concat(district_frames, ignore_index=True).drop_duplicates()
dim_district = dim_district.sort_values(["State", "District"]).reset_index(drop=True)
dim_district["District_ID"] = range(1, len(dim_district) + 1)

# Date dimension
all_dates = pd.concat([
    agg_trans[["Year", "Quarter"]],
    agg_user[["Year", "Quarter"]],
    map_trans[["Year", "Quarter"]],
    map_user[["Year", "Quarter"]],
    top_trans[["Year", "Quarter"]],
    top_user[["Year", "Quarter"]],
], ignore_index=True).drop_duplicates()

dim_date = all_dates.sort_values(["Year", "Quarter"]).reset_index(drop=True)
dim_date["YearQuarter"] = dim_date["Year"].astype(str) + "-Q" + dim_date["Quarter"].astype(str)
dim_date["Sort_Order"] = range(1, len(dim_date) + 1)

# Transaction type dimension
if "Transaction_Type" in agg_trans.columns:
    dim_transaction_type = agg_trans[["Transaction_Type"]].drop_duplicates().sort_values("Transaction_Type").reset_index(drop=True)
    dim_transaction_type["TransactionType_ID"] = range(1, len(dim_transaction_type) + 1)
else:
    dim_transaction_type = pd.DataFrame()

# Brand dimension
if "Brand" in agg_user.columns:
    dim_brand = agg_user[["Brand"]].drop_duplicates().sort_values("Brand").reset_index(drop=True)
    dim_brand["Brand_ID"] = range(1, len(dim_brand) + 1)
else:
    dim_brand = pd.DataFrame()

# ============================================================
# 14. EXPORT CLEANED FACT TABLES
# ============================================================

agg_trans.to_csv(os.path.join(CLEAN_DIR, "fact_aggregated_transaction.csv"), index=False)
agg_user.to_csv(os.path.join(CLEAN_DIR, "fact_aggregated_user.csv"), index=False)
map_trans.to_csv(os.path.join(CLEAN_DIR, "fact_map_transaction.csv"), index=False)
map_user.to_csv(os.path.join(CLEAN_DIR, "fact_map_user.csv"), index=False)
top_trans.to_csv(os.path.join(CLEAN_DIR, "fact_top_transaction.csv"), index=False)
top_user.to_csv(os.path.join(CLEAN_DIR, "fact_top_user.csv"), index=False)

# ============================================================
# 15. EXPORT DIMENSION TABLES
# ============================================================

dim_state.to_csv(os.path.join(CLEAN_DIR, "dim_state.csv"), index=False)
dim_district.to_csv(os.path.join(CLEAN_DIR, "dim_district.csv"), index=False)
dim_date.to_csv(os.path.join(CLEAN_DIR, "dim_date.csv"), index=False)

if not dim_transaction_type.empty:
    dim_transaction_type.to_csv(os.path.join(CLEAN_DIR, "dim_transaction_type.csv"), index=False)

if not dim_brand.empty:
    dim_brand.to_csv(os.path.join(CLEAN_DIR, "dim_brand.csv"), index=False)

# ============================================================
# 16. BASIC VALIDATION OUTPUT
# ============================================================

print("\n========== CLEANING COMPLETED ==========")
print("Cleaned files saved in:", CLEAN_DIR)

print("\nFinal Shapes:")
print("fact_aggregated_transaction:", agg_trans.shape)
print("fact_aggregated_user:", agg_user.shape)
print("fact_map_transaction:", map_trans.shape)
print("fact_map_user:", map_user.shape)
print("fact_top_transaction:", top_trans.shape)
print("fact_top_user:", top_user.shape)

print("\nDimension Shapes:")
print("dim_state:", dim_state.shape)
print("dim_district:", dim_district.shape)
print("dim_date:", dim_date.shape)

if not dim_transaction_type.empty:
    print("dim_transaction_type:", dim_transaction_type.shape)

if not dim_brand.empty:
    print("dim_brand:", dim_brand.shape)

print("\nSample cleaned state names:")
print(dim_state.head(10))

print("\nSample cleaned district names:")
print(dim_district.head(10))