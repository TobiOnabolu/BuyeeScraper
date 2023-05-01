# CSS Selectors Needed

## For Auction
products = response.css('li.itemCard')
productLink = product.css('a::attr(href)').get()
productImage = product.css('img.g-thumbnail__image::attr(data-src)').get() 
productNameJP = product.css('img.g-thumbnail__image::attr(alt)').get()
productPriceUnfiltered = product.css('span.g-priceFx::text').get()

nextPageNum = response.css('a.arrow::attr("data-bind")').re_first(r'page":(\d+)')



