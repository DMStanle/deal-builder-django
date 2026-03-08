from django.shortcuts import render

TAX_RATE = 0.06

PRODUCTS = {
    "macbook": {"name": 'MacBook Pro 15"', "price": 1899.99},
    "ipad": {"name": "iPad Air", "price": 599.99},
    "iphone": {"name": "iPhone", "price": 999.99},
}

DEALS = {
    "none": "No discount",
    "10off": "10% off",
    "20off": "20% off",
    "tax-exempt": "Tax exempt",
}

def money(value):
    return f"${value:.2f}"

def builder_view(request):
    context = {
        "products": PRODUCTS,
        "deals": DEALS,
        "selected_product": "",
        "selected_deal": "",
        "quantity": "1",
        "error": "",
        "summary": "Choose a product, deal, and quantity, then click Build Deal.",
        "total": "$0.00",
    }

    if request.method == "POST":
        product_id = request.POST.get("product", "").strip()
        deal_id = request.POST.get("deal", "").strip()
        quantity_raw = request.POST.get("quantity", "").strip()

        context["selected_product"] = product_id
        context["selected_deal"] = deal_id
        context["quantity"] = quantity_raw

        if product_id not in PRODUCTS:
            context["error"] = "Please select a valid product."
            return render(request, "deals/builder.html", context)

        if deal_id not in DEALS:
            context["error"] = "Please select a valid deal."
            return render(request, "deals/builder.html", context)

        try:
            quantity = int(quantity_raw)
            if quantity < 1:
                raise ValueError
        except ValueError:
            context["error"] = "Quantity must be a whole number of at least 1."
            return render(request, "deals/builder.html", context)

        product = PRODUCTS[product_id]
        base_price = product["price"] * quantity
        discount = 0
        taxable_amount = base_price

        if deal_id == "10off":
            discount = base_price * 0.10
            taxable_amount = base_price - discount
        elif deal_id == "20off":
            discount = base_price * 0.20
            taxable_amount = base_price - discount
        elif deal_id == "tax-exempt":
            taxable_amount = 0

        tax = taxable_amount * TAX_RATE
        total = base_price - discount + tax

        context["total"] = money(total)
        context["summary"] = (
            f"Product: {product['name']} | "
            f"Quantity: {quantity} | "
            f"Deal: {DEALS[deal_id]} | "
            f"Base Price: {money(base_price)} | "
            f"Discount: {money(discount)} | "
            f"Tax: {money(tax)} | "
            f"Final Total: {money(total)}"
        )

    return render(request, "deals/builder.html", context)