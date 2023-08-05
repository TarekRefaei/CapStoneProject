/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
}

// For the first Task

// const { CloudantV1 } = require('@ibm-cloud/cloudant');
// const { IamAuthenticator } = require('ibm-cloud-sdk-core');
// async function main(params) {
//   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
//   const cloudant = CloudantV1.newInstance({
//     authenticator: authenticator,
//   });
//   cloudant.setServiceUrl(params.COUCH_URL);
//   const userState = params.state;
//   try {
//     let dbQueryResponse;
//     let docs;
//     if (!userState) {
//       dbQueryResponse = await cloudant.postAllDocs({
//         db: 'dealerships',
//         includeDocs: true,
//       });
//       docs = dbQueryResponse.result.rows.map(doc => {
//       delete doc._id;
//       delete doc._rev;
//       return doc;
//     });
//     } else {
//       const query = {
//         selector: {
//           state: userState,
//         },
//       };
//       dbQueryResponse = await cloudant.postFind({
//         db: 'dealerships',
//         selector: query.selector,
//       });
//       docs = dbQueryResponse.result.docs.map(doc => {
//       delete doc._id;
//       delete doc._rev;
//       return doc;
//       });
//     }
//     const response = {
//       statusCode: 200,
//       body: JSON.stringify(docs),
//     };
//     return response;
//   } catch (error) {
//     const errorResponse = {
//       statusCode: error.code || 500,
//       body: JSON.stringify({ error: error.message || 'An error occurred.' }),
//     };
//     return errorResponse;
//   }
// }


//for the second Task

// const { CloudantV1 } = require('@ibm-cloud/cloudant');
// const { IamAuthenticator } = require('ibm-cloud-sdk-core');
// async function main(params) {
//   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
//   const cloudant = CloudantV1.newInstance({
//     authenticator: authenticator,
//   });
//   cloudant.setServiceUrl(params.COUCH_URL);
//   try {
//     const dealership = params.dealership; 
//     if (!dealership) {
//       return {
//         statusCode: 400,
//         body: JSON.stringify({ error: 'Missing dealershipNumber.' }),
//       };
//     }
//     const query = {
//       selector: {
//         dealership: parseInt(dealership),
//       },
//     };
//     const dbQueryResponse = await cloudant.postFind({
//       db: 'reviews',
//       selector: query.selector,
//     });
//     const docs = dbQueryResponse.result.docs.map(doc => {
//       delete doc._id;
//       delete doc._rev;
//       return doc;
//     });
//     const response = {
//       statusCode: 200,
//       body: JSON.stringify(docs),
//     };
//     return response;
//   } catch (error) {
//     const errorResponse = {
//       statusCode: error.code || 500,
//       body: JSON.stringify({ error: error.message || 'An error occurred.' }),
//     };
//     return errorResponse;
//   }
// }

//for the third task
// const { CloudantV1 } = require('@ibm-cloud/cloudant');
// const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// async function main(params) {
//   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
//   const cloudant = CloudantV1.newInstance({
//     authenticator: authenticator,
//   });

//   cloudant.setServiceUrl(params.COUCH_URL);

//   try {
//     const reviewData = params.review;

//     if (!reviewData) {
//       return {
//         statusCode: 400,
//         body: JSON.stringify({ error: 'Missing review data.' }),
//       };
//     }

//     // Add the review data to the "reviews" database
//     const dbResponse = await cloudant.postDocument({
//       db: 'reviews',
//       document: reviewData,
//     });

//     const response = {
//       statusCode: 201,
//       body: JSON.stringify({ success: true, id: dbResponse.result.id }),
//     };

//     return response;
//   } catch (error) {
//     const errorResponse = {
//       statusCode: error.code || 500,
//       body: JSON.stringify({ error: error.message || 'An error occurred.' }),
//     };

//     return errorResponse;
//   }
// }