from data_generation.generate_brand import generate_brands
from data_generation.generate_category import generate_categories
from data_generation.generate_seller import generate_sellers
from data_generation.generate_customer import generate_customers
from data_generation.generate_product import generate_products
from data_generation.generate_promotion import generate_promotions
from data_generation.generate_promotion_product import generate_promotion_products


def main():
    generate_brands()
    generate_categories()
    generate_sellers()
    generate_customers()
    generate_products()
    generate_promotions()
    generate_promotion_products()


if __name__ == "__main__":
    main()