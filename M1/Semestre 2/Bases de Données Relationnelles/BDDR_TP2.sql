SELECT customer.contactname, salesorder.orderdate, salesorder.orderid FROM customer, salesorder
WHERE customer.customerid = salesorder.customerid AND customer.customerid = 2;

SELECT * FROM salesorder
WHERE customerid=2;

------------------------------------------------------------------------------------------------------------------

SELECT customer.contactname, salesorder.orderdate FROM customer INNER JOIN salesorder ON customer.customerid=salesorder.customerid 
WHERE customer.customerid = 2;

---------------------------------------------------------------------------------------------------

SELECT contactname,customer.customerid FROM customer
LEFT JOIN salesorder ON customer.customerid=salesorder.customerid
WHERE salesorder.customerid is NULL;

--------------------------------------------------------------------------------------------------

SELECT category.categoryname, supplier.companyname FROM category 
INNER JOIN product ON category.categoryid=product.categoryid
INNER JOIN supplier ON product.supplierid=supplier.supplierid
ORDER BY category.categoryname,supplier.companyname;

--------------------------------------------------------------------------------

SELECT category.categoryname FROM category 
LEFT JOIN product ON category.categoryid=product.categoryid
WHERE product.supplierid is NULL;

---------------------------------------------------------------------------------

SELECT category.categoryname, product.supplierid FROM category 
LEFT JOIN product ON category.categoryid=product.categoryid
ORDER BY product.supplierid;

----------------------------------------------------------------------------------


