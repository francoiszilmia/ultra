###########################################################################################
Framework choice: Postman

Reason: API test
###########################################################################################

1) Prerequisites
- Postman


2) Import the postman collection file to Postman:

Select File > Import > Upload File ("Utra.postman_collection.json")

3) Create a user: 

Request:
POST https://gorest.co.in/public/v2/users

Body:
{
    "name": "Jo Martin",
    "gender": "male",
    "email": "jo.martin@dummydata.com", //email must be unique
    "status": "active"
}

Header:
Accept:application/json
Content-Type:application/json
Authorization:Bearer 7e5285f35a8ff41e4c4547c87d18a977e24a4cbd89cd2dbf240a2829ea24eb37

Test:
pm.test("the endpoint returns the expected status code", () => {
  // comma separate the valid response codes below
  //201: new user (unique email address)
  //401: email already exists
  const expectedStatusCodes = [201, 422]; 

  pm.expect(pm.response.code).to.be.oneOf(
    expectedStatusCodes,
    `expected response status to be one of ${expectedStatusCodes} but got ${pm.response.code}.`
  );
});

4) List All users:

GET https://gorest.co.in/public/v2/users

Header:
Accept:application/json
Content-Type:application/json
Authorization:Bearer 7e5285f35a8ff41e4c4547c87d18a977e24a4cbd89cd2dbf240a2829ea24eb37

Test:
pm.test("the endpoint returns the expected status code", () => {
  // change 200 to the response code you expect
  const expectedStatusCode = 200;

  pm.response.to.have.status(expectedStatusCode);
});

5) Update a user:

PATCH https://gorest.co.in/public/v2/users/4599  

//4599 was the user ID of step 3) create a user

Body:
{
    "name": "Jo Martin",
    "email": "jo.marti@dummy.com",
    "id": "9999",
    "status": "active"
}

Header:
Accept:application/json
Content-Type:application/json
Authorization:Bearer 7e5285f35a8ff41e4c4547c87d18a977e24a4cbd89cd2dbf240a2829ea24eb37

Test:
pm.test("the endpoint returns the expected status code", () => {
  // change 200 to the response code you expect
  const expectedStatusCode = 200;

  pm.response.to.have.status(expectedStatusCode);
});
