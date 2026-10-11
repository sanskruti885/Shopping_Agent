# 🛒 AI Shopping Assistant

An AI-powered shopping assistant built using **Python, Streamlit, LangChain, Groq, and SQLite**. It helps users find products using natural-language queries or product images, compare customer ratings, filter products based on preferences, and place orders through a conversational interface.

## ✨ Features

- **Natural Language Product Search:** Search for products using everyday language, such as "Find organic honey under $20."
- **Image-Based Product Search:** Upload a product image to identify its key attributes and find similar products in the store.
- **Price Filtering:** Find products within your specified budget.
- **Organic Product Filtering:** Filter products based on their organic status.
- **Customer Ratings:** Retrieve average product ratings and total review counts from the database.
- **Rating-Based Recommendations:** Filter products based on minimum rating requirements.
- **Order Checkout:** Place an order after explicitly confirming your choice.
- **Conversational Interface:** Interact with the shopping agent through a Streamlit chat interface.
- **SQLite Database:** Store product information, customer reviews, and order records locally.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| LangChain | AI agent creation and tool integration |
| Groq | Language models for text-based shopping and image analysis |
| SQLite | Product, review, and order storage |
| python-dotenv | Environment variable management |
| Base64 | Image encoding for vision-model input |

## 🏗️ Project Architecture

The application uses an AI agent that interacts with specialized tools to perform shopping operations.

```text
                  User
                    |
                    v
             Streamlit UI
                app.py
                    |
                    v
          LangChain Shopping Agent
            shopping_agent.py
                    |
          +---------+----------+
          |         |          |
          v         v          v
     Product     Ratings     Checkout
      Search      Tool         Tool
          |         |          |
          v         v          v
       Products   Reviews     Orders
             SQLite Database
                    ^
                    |
             Image Analysis
             Vision Model
```

### Shopping Workflow

1. The user describes a product or uploads an image.
2. The agent identifies the user's requirements.
3. The product search tool retrieves matching products from SQLite.
4. The rating tool retrieves average ratings and review counts.
5. The agent filters and presents suitable products.
6. The user explicitly confirms the product they want to purchase.
7. The checkout tool records the order and returns a confirmation.

**Important:** The agent instructions prohibit placing an order before explicit user confirmation.

## 📁 Project Structure

```text
shopping_agent/
│
├── app.py              # Streamlit user interface
├── shopping_agent.py   # AI agent and shopping tools
├── review_api.py       # Product rating and review queries
├── setup_db.py         # Database creation and sample data
├── store.db            # SQLite database generated during setup
├── .env                # Groq API key
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

## ⚙️ Prerequisites

Before running the application, ensure you have:

- Python installed.
- A Groq API key.
- Internet connectivity for Groq model API requests.

The application currently configures these models in `shopping_agent.py`:

- **Shopping agent:** `openai/gpt-oss-120b`
- **Image analysis:** `qwen/qwen3.8-27b`

Model availability depends on the Groq API and your account access. If a model is unavailable, configure a currently supported model with the required text or image capabilities.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Create a virtual environment

On Windows:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If the Python launcher is unavailable, use `python` instead of `py`, provided Python is installed and available on your PATH.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install streamlit langchain langchain-core langchain-groq python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual API key.

**Security:** Never commit your `.env` file or expose your API key publicly.

### 5. Initialize the database

Run:

```bash
python setup_db.py
```

This creates `store.db` and initializes the following tables:

- `products`
- `reviews`
- `orders`

The setup script also populates the database with sample products and reviews.

**Note:** Running the setup script again resets the seeded review data and replaces the sample product records. Back up any database containing data you want to preserve.

### 6. Run the application

Start Streamlit:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 💬 Example Queries

Try the following prompts in the chat interface:

**Product search**

```text
Find organic honey under $20 with a rating of at least 4.5.
```

**Budget-based search**

```text
Show me products under $10.
```

**Category search**

```text
Find organic almonds.
```

**Image-based search**

Upload a product image through the sidebar and select **Find similar products**.

**Order confirmation**

```text
Yes, place the order.
```

You can also refer to a product by its number in the recommendation list.

## 🧠 Core Components

### 1. `app.py` — Streamlit Interface

Responsible for the application's user interface.

- Configures the Streamlit page.
- Displays the conversation history.
- Accepts text-based shopping requests.
- Supports product image uploads.
- Stores conversation messages in `st.session_state`.
- Invokes the shopping agent and displays its response.

### 2. `shopping_agent.py` — AI Shopping Agent

Creates the LangChain agent and defines the shopping tools.

**`search_products(query, max_price, is_organic)`**

Searches the product database by product name, description, or category. It supports optional maximum-price and organic-status filters.

**`get_rating(product_id)`**

Returns the average customer rating and total review count for a product.

**`checkout(product_id)`**

Retrieves the selected product, inserts an order into the database, and returns an order confirmation.

**`describe_product_image(image_path)`**

Reads an uploaded image, encodes it in Base64, and sends it to the vision model to extract product attributes.

### 3. `review_api.py` — Rating Service

Provides functions for retrieving product ratings from the `reviews` table.

- `get_products_rating(product_id)` retrieves the average rating and review count for one product.
- `get_ratings_for_products(product_ids)` retrieves rating information for multiple products.

Average ratings are rounded to two decimal places.

### 4. `setup_db.py` — Database Initialization

Creates the SQLite tables and inserts sample products and customer reviews.

Run this script before starting the application if the database has not yet been initialized.

## 🗃️ Database Schema

### Products Table

| Column | Description |
|---|---|
| `id` | Unique product identifier |
| `name` | Product name |
| `category` | Product category |
| `price` | Product price |
| `description` | Product description |
| `is_organic` | Organic status represented as `1` or `0` |

### Reviews Table

| Column | Description |
|---|---|
| `id` | Unique review identifier |
| `product_id` | ID of the reviewed product |
| `rating` | Customer rating |
| `reviewer_name` | Reviewer name |
| `review_text` | Written review |

### Orders Table

| Column | Description |
|---|---|
| `id` | Unique order identifier |
| `product_id` | ID of the ordered product |
| `product_name` | Name of the ordered product |
| `price` | Recorded product price |
| `ordered_at` | Order timestamp |

The checkout tool saves confirmed orders in the `orders` table.

## 🔐 Security and Limitations

- **API credentials:** Store API keys in environment variables and exclude `.env` from version control.
- **Demo checkout:** Orders are recorded locally; the application does not process real payments or integrate with shipping services.
- **Local database:** SQLite is suitable for local development and demonstrations. Production applications may require a database designed for concurrent users.
- **Temporary image files:** Uploaded images are written to temporary files. The current implementation does not explicitly remove those files after processing.
- **AI-generated results:** Validate product information, prices, product IDs, and order details before using the application for real transactions.
- **Model compatibility:** Image search requires a vision-capable model that supports the image input format used by the code.

## 🚀 Future Improvements

- Add automated tests for search, ratings, and checkout.
- Add exception handling for model API failures and database errors.
- Implement temporary image-file cleanup.
- Add inventory validation and order history.
- Introduce authentication and user-specific shopping sessions.
- Improve product presentation with images and interactive product cards.
- Integrate a payment gateway for real transactions.
- Migrate to PostgreSQL for a production deployment.


