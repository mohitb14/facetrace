from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json


class WebSearcher:

    def search_image(self, image_path):

        print("=" * 60)
        print("          FACETRACE - WEB IMAGE SEARCH")
        print("=" * 60)

        with sync_playwright() as p:

            print("\n🌐 Opening browser...")

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            print("🔎 Opening Yandex Images...")

            page.goto(
                "https://yandex.com/images/",
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(3000)

            print("📷 Finding image search button...")

            selectors = [
                'button[aria-label="Search by image"]',
                'button[aria-label*="image"]',
                'button[aria-label*="Image"]',
                '[class*="camera"]',
                '[class*="Camera"]'
            ]

            camera_button = None

            for selector in selectors:

                locator = page.locator(selector)

                if locator.count() > 0:

                    camera_button = locator.first

                    print(
                        f"✅ Found button: {selector}"
                    )

                    break

            if camera_button is None:

                print(
                    "❌ Image search button not found"
                )

                browser.close()

                return []

            camera_button.click()

            page.wait_for_timeout(1500)

            print("📤 Uploading image...")

            file_input = page.locator(
                'input[type="file"]'
            ).first

            file_input.set_input_files(
                image_path
            )

            print(
                "⏳ Waiting for Yandex results..."
            )

            page.wait_for_timeout(8000)

            print("✅ Search completed!")

            # ------------------------------------------------
            # Extract Yandex result data from the page
            # ------------------------------------------------

            html = page.content()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            results = []

            print(
                "\n🔗 Extracting source information..."
            )

            # Search through all external links.
            # For each link, inspect its surrounding
            # HTML for an image.
            for a in soup.find_all("a"):

                href = a.get("href")

                if not href:
                    continue

                if not href.startswith("http"):
                    continue

                domain = urlparse(href).netloc

                # Ignore Yandex's own URLs
                if "yandex." in domain:
                    continue

                # Look for image inside this link
                img = a.find("img")

                if img is not None:

                    image_url = (
                        img.get("src")
                        or img.get("data-src")
                    )

                    if image_url and image_url.startswith("http"):

                        result = {
                            "source_url": href,
                            "image_url": image_url
                        }

                        if result not in results:

                            results.append(result)

            # ------------------------------------------------
            # If direct pairs were not found,
            # inspect Yandex result blocks.
            # ------------------------------------------------

            if len(results) == 0:

                print(
                    "⚠️ Direct image/source pairs "
                    "were not detected."
                )

                print(
                    "🔎 Looking for Yandex result blocks..."
                )

                # Common Yandex result containers
                possible_blocks = soup.select(
                    "[data-bem], "
                    "[class*='serp-item'], "
                    "[class*='CbirSites-Item'], "
                    "[class*='CbirSites']"
                )

                for block in possible_blocks:

                    block_links = []

                    for a in block.find_all("a"):

                        href = a.get("href")

                        if not href:
                            continue

                        if not href.startswith("http"):
                            continue

                        domain = urlparse(
                            href
                        ).netloc

                        if "yandex." in domain:
                            continue

                        block_links.append(
                            href
                        )

                    block_images = []

                    for img in block.find_all("img"):

                        src = (
                            img.get("src")
                            or img.get("data-src")
                        )

                        if src and src.startswith("http"):

                            block_images.append(
                                src
                            )

                    if (
                        block_links
                        and block_images
                    ):

                        result = {
                            "source_url":
                                block_links[0],
                            "image_url":
                                block_images[0]
                        }

                        if result not in results:

                            results.append(
                                result
                            )

            # ------------------------------------------------
            # Collect external links as fallback information
            # ------------------------------------------------

            external_links = []

            for a in soup.find_all("a"):

                href = a.get("href")

                if not href:
                    continue

                if not href.startswith("http"):
                    continue

                domain = urlparse(
                    href
                ).netloc

                if "yandex." in domain:
                    continue

                if href not in external_links:

                    external_links.append(
                        href
                    )

            # ------------------------------------------------
            # Print results
            # ------------------------------------------------

            print("\n" + "=" * 60)
            print("          DISCOVERED SOURCE POSTS")
            print("=" * 60)

            if len(results) == 0:

                print(
                    "\n⚠️ No direct source/image pairs found."
                )

            else:

                for i, result in enumerate(
                    results[:20],
                    start=1
                ):

                    print(f"\n{i}. SOURCE:")
                    print(
                        result["source_url"]
                    )

                    print("\n   IMAGE:")
                    print(
                        result["image_url"]
                    )

            # ------------------------------------------------
            # Save structured search results
            # ------------------------------------------------

            output = {
                "search_engine": "Yandex Images",
                "image_source_pairs": results,
                "external_links": external_links
            }

            with open(
                "test/search_results.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    output,
                    file,
                    indent=4
                )

            # Keep the old text file too
            with open(
                "test/search_results.txt",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "FACETRACE YANDEX SEARCH RESULTS\n"
                )

                file.write(
                    "=" * 60 + "\n\n"
                )

                file.write(
                    "IMAGE / SOURCE PAIRS\n"
                )

                file.write(
                    "-" * 60 + "\n"
                )

                for result in results:

                    file.write(
                        "IMAGE="
                        + result["image_url"]
                        + "\n"
                    )

                    file.write(
                        "SOURCE="
                        + result["source_url"]
                        + "\n\n"
                    )

                file.write(
                    "\nEXTERNAL WEBSITES\n"
                )

                file.write(
                    "-" * 60 + "\n"
                )

                for link in external_links:

                    file.write(
                        link + "\n"
                    )

            print(
                "\n💾 Structured results saved to:"
            )

            print(
                "test/search_results.json"
            )

            print(
                "\n💾 Text results saved to:"
            )

            print(
                "test/search_results.txt"
            )

            print(
                "\n🌐 Browser is still open."
            )

            input(
                "\nPress ENTER to close browser..."
            )

            browser.close()

            return results


def main():

    searcher = WebSearcher()

    searcher.search_image(
        "test/person.png"
    )


if __name__ == "__main__":

    main()