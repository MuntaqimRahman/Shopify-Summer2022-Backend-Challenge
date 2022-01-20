# Shopify-Summer2022-Backend-Challenge
Backend Challenge for Shopify's Sumer 2022 Internship

I wrote the project in Django with a Postgres database.
All inventory resources are managed with a RESTful API.

It's hosted here: https://muntaqim-shopify-backend2022.herokuapp.com/v1/inventory/

The website has a rudimentary API caller which you can use. You can also use postman to call the routes I identify below.

I implemented filtering of the inventory metadata as my extra feature. How this works is explained below.
I also implemented versioning to make space for new features and clients in the future.

The salient code is in the Inventory subfolder which contains the app for Inventory server. The models feed into the serializers which are called by the views.

Each inventory item has the following fields:

created -> auto added field denoting when the inventory was added to the API
pk -> unique primary key of the inventory item
name -> name of the inventory item (required)
amount -> the amount of the inventory in stock (required, must be >= 0)
description -> description on the inventory item
msrp -> the msrp of the unit, assumed to be CAD or USD so has two decimal places (must be >= 0)
tags -> array of tags that can be used to filter it

#Filtering and Pagination - GET

When making a GET call, you can choose to invoke pagination and filter for items. The query parameters works as follows:

GET https://muntaqim-shopify-backend2022.herokuapp.com/v1/inventory/

  It has the following query parameters:
  
    page_size -> num of the amount of inventory items per page - defaults to 10
    page -> the page you want to navigate - defaults to 1
    
    name -> filters for name fields that *contains* your filter, does not require an exact match
    description -> filters for name fields that *contains* your filter, does not require an exact match
    min_msrp, max_msrp -> filters for inventory msrp that is >= the min_msrp, and <= the max_msrp
    min_amount, max_amount -> filters for inventory amount that is >= the min_amount, and <= the max_amount
    tags -> filters for inventory items that match your filter, must match the exact tag and is case-sensitive
   
  If you apply multiple filters the items returned will be those that pass ALL filters. An example of applying multiple filters is seen below:
  https://muntaqim-shopify-backend2022.herokuapp.com/v1/inventory/?min_msrp=1&name=pen&description=Transparent&min_amount=1&max_amount=45&tags=["Red"]
  
#POST Call

POST https://muntaqim-shopify-backend2022.herokuapp.com/v1/inventory/

Make a POST call to the above route to make a new inventory object. You must provide a JSON of the fields you want to populate.

An example body specifying all fields is below:
{
    "name": "Fountain Pen - Vista",
    "description": "Transparent fountain pen",
    "amount": 30,
    "msrp": 50.00,
    "tags": ["Red","Ink"]
}


#Detailed Calls - GET,PUT,PATCH,DELETE

GET/PUT/PATCH/DELETE https://muntaqim-shopify-backend2022.herokuapp.com/v1/inventory/<pk>

 A GET call to the above endpoint will retreive just that single inventory object.
  
 PUT will replace all fields with the new data. If a field is not speicified, it will become its default (E.g if msrp is not defined in the request body, it will become 0). 
 PATCH will only update the specified fields (E.g if msrp is not defined in the request body, it will remain as is).
 DELETE will remove the inventory item from the database.
  
 
 I've tried to think of future developments by doing things manually where possible in order to allow for future customizability. API verisioning also makes space for future
 features without modifying the existing API server.
  
 Thanks for the challenge. I had a great time making the API and tried to focus on doing the core functions well while making space for new features.
