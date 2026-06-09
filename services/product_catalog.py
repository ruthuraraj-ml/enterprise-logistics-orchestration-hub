import pandas as pd


class ProductCatalog:

    def __init__(
        self,
        data_path="data/DataCoSupplyChainDatasetRefined_First_5000.csv"
    ):
        self.df = pd.read_csv(data_path)

    def get_all_products(self):

        products = (
            self.df["product_name"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return sorted(products)