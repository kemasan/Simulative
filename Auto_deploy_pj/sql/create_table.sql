CREATE TABLE public.sales (
	doc_id varchar NULL,
	item varchar NULL,
	category varchar NULL,
	amount numeric NULL,
	price numeric NULL,
	discount numeric NULL,
	CONSTRAINT sales_unique_doc_item UNIQUE (doc_id, item)
);
