# Copyright (c) 2024, Ajmal Roshan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class LibraryTransaction(Document):
    def before_submit(self):
        self.validate_membership()  # Validate membership before processing transactions
        for item in self.add_article:
            article_type = item.get('type')
            if article_type == "Issue":
                self.validate_issue()
                self.validate_maximum_limit()
                # Set the article status to be Issued
                article = frappe.get_doc("Article", item['add_article'])
                article.status = "Issued"
                article.save()

            elif article_type == "Return":
                self.validate_return()
                # Set the article status to be Available
                article = frappe.get_doc("Article", item['add_article'])
                article.status = "Available"
                article.save()

    def validate_issue(self):
        for item in self.add_article:
            article = frappe.get_doc("Article", item.get('add_article'))
            if article.status == "Issued":
                frappe.throw(f"Article {article.name} is already issued by another member")

    def validate_return(self):
        for item in self.add_article:
            article = frappe.get_doc("Article", item.get('add_article'))
            if article.status == "Available":
                frappe.throw(f"Article {article.name} cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = 0
        issued_transactions = frappe.get_all(
            "Library Transaction",
            filters={"library_member": self.library_member, "docstatus": 1},
            fields=["name"]
        )

        for transaction in issued_transactions:
            if frappe.db.exists(
                "Article Child",
                {"type_tran": "Issue", "parent": transaction["name"]}
            ):
                count += 1

        if count + len(self.add_article) > max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # Check for valid membership
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")



@frappe.whitelist()
def get_valid_library_members():
    today = datetime.now().date()


    valid_members = frappe.get_all(
        'Library Membership',
        filters = {'from_date':['<',today],
                  'to_date':['>',today]},
        fields = ['library_member']          
    )

    member_name = [member['library_member'] for member in valid_members]

    return member_name