
INSERT INTO event_details (name, adult_fee, child_fee, created, updated, is_deleted, is_default, uuid) VALUES ("কুড়িগ্রাম পলিটেকনিক ইনস্টিটিউট পুনর্মিলনী - ২০২৩", 750, 600, strftime('%Y-%m-%d %H:%M:%S','now'), strftime('%Y-%m-%d %H:%M:%S','now'), 0, 1, '80B2E23A-7E38-11ED-A7BB-8X2AFD1190BD');

UPDATE member SET access_type = "Admin" WHERE mobile = "01756702340";
UPDATE member SET access_type = "Admin" WHERE mobile = "01717743019";

UPDATE member SET access_type = "Manager" WHERE mobile = "01734676264";
UPDATE member SET access_type = "Manager" WHERE mobile = "01731935687";
UPDATE member SET access_type = "Manager" WHERE mobile = "01746956526";

UPDATE member SET access_type = "Volunteer" WHERE mobile = "01234567899";