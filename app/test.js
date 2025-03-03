const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

// Function to fetch Shopify products using GraphQL
const fetchShopifyProducts = async () => {
    const SHOPIFY_STORE_URL = "https://rt0jc6-pw.myshopify.com/api/2023-01/graphql.json";
    const ACCESS_TOKEN = process.env.SHOPIFY_STOREFRONT_ACCESS_TOKEN;

    const query = `
        {
          products(first: 10) {
            edges {
              node {
                id
                title
                variants(first: 3) {
                  edges {
                    node {
                      id
                      price {
  amount
  currencyCode
}
                      availableForSale
                    }
                  }
                }
              }
            }
          }
        }
    `;

    try {
        const response = await fetch(SHOPIFY_STORE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Shopify-Storefront-Access-Token": ACCESS_TOKEN
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        console.log("Test script is running successfully!", JSON.stringify(data, null, 2));

    } catch (error) {
        console.error("Error fetching products:", error);
    }
};

// Call the function to test
fetchShopifyProducts();
