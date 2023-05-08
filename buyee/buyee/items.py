from scrapy import Item, Field 

class BuyeeItem(Item):
    """
    A class representing a scraped product from the Buyee website.
    
    Attributes
    ----------
    productLink : Field()
        A Field object representing the link to the product.
    productImage : Field()
        A Field object representing the image of the product.
    productPrice : Field()
        A Field object representing the price of the product.
    productName : Field()
        A Field object representing the name of the product.
    """
    productLink = Field()
    productImage = Field() 
    productPrice = Field()
    productName = Field()




