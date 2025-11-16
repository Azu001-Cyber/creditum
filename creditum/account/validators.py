# validators.py
from django.core.validators import RegexValidator

"A regex validator to check the integrity of submitted inputs"
# ✅ Nigerian TIN validator (either 8-4 with hyphen or 12 digits)
validate_tin = RegexValidator(
    regex=r'^(?:\d{8}-\d{4}|\d{12})$',
    message="Enter a valid TIN (8-4 format or 12 digits)."
)

# ✅ Nigerian BVN validator (exactly 11 digits)
validate_bvn = RegexValidator(
    regex=r'^\d{11}$',
    message="Enter a valid 11-digit BVN."
)
