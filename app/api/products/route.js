export async function GET() {
    const SHOPIFY_STORE = "mjy0hw-q7"; // Your Shopify store name
    const SHOPIFY_STOREFRONT_ACCESS_TOKEN = process.env.SHOPIFY_STOREFRONT_ACCESS_TOKEN;

    const query = JSON.stringify({
        query: `{
            products(first: 10) {
                edges {
                    node {
                        id
                        title
                        variants(first: 10) {
                            edges {
                                node {
                                    id
                                    price
                                    availableForSale
                                }
                            }
                        }
                    }
                }
            }
        }`
    });

    const response = await fetch(`https://${SHOPIFY_STORE}.myshopify.com/api/2023-10/graphql.json`, {
        method: "POST",
        headers: {
            "X-Shopify-Storefront-Access-Token": SHOPIFY_STOREFRONT_ACCESS_TOKEN,
            "Content-Type": "application/json"
        },
        body: query
    });

    const data = await response.json();
    return Response.json(data);
}
