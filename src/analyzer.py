import pandas as pd

class Analyzer:
    def __init__(self, parsed_json: list, file_name: str):
        self.df = pd.DataFrame(parsed_json)
        self.file_name = file_name
        self.clean_data()
        self.generate_excel()

    def clean_data(self):
        if 'price' in self.df.columns and 'apartment_size' in self.df.columns:
            self.df = self.df[(self.df['price'] > 0) & (self.df['apartment_size'] > 0)]

        if 'url' in self.df.columns:
            self.df = self.df.drop_duplicates(subset=['url'])

        return self.df

    def generate_excel(self):

        if self.df.empty:
            print("[Analyzer] no data for writing.")
            return

        df_sorted = self.df.sort_values(by="price_per_m2", ascending=True)

        columns_mapping = {
            "title": "Offer title",
            "price": "Price (zł)",
            "apartment_size": "Meters (m²)",
            "price_per_m2": "Price per m²",
            "num_rooms": "Number of rooms",
            "street": "Street",
            "city": "City",
            "url": "Url",
            "description": "Description",
        }

        available_cols = [col for col in columns_mapping.keys() if col in df_sorted.columns]
        final_df = df_sorted[available_cols].rename(
            columns={k: v for k, v in columns_mapping.items() if k in available_cols})

        final_df.to_excel(self.file_name, index=False)