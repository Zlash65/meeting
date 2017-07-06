// Copyright (c) 2017, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meeting Attendee', {
	attendee: function(frm, cdt, cdn) {
		console.log("here");
		var attendee = frappe.model.get_doc(cdt, cdn);
		if(attendee.attendee){
			// if attendee is set then
			frappe.call({
				method: "meeting.meeting.doctype.meeting.meeting.get_full_name",
				args: {
					attendee: attendee.attendee
				},
				callback: function(r){
					frappe.model.set_value(cdt, cdn, "full_name", r.message);
				}
			});
		}
		else{
			// if no attendee, clear full name
			frappe.model.set_value(cdt, cdn, "full_name", null);
		}		
	}
});

frappe.ui.form.on("Meeting", {
	send_emails: function(frm){
		console.log("here");
		if(frm.doc.status==="Planned"){
			frappe.call({
				method: "meeting.api.send_invitation_emails",
				args: {
					meeting: frm.doc.name
				},
				callback: function(r){
					console.log(r.message);
				}
			});
		}
	}
});