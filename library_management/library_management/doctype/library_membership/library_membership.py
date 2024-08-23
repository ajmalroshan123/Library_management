import frappe
from frappe.model.document import Document
from frappe import _

class LibraryMembership(Document):
    # check before submitting this document
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                # check if the membership's end date is later than this membership's start date
                "to_date": (">=", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")


    def validate(self):
        if self.from_date and self.to_date :

            from_date = frappe.utils.getdate(self.from_date)
            to_date = frappe.utils.getdate(self.to_date)

            if from_date >= to_date:
                frappe.throw(_("The 'From Date' must be earlier than the 'To Date'."))




        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
