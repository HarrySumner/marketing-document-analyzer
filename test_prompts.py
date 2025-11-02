from orchestrator.prompt_tester import PromptTester
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found")
        return

    # Initialize tester
    tester = PromptTester()

    # Test input (same as your dissertation methodology)
    input_data = {
        'document': """
        Shiseido Future Solution LX - Premium Anti-Aging Serum

        "Unlock Timeless Beauty with 20 Years of Research"

        Our revolutionary serum combines exclusive RetinSphere Technology
        with Japanese botanical extracts to deliver visible results in just
        30 days. Dermatologist-tested and clinically proven.

        96% of women experienced smoother, more radiant skin.

        Limited Edition Launch - Available exclusively at select retailers.

        $450 / 50ml
        """,
        'context': """
        Target Audience: Affluent women aged 45-60
        Product Category: Premium anti-aging skincare
        Price Point: $450
        Competitive Set: La Mer, SK-II, Clé de Peau
        """
    }

    # Optional: Ground truth from expert coding
    ground_truth = {
        'strategic_assessment': 'Premium positioning through heritage and scientific authority',
        'key_strength': 'Clear luxury tier signaling with specific timeline',
        'key_weakness': 'Insufficient value justification at $450 price point'
    }

    # Run A/B test
    results = tester.run_ab_test(
        agent_name='strategic_analyst',
        input_data=input_data,
        ground_truth=ground_truth,
        iterations=3  # Run each variant 3 times
    )

    # Save results
    tester.save_test_results(results)

    # Display winner
    print(f"\n{'='*70}")
    print("WINNER:")
    print(f"  {results['winner']['variant_name']}")
    print(f"  Composite Score: {results['winner']['composite_score']:.3f}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
