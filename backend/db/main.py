import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use the application default credentials
pth = os.path.join(os.getcwd(), "db", "book-management-api-58a60-ddc378f8388b.json")
cred = credentials.Certificate(pth)
firebase_admin.initialize_app(cred)
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(
#     cred,
#     {
#         "projectId": "book-management-api-58a60",
#     },
# )

db = firestore.client()
