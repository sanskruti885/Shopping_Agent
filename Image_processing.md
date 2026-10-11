How does image processing works
                    USER
                     │
                     │ uploads honey.jpg
                     ▼
              ┌───────────────┐
              │   Streamlit   │
              └───────┬───────┘
                      │
                      │ save temporarily
                      ▼
             Temporary .jpg file
             C:\...\Temp\abc.jpg
                      │
                      │ image path
                      ▼
                ┌───────────┐
                │   AGENT   │
                └─────┬─────┘
                      │
                      │ decides:
                      │ "I need image analysis"
                      ▼
          describe_product_image()
                      │
                      │ reads image
                      ▼
              Base64 encoded image
                      │
                      ▼
              ┌───────────────┐
              │  VISION LLM   │
              └───────┬───────┘
                      │
                      │ analyzes pixels/text
                      ▼
              "This is organic honey"
                      │
                      │ returns
                      ▼
       {
         search_query: "honey",
         is_organic: true
       }
                      │
                      ▼
              search_products()
                      │
                      ▼
              ┌───────────────┐
              │   SQLite DB   │
              │               │
              │   products    │
              └───────┬───────┘
                      │
                      ▼
             Matching honey products
                      │
                      ▼
                 AGENT
                      │
                      ▼
               Streamlit UI