INSERT INTO invoices (
    invoice_id,
    invoice_number,
    customer_id,
    store_id,
    created_by_user_id,
    invoice_date,
    due_date,
    subtotal,
    discount_amount,
    tax_amount,
    total_amount,
    payment_status,
    invoice_status,
    notes
)
VALUES
('INV900001','INV900001','RH-19495','1',1,'2026-07-01','2026-07-15',2309.65,0.00,415.74,2725.39,'Paid','Completed','Paid via UPI'),

('INV900002','INV900002','JR-16210','2',1,'2026-07-02','2026-07-16',3709.40,370.94,600.92,3939.38,'Paid','Completed','Corporate order'),

('INV900003','INV900003','CR-12730','3',1,'2026-07-03','2026-07-17',5175.17,517.52,838.74,5496.39,'Pending','Generated','Awaiting payment'),

('INV900004','INV900004','KM-16375','4',1,'2026-07-04','2026-07-18',2892.51,100.00,502.65,3295.16,'Partially Paid','Generated','Advance received'),

('INV900005','INV900005','JM-15655','5',1,'2026-07-05','2026-07-19',2862.68,0.00,515.28,3377.96,'Paid','Completed','Cash payment'),

('INV900006','INV900006','TS-21340','6',1,'2026-07-06','2026-07-20',1822.08,0.00,327.97,2150.05,'Pending','Generated','Payment due'),

('INV900007','INV900007','MB-18085','7',1,'2026-07-07','2026-07-21',5244.84,500.00,854.07,5598.91,'Paid','Completed','Bulk purchase'),

('INV900008','INV900008','JW-15220','8',1,'2026-07-08','2026-07-22',5083.96,300.00,861.11,5645.07,'Paid','Completed','Card payment'),

('INV900009','INV900009','JH-15985','9',1,'2026-07-09','2026-07-23',4297.64,400.00,701.58,4599.22,'Partially Paid','Generated','Half payment received'),

('INV900010','INV900010','GM-14695','10',1,'2026-07-10','2026-07-24',4164.05,0.00,749.53,4913.58,'Pending','Generated','Due next week');


INSERT INTO invoice_items (
    invoice_id,
    product_id,
    quantity,
    unit_price,
    discount,
    tax,
    line_total,
    category_snapshot,
    product_name_snapshot
)
VALUES
('INV900001','TEC-AC-10003033',7,329.95,0.00,415.74,2725.39,'Technology','Acco 7-Outlet Surge Protector'),

('INV900002','FUR-CH-10003950',9,412.16,370.94,600.92,3939.38,'Furniture','Novimex Executive Leather Chair'),

('INV900003','TEC-PH-10004664',9,575.02,517.52,838.74,5496.39,'Technology','Cisco Smart Phone'),

('INV900004','TEC-PH-10004583',5,578.50,100.00,502.65,3295.16,'Technology','Nokia Smart Phone'),

('INV900005','TEC-SHA-10000501',5,572.54,0.00,515.28,3377.96,'Technology','Sharp Wireless Fax'),

('INV900006','FUR-CH-10004050',4,455.52,0.00,327.97,2150.05,'Furniture','Office Chair'),

('INV900007','FUR-TA-10002958',6,874.14,500.00,854.07,5598.91,'Furniture','Conference Table'),

('INV900008','OFF-BI-10003527',5,1016.79,300.00,861.11,5645.07,'Office Supplies','Heavy Duty Binder'),

('INV900009','FUR-TA-10000198',13,330.59,400.00,701.58,4599.22,'Furniture','Computer Table'),

('INV900010','OFF-SU-10002881',5,832.81,0.00,749.53,4913.58,'Office Supplies','Office Supply Kit');


INSERT INTO payments (
    invoice_id,
    payment_date,
    amount_paid,
    payment_method,
    transaction_reference,
    remarks
)
VALUES
('INV900001','2026-07-02',2725.39,'UPI','UPI900001','Full payment'),

('INV900002','2026-07-03',3939.38,'Net Banking','NB900002','Corporate transfer'),

('INV900004','2026-07-05',1500.00,'Cash',NULL,'Advance payment'),

('INV900005','2026-07-06',3377.96,'Cash',NULL,'Paid in cash'),

('INV900007','2026-07-08',5598.91,'Credit Card','CC900007','Card payment'),

('INV900008','2026-07-09',5645.07,'Debit Card','DC900008','Debit card payment'),

('INV900009','2026-07-10',2500.00,'UPI','UPI900009','Partial payment');
