"""
Debug Script: Patient Not Found Issue
This script helps identify why patient lookup is failing
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "healthcare_blockchain")

def debug_patient_search():
    print("=" * 70)
    print("PATIENT SEARCH DEBUG TOOL")
    print("=" * 70)
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        patients = db.patients
        
        print(f"\n✓ Connected to database: {MONGO_DB_NAME}")
        
        # Count total patients
        total_patients = patients.count_documents({})
        print(f"✓ Total patients in database: {total_patients}")
        
        if total_patients == 0:
            print("\n⚠️  WARNING: No patients found in database!")
            print("   Please register a patient first.")
            return
        
        # Show all patients
        print("\n" + "=" * 70)
        print("ALL PATIENTS IN DATABASE:")
        print("=" * 70)
        
        all_patients = list(patients.find({}, {
            "_id": 0,
            "health_id": 1,
            "name": 1,
            "email": 1,
            "phone": 1,
            "created_by_hospital_id": 1
        }))
        
        for idx, patient in enumerate(all_patients, 1):
            print(f"\n{idx}. Patient Details:")
            print(f"   Health ID: {patient.get('health_id')}")
            print(f"   Name: {patient.get('name')}")
            print(f"   Email: {patient.get('email')}")
            print(f"   Phone: {patient.get('phone')}")
            print(f"   Hospital ID: {patient.get('created_by_hospital_id')}")
        
        # Interactive search test
        print("\n" + "=" * 70)
        print("TEST PATIENT SEARCH")
        print("=" * 70)
        
        print("\nEnter search details to test:")
        search_type = input("Search type (health_id/mobile/email): ").strip().lower()
        search_value = input("Search value: ").strip()
        hospital_id = input("Your Hospital ID: ").strip()
        
        # Build query
        query = {}
        if search_type == "health_id":
            query = {"health_id": search_value}
        elif search_type == "mobile":
            query = {"phone": search_value}
        elif search_type == "email":
            query = {"email": search_value.lower()}
        else:
            print(f"\n✗ Invalid search type: {search_type}")
            return
        
        print(f"\n🔍 Searching with query: {query}")
        
        # Search patient
        patient = patients.find_one(query, {"_id": 0})
        
        if not patient:
            print("\n✗ PATIENT NOT FOUND")
            print("\nPossible reasons:")
            print("1. Wrong search value (check spelling/format)")
            print("2. Patient not registered yet")
            print("3. Case sensitivity issue (for email)")
            
            # Try fuzzy search
            print("\n🔍 Trying fuzzy search...")
            if search_type == "email":
                fuzzy_results = list(patients.find(
                    {"email": {"$regex": search_value, "$options": "i"}},
                    {"_id": 0, "email": 1, "name": 1}
                ).limit(5))
                if fuzzy_results:
                    print(f"   Found {len(fuzzy_results)} similar emails:")
                    for r in fuzzy_results:
                        print(f"   - {r.get('email')} ({r.get('name')})")
            elif search_type == "mobile":
                fuzzy_results = list(patients.find(
                    {"phone": {"$regex": search_value}},
                    {"_id": 0, "phone": 1, "name": 1}
                ).limit(5))
                if fuzzy_results:
                    print(f"   Found {len(fuzzy_results)} similar phones:")
                    for r in fuzzy_results:
                        print(f"   - {r.get('phone')} ({r.get('name')})")
            
            return
        
        print("\n✓ PATIENT FOUND!")
        print(f"\n   Health ID: {patient.get('health_id')}")
        print(f"   Name: {patient.get('name')}")
        print(f"   Email: {patient.get('email')}")
        print(f"   Phone: {patient.get('phone')}")
        print(f"   Hospital ID: {patient.get('created_by_hospital_id')}")
        
        # Check hospital match
        patient_hospital = patient.get('created_by_hospital_id')
        print(f"\n🏥 Hospital Check:")
        print(f"   Your Hospital ID: {hospital_id}")
        print(f"   Patient's Hospital ID: {patient_hospital}")
        
        if patient_hospital == hospital_id:
            print("   ✓ Hospital IDs MATCH - Access allowed")
        else:
            print("   ✗ Hospital IDs DON'T MATCH - Access denied")
            print("\n   This is why you're getting 'Patient not registered with your hospital' error")
        
        # Check email
        patient_email = patient.get('email')
        if not patient_email:
            print("\n⚠️  WARNING: Patient has no email - OTP cannot be sent!")
        else:
            print(f"\n✓ Patient email exists: {patient_email}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

def check_database_indexes():
    """Check if proper indexes exist"""
    print("\n" + "=" * 70)
    print("DATABASE INDEXES CHECK")
    print("=" * 70)
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        patients = db.patients
        
        indexes = list(patients.list_indexes())
        print(f"\nIndexes on 'patients' collection:")
        for idx in indexes:
            print(f"  - {idx['name']}: {idx.get('key', {})}")
        
        # Check for required indexes
        required_fields = ['health_id', 'email', 'phone']
        indexed_fields = []
        for idx in indexes:
            for field in idx.get('key', {}).keys():
                indexed_fields.append(field)
        
        print(f"\nRequired fields: {required_fields}")
        print(f"Indexed fields: {list(set(indexed_fields))}")
        
        missing = set(required_fields) - set(indexed_fields)
        if missing:
            print(f"\n⚠️  Missing indexes for: {missing}")
            print("   This may slow down searches but won't cause 'not found' errors")
        else:
            print("\n✓ All required fields are indexed")
            
    except Exception as e:
        print(f"\n✗ Error checking indexes: {e}")

def show_common_issues():
    """Display common issues and solutions"""
    print("\n" + "=" * 70)
    print("COMMON ISSUES & SOLUTIONS")
    print("=" * 70)
    
    print("""
