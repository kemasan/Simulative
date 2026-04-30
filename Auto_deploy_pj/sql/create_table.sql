CREATE TABLE public.sales (
	doc_id varchar NULL,
	item varchar NULL,
	category varchar NULL,
	amount int4 NULL,
	price varchar NULL,
	discount int4 NULL,
	CONSTRAINT sales_unique_doc_item UNIQUE (doc_id, item)
);
