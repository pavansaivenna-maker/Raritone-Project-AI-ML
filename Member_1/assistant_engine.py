import re

class ProductAssistantEngine:
    """
    Enterprise NLP text generation engine for dynamically rendering e-commerce titles,
    descriptions, search keywords, and categorization tags from product data inputs.
    """
    def __init__(self):
        # Professional vocabulary matrix mapping for premium text generation enrichment
        self.adjectives = ["premium", "luxury", "essential", "tailored", "breathable", "urban"]
        
    def clean_input_token(self, text: str) -> str:
        """Sanitizes incoming string items to prevent injection or malformed strings."""
        return re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip()

    def generate_product_title(self, garment: str, color: str, gender: str) -> str:
        """Generates an optimized, highly clickable e-commerce marketplace title[cite: 26]."""
        adj = self.adjectives[len(garment) % len(self.adjectives)].capitalize()
        return f"{adj} {color.capitalize()} {garment.capitalize()} for {gender.capitalize()}"

    def generate_product_description(self, garment: str, color: str, gender: str) -> str:
        """Constructs a high-converting, professional marketing overview[cite: 27]."""
        return (
            f"Step up your personal fashion collection with this masterfully designed {color} {garment}. "
            f"Explicitly structured to accommodate modern {gender} silhouettes, it offers an optimal balance "
            f"of comfort, utility, and aesthetic versatility. Perfect for multi-seasonal wear."
        )

    def generate_seo_metadata(self, garment: str, color: str, gender: str) -> str:
        """Generates target high-ranking keyword search strings for indexing platforms[cite: 28]."""
        return f"buy {color} {garment}, high-quality {garment}, trendy {gender} streetwear, best casual {color} apparel"

    def extract_product_tags(self, garment: str, color: str, gender: str) -> list[str]:
        """Maps structured taxonomies to facilitate database indexing and dashboard tracking[cite: 29]."""
        base_tags = [garment.lower(), color.lower(), gender.lower(), "fashion-ai", "catalog-ready"]
        if len(garment) > 5:
            base_tags.append("premium-cut")
        return base_tags