1. PATIENT NOT FOUND
   Causes:
   - Wrong Health ID, phone, or email
   - Patient not registered yet
   - Typo in search value
   
   Solutions:
   - Verify patient exists in database
   - Check spelling and format
   - Use this debug script to find exact values

2. PATIENT NOT REGISTERED WITH YOUR HOSPITAL
   Causes:
   - Patient registered by different hospital
   - Hospital ID mismatch
   
   Solutions:
   - Verify your hospital ID
   - Check patient's created_by_hospital_id field
   - Only access patients from your hospital

3. PATIENT EMAIL NOT FOUND
   Causes:
   - Patient registered without email
   - Email field is empty/null
   
   Solutions:
   - Update patient record with email
   - Re-register patient with email

4. CASE SENSITIVITY (Email)
   Causes:
   - Email stored as "Patient@Example.com"
   - Searching for "patient@example.com"
   
   Solutions:
   - System automatically converts to lowercase
   - Should not be an issue

5. PHONE NUMBER FORMAT
   Causes:
   - Stored as "+1234567890"
   - Searching for "1234567890"
   
   Solutions:
   - Use exact format as stored
   - Include country code if stored with it
""")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("HEALTHCARE BLOCKCHAIN - PATIENT SEARCH DEBUGGER")
    print("=" * 70)
    
    print("\nThis tool helps debug 'Patient not found' errors")
    print("\nOptions:")
    print("1. Debug patient search")
    print("2. Check database indexes")
    print("3. Show common issues")
    print("4. All of the above")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        debug_patient_search()
    elif choice == "2":
        check_database_indexes()
    elif choice == "3":
        show_common_issues()
    elif choice == "4":
        debug_patient_search()
        check_database_indexes()
        show_common_issues()
    else:
        print("\nInvalid choice. Running full debug...")
        debug_patient_search()
        check_database_indexes()
        show_common_issues()
    
    print("\n" + "=" * 70)
    print("DEBUG COMPLETE")
    print("=" * 70)
