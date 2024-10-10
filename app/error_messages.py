# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

# ================
# Error messages
# ================


def get_error_message(error_key):
    error_messages = {
        "invalid_date_format": "Invalid date format."
        " Use ISO 8601 format (YYYY-MM-DD).",
        "no_violations_found_dates": "No violations"
        " found between the specified dates.",
        "no_violations": "No violations found.",
        "bad_request": "Bad request. See API documentation" " at /api/doc.",
        "internal_error": "An internal error occurred."
        " The error has been reported to the development team.",
        "no_violations_for_business_id": "No violations found"
        " for this business_id.",
        "violations_update_success": "Violations have"
        " been successfully updated.",
        "violations_delete_success": "All violations"
        " associated with this establishment have"
        " been successfully deleted.",
        "inspection_delete_success": "Inspection"
        " request have been successfully deleted",
    }
    return error_messages.get(error_key, "Unknown error")
