"""
Reviews the API = reads from the `reviews` table in store.db and returns
aggregated rating information for products.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__),"store.db")

def get_products_rating(product_id: int) -> dict:
    """Review and return average rating and review count for a single product"""
    conn = sqlite3.connect(DB_PATH) #connect to store.db
    cursor = conn.cursor() #cursor object used to execute queries/send sql command
    cursor.execute( #execute the query
        "SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ? ",
        (product_id,), #parametrized query (product_id,) tuple
    )
    row = cursor.fetchone() #retrive one row from query since in 1 row[0] we have AVG and row[1] COUNT
    conn.close()
    #row[0] is average make decimal 2 fig round if row[0] has some value
    avg = round(row[0],2) if row and row[0] is not None else 0.0
    count = row[1] if row else 0 #row[1] has count
    return {"product_id":product_id,"average_rating":avg,"review_count":count}

#function get rating for multiple products at once ex: get rating for product_id 1,2,3
#return a list of dictionary like
#[
#     {"product_id": 1, "average_rating": 4.5, "review_count": 20},
#     {"product_id": 2, "average_rating": 3.8, "review_count": 12},
#     {"product_id": 3, "average_rating": 4.9, "review_count": 35}
# ]
def get_ratings_for_products(product_ids: list[int]) -> list[dict]:
    """Return ratings for a list of product IDs."""
    if not product_ids:
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join("?" * len(product_ids)) # placeholders = ?,?,?
    cursor.execute(
        f"""
        SELECT product_id, AVG(rating), COUNT(*)
        FROM reviews
        WHERE product_id IN ({placeholders}) 
        GROUP BY product_id
        """,
        product_ids, #in placeholder there will be question mark same length as product id
    )
    rows = cursor.fetchall()
    conn.close()
    # r = (101, 4.6666, 3)
#     101: {
#     "average_rating": 4.67,
#     "review_count": 3
# }
    ratings_map = {r[0]: {"average_rating": round(r[1], 2), "review_count": r[2]} for r in rows}
    return [
        {
            "product_id": pid,
            "average_rating": ratings_map.get(pid, {}).get("average_rating", 0.0),#if no product id return 0.0
            "review_count":   ratings_map.get(pid, {}).get("review_count", 0),
        }
        for pid in product_ids
    ]

if __name__ == "__main__":
    # Single product
    result = get_products_rating(1)
    print("Single product rating:")
    print(f"  Product {result['product_id']}: {result['average_rating']} stars ({result['review_count']} reviews)")

    # Multiple products
    print("\nBatch ratings:")
    results = get_ratings_for_products([1, 3, 5, 7])
    for r in results:
        print(f"  Product {r['product_id']}: {r['average_rating']} stars ({r['review_count']} reviews)")